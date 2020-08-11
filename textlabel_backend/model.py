# Name: model
# Author: Reacubeth
# Time: 2020/8/11 17:30
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

from typing import List
from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    time: float = Field(..., description='spent time', example=2.324)


class GetResponse(BaseModel):
    time: float = Field(..., description='spent time', example=2.324)
    data: List[dict] = Field(..., description='json list from database', example=[{'id': '001', 'name': 'xxx'}])


class UploadResponse(BaseModel):
    time: float = Field(..., description='spent time', example=2.324)
    filepath: str = Field(..., description='zip file name', example='KnowledgeGraph')


class UnzipResponse(BaseModel):
    time: float = Field(..., description='spent time', example=2.324)
    message: str = Field(..., description='message of unzipping', example='No Papers in zip')
