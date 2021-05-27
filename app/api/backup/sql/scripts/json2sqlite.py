from sql.database import SessionLocal, engine
from sql.models import Base, Disease, MedicalDepartment
import pandas as pd
import json
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)
session = Session(bind=engine)
res = []

with open("./result.txt", "r") as fin:
    for line in fin:
        obj = eval(line)
        # print(obj)
        disease = Disease(
            name=obj["疾病名"],
            category=obj["科室"],
            alias=obj["别名"] if "别名" in obj else None,
            overview=obj["概述"] if "概述" in obj else None,
            epidemiology=obj["流行病学"] if "流行病学" in obj else None,
            etiology=obj["病因与发病机制"] if "病因与发病机制" in obj else None,
            diagnostic_points=obj["诊断要点"] if "诊断要点" in obj else None,
            treatment=obj["治疗概述"] if "治疗概述" in obj else None,
            prevention=obj["预防"] if "预防" in obj else None
        )

        item = MedicalDepartment
        res.append(disease)
session.add_all(res)
session.commit()
session.close()
# res = []
# with open("./result.txt", "r") as fin:
#     for line in fin:
#         obj = eval(line)
#         # print(obj)
#         res.append(obj["科室"])
# departments = []
# for name in set(res):
#     item = MedicalDepartment(name=name, description="")
#     departments.append(item)
# session.add_all(departments)
# session.commit()
# session.close()

# drugs.to_sql('domestic_drugs', con, index=False)
# # drugs = pd.read_excel(
# #     '../data/国家药品编码本位码信息（进口药品）.xls',
# #     sheet_name='国家药品编码本位码信息(进口药品)',
# #     skiprows=2,
# #     header=0)
# # drugs.to_sql('import_drugs', con, index=False)
# con.commit()
# con.close()
