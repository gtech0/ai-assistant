from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(100))
    budget = db.Column(db.String(100))
    lifecycle_type = db.Column(db.String(50))
    dev_type = db.Column(db.String(50))
    tech_stack = db.Column(db.Text)
    team = db.Column(db.String(255))
    team_skill_level = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    risks = db.relationship('Risk', backref='project', lazy=True, cascade='all, delete-orphan')


class Risk(db.Model):
    __tablename__ = 'risks'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    risk_type = db.Column(db.String(50))
    factor_category = db.Column(db.String(100))
    category = db.Column(db.String(100))

    probability = db.Column(db.Float)
    impact = db.Column(db.SmallInteger)
    criticality = db.Column(db.Numeric(precision=10, scale=2))
    strategy = db.Column(db.String(100))
    owner = db.Column(db.String(100))
    is_llm_generated = db.Column(db.Boolean, default=False)
