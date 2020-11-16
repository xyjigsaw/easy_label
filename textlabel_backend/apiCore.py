# Name: apiCore
# Author: Reacubeth
# Time: 2020/6/22 21:45
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import uvicorn
import traceback
from fastapi import FastAPI, Query, Form, APIRouter, File, UploadFile, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
import threading
import time
import os
import uuid
import shutil
import base64

import async_db
from toolkit.pdf_parser import Parser
from readXML import PaperXML
from readXML_grobid import PaperXMLGrobid
from wsCore import users, routes
from model import *

from urllib import parse
from toolkit.sequence_tagging import text2entity

from pydantic import BaseModel
from external_db import db_search, db_rand, db_get_entity_class, db_update_entity_list, db_insert_entity_class, \
    db_update_relation_list, dqa_search_paper, dqa_all_paper_id, update_dde_mark


app = FastAPI(routes=routes)
router = APIRouter()
os.makedirs('upload', exist_ok=True)


#############################################
# Basic
#############################################


@router.get('/fetch_project', response_model=GetResponse)
async def fetch_project():
    start = time.time()
    api_data = await async_db.get_project()
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch Project Success')
    return {'time': time.time() - start, 'data': api_data}


@router.delete('/delete_project', response_model=SuccessResponse)
async def delete_project(
        p_id: str = Query(..., description='project id', example='4beb867cdeba4f259d9202f5bc58a47c'),
        path: str = Query(..., description='project path', example='/upload/xxx')
):
    start = time.time()
    path = path + '/'
    if os.path.exists(path):
        shutil.rmtree(path)
    info = await async_db.delete_project(p_id)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Delete Project Success')
    return {'time': time.time() - start}


@router.get('/fetch_class', response_model=GetResponse)
async def fetch_class(
        p_id: str = Query(..., description='project id', example='4beb867cdeba4f259d9202f5bc58a47c')
):
    start = time.time()
    api_data = await async_db.get_entity_class(p_id)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch Entity_class Success')
    return {'time': time.time() - start, 'data': api_data}


@router.post('/add_class', response_model=SuccessResponse)
async def add_class(
        addLabelName: str = Form(..., description='label name', example='Name'),
        addLabelColor: str = Form(..., description='label color', example='#00CCFF'),
        addLabelDes: str = Form(..., description='label description', example='Entity'),
        p_id: str = Form(..., description='project id', example='4beb867cdeba4f259d9202f5bc58a47c')
):
    start = time.time()
    info = await async_db.insert_entity_class(addLabelName, addLabelColor, addLabelDes, p_id)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Add Entity_class Success')
    return {'time': time.time() - start}


@router.put('/update_class', response_model=SuccessResponse)
async def update_class(
        rLabelName: str = Form(..., description='modified label name', example='Name'),
        rLabelColor: str = Form(..., description='modified color', example='#00CCFF'),
        rLabelDes: str = Form(..., description='modified description', example='Entity'),
        c_id: str = Form(..., description='label/class id', example='4beb867cdeba4f259d9202f5bc58a47c')
):
    start = time.time()
    info = await async_db.update_entity_class(rLabelName, rLabelColor, rLabelDes, c_id)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Update Entity_class Success')
    return {'time': time.time() - start}


@router.delete('/delete_class', response_model=SuccessResponse)
async def delete_class(
        c_id: str = Query(..., description='label/class id', example='4beb867cdeba4f259d9202f5bc58a47c')
):
    start = time.time()
    info = await async_db.delete_entity_class(c_id)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Delete Entity_class Success')
    return {'time': time.time() - start}


@router.get('/fetch_file', response_model=GetResponse)
async def fetch_file(
        p_id: str = Query(..., description='project id', example='4beb867cdeba4f259d9202f5bc58a47c'),
        anchor: int = Query(0, description='start row', example=11),
        pageSize: int = Query(8, description='page size', example=10)
):
    start = time.time()
    api_data = await async_db.fetch_file_limit(p_id, anchor, pageSize)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch File Success')
    return {'time': time.time() - start, 'data': api_data}


@router.put('/update_entity_list', response_model=SuccessResponse)
async def update_entity_list(
        f_id: str = Form(..., description='file id', example='Name'),
        entity_list: str = Form(..., description='entity list string type',
                                example='[{"end": 366, "type": "Research", "word": "entities", "start": 358}]')
):
    start = time.time()
    # print(entity_list)
    entity_list = eval(entity_list)
    info = await async_db.update_entity_list(f_id, entity_list)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Submit Entity_list Success')
    return {'time': time.time() - start}


@router.put('/update_relation_list', response_model=SuccessResponse)
async def update_relation_list(
        f_id: str = Form(..., description='file id', example='Name'),
        relation_list: str = Form(..., description='relation list string type',
                                example='[{"head": {}, "relation": {}, "tail": {}}]')
):
    start = time.time()
    relation_list = eval(relation_list)
    info = await async_db.update_relation_list(f_id, relation_list)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Submit Relation_list Success')
    return {'time': time.time() - start}


