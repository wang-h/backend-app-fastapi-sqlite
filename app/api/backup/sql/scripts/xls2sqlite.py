import pandas as pd
import json
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql.database import SessionLocal, engine
from sql.models import Base, Disease, MedicalDepartment, Drug

Base.metadata.create_all(bind=engine)
session = Session(bind=engine)
res = []
sheet = pd.read_excel(
    './sql/data/国家药品编码本位码信息（国产药品）.xls',
    sheet_name='国家药品编码本位码信息(国产药品)',
    skiprows=2,
    header=0)
print(type(sheet))
for index, row in sheet.iterrows():
    #print(index, row)
    drug = list(row)
    print(drug)
    session.add(Drug(name=drug[2],
                     approval_number=drug[1],
                     dosage=drug[3],
                     specification=drug[4],
                     mah=drug[5] if str(drug[5]) != "nan" else drug[6],
                     producer=drug[6] if str(drug[6]) != "nan" else drug[5],
                     code=str(drug[7]),
                     description=""))
# drugs.to_sql('domestic_drugs', session, index=False)
# # drugs = pd.read_excel(
# #     '../data/国家药品编码本位码信息（进口药品）.xls',
# #     sheet_name='国家药品编码本位码信息(进口药品)',
# #     skiprows=2,
# #     header=0)
# # drugs.to_sql('import_drugs', con, index=False)


session.commit()
session.close()
