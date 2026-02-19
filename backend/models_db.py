from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class Report(db.Model):
    """Database model for storing crop stress reports"""
    __tablename__ = 'reports'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Crop Information
    crop_type = db.Column(db.String(100), nullable=False)
    growth_stage = db.Column(db.String(100))
    
    # Analysis Results
    stress_level = db.Column(db.Integer)  # 0=healthy, 1=moderate, 2=severe
    confidence = db.Column(db.Float)  # 0-100 confidence percentage
    
    # Detailed Analysis Data
    observations = db.Column(db.JSON)  # List of observed symptoms
    symptom_analysis = db.Column(db.JSON)  # Detailed analysis per symptom
    recommendations = db.Column(db.JSON)  # Crop-specific recommendations
    combined_assessment = db.Column(db.Text)  # Combined text assessment
    action_priority = db.Column(db.JSON)  # Prioritized action items
    
    # AI Analysis
    ai_analysis = db.Column(db.Text)  # LLM-generated detailed analysis
    ml_based_recommendation = db.Column(db.Text)  # ML model recommendation
    
    # Location Data
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert report to dictionary for JSON response"""
        return {
            'id': self.id,
            'crop_type': self.crop_type,
            'growth_stage': self.growth_stage,
            'stress_level': self.stress_level,
            'confidence': self.confidence,
            'observations': self.observations,
            'symptom_analysis': self.symptom_analysis,
            'recommendations': self.recommendations,
            'combined_assessment': self.combined_assessment,
            'action_priority': self.action_priority,
            'ai_analysis': self.ai_analysis,
            'ml_based_recommendation': self.ml_based_recommendation,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_minimal(self):
        """Minimal response for list endpoints"""
        return {
            'id': self.id,
            'crop_type': self.crop_type,
            'stress_level': self.stress_level,
            'confidence': self.confidence,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
