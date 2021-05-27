from sql.database import SessionLocal, engine
from sql.schemas import Drug
from sql import crud
from sql.models import Base
from typing import Optional, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import jieba
from jieba import Tokenizer

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Optional, List
from sql.models import Base
from sql import crud
from sql.schemas import Drug
from sql.database import SessionLocal, engine

app = FastAPI()

tk = Tokenizer()
# tk.load_userdict("/home/ubuntu/backend/api/dict.txt")
tk.load_userdict("dict.txt")

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://localtest",
    "http://www.localtest"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/api/task/word-segmentation/", name="分词")
async def word_segmentation(use_term_table: bool = False, text: Optional[str] = None):
    if use_term_table:
        result = tk.cut(text, cut_all=False)
    else:
        result = jieba.cut(text, cut_all=False)
    data = {
        "result": "  ".join(result)}
    return {"data": data}


@app.get("/api/task/knowledge-graph/", name="知识图谱")
async def get_drugs(skip: int = 0, limit: int = 300, db: Session = Depends(get_db), text: Optional[str] = None):
    drugs = crud.get_drugs(db, skip=skip, limit=min(limit, 200))

    drug_names = {x: i for i, x in enumerate(
        set(drug.name for drug in drugs))}
    drug_producers = {x: i for i, x in enumerate(
        set(drug.producer for drug in drugs))}
    nodes = []
    node_num = 0

    for name in drug_names:
        nodes.append({"id": node_num, "category": "drug", "name": name})
        node_num += 1
    num_drug = node_num
    for name in drug_producers:
        nodes.append({"id": node_num, "category": "producer", "name": name})
        node_num += 1
    categories = ["drug", "producer"]
    links = [{"id": i, "source": drug_names[drug.name],
              "target": num_drug + drug_producers[drug.producer]} for i, drug in enumerate(drugs)]

    data = {
        "nodes": nodes,
        "links": links,
        "categories": categories
    }
    json_compatible_item_data = jsonable_encoder(data)
    # JSONResponse(content=json_compatible_item_data)
    return JSONResponse(content=json_compatible_item_data)


# 数据库查询操作
