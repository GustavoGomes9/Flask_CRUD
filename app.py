from os import name
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Planing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, content, description, price):
        self.content = content
        self.description = description
        self.price = price

@app.route('/') 
def index():
    plans = Planing.query.order_by(Planing.date_created).all()
    return render_template('index.html', plans=plans )

@app.route('/new', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        new_data = Planing(content=request.form['content'], description=request.form['description'], price=request.form['price'] )
        try:
            db.session.add(new_data) 
            db.session.commit()
            return redirect('/')

        except:
            return 'Sorry, something went wrong.'
    else:
        return render_template('create.html')

@app.route('/delete/<int:id>')
def delete(id):
    post_delete = Planing.query.get_or_404(id)
    try:
        db.session.delete(post_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Sorry, something went wrong."

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    post = Planing.query.get_or_404(id)

    if request.method == 'POST':
        post.content = request.form['content']
        post.description = request.form['description']
        post.price = request.form['price']

        try:
            db.session.commit()
            return redirect('/')
        except:
            'Sorry, was not possible to update'
    else:
        return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)