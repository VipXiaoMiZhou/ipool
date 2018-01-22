import tools
import unittest

class ToolsTestCases(unittest.TestCase):

    def test_jude_http(self):
        http = 'http,eqweqe'
        self.assertEqual(1,tools.jude_procotol(http))

    def test_jude_https(self):
        https = 'https-erwesdfsfe'
        self.assertEqual(2,tools.jude_procotol(https))
        self.assertEqual(None,tools.jude_procotol(None))

class HtmlParserTest(unittest.TestCase):

    def test_chongdaili_parser(self):
        from html import ChongDaiLiHtmlParser as parser
        path = '/home/eason/workspace/python/proxy_pool/test/conf/chongdaili.html'
        html = get_html_str(path)
        p = parser()
        self.assertIsNotNone(p.parse(html))

    def test_xicidaili_parser(self):
        from html import XiCiDaiLiHtmlParser as parser
        path = '/home/eason/workspace/python/proxy_pool/test/conf/xici.html'
        p = parser()
        html = get_html_str(path)
        p.parse(html)
        pass




def get_html_str(path):
    html_content = open(path, encoding='utf8')
    html_str = ''
    for line in html_content.readlines():
        html_str = html_str + str(line)
    return html_str


if __name__ == '__main__':
    unittest.main()
