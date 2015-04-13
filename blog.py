from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/skeleton/test.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140), unique=True)
    content = db.Column(db.String(5000))

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return "Title: {title}, content: {content}".format(title=self.title, content=self.content)

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/')
def home():
    return render_template('index.html', articles = Article.query.all())


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,  debug=True)
