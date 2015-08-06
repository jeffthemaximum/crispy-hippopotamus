from datetime import datetime
from flask import render_template, redirect, url_for
from flask import flash, abort, request, current_app
from flask.ext.login import current_user, login_required
from . import main
from .. import db
from ..models import User, Role, Post, Permission, Game
from ..decorators import admin_required
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from .forms import StartChessForm
import json
import pudb


@main.route('/')
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())


@main.route('/posts', methods=['POST', 'GET'])
@login_required
def posts():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(
            body=form.body.data,
            author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.posts'))
    # page number is obtained from request's query string
    # which is available at request.args
    # when a page isn't given, a default of 1 is used
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,
        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template(
        'posts.html',
        form=form,
        posts=posts,
        pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['POST', 'GET'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("Ur profiles been updatd")
        return redirect(url_for('.user', username=current_user.username))
    # prepopulates form with data that's already in the db for the user
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash("Da profilez been upd8td")
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', user=user, form=form)


@main.route('/chess', methods=['POST', 'GET'])
@login_required
def chess():
    form = StartChessForm()
    if form.validate_on_submit():
        game = Game(player_id=current_user.id)
        game.start_playing()
        db.session.add(game)
        return render_template('chess.html')
    current_user_name = current_user.name
    return render_template(
        'start_chess.html',
        form=form,
        username=current_user_name)


@main.route('/getmethod/<jsdata>')
@login_required
def get_javascript_data(jsdata):
    current_game = Game.query.filter_by(player_id=current_user.id).order_by(Game.id.desc()).first()
    # current_game = Game.query.filter_by(proc_id=current_user.id).last()
    jsdata = jsdata[1:5]
    inp = jsdata + "\n"
    print 'sending:', repr(inp)

    # add usr move to list
    current_game.usr_moves.append(inp[:4])
    print "usr: ", repr(current_game.usr_moves)

    # send usr move to gnuchess via subprocess
    # pu.db
    current_game.make_move(input=inp)
    return jsdata


# instantiate a GET route to push python data to js
@main.route('/getpythondata')
def get_python_data():
    current_game = Game.query.filter_by(player_id=current_user.id).order_by(Game.id.desc()).first()
    print "hello world"
    for i in range(0, 5):
        # pu.db
        line = current_game.proc.stdout.readline().rstrip()
        print line

    # append cpu move to list
        if i == 4:
            cpu_line = line[-4:]
            current_game.cpu_moves.append(cpu_line)
            cpu_line = list(cpu_line)
            cpu_line.insert(2, "-")
            cpu_line = "".join(cpu_line)
            pythondata = cpu_line
            print"json_move: ", repr(pythondata)
    print "cpu: ", repr(current_game.cpu_moves)

    return json.dumps(pythondata)
