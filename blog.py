from flask import Flask
from flask_admin import Admin
from flask import render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask import url_for
from time import time
from flask import request
from wtforms import Form, TextField, TextAreaField, validators
#next is tricky
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/skeleton/test.db'
app.secret_key = 'rykdtfigcuohtgreafgsdhic;hpq'

db = SQLAlchemy(app)
admin = Admin(app)


class ArtForm(Form):
    title = TextField('Title', [validators.Length(min=3,max=140)])
    content = TextAreaField('Content')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True,autoincrement=True )
    title = db.Column(db.String(140), unique = True)
    content = db.Column(db.String(5000))

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return "Title: {title}, content: {content}".format(title=self.title, content=self.content)


admin.add_view(ModelView(Article, db.session))
@app.route('/')
def home():
    return render_template('index.html', articles = Article.query.all())

@app.route('/<int:post_id>')
def show_post(post_id):
    return render_template('single.html', article = Article.query.get(post_id), articles = Article.query.all())

@app.route('/add', methods=['GET','POST'])
def add_new():
    form = ArtForm(request.form)
    if request.method == 'POST' and form.validate():
        prefetch = Article(form.title.data, form.content.data)
        db.session.add(prefetch)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('data_input.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
