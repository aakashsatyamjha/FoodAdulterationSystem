"""
SQLAlchemy Data Models for Scan History and Product Records
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from .database import Base

class ScanRecord(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), default="Analyzed Food Product")
    brand = Column(String(255), default="N/A")
    barcode = Column(String(64), nullable=True, index=True)
    scan_type = Column(String(64), default="barcode") # 'barcode', 'ingredient_image', 'manual'
    category = Column(String(128), default="Packaged Food")
    quality_score = Column(Integer, default=50)
    risk_level = Column(String(64), default="Moderate Risk")
    ingredients = Column(Text, default="")
    adulteration_flags = Column(Text, default="[]") # JSON string
    concerning_additives = Column(Text, default="[]") # JSON string
    allergens = Column(Text, default="[]") # JSON string
    nutritional_data = Column(Text, default="{}") # JSON string
    image_url = Column(String(512), nullable=True)
    explanation = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
