from app import db
from datetime import datetime
from sqlalchemy import func
from decimal import Decimal

class Person(db.Model):
    """Model for people who participate in expenses"""
    __tablename__ = 'people'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses_paid = db.relationship('Expense', backref='payer', lazy=True)
    
    def __repr__(self):
        return f'<Person {self.name}>'
    
    @classmethod
    def get_or_create(cls, name):
        """Get existing person or create new one"""
        person = cls.query.filter_by(name=name).first()
        if not person:
            person = cls(name=name)
            db.session.add(person)
            db.session.flush()  # Get the ID without committing
        return person

class Expense(db.Model):
    """Model for expenses"""
    __tablename__ = 'expenses'
    
    CATEGORIES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other')
    ]
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='Other')
    paid_by_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Expense {self.description}: ${self.amount}>'
    
    @property
    def amount_float(self):
        """Convert Decimal amount to float for calculations"""
        return float(self.amount)

class Settlement(db.Model):
    """Model for tracking settlements between people"""
    __tablename__ = 'settlements'
    
    id = db.Column(db.Integer, primary_key=True)
    from_person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    to_person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    from_person = db.relationship('Person', foreign_keys=[from_person_id])
    to_person = db.relationship('Person', foreign_keys=[to_person_id])
    
    def __repr__(self):
        return f'<Settlement {self.from_person.name} owes {self.to_person.name}: ${self.amount}>'
