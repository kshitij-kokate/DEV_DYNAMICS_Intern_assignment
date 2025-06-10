from models import Person, Expense
from app import db
from collections import defaultdict
import logging

def calculate_balances():
    """
    Calculate how much each person has spent vs their fair share
    Returns dict with person_name: balance (positive = owed money, negative = owes money)
    """
    try:
        # Get all expenses and people
        expenses = Expense.query.all()
        people = Person.query.all()
        
        if not expenses or not people:
            return {}
        
        # Calculate total expenses and per-person share
        total_amount = sum(float(expense.amount) for expense in expenses)
        num_people = len(people)
        per_person_share = total_amount / num_people if num_people > 0 else 0
        
        # Calculate how much each person has paid
        paid_by_person = defaultdict(float)
        for expense in expenses:
            paid_by_person[expense.payer.name] += float(expense.amount)
        
        # Calculate balances (what they paid - their fair share)
        balances = {}
        for person in people:
            amount_paid = paid_by_person.get(person.name, 0)
            balance = amount_paid - per_person_share
            balances[person.name] = round(balance, 2)
        
        return balances
        
    except Exception as e:
        logging.error(f"Error calculating balances: {e}")
        return {}

def calculate_settlements(balances):
    """
    Calculate optimized settlements to minimize number of transactions
    Returns list of settlements: [{'from': person, 'to': person, 'amount': amount}]
    """
    try:
        if not balances:
            return []
        
        # Separate creditors (positive balance) and debtors (negative balance)
        creditors = [(name, balance) for name, balance in balances.items() if balance > 0.01]
        debtors = [(name, -balance) for name, balance in balances.items() if balance < -0.01]
        
        # Sort by amount (largest first)
        creditors.sort(key=lambda x: x[1], reverse=True)
        debtors.sort(key=lambda x: x[1], reverse=True)
        
        settlements = []
        
        # Match debtors with creditors
        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor_name, debt_amount = debtors[i]
            creditor_name, credit_amount = creditors[j]
            
            # Settlement amount is minimum of debt and credit
            settlement_amount = min(debt_amount, credit_amount)
            
            if settlement_amount > 0.01:  # Only create settlement if amount is significant
                settlements.append({
                    'from': debtor_name,
                    'to': creditor_name,
                    'amount': round(settlement_amount, 2)
                })
            
            # Update remaining amounts
            debtors[i] = (debtor_name, debt_amount - settlement_amount)
            creditors[j] = (creditor_name, credit_amount - settlement_amount)
            
            # Move to next debtor/creditor if current one is settled
            if debtors[i][1] < 0.01:
                i += 1
            if creditors[j][1] < 0.01:
                j += 1
        
        return settlements
        
    except Exception as e:
        logging.error(f"Error calculating settlements: {e}")
        return []

def get_expense_summary_by_category():
    """Get expenses grouped by category"""
    try:
        expenses = Expense.query.all()
        category_totals = defaultdict(float)
        
        for expense in expenses:
            category_totals[expense.category] += float(expense.amount)
        
        return dict(category_totals)
        
    except Exception as e:
        logging.error(f"Error getting expense summary: {e}")
        return {}

def get_monthly_expense_summary():
    """Get expenses grouped by month"""
    try:
        expenses = Expense.query.all()
        monthly_totals = defaultdict(float)
        
        for expense in expenses:
            month_key = expense.created_at.strftime('%Y-%m')
            monthly_totals[month_key] += float(expense.amount)
        
        return dict(monthly_totals)
        
    except Exception as e:
        logging.error(f"Error getting monthly summary: {e}")
        return {}
