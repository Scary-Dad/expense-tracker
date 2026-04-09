from flask import Flask, render_template, request, redirect
import json
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# Load data
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        return []

# Save data
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


from collections import defaultdict

@app.route('/')
def index():
    expenses = load_data()

    selected_category = request.args.get('category')
    selected_month = request.args.get('month')

    filtered_expenses = expenses

    # Category filter
    if selected_category and selected_category != "All":
        filtered_expenses = [e for e in filtered_expenses if e['category'] == selected_category]

    # Month filter
    if selected_month and selected_month != "All":
        filtered_expenses = [
            e for e in filtered_expenses 
            if e['date'][5:7] == selected_month
        ]

    # Total
    total = sum(item['amount'] for item in filtered_expenses)

    # 👉 Chart data (IMPORTANT: use filtered_expenses)
    category_data = defaultdict(float)
    for item in filtered_expenses:
        category_data[item['category']] += item['amount']

    labels = list(category_data.keys())
    values = list(category_data.values())

    return render_template(
        'index.html',
        expenses=filtered_expenses,
        total=total,
        labels=labels,
        values=values
    )
@app.route('/add', methods=['POST'])
def add():
    expenses = load_data()
    
    new_expense = {
        'amount': float(request.form['amount']),
        'category': request.form['category'],
        'date': request.form['date']
    }
    
    expenses.append(new_expense)
    save_data(expenses)
    
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    expenses = load_data()
    expenses.pop(index)
    save_data(expenses)
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
    
app.run(debug=True, host='0.0.0.0', port=5000)