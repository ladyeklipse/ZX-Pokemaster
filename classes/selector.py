import bs4
from bs4 import BeautifulSoup
import lxml
import lxml.html.soupparser
from lxml.etree import HTMLParser, XMLParser
try:
    from StringIO import StringIO as StringIO
except ImportError:
    from io import StringIO as StringIO
et = lxml.etree
parser = HTMLParser(encoding='utf-8', recover=True)

class Selector:

    def __init__(self, text=''):
        if not text:
            return
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        text = text.replace('&nbsp;', ' ')
        # self.tree = lxml.html.fromstring(text)
        # self.tree = lxml.etree.parse(StringIO(text), parser)
        text = str(bs4.BeautifulSoup(text, 'lxml'))
        self.tree = lxml.html.fromstring(text)

    def xpath(self, selector):
        x = Selector()
        x.tree = self.tree.xpath(selector)
        return x

    def extract_all(self, as_string=False):
        return self.extract(as_string=as_string)

    def extract(self, as_string=False):
        result = []
        for element in self.tree:
            result.append(self.extract_element(element))
        if as_string:
            return '\n'.join([x.strip() for x in result if x.strip()])
        return result

    def extract_first(self):
        if self.tree:
            return self.extract_element(self.tree[0])
        else:
            return None

    def extract_element(self, element):
        if type(element) in [str, lxml.etree._ElementStringResult,
                             lxml.etree._ElementUnicodeResult]:
            return element
        else:
            return et.tostring(element)

    def text(self):
        return [x for x in self.tree]