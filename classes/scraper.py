import random
import hashlib
import os
import gzip
import requests
import traceback
import lxml
from lxml import html
from classes.selector import Selector
from classes.proxy import Proxy
import time
from classes.user_agents import USER_AGENTS
import shutil
from ftplib import FTP
from urllib.parse import urlparse


ITER_CONTENT_CHUNK_SIZE = 1024*1024

class Scraper(object):

    time_started = time.time()
    use_fake_accounts = False
    no_vpn = True
    no_cache = False
    cached_only = False
    identity = None
    thread_status = 'Ready'
    thread_id=0
    should_exit = False
    parent = None
    retries = 0
    max_retries = 3
    proxy = Proxy()
    parent = None
    session = None
    login_url = None
    min_timeout_between_requests = .1
    max_timeout_between_requests = 1
    webdriver = 'requests'

    def __init__(self, parent=None,
                 thread_id=0,
                 webdriver='requests'):
        self.thread_id = thread_id
        self.webdriver = webdriver
        if parent:
            self.parent = parent
            self.use_fake_accounts = parent.use_fake_accounts
            self.no_cache = parent.no_cache
            self.cached_only = parent.cached_only
            self.no_vpn = parent.no_vpn

    def setProxy(self, ip, port=80, username='', password=''):
        proxy = Proxy(ip, port, username, password)
        self.proxy = proxy

    def loadUrl(self, url, no_cache=False):
        if self.should_exit == True:
            print('cancelling url', url, 'to exit thread')
            return None
        if self.retries < self.max_retries:
            self.retries += 1
        cache_file_path = self.getCachefile_path(url)
        if (not no_cache and not self.no_cache and
                os.path.exists(cache_file_path)):
            # print('will load from cache')
            if not self.isCacheFileStale(cache_file_path):
                # Trying to get page from cache
                try:
                    return self.loadUrlFromCache(url, cache_file_path)
                except Exception as e:
                    print('could not load:', url, 'from cache', traceback.format_exc())
                    self.retries += 1
                    return self.loadUrl(url, no_cache=True)
        else:
            if self.cached_only:
                # speeds up testing
                return None
            self.thread_status = 'loading ' + str(url) + ' attempt:' + str(self.retries)
            try:
                self.waitForVPNReload()
                self.waitForIdentity()
                self.getSession()
                self.waitBetweenRequests()
                html = self.getPageSourceWithCurrentSession(url, timeout=15)
                selector = self.validateScrapedData(url, html)
                if selector:
                    self.saveUrlToDiscCache(url, html)
                    self.retries = 0
                    return selector
                else:
                    print(url, 'scraped, but data inside is not valid')
                    return None
            except Exception as e:
                print('Could not load', url, e)
                print(traceback.format_exc())
                if self.retries >= self.max_retries or (self.no_vpn and self.retries >= 2):
                    self.retries = 0
                    return None
                else:
                    self.retries += 1
                    return self.loadUrl(url, no_cache)

    def loadUrlFromCache(self,  url, cache_file_path):
        with gzip.open(cache_file_path, 'rb') as f:
            text = f.read().decode('utf-8')
            selector = Selector(text=text)
            if selector.xpath('//body'):
                if self.parent:
                    self.parent.loaded_urls_from_cache += 1
                print(url, 'loaded from cache', os.path.abspath(cache_file_path))
                return selector
            else:
                # Cached file is corrupt. Should reload.
                self.retries += 1
                return self.loadUrl(url, no_cache=True)

    def getCachefile_path(self, url):
        login = 'true' if self.use_fake_accounts else ''
        cache_file_name = hashlib.md5((url + '&login=' + login).encode('utf-8')).hexdigest() + '.html.gz'
        cache_file_path = os.path.join('cache', cache_file_name[:2], cache_file_name)
        return cache_file_path

    def isCacheFileStale(self, cache_file_path):
        return False #handled by cron instead
        return self.time_started - os.path.getmtime(cache_file_path) > MAX_DISK_CACHE_LIFETIME * 86400

    def saveUrlToDiscCache(self, url, html):
        # db cached will be used instead. Hopefully bloated disk cache no loner needed
        cache_file_path = self.getCachefile_path(url)
        dirname = os.path.dirname(cache_file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with gzip.open(cache_file_path, 'wb') as f:
            f.write(html.encode('utf-8'))
        print(url, 'fetched and saved to cache', os.path.abspath(os.path.join(os.getcwd(), cache_file_path)))

    def closeSession(self):
        if self.session:
            if self.webdriver == 'requests':
                self.session.close()
            else:
                self.session.quit()
            self.session = None
            print('session closed')

    def waitForVPNReload(self):
        if self.parent:
            if self.parent.no_vpn:
                return
            while self.parent.should_reload_vpn:
                self.thread_status = 'Ready'
                self.retries = 1
                time.sleep(1)

    def waitForIdentity(self):
        if self.use_fake_accounts:
            if not self.identity:
                self.closeSession()
            while not self.identity:
                self.thread_status = 'Waiting for new login identity'
                time.sleep(2)
                if self.should_exit:
                    break

    def isWaitingForIdentity(self):
        return True if not self.identity else False

    def getSession(self):
        if self.session:
            return self.session
        else:
            self.initSession()
            if self.use_fake_accounts:
                login_response_html = self.login()
                if not login_response_html:
                    return None
            return self.session

    def initSession(self):
        if self.webdriver == 'requests':
            self.session = requests.session()
            self.session.proxies = self.proxy.getRequestsFormat()
            self.headers = self.getHeaders()
        elif self.webdriver == 'chrome':
            self.session = get_chrome_webdriver(self.proxy)
        elif self.webdriver == 'firefox':
            self.session = get_firefox_webdriver(self.proxy)
        elif self.webdriver == 'phantomjs':
            self.session = get_phantomjs_webdriver(self.proxy)

    def getHeaders(self):
        return {
            "Accept-Language": "en-US",
            'User-Agent': random.choice(USER_AGENTS)
        }

    def waitBetweenRequests(self):
        sleeping_time = random.uniform(self.min_timeout_between_requests,
                                       self.max_timeout_between_requests)
        time.sleep(sleeping_time)

    def validateScrapedData(self, url, html):
        #STUB: for subclassing
        return Selector(text=html)

    def login(self):
        try:
            login_response = self.getPageSourceWithCurrentSession(self.login_url, timeout=3)
        except Exception as e:
            print('Could not load login form:', self.login_url, e)
            print(traceback.format_exc())
            return False
        login_selector = Selector(text=login_response)
        post_url = self.getLoginPostUrl(login_selector)
        post_data = self.getLoginPostData(login_selector)
        post_data = self.fillLoginFormWithCredentials(post_data)
        if not self.identity:
            print('Login identity was reset while loading Login form')
            return False
        try:
            login_response_html = self.getPageSourceWithCurrentSession(post_url, method='POST', data=post_data, timeout=10)
            self.saveLoginResponse(login_response_html)
        except Exception as e:
            print('could not post login form:', e)
            return False
        return login_response_html

    def getPageSourceWithCurrentSession(self, url,
                                 method='GET', data={},
                                 timeout=3):
        if url.startswith('file:///'):
            url = url.replace('file:///', '')
            with open(url, 'r', encoding='utf-8') as f:
                return f.read()
        if self.webdriver == 'requests':
            if method=='GET':
                response = self.session.get(url, headers=self.headers, timeout=timeout)
            elif method=='POST':
                response = self.session.post(url, data=data, headers=self.headers, timeout=timeout)
            return response.text
        else: #using Selenium
            print('will get', url, 'with selenium')
            self.session.get(url)
            response = self.session.page_source
            return response

    def getLoginPostUrl(self, login_selector):
        return login_selector.xpath('//form/@action').extract_first()

    def getLoginPostData(self, login_selector):
        post_data = {}
        inputs = login_selector.xpath('//form//input')
        for input in inputs:
            name = input.xpath('@name').extract_first()
            value = input.xpath('@value').extract_first()
            post_data[name] = value
        return post_data

    def fillLoginFormWithCredentials(self, post_data):
        #STUB: for subclassing
        return post_data

    def saveLoginResponse(self, login_response_html):
        with open('login_response.html', 'w', encoding='utf-8') as f:
            f.write(login_response_html)

    def checkIP(self, ip_test_url):
        use_fake_accounts = self.use_fake_accounts
        self.use_fake_accounts = False
        response = self.loadUrl(ip_test_url, no_cache=True)
        self.use_fake_accounts = use_fake_accounts
        ip = response.xpath('//body//text()').extract_first().strip()
        print('Current IP:', ip)
        if not self.proxy.ip:
            return True
        if ip == self.proxy.ip:
            return True
        else:
            print('proxy does not work')
            return False

    def downloadFile(self, src, dest):
        if not src or not dest:
            return -1
        if src.startswith('ftp://'):
            url = urlparse(src)
            ftp = FTP(url.netloc)
            ftp.login()
            ftp.retrbinary("RETR " + url.path, open(dest, 'wb').write)
            ftp.quit()
            return 200
        print('prepare to download', src, 'to', dest)
        session = self.getSession()
        self.waitBetweenRequests()
        response = session.get(src, headers=self.headers, timeout=3, stream=True)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'wb') as f:
                for chunk in response.iter_content(ITER_CONTENT_CHUNK_SIZE):
                    f.write(chunk)
            print('File', dest, 'saved.')
        else:
            # raise Exception('Failed to download file:'+str(response.status_code))
            print('Failed to download file:'+str(response.status_code))
        return response.status_code
