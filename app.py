from flask import Flask, render_template, url_for,flash,session,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLACHEMY_DATABASE_URI'] = 'mysql+pymsql://root.!AweSomeNess150@localhost/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class blog_posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(100),nullable=False,default='N/A')
    
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return f'Blog Post {self.id}'
    
    
    
@app.route('/', methods=['GET','POST'])
def home():
    return render_template('home.html')


@app.route('/posts', methods=['GET','POST'])
def posts():
    if request.method == 'POST': 
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form.get('author',False)
        new_post = blog_posts(title=post_title,content=post_content,author= post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = blog_posts.query.all()
        return render_template('posts.html',all_posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id): 
    post = blog_posts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post = blog_posts.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form.get('author',False)
        db.session.commit()
        return redirect('/posts')
    return render_template('edit.html',post=post)

@app.route('/posts/new')
def new():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form.get('author',False)
        new_post = blog_posts(title=post_title,content=post_content,author= post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    return render_template('/new_post.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)