@router.put('/change_status', response_model=SuccessResponse)
async def change_status(
        f_id: str = Form(..., description='file id', example='Name'),
        status: int = Form(0, description='file lock', example=1)
):
    start = time.time()
    info = await async_db.change_status(f_id, status)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'File Status Change Success')
    return {'time': time.time() - start}


@router.post('/fetch_hint', response_model=GetResponse)
async def fetch_hint(
        text_detail: str = Form(..., description='text detail', example='{[]}'),
):
    start = time.time()

    text_detail = text_detail.strip('"')
    print(text_detail)
    api_data = text2entity.abstract2entity(text_detail)
    print(api_data)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch Hint Success')
    return {'time': time.time() - start, 'data': api_data}


@router.post('/heart_beat')
async def heart_beat(
        string: str = Form(..., description='random string', example='a'),
):
    start = time.time()
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'HEART BEAT ' + string)
    return {'time': time.time() - start, 'data': 'heart_beat'}


#############################################
# Upload
#############################################


@router.post("/file_upload", response_model=UploadResponse)
async def file_upload(file: UploadFile = File(..., description='ZIP file to upload. (Use multipart form)')):
    start = time.time()
    res = await file.read()
    with open('upload/' + file.filename, "wb") as f:
        f.write(res)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'File Upload Success')
    return {'time': time.time() - start, 'filepath': file.filename}


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
            pass
        print('Done')

    def getResult(self):
        if self.output_texts is not None:
            return self.output_texts


@router.get('/unzip', response_model=UnzipResponse)
async def unzip(
        filePath: str = Query(..., description='zip file path', example='upload/xxx'),
        addProjectName: str = Query(..., description='project name', example='xxx'),
        sectionList: str = Query(..., description='section to be parsed', example="['abstract']"),
):
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
    output_texts_ls = []
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

    p_id = str(uuid.uuid4())
    p_id = ''.join(p_id.split('-'))
    if len(output_texts_ls) == 0:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Unzip Error No Papers in zip')
        return {"message": 'No Papers in zip', 'time': time.time() - start}
    try:
        file_num = 0
        for item in output_texts_ls:
            try:
                await async_db.insert_file(item['name'], item['path'], item['texts'], p_id, item['entity_list'], item['hint'])
                file_num += 1
            except Exception as e:
                pass
        await async_db.insert_project(p_id, 'upload/' + addProjectName, addProjectName, file_num)
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Unzip Success')
        return {"message": "success", 'time': time.time() - start}
    except Exception as e:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Unzip Error')
        return {"message": str(e), 'time': time.time() - start}


@router.get("/get_file/{file_path}")
async def download_file(file_path: str):
    file_path = parse.unquote(base64.b64decode(file_path).decode())
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Get File: ' + file_path)
    return FileResponse(file_path)


@router.get('/unzip_more', response_model=UnzipResponse)
async def unzip_more(
        p_id: str = Query(..., description='project id', example='4beb867cdeba4f259d9202f5bc58a47c'),
        filePath: str = Query(..., description='zip file path', example='upload/xxx'),
        projectName: str = Query(..., description='project name', example='xxx'),
        sectionList: str = Query(..., description='section to be parsed', example="['abstract']"),
):
    start = time.time()
    add_id = str(uuid.uuid4())
    add_id = ''.join(add_id.split('-'))
    cmd = 'unzip -o upload/' + filePath + ' -d upload/' + projectName + '/' + add_id
    os.system(cmd)
    base = os.path.join('upload', projectName, add_id)
    output_texts_ls = []
    thread_pool = []
    for i in findAllFile(base):
        if '__MACOSX' not in i:
            tmpName = i.replace('\\', '/')
            thread_pool.append(ParseThread(tmpName, projectName, sectionList.split(',')))
    for th in thread_pool:
        th.start()
    for th in thread_pool:
        th.join()
        output_texts_ls.append(th.getResult())

    if len(output_texts_ls) == 0:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Unzip Error No Papers in zip')
        return {"message": 'No Papers in zip', 'time': time.time() - start}
    try:
        file_num = 0
        for item in output_texts_ls:
            try:
                await async_db.insert_file(item['name'], item['path'], item['texts'], p_id, item['entity_list'], item['hint'])
                file_num += 1
            except Exception as e:
                print(e)

        await async_db.update_project(p_id, file_num)
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Unzip Add Success')
        return {"message": "success", 'time': time.time() - start}
    except Exception as e:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Unzip Add Error')
        return {"message": str(e), 'time': time.time() - start}


#############################################
# Researcher
#############################################

@router.get("/research_get")
async def research_get(name: str, affiliation: str, limit: int, version: str):
    start = time.time()
    api_data = await db_search(name, affiliation, limit, version)
    return {"message": "success", 'time': time.time() - start, 'data': api_data}


class ResearchItem(BaseModel):
    name: str = ''
    affiliation: str = ''
    limit: int = 10
    rand_search: int = 0
    version: str = ''


