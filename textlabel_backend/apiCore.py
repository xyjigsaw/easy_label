# Name: apiCore
# Author: Reacubeth
# Time: 2020/6/22 21:45
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from pydantic import BaseModel
import threading
import time
import os
import uuid

from db_toolkit import db_get_project, db_insert_project, db_delete_project, db_insert_file, \
    db_get_entity_class, db_update_entity_class, db_delete_entity_class, db_fetch_file_limit, \
    db_update_entity_list, db_insert_entity_class, db_change_status
from toolkit.pdf_parser import Parser
from readXML import PaperXML
from readXML_grobid import PaperXMLGrobid
from wsCore import users, routes

app = FastAPI(routes=routes)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://10.10.10.1:8082",
    "http://10.10.10.1:8081",
    "http://10.10.10.1:8080",
    "http://10.10.10.2:8080",
    "http://192.168.0.3:8080",
    "http://192.168.0.4:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#############################################
# Basic
#############################################


class ProjectItem(BaseModel):
    p_id: str = ''
    name: str = ''


@app.post('/fetch_project')
async def fetch_project(request: ProjectItem):
    start = time.time()
    api_data = db_get_project()
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch Project Success')
    return {"message": "success", 'time': time.time() - start, 'data': api_data}


class ClassItem4project(BaseModel):
    p_id: str = ''


@app.post('/fetch_class')
async def fetch_class(request: ClassItem4project):
    start = time.time()
    p_id = request.p_id
    api_data = db_get_entity_class(p_id)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch Entity_class Success')
    return {"message": "success", 'time': time.time() - start, 'data': api_data}


class ClassItem(BaseModel):
    addLabelName: str = ''
    addLabelColor: str = ''
    addLabelDes: str = ''
    p_id: str = ''


@app.post('/add_class')
async def add_class(request: ClassItem):
    start = time.time()
    try:
        addLabelName = request.addLabelName
        addLabelColor = request.addLabelColor
        addLabelDes = request.addLabelDes
        p_id = request.p_id
        info = db_insert_entity_class(addLabelName, addLabelColor, addLabelDes, p_id)
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Add Entity_class Success')
        return {"message": info, 'time': time.time() - start, 'data': ''}
    except Exception as e:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Add Entity_class Error')
        return {"message": str(e), 'time': time.time() - start, 'data': ''}


class UpdateClassItem(BaseModel):
    rLabelName: str = ''
    rLabelColor: str = ''
    rLabelDes: str = ''
    c_id: str = ''


@app.post('/update_class')
async def update_class(request: UpdateClassItem):
    start = time.time()
    try:
        rLabelName = request.rLabelName
        rLabelColor = request.rLabelColor
        rLabelDes = request.rLabelDes
        c_id = request.c_id
        info = db_update_entity_class(rLabelName, rLabelColor, rLabelDes, c_id)
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Update Entity_class Success')
        return {"message": info, 'time': time.time() - start, 'data': ''}
    except Exception as e:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Update Entity_class Error')
        return {"message": str(e), 'time': time.time() - start, 'data': ''}


class DeleteClassItem(BaseModel):
    c_id: str = ''


@app.post('/delete_class')
async def delete_class(request: DeleteClassItem):
    start = time.time()
    try:
        c_id = request.c_id
        info = db_delete_entity_class(c_id)
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Delete Entity_class Success')
        return {"message": info, 'time': time.time() - start, 'data': ''}
    except Exception as e:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Delete Entity_class Error')
        return {"message": str(e), 'time': time.time() - start, 'data': ''}


class DeleteProjectItem(BaseModel):
    p_id: str = ''
    path: str = ''


@app.post('/delete_project')
async def delete_class(request: DeleteProjectItem):
    start = time.time()
    try:
        p_id = request.p_id
        path = request.path
        info = db_delete_project(p_id)
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Delete Project Success')
        return {"message": info, 'time': time.time() - start, 'data': ''}
    except Exception as e:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Delete Project Error')
        return {"message": str(e), 'time': time.time() - start, 'data': ''}


class FileItem(BaseModel):
    p_id: str = ''
    anchor: int = 0
    pageSize: int = None


@app.post('/fetch_file')
async def fetch_file(request: FileItem):
    start = time.time()
    p_id = request.p_id
    anchor = request.anchor
    pageSize = request.pageSize
    api_data = db_fetch_file_limit(p_id, anchor, pageSize)
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Fetch File Success')
    return {"message": "success", 'time': time.time() - start, 'data': api_data}


