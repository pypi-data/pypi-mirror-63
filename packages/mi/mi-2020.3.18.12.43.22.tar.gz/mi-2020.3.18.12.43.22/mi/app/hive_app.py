#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : EmailApp
# @Time         : 2020-03-06 09:41
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import time
import pandas as pd
from typing import Optional
from fastapi import FastAPI, Form, Depends, File, UploadFile
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import \
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse
from starlette.status import *

ROUTE = ""
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)


@app.post("/my-form-endpoint")
async def my_endpoint(request: Request):
    form_data = await request.form()

    s = dict(form_data)['data'].strip().replace('null', "''")
    data = eval(s)
    df = pd.DataFrame(data[1:], columns=data[0])
    print(df)
    return "post succeed"


if __name__ == '__main__':
    import os
    import socket

    me = socket.gethostname() == 'yuanjie-Mac.local'

    uvicorn = "uvicorn" if me else "/opt/soft/python3/bin/uvicorn"

    main_file = __file__.split('/')[-1].split('.')[0]

    # --reload测试环境
    os.system(f"uvicorn {main_file}:app --reload --host 0.0.0.0 --port 9000")
