import hashlib
import subprocess
import signal
import os
import pudb
from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from datetime import datetime


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db. String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    # sets up one-to-many relationships between user-posts
    # Users have many posts and many games
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    games = db.relationship('Game', backref='player', lazy='dynamic')

    # makes password a write-only property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        # stores cached avatar MD5 hash is self.avatar_hash
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    # performs a "bitwise and" operation between the requested permission
    # and the permissions of the assigned role. Returns true if user has
    # permissions, else false
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # called each time a request from the user is received
    # refreshes self.last_seen each time user visits site
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if self.query.filter_by(email=new_email) is None:
            return False
        self.email = new_email
        # caches new avatar_hash in db as self.avatar_hash
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def gravatar(self, size=100, default='identicon', rating='g'):
        generate_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or generate_hash
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    # I wrote this function to check if current_user is owner of the chess game
    # being viewed
    # because if game belongs to current_user, then "quit" buttons should be
    # visible
    # quit buttons should not be visible to other users
    def is_game_owner(self, game_id):
        games = Game.query.filter_by(player_id=self.id).all()
        game_id_array = []
        game_id = int(game_id)
        for game in games:
            game_id_array.append(game.id)
        if game_id in game_id_array:
            return True
        else:
            return False

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # posts have one user and one game
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_played = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    proc_pid = db.Column(db.Integer)
    fen_state = db.Column(db.String(128))
    cpu_moves = []
    usr_moves = []
    # Games have one player and many posts
    player_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posts = db.relationship('Post', backref='game', lazy='dynamic')

    def start_playing(self, ai):
        if ai is "gnuchess":
            proc = subprocess.Popen(
                [os.environ.get('GNUCHESS_PATH'), '--post'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )
        if ai is "crafty":
            proc = subprocess.Popen(
                [os.environ.get('CRAFTY_PATH'), "time sd/15"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )
        self.proc_pid = proc.pid
        print self.proc_pid
        return proc
        # save self.proc.pid
        # self.cpu_moves = []
        # self.usr_moves = []

    def kill_proc(self):
        # get process with self.proc.pid
        # pu.db
        try:
            os.kill(self.proc_pid, signal.SIGKILL)
        except Exception as e:
            print "Process no longer running"
            print e
        try:
            os.kill(self.proc_pid + 1, signal.SIGKILL)
        except Exception as e:
            print "Process +1 no longer running"
            print e
        try:
            os.kill(self.proc_pid + 2, signal.SIGKILL)
        except Exception as e:
            print "Process +2 no longer running"
            print e
        return True

    def save_board_state(self, fen_string):
        self.fen_state = fen_string
        return True


# is registered as the class of the object that is assinged to
# current_user with the user is not logged in.
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    # the return value is a user object, or None
    return User.query.get(int(user_id))