@router.post('/research_post')
async def research_post(request: ResearchItem):
    start = time.time()
    name = request.name
    affiliation = request.affiliation
    limit = request.limit
    rand_search = request.rand_search
    version = request.version
    if rand_search == 1:
        api_data = await db_rand(version)
    else:
        api_data = await db_search(name, affiliation, limit, version)
    entity_class = await db_get_entity_class()
    print('Search: ', 'success', name, affiliation, limit,
          time.strftime('%Y/%m/%d/%H/%M/%S', time.localtime(time.time())))
    return {"message": "success", 'time': time.time() - start, 'data': api_data, 'entity_class': entity_class}


class SubmitItem(BaseModel):
    e_id: str = ''
    res: dict = {}
    version: str = ''


@router.post('/research_submit')
async def research_submit(request: SubmitItem):
    start = time.time()
    try:
        e_id = request.e_id
        res = request.res
        version = request.version
        info = await db_update_entity_list(e_id, str(res['Entity_list']), version)
        print('Submit: ', info, e_id, time.strftime('%Y/%m/%d/%H/%M/%S', time.localtime(time.time())))
        return {"message": info, 'time': time.time() - start, 'data': ''}
    except Exception:
        return {"message": "error", 'time': time.time() - start, 'data': ''}


@router.post('/research_rel_submit')
async def research_rel_submit(request: SubmitItem):
    start = time.time()
    try:
        e_id = request.e_id
        res = request.res
        version = request.version
        info = await db_update_relation_list(e_id, str(res['Relation_list']), version)
        print('Submit: ', info, e_id, time.strftime('%Y/%m/%d/%H/%M/%S', time.localtime(time.time())))
        return {"message": info, 'time': time.time() - start, 'data': ''}
    except Exception:
        return {"message": "error", 'time': time.time() - start, 'data': ''}


class ClassItem(BaseModel):
    addLabelName: str = ''
    addLabelColor: str = ''


@router.post('/research_class_submit')
async def research_class_submit(request: ClassItem):
    start = time.time()
    try:
        addLabelName = request.addLabelName
        addLabelColor = request.addLabelColor
        info = await db_insert_entity_class(addLabelName, addLabelColor)
        print('Submit Label: ', info, addLabelName, addLabelColor,
              time.strftime('%Y/%m/%d/%H/%M/%S', time.localtime(time.time())))
        return {"message": info, 'time': time.time() - start, 'data': ''}
    except Exception:
        return {"message": "error", 'time': time.time() - start, 'data': ''}


#############################################
# Figure
#############################################

@router.get('/fetch_figure_class', response_model=GetResponse)
async def fetch_figure_class():
    start = time.time()
    api_data = await async_db.get_figure_class()
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch figure_class Success')
    return {'time': time.time() - start, 'data': api_data}


@router.get('/fetch_figure', response_model=GetResponse)
async def fetch_figure(
        figure_id: str = Query(..., description='figure id', example='4beb867cdeba4f259d9202f5bc58a47c')
):
    start = time.time()
    api_data = await async_db.get_figure(figure_id)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch figure Success')
    return {'time': time.time() - start, 'data': api_data}


@router.get('/fetch_rand_figure', response_model=GetResponse)
async def fetch_rand_figure():
    start = time.time()
    api_data = await async_db.get_rand_figure()
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch rand figure Success')
    return {'time': time.time() - start, 'data': api_data}


@router.put('/update_figure_class', response_model=SuccessResponse)
async def update_figure_class(
        figure_id: str = Form(..., description='figure id', example='4beb867cdeba4f259d9202f5bc58a47c'),
        figure_class: str = Form(..., description='figure class', example='research')
):
    start = time.time()
    info = await async_db.update_figure_class(figure_id, figure_class)
    print(figure_id, figure_class)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Update figure class Success')
    return {'time': time.time() - start}


#############################################
# dqa
#############################################

@router.get('/fetch_dqa_paper', response_model=GetResponse)
async def fetch_dqa_paper(
        paper_id: str = Query(..., description='paper id', example='448724959')
):
    start = time.time()
    api_data = await dqa_search_paper(paper_id)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch dqa paper Success')
    return {'time': time.time() - start, 'data': api_data}


@router.get('/fetch_all_paper_id', response_model=GetResponse)
async def fetch_all_paper_id():
    start = time.time()
    api_data = await dqa_all_paper_id()
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch all paper id Success')
    return {'time': time.time() - start, 'data': api_data}


@router.put('/update_dqa_mark', response_model=SuccessResponse)
async def update_dqa_mark(
        dpaqn_id: str = Form(..., description='dpaqn id', example='448724959'),
        mark: str = Form(..., description='mark value', example='1')
):
    start = time.time()
    info = await update_dde_mark(dpaqn_id, mark)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Update DDE mark Success')
    return {'time': time.time() - start}



#############################################
# Config
#############################################


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        # print(e)
        # print("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
        traceback.print_exc()
        return Response("Internal server error", status_code=500)


app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8000, workers=1)

# uvicorn apiCore:app --reload --port 8000 --host 0.0.0.0
# pip install python-multipart
# pip install aiofiles
