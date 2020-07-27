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

    def get_paper_abstract(self):
        abstract_xml = \
            self.data.getElementsByTagName('abstract')[0].getElementsByTagName('div')[0].getElementsByTagName('p')
        abstract_text = ""
        for p in abstract_xml:
            p_val = str(p.childNodes[0].nodeValue).replace('\n', ' ').strip()
            p_val = re.findall('[a-zA-Z0-9\s+\t\.\!\/_,$%^*(+\"\'\-]+', p_val, re.S)
            p_val = "".join(p_val)
            abstract_text += p_val + '\n'
        return abstract_text[:-1]


if __name__ == '__main__':
    start = time.time()
    paper = PaperXML('xxx/acemap.grobid.xml')
    print(paper.get_paper_abstract())
    print(time.time() - start)
