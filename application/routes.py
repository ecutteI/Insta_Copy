from flask import render_template, redirect, url_for, flash, request, make_response, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from application import app
from application.models import *
from application.forms import *
from application.utils import save_image

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('profile', username = username))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/<string:username>')
@login_required
def profile(username):
    posts = current_user.posts
    posts.reverse()
    return render_template('profile.html', title=f'{current_user.fullname} Profile', posts = posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    user = User.query.filter_by(id=current_user.id).first()
    tmp1, tmp2 = user.join_date, user.status
    print(user.username)
    if form.validate_on_submit():
        user.username = form.username.data
        user.fullname = form.fullname.data
        user.email    = form.email.data
        user.profile_pic = save_image(form.profile_pic.data)
        if user.profile_pic == None:
            user.profile_pic = "default.png"
        user.bio = form.bio.data
        user.join_date = tmp1
        user.status = tmp2
        db.session.commit()        
        flash('Your profile is successfully updated!')

        return render_template('profile.html', title=f'{current_user.fullname} Profile', posts = current_user.posts)

    elif request.method == 'GET':
        form.username.data = user.username
        form.fullname.data = user.fullname
        form.email.data = user.email
        form.bio.data = user.bio

    return render_template('edit_profile.html', title='Edit Profile', form = form, username=user.username)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CreatePostForm()

    if form.validate_on_submit():
        post = Post(
            author_id = current_user.id,
            caption = form.caption.data
        )
        post.photo = save_image(form.post_pic.data)
        db.session.add(post)
        db.session.commit()
        flash('Your image has been posted!', 'success')

    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author_id=current_user.id)\
                        .order_by(Post.post_date.desc())\
                        .paginate(page=page, per_page=3)

    return render_template('index.html', title='Home', form=form, posts=posts)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()
    return render_template('signup.html', title='SignUp', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/forgot' )
def forgot():
    form = ForgotPasswordForm()
    return render_template('forgot_pass.html', title='Forgot Password', form=form)

@app.route('/like', methods=['GET', 'POST'])
@login_required
def like():
    data = request.json
    post_id = int(data['postId'])
    like = Like.query.filter_by(user_id=current_user.id,post_id=post_id).first()
    if not like:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return make_response(jsonify({"status" : True}), 200)
    
    db.session.delete(like)
    db.session.commit()
    return make_response(jsonify({"status" : False}), 200)

@app.route("/reset", methods=["GET", "POST"])
def reset():
    form = ResetPasswordForm()

    user = User.query.filter_by(id=current_user.id).first()

    if form.validate_on_submit():
        if user.password == form.new_password.data:
            flash('You cannot change your password to the same one')
        elif form.new_password.data != form.confirm_new_password.data:
            flash('Password and confirm password do not match')
        elif user.password != form.old_password.data:
            flash('Password is not correct')
        else:
            user.password = form.new_password.data
            posts = current_user.posts
            db.session.commit()

            return render_template('profile.html', title=f'{current_user.fullname} Profile', posts = posts)

    return render_template('reset.html', title='Reset', form = form)
@app.route('/edit_post/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):

    form = EditPostForm()

    post = Post.query.get(id)

    if form.validate_on_submit():
        post.caption = form.caption.data
        db.session.commit()
        return redirect(url_for('index', username = current_user.username))

    elif request.method == 'GET':
        form.caption.data = post.caption

    return render_template('edit_post.html', title='Edit Post', form = form)