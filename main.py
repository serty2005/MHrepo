from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from crud import CRUD
from db import engine
from schemas import CompanyModel

app = FastAPI(
    title= 'Companys API',
    description= 'Simple service for companys',
    docs_url= '/'
)

session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
db = CRUD()

@app.get('/companys')
async def get_all_companys():
    companys = await db.get_all(session)

    return companys

@app.get('/company/{company_uuid}')
async def get_company_by_uuid(company_uuid):
    pass

@app.post('/companys')
async def add_company():
    pass

@app.patch('/company/{company_uuid}')
async def update_company(company_uuid):
    pass

