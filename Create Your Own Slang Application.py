# File: slang_app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///slang.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Slang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, unique=True)
    meaning = db.Column(db.String(255), nullable=False)
    votes = db.Column(db.Integer, default=0)

# Route for homepage with popular slang words
@app.route('/')
def index():
    slangs = Slang.query.order_by(Slang.votes.desc()).all()
    return render_template('index.html', slangs=slangs)

# Route for submitting a new slang word
@app.route('/submit', methods=['POST'])
def submit_slang():
    word = request.form.get('word')
    meaning = request.form.get('meaning')
    
    if word and meaning:
        new_slang = Slang(word=word, meaning=meaning)
        db.session.add(new_slang)
        db.session.commit()
    return redirect(url_for('index'))

# Route for voting on a slang word
@app.route('/vote/<int:slang_id>', methods=['POST'])
def vote_slang(slang_id):
    slang = Slang.query.get(slang_id)
    if slang:
        slang.votes += 1
        db.session.commit()
    return redirect(url_for('index'))

# Route for displaying the submission form page
@app.route('/submit_form')
def submit_form():
    return render_template('submit_form.html')

# Initialize the database in a function and call it in main
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()  # Initializes the database tables
    app.run(debug=True)