class SubmitFileItem(BaseModel):
    f_id: str = ''
    entity_list: list = []


@app.post('/submit_entity_list')
async def submit_entity_list(request: SubmitFileItem):
    start = time.time()
    try:
        f_id = request.f_id
        entity_list = request.entity_list
        info = db_update_entity_list(f_id, entity_list)
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Submit Entity_list Success')
        return {"message": info, 'time': time.time() - start, 'data': ''}
    except Exception:
        return {"message": "error", 'time': time.time() - start, 'data': ''}


class StatusItem(BaseModel):
    f_id: str = ''
    status: int = None


@app.post('/change_status')
async def change_status(request: StatusItem):
    start = time.time()
    try:
        f_id = request.f_id
        status = request.status
        info = db_change_status(f_id, status)
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'File Status Change Success')
        return {"message": info, 'time': time.time() - start, 'data': ''}
    except Exception:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'File Status Change Error')
        return {"message": "error", 'time': time.time() - start, 'data': ''}


#############################################
# Upload
#############################################


@app.post("/file_upload")
async def file_upload(file: UploadFile = File(...)):
    start = time.time()
    try:
        res = await file.read()
        with open('upload/' + file.filename, "wb") as f:
            f.write(res)
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'File Upload Success')
        return {"message": "success", 'time': time.time() - start, 'filepath': file.filename}
    except Exception as e:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'File Upload Error')
        return {"message": str(e), 'time': time.time() - start, 'filepath': file.filename}


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.pdf'):
                fullname = os.path.join(root, f)
                yield fullname


class ParseThread(threading.Thread):
    def __init__(self, tmpName, addProjectName):
        threading.Thread.__init__(self)
        self.parser = Parser('grobid')
        self.tmpName = tmpName
        self.addProjectName = addProjectName
        self.output_texts = None

    def run(self):
        print('Start Parsing ' + self.tmpName)
        try:
            self.parser.parse('text', self.tmpName, 'upload/' + self.addProjectName + '/parse', 50)
            paper = PaperXML(
                'upload/' + self.addProjectName + '/parse/' + self.tmpName[self.tmpName.rfind('/') + 1:-3] + 'cermine.xml')
            texts = paper.get_secs()

            self.output_texts = {'texts': texts, 'name': self.tmpName[self.tmpName.rfind('/') + 1:-4], 'path': self.tmpName}
        except Exception as e:
            pass
        print('Done')

    def getResult(self):
        if self.output_texts is not None:
            return self.output_texts


class ZIPItem(BaseModel):
    filePath: str = None
    addProjectName: str = None


@app.post('/unzip')
async def unzip(request: ZIPItem):
    start = time.time()
    filePath = request.filePath
    addProjectName = request.addProjectName
    # unzip upload/test.zip -d upload/xx
    cmd = 'unzip -o upload/' + filePath + ' -d upload/' + addProjectName
    os.system(cmd)

    base = 'upload/' + addProjectName  # Windows is \\
    output_texts_ls = []
    thread_pool = []
    for i in findAllFile(base):
        if '__MACOSX' not in i:
            tmpName = i.replace('\\', '/')
            print(tmpName)
            thread_pool.append(ParseThread(tmpName, addProjectName))
    for th in thread_pool:
        th.start()
    for th in thread_pool:
        th.join()
        output_texts_ls.append(th.getResult())

    p_id = str(uuid.uuid4())
    p_id = ''.join(p_id.split('-'))
    if len(output_texts_ls) == 0:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Unzip Error No Papers in zip')
        return {"message": 'No Papers in zip', 'time': time.time() - start, 'data': ''}
    try:
        file_num = 0
        for item in output_texts_ls:
            try:
                db_insert_file(item['name'], item['path'], item['texts'], p_id)
                file_num += 1
            except Exception as e:
                pass
        db_insert_project(p_id, 'upload/' + addProjectName, addProjectName, file_num)
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Unzip Success')
        return {"message": "success", 'time': time.time() - start, 'data': ''}
    except Exception as e:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Unzip Error')
        return {"message": str(e), 'time': time.time() - start, 'data': ''}


@app.get("/get_file/{file_path}")
async def download_file(file_path: str):
    file_path = file_path.replace('@@@', '/')
    print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), 'Get File: ' + file_path)
    return FileResponse(file_path)


if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000, workers=1)

# uvicorn apiCore:app --reload --port 8000 --host 0.0.0.0
# pip install python-multipart
# pip install aiofiles
