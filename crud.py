from models import Company
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from models import Company

class CRUD:

    async def get_all(self,async_session:async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            statement = select(Company).order_by(Company.uuid)

            result = await session.execute(statement)

            return result.scalars()
        

    async def add(self, async_session:async_sessionmaker[AsyncSession], company:Company):
        async with async_session() as session:
            session.add(company)
            await session.commit()



    async def get_by_uuid(self, async_session:async_sessionmaker[AsyncSession], check_uuid:str):
        async with async_session() as session:
            statement = select(Company).filter(Company.uuid == check_uuid)

            result = await session.execute(statement)

            await result.scalars().one()

    async def update(self, async_session:async_sessionmaker[AsyncSession], update_uuid, data):
        async with async_session() as session:
            company = await self.get_by_uuid(session,update_uuid)

            company.title = data['title']
            company.additionalname = data['additionalName']
            company.lastmodify = data['lastModifiedDate']

            await session.commit()
            return company

    async def delete(self, async_session:async_sessionmaker[AsyncSession], company:Company):
        async with async_session() as session:
            session.delete(company)
            await session.commit()