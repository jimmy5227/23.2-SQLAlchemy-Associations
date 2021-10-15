"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, users, default, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'HelloWorld'

connect_db(app)
db.create_all()


@app.route('/')
def index():
    listed_users = users.query.all()
    return render_template('index.html', listed_users=listed_users)


@app.route('/users')
def Users():
    listed_users_with_link = users.query.all()
    return render_template('users.html', listed_users_with_link=listed_users_with_link)


@app.route('/users/new')
def UsersNew():
    return render_template('users_new.html')


@app.route('/users/new', methods=['POST'])
def UsersNewPost():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    imageurl = request.form['imageurl']
    if imageurl == '':
        imageurl = default

    new_user = users(first_name=firstname,
                     last_name=lastname, image_url=imageurl)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')
    # return redirect(f'/{new_user.id}')


@app.route('/users/<int:users_id>')
def UsersUserId(users_id):
    user = users.query.get_or_404(users_id)
    post = Post.query.filter(Post.user_id == users_id)
    return render_template('users_userid.html', user=user, post=post)


@app.route('/users/<int:users_id>/delete', methods=["POST"])
def delete(users_id):

    user = users.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route('/users/<int:users_id>/edit')
def edit(users_id):
    user = users.query.get(users_id)
    return render_template('edit_a_user.html', user=user)


@app.route('/users/<int:users_id>/edit', methods=['POST'])
def edited(users_id):
    Id = request.form['id']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    imageurl = request.form['imageurl']

    user = users.query.get(Id)
    user.first_name = firstname
    user.last_name = lastname
    user.image_url = imageurl

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route('/users/<int:users_id>/posts/new')
def newPost(users_id):
    user = users.query.get(users_id)
    return render_template('post_new.html', user=user)


@app.route('/users/<int:users_id>/posts/new', methods=['POST'])
def newPosted(users_id):
    user = users.query.get(users_id)

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{users_id}')


@app.route('/posts/<int:post_id>')
def showpost(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.users
    return render_template('post_detail.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def editpost(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def editposted(post_id):
    title = request.form['title']
    postcontent = request.form['postcontent']

    post = Post.query.get(post_id)
    post.title = title
    post.content = postcontent

    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def deletepost(post_id):

    post = Post.query.get_or_404(post_id)
    user = post.users
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")
