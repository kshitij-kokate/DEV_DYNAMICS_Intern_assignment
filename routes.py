from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Person, Expense, Settlement
from utils import calculate_balances, calculate_settlements
from decimal import Decimal, InvalidOperation
import logging

@app.route('/')
def index():
    """Home page showing recent expenses and quick stats"""
    try:
        expenses = Expense.query.order_by(Expense.created_at.desc()).limit(10).all()
        people = Person.query.all()
        total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
        
        # Quick balance calculation
        balances = calculate_balances()
        
        return render_template('index.html', 
                             expenses=expenses, 
                             people=people,
                             total_expenses=float(total_expenses),
                             balances=balances)
    except Exception as e:
        logging.error(f"Error in index route: {e}")
        flash('An error occurred while loading the page.', 'error')
        return render_template('index.html', expenses=[], people=[], total_expenses=0, balances={})

@app.route('/expenses')
def list_expenses():
    """List all expenses with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        expenses = Expense.query.order_by(Expense.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('index.html', expenses=expenses.items, pagination=expenses)
    except Exception as e:
        logging.error(f"Error in list_expenses route: {e}")
        flash('An error occurred while loading expenses.', 'error')
        return redirect(url_for('index'))

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    """Add a new expense"""
    if request.method == 'GET':
        people = Person.query.all()
        categories = Expense.CATEGORIES
        return render_template('add_expense.html', people=people, categories=categories)
    
    try:
        # Validate and process form data
        amount_str = request.form.get('amount', '').strip()
        description = request.form.get('description', '').strip()
        paid_by_name = request.form.get('paid_by', '').strip()
        category = request.form.get('category', 'Other')
        
        # Validation
        if not amount_str or not description or not paid_by_name:
            flash('All fields are required.', 'error')
            people = Person.query.all()
            categories = Expense.CATEGORIES
            return render_template('add_expense.html', people=people, categories=categories)
        
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                flash('Amount must be positive.', 'error')
                people = Person.query.all()
                categories = Expense.CATEGORIES
                return render_template('add_expense.html', people=people, categories=categories)
        except (InvalidOperation, ValueError):
            flash('Please enter a valid amount.', 'error')
            people = Person.query.all()
            categories = Expense.CATEGORIES
            return render_template('add_expense.html', people=people, categories=categories)
        
        # Get or create person
        person = Person.get_or_create(paid_by_name)
        
        # Create expense
        expense = Expense(
            amount=amount,
            description=description,
            category=category,
            paid_by_id=person.id
        )
        
        db.session.add(expense)
        db.session.commit()
        
        flash(f'Expense "{description}" added successfully!', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding expense: {e}")
        flash('An error occurred while adding the expense. Please try again.', 'error')
        people = Person.query.all()
        categories = Expense.CATEGORIES
        return render_template('add_expense.html', people=people, categories=categories)

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    """Edit an existing expense"""
    try:
        expense = Expense.query.get_or_404(expense_id)
        
        if request.method == 'GET':
            people = Person.query.all()
            categories = Expense.CATEGORIES
            return render_template('edit_expense.html', expense=expense, people=people, categories=categories)
        
        # Process form data
        amount_str = request.form.get('amount', '').strip()
        description = request.form.get('description', '').strip()
        paid_by_name = request.form.get('paid_by', '').strip()
        category = request.form.get('category', 'Other')
        
        # Validation
        if not amount_str or not description or not paid_by_name:
            flash('All fields are required.', 'error')
            people = Person.query.all()
            categories = Expense.CATEGORIES
            return render_template('edit_expense.html', expense=expense, people=people, categories=categories)
        
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                flash('Amount must be positive.', 'error')
                people = Person.query.all()
                categories = Expense.CATEGORIES
                return render_template('edit_expense.html', expense=expense, people=people, categories=categories)
        except (InvalidOperation, ValueError):
            flash('Please enter a valid amount.', 'error')
            people = Person.query.all()
            categories = Expense.CATEGORIES
            return render_template('edit_expense.html', expense=expense, people=people, categories=categories)
        
        # Get or create person
        person = Person.get_or_create(paid_by_name)
        
        # Update expense
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.paid_by_id = person.id
        
        db.session.commit()
        
        flash(f'Expense "{description}" updated successfully!', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error editing expense: {e}")
        flash('An error occurred while updating the expense. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    """Delete an expense"""
    try:
        expense = Expense.query.get_or_404(expense_id)
        description = expense.description
        
        db.session.delete(expense)
        db.session.commit()
        
        flash(f'Expense "{description}" deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting expense: {e}")
        flash('An error occurred while deleting the expense. Please try again.', 'error')
    
    return redirect(url_for('index'))

@app.route('/balances')
def balances():
    """Show individual balances"""
    try:
        balances = calculate_balances()
        people = Person.query.all()
        
        return render_template('balances.html', balances=balances, people=people)
        
    except Exception as e:
        logging.error(f"Error calculating balances: {e}")
        flash('An error occurred while calculating balances.', 'error')
        return render_template('balances.html', balances={}, people=[])

@app.route('/settlements')
def settlements():
    """Show optimized settlements"""
    try:
        balances = calculate_balances()
        settlements = calculate_settlements(balances)
        
        return render_template('settlements.html', settlements=settlements, balances=balances)
        
    except Exception as e:
        logging.error(f"Error calculating settlements: {e}")
        flash('An error occurred while calculating settlements.', 'error')
        return render_template('settlements.html', settlements=[], balances={})

@app.route('/people')
def list_people():
    """List all people (API endpoint)"""
    try:
        people = Person.query.all()
        return jsonify({
            'success': True,
            'data': [{'id': p.id, 'name': p.name} for p in people],
            'message': 'People retrieved successfully'
        })
    except Exception as e:
        logging.error(f"Error retrieving people: {e}")
        return jsonify({
            'success': False,
            'data': [],
            'message': 'An error occurred while retrieving people'
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
