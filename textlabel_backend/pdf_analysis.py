# Name: unzip_parse
# Author: Reacubeth
# Time: 2020/11/27 10:24
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import threading
import time
import os
import uuid
import shutil

from toolkit.pdf_parser import Parser
from readXML_grobid import PaperXMLGrobid
from toolkit.sequence_tagging import text2entity


output_texts_ls = []
parse_done = False
p_id = ''
apn = ''


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.pdf'):
                fullname = os.path.join(root, f)
                yield fullname


class HintThread(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.text = text
        self.hintList = None

    def run(self):
        try:
            self.hintList = text2entity.abstract2entity(self.text)
        except:
            pass

    def getResult(self):
        if self.hintList is not None:
            return self.hintList


class ParseThread(threading.Thread):
    def __init__(self, tmpName, addProjectName, sectionList):
        threading.Thread.__init__(self)
        self.parser = Parser('grobid')
        self.tmpName = tmpName
        self.addProjectName = addProjectName
        self.sectionList = sectionList
        self.output_texts = None

    def run(self):
        print('Start Parsing ' + self.tmpName)
        try:
            self.parser.parse('text', self.tmpName, 'upload/' + self.addProjectName + '/parse', 50)
            paper = PaperXMLGrobid(
                'upload/' + self.addProjectName + '/parse/' + self.tmpName[
                                                              self.tmpName.rfind('/') + 1:-3] + 'grobid.xml')
            '''
            self.output_texts = {'texts': {'text_detail_0': paper.get_paper_abstract(),
                                           'text_detail_1': paper.get_paper_introduction(),
                                           'text_detail_2': paper.get_paper_conclusion()},
                                 'name': self.tmpName[self.tmpName.rfind('/') + 1:-4],
                                 'path': self.tmpName}
            '''
            if 'others' in self.sectionList:

                self.output_texts = {'texts': {},
                                     'name': self.tmpName[self.tmpName.rfind('/') + 1:-4],
                                     'path': self.tmpName,
                                     'entity_list': {},
                                     'hint': {}
                                     }
                section_texts = paper.get_paper_sections()
                hint_thread_pool = []
                text_prefix = 'text_detail_'
                for i in range(len(section_texts)):
                    self.output_texts['texts'][text_prefix + str(i)] = section_texts[i]
                    self.output_texts['entity_list'][text_prefix + str(i)] = []
                    # self.output_texts['hint'][text_prefix + str(i)] = text2entity.abstract2entity(section_texts[i])
                    hint_thread_pool.append(HintThread(section_texts[i]))
                for th in hint_thread_pool:
                    th.start()
                for i in range(len(hint_thread_pool)):
                    hint_thread_pool[i].join()
                    self.output_texts['hint'][text_prefix + str(i)] = (hint_thread_pool[i].getResult())

            else:
                self.output_texts = {'texts': {'text_detail_0': paper.get_paper_abstract(),
                                               'text_detail_1': paper.get_paper_introduction(),
                                               'text_detail_2': paper.get_paper_conclusion()},
                                     'name': self.tmpName[self.tmpName.rfind('/') + 1:-4],
                                     'path': self.tmpName,
                                     'entity_list': {'text_detail_0': [],
                                                     'text_detail_1': [],
                                                     'text_detail_2': []},
                                     'hint': {'text_detail_0': text2entity.abstract2entity(paper.get_paper_abstract()),
                                              'text_detail_1': text2entity.abstract2entity(paper.get_paper_introduction()),
                                              'text_detail_2': text2entity.abstract2entity(paper.get_paper_conclusion())}
                                     }
        except Exception as e:
            self.output_texts = {'name': self.tmpName, 'log': str(e)}
            print('Parse Error: ' + str(e))
        print('Done')

    def getResult(self):
        if self.output_texts is not None:
            return self.output_texts


async def unzip_parse(filePath, addProjectName, sectionList):
    global output_texts_ls
    global parse_done
    global apn
    apn = addProjectName
    start = time.time()
    project_dir = 'upload/' + addProjectName + '/'
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir)
    add_id = str(uuid.uuid4())
    add_id = ''.join(add_id.split('-'))
    cmd = 'unzip -o upload/' + filePath + ' -d upload/' + addProjectName + '/' + add_id
    os.system(cmd)
    base = os.path.join('upload', addProjectName, add_id)

    thread_pool = []
    for i in findAllFile(base):
        if '__MACOSX' not in i:
            tmpName = i.replace('\\', '/')
            thread_pool.append(ParseThread(tmpName, addProjectName, sectionList.split(',')))
    for th in thread_pool:
        th.start()
    for th in thread_pool:
        th.join()
        output_texts_ls.append(th.getResult())
    parse_done = True
