from fastapi import APIRouter, Depends
from typing import Optional, List
import redis
from ..sql import crud
from ..sql import models
from ..sql import schemas
from sqlalchemy.orm import Session
from collections import Counter
from fastapi import status
from ..database import get_db
##########################################
router = APIRouter()

##########################################


@router.get("/medical-department/", name="疾病百科", status_code=status.HTTP_200_OK)
async def get_medical_departments(db: Session = Depends(get_db)):
    medical_departments = crud.get_medical_departments(db)
    data = {
        "medical_departments": [medical_department.name for medical_department in medical_departments]
    }
    # return {"data": data}
    return {"data": data}


@router.get("/disease-base/", name="医学科疾病")
async def get_disease_given_medical_department(name: str, db: Session = Depends(get_db)):

    diseases = crud.get_disease_by_given_medical_department(
        db, name)
    data = {
        "diseases": [disease.name for disease in diseases]
    }
    # return {"data": data}
    return {"data": data}


@router.get("/drug/", name="医学科疾病")
async def get_drugs(db: Session = Depends(get_db)):

    drugs = crud.get_drugs(db)
    data = {
        "drugs": list(set([drug.name for drug in drugs]))
    }
    # return {"data": data}
    return {"data": data}


@router.get("/disease/", name="疾病百科")
async def get_disease_details(name: str, db: Session = Depends(get_db)):
    disease_details = crud.get_disease_by_given_name(
        db, name)
    data = {
        "disease": disease_details,
        "en2zh": {
            "CATEGORY": "【医学科】",
            "OVERVIEW": "【概述】",
            "CATEGORY": "【医学科】",
            "ETIOLOGY": "【发病原因】",
            "TREATMENT": "【治疗方案】",
            "prevention": "【预防】",
            "NAME": "【名称】",
            "ALIAS": "【别名】",
            "DIAGNOSTIC_POINTS": "【诊断要点】",
        },
    }
    # return {"data": data}
    return {"data": data}


@ router.get("/knowledge-graph/", name="药物图谱")
async def knowledge_graph(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, name: Optional[str] = ""):

    if name != "":
        data = crud.get_drugs_given_name(db, name)
    else:
        data = crud.get_drugs(db,  skip=skip, limit=min(limit, 200))
    # print(len(name))
    dependentsCount = Counter(drug.name for drug in data)
    drugs = set(list(dependentsCount.keys()))
    dependentsCount.update(drug.producer for drug in data)
    nodes = []
    for index, name in enumerate(dependentsCount.keys()):
        nodes.append({"id": index,  "name": name,
                      "category": 0 if name in drugs else 1})
    node2id = {node["name"]: node["id"] for node in nodes}
    links = [{
        "id": i,
        "source": node2id[drug.name],
        "target": node2id[drug.producer]
    } for i, drug in enumerate(data)]
    totalCount = sum(dependentsCount.values())
    data = {
        "nodes": nodes,
        "links": links,
        "categories": [
            {"name": "药品"},
            {"name": "生产商"}
        ],
        "dependentsCount": dependentsCount,
        "totalCount": totalCount,
    }
    return {"data": data}
