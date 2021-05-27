from fastapi.encoders import jsonable_encoder
from jieba import Tokenizer
import jieba
from fastapi import APIRouter, Depends
from typing import Optional, List
import redis
from starlette.responses import JSONResponse
from ..dependencies import get_token_header
from collections import defaultdict
from ..sql import crud
from ..sql import models
from ..sql import schemas
from ..sql.database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import status
from fastapi import Response
from ..database import get_db
models.Base.metadata.create_all(bind=engine)
##########################################
router = APIRouter()

tokenizer = Tokenizer()
redis_con = redis.Redis(host='localhost', port=6379,
                        decode_responses=True, db=0)


def set_len_data(ip):
    """访问次数统计"""
    ip_lens = redis_con.hmget('ip', ip)[0]
    if ip_lens == None:
        '未记录IP'
        ip_dict = {ip: 1, 'is_active': 0}
        lens_lens = 1
    else:
        ip_lens = int(ip_lens)+1
        ip_dict = {ip: ip_lens}
    redis_con.hmset('ip', ip_dict)
    return ip_lens


def load_predefined_dicts(tk):
    d = {}
    dict_list = [
        "api/dicts/general.txt",
        "api/dicts/symptom.txt",
        "api/dicts/drug.txt",
        "api/dicts/disease.txt"
    ]
    for item in dict_list:
        tk.load_userdict(item)
        with open(item, "r") as fin:
            for key in fin:
                d[key.rstrip("\n")] = item.rstrip(".txt").split('/')[-1]
    return d


dic = load_predefined_dicts(tokenizer)
##########################################


@router.get("/word-segmentation/", name="医学分词")
async def word_segmentation(response: Response, use_term_table: bool = False, text: Optional[str] = None):

    if use_term_table:
        result = tokenizer.cut(text, cut_all=False)

    else:
        result = jieba.cut(text, cut_all=False)
    response.status_code = status.HTTP_200_OK
    data = {
        "result": "  ".join(result)}
    return {"data": data}


@router.get("/term-extraction/", name="术语提取")
async def term_extraction(use_term_table: bool = False, text: Optional[str] = None):
    result = list(tokenizer.cut(text, cut_all=False))
    labels = [dic[word] if word in dic else 'O' for word in result]

    uni_tags = set(labels)
    terms = {}
    for tag in uni_tags:
        terms[tag] = set([result[index] for index,
                          value in enumerate(labels) if value == tag])
    data = {
        "result": " ".join(result),
        "labels": " ".join(labels),
        "terms": [{"name": item, "type": k.upper()} for k, v in terms.items() for item in v if k != "O"]}

    return {"data": data}


@ router.get("/word-embedding/", name="词向量生成")
async def word_segmentation(use_term_table: List[str], text: Optional[str] = None):
    result = jieba.cut(text, cut_all=False)
    data = {
        "result": "  ".join(result)}
    return {"data": data}


@ router.get("/knowledge-graph/", name="知识图谱")
async def knowledge_graph(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), text: Optional[str] = None):
    drugs = crud.get_drugs(db, skip=skip, limit=min(limit, 200))

    drug_names = {x: i for i, x in enumerate(
        set(drug.name for drug in drugs))}
    drug_producers = {x: i for i, x in enumerate(
        set(drug.producer for drug in drugs))}
    nodes = []
    node_num = 0

    for name in drug_names:
        nodes.append({"id": node_num,  "name": name})
        node_num += 1
    num_drug = node_num
    for name in drug_producers:
        nodes.append({"id": node_num,  "name": name})
        node_num += 1
    categories = ["drug", "producer"]
    links = [{"id": i, "source": drug_names[drug.name],
              "target": num_drug + drug_producers[drug.producer]} for i, drug in enumerate(drugs)]

    data = {
        "nodes": nodes,
        "links": links,
    }
    #json_compatible_item_data = jsonable_encoder({"data": data})
    # return {"data": data}
    return {"data": data}
    # json_compatible_item_data = jsonable_encoder(data)
    # # JSONResponse(content=json_compatible_item_data)
    # return JSONResponse(content=json_compatible_item_data)


# 数据库查询操作
