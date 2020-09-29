# Name: readXML_grobid
# Author: Reacubeth
# Time: 2020/7/26 14:50
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

from xml.dom.minidom import parse
import os
import time
import re


class PaperXMLGrobid:
    def __init__(self, file_path):
        self.dom = parse(file_path)
        self.data = self.dom.documentElement

    @staticmethod
    def parse_p(item_xml):
        item_text = ""
        for p in item_xml:
            p_val = str(p.childNodes[0].nodeValue).replace('\n', ' ').strip()
            p_val = re.findall('[a-zA-Z0-9\s+\t\.\!\/_,$%^*()+\"\'\-]+', p_val, re.S)
            p_val = "".join(p_val)
            item_text += p_val + '\n'
        return item_text[:-1]

    def get_paper_abstract(self):
        try:
            abstract_xml = \
                self.data.getElementsByTagName('abstract')[0].getElementsByTagName('div')[0].getElementsByTagName('p')
            return self.parse_p(abstract_xml).strip('\n')
        except Exception:
            return ''

    def get_paper_introduction(self):
        try:
            raw_xml = \
            self.data.getElementsByTagName('text')[0].getElementsByTagName('body')[0].getElementsByTagName('div')
            for item in raw_xml:
                item_head = item.getElementsByTagName('head')[0].childNodes[0].nodeValue.lower()
                if 'introduction' in item_head:
                    text = item.toprettyxml()
                    text = text.replace('<p>', '').replace('</p>', '@@@')
                    pattern = re.compile(r'<[^>]+>', re.S)
                    result = pattern.sub('', text).replace('\n', ' ')
                    result = ' '.join([i for i in result.split() if i.lower() != 'introduction']).replace('@@@', '\n')
                    p_val = re.findall('[a-zA-Z0-9\s+\t\.\!\/_,$%^*()+\"\'\-]+', result, re.S)
                    p_val = "".join(p_val)
                    return p_val.strip('\n')
            return ''
        except Exception:
            return ''

    def get_paper_conclusion(self):
        try:
            raw_xml = \
                self.data.getElementsByTagName('text')[0].getElementsByTagName('body')[0].getElementsByTagName('div')

            for item in raw_xml:
                item_head = item.getElementsByTagName('head')[0].childNodes[0].nodeValue.lower()
                if 'conclusion' in item_head or 'conclusions' in item_head:
                    text = item.toprettyxml()
                    text = text.replace('<p>', '').replace('</p>', '@@@')
                    pattern = re.compile(r'<[^>]+>', re.S)
                    result = pattern.sub('', text).replace('\n', ' ')
                    result = ' '.join([i for i in result.split() if i.lower() != 'conclusion']).replace('@@@', '\n')
                    p_val = re.findall('[a-zA-Z0-9\s+\t\.\!\/_,$%^*()+\"\'\-]+', result, re.S)
                    p_val = "".join(p_val)
                    return p_val.strip('\n')
            return ''
        except Exception:
            return ''

            return ''
        except Exception:
            return ''

    def getLeastNode(self, node):
        flag = node.hasChildNodes()
        if flag:
            for nodechild in node.childNodes:
                if nodechild.nodeType == 1 and nodechild.tagName == 'p':
                    print(nodechild.data)
                    self.getLeastNode(nodechild)


if __name__ == '__main__':
    start = time.time()
    paper = PaperXMLGrobid('upload/dde_test/parse/10三古，巴西马里诺冰期盖帽白云岩.grobid.xml')
    print(paper.get_paper_introduction())
    print(time.time() - start)
