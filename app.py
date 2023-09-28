from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import stripe

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['DATABASE'] = 'subscriptions.db'

stripe.api_key = "your_stripe_api_key_here"

def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    return db

@app.route('/')
def index():
    if 'user' in session:
        return 'Welcome, {}!'.format(session['user'])
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    db.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
    if user:
        session['user'] = user[1]
        return redirect(url_for('index'))
    flash('Invalid credentials')
    return redirect(url_for('index'))

@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')

@app.route('/payment', methods=['POST'])
def payment():
    token = request.form['stripeToken']
    try:
        charge = stripe.Charge.create(
            amount=1000, #amount in cents
            currency="usd",
            source=token,
            description="Subscription Fee"
        )
        db = get_db()
        db.execute('UPDATE users SET subscribed=1 WHERE username=?', (session['user'],))
        db.commit()
    except stripe.stripeError as e:
        flash('Payment failed: {}'.format(e))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
