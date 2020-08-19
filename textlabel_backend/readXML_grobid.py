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
            p_val = re.findall('[a-zA-Z0-9\s+\t\.\!\/_,$%^*(+\"\'\-]+', p_val, re.S)
            p_val = "".join(p_val)
            item_text += p_val + '\n'
        return item_text[:-1]

    def get_paper_abstract(self):
        try:
            abstract_xml = \
                self.data.getElementsByTagName('abstract')[0].getElementsByTagName('div')[0].getElementsByTagName('p')
            return self.parse_p(abstract_xml)
        except Exception:
            return ''

    def get_paper_introduction(self):
        try:
            raw_xml = \
                self.data.getElementsByTagName('text')[0].getElementsByTagName('body')[0].getElementsByTagName('div')[0].getElementsByTagName('head')[0]

            if raw_xml.childNodes[0].nodeValue.lower() == 'introduction':
                introduction_xml = \
                    self.data.getElementsByTagName('text')[0].getElementsByTagName('body')[0].getElementsByTagName('div')[0].getElementsByTagName('p')
                return self.parse_p(introduction_xml)
            return ''
        except Exception:
            return ''

    def get_paper_conclusion(self):
        try:
            raw_xml = \
                self.data.getElementsByTagName('text')[0].getElementsByTagName('body')[0].getElementsByTagName('div')

            for item in raw_xml:
                item_head = item.getElementsByTagName('head')[0].childNodes[0].nodeValue.lower()
                if item_head == 'conclusion':
                    return self.parse_p(item.getElementsByTagName('p'))

            return ''
        except Exception:
            return ''


if __name__ == '__main__':
    start = time.time()
    paper = PaperXMLGrobid('upload/ff/parse/How to keep a knowledge base synchronized with its encyclopedia source-IJCAI2017-Liang.grobid.xml')
    print(paper.get_paper_conclusion())
    print(time.time() - start)
