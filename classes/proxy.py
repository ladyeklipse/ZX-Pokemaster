import urllib
try:
    quote = urllib.pathname2url
except:
    quote = urllib.request.pathname2url

class Proxy():

    def __init__(self, ip='', port=80, login='', password=''):
        self.ip = ip.strip()
        self.port = str(port)
        self.login = quote(login)
        self.password = quote(password)

    def getAuthFormat(self):
        if not self.ip:
            return ''
        ip_port = '{}:{}'.format(self.ip, self.port)
        if self.login and self.password:
            return '{}:{}@{}'.format(self.login, self.password, ip_port)
        elif self.login and not self.password:
            return '{}@{}'.format(self.login, ip_port)

    def getRequestsFormat(self):
        auth_format = self.getAuthFormat()
        if not auth_format:
            return ''
        return {
            'http':'http://{}'.format(auth_format),
            'https':'https://{}'.format(auth_format)
        }