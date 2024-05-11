from db import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

"""
class Company:
    uuid str
    title str
    additionalname str
    lastmodify datetime

"""



class Company(Base):
    __tablename__='companys'

    uuid : Mapped[str] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(nullable=False)
    additionalname : Mapped[str] = mapped_column(nullable=True)
    lastmodify : Mapped[datetime]

    def __repr__(self) -> str:
        return f'Компания {self.title} меняли {self.lastmodify}'