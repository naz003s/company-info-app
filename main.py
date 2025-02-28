from flask import Flask, request, render_template, redirect, url_for
from google.cloud import datastore

app = Flask(__name__)

# Initialize the Datastore client
datastore_client = datastore.Client()

# Define the Kind for Company Info
KIND = "Company_Info"

@app.route('/')
def index():
    """Home page that lists all companies."""
    query = datastore_client.query(kind=KIND)
    companies = list(query.fetch())
    return render_template('index.html', companies=companies)

@app.route('/create_company', methods=['GET', 'POST'])
def create_company():
    """Create a new company record."""
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        # Use the Ticker as the unique key
        key = datastore_client.key(KIND, data['Ticker'])
        entity = datastore.Entity(key=key)
        entity.update({
            'Ticker': data['Ticker'],
            'Company_Name': data['Company_Name'],
            'Industry': data['Industry']
        })
        datastore_client.put(entity)
        return redirect(url_for('index'))
    else:
        return render_template('create_company.html')

@app.route('/read_company/<ticker>')
def read_company(ticker):
    """Retrieve a single company record."""
    key = datastore_client.key(KIND, ticker)
    company = datastore_client.get(key)
    if not company:
        return "Company not found", 404
    return render_template('read_company.html', company=company)

@app.route('/update_company/<ticker>', methods=['GET', 'POST'])
def update_company(ticker):
    """Update a company record."""
    key = datastore_client.key(KIND, ticker)
    company = datastore_client.get(key)
    if not company:
        return "Company not found", 404

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        company['Company_Name'] = data['Company_Name']
        company['Industry'] = data['Industry']
        datastore_client.put(company)
        return redirect(url_for('read_company', ticker=ticker))
    else:
        return render_template('update_company.html', company=company)

@app.route('/delete_company/<ticker>')
def delete_company(ticker):
    """Delete a company record."""
    key = datastore_client.key(KIND, ticker)
    datastore_client.delete(key)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
