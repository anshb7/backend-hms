from sqlalchemy import Column, Integer, String, Date
from database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    doc_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  