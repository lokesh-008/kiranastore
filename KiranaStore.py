from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

# HTML Template
html_form = """
<!doctype html>
<title>Kirana Billing</title>
<h2>Kirana Bill Calculator</h2>
<form method="POST">
    <label>Enter Price (or click Finish):</label><br>
    <input type="number" name="price" autofocus>
    <button type="submit" name="action" value="add">Add</button>
    <button type="submit" name="action" value="finish">Finish</button>
</form>

{% if total is not none %}
    <p><strong>Order total so far:</strong> ₹{{ total }}</p>
{% endif %}

{% if items %}
    <p><strong>Items:</strong></p>
    <ul>
    {% for item in items %}
        <li>₹{{ item }}</li>
    {% endfor %}
    </ul>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def kirana():
    if 'items' not in session:
        session['items'] = []

    if request.method == 'POST':
        action = request.form['action']
        if action == 'add':
            price = request.form.get('price')
            if price and price.isdigit():
                session['items'].append(int(price))
                session.modified = True
        elif action == 'finish':
            total = sum(session['items'])
            items = session['items']
            session.clear()  # Clear session after finishing
            return f"<h2>Thank you for using the service!</h2><p>Your total bill is ₹{total}</p><p>Items: {items}</p>"

    items = session.get('items', [])
    total = sum(items) if items else None
    return render_template_string(html_form, items=items, total=total)

if __name__ == "__main__":
    app.run(debug=True)
