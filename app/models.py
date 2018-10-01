from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
from hashlib import md5


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')), db.Column('followed_id', db.Integer, db.ForeignKey('users.id')))

class User(UserMixin, db.Model):
    """
    User Model
    """
    #tablename
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    about_me = db.Column(db.String(140))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    parties = db.relationship('Party', backref='user', lazy='dynamic')
    songs = db.relationship('Song', backref='song_users', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __init__(self, data):
        """
        Class constructor
        """
        self.username = data.get('username')
        self.email=data.get('email')
        self.password = self.set_password(data.get('password'))
        self.about_me = data.get(data.get('about_me'))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.last_seen = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "username: "+self.username+", password: "+self.password
        #return '<User {}>'.format(self.username)

    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_parties(self):
        followed = Party.query.join(followers, (followers.c.followed_id == Party.owner_id)).join(User, (User.id == Party.owner_id)).filter(followers.c.follower_id == self.id).order_by(Party.created_at.desc())
        own = Party.query.filter_by(owner_id=self.id)
        # print('DOBULBLEBLE')
        # print('followed: ', followed)
        # print('own: ', own)
        return followed.union(own).order_by(Party.created_at.desc())


class Party(db.Model):
    """
    Party Model
    """
    __tablename__ = 'parties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True,nullable=False)
    #queue_content = db.Column(db.Dict, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    songs = db.relationship('Song', backref='users', lazy=True)

    def __init__(self, data):
        self.title = data.get('title')
        #self.contents = data.get('queue_content')
        self.owner_id = data.get('owner_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    @staticmethod
    def get_all_parties_with_owner_id():
        return Party.query.join(User).add_columns(User.username, Party.title, Party.created_at).order_by(Party.created_at).limit(10)

class Song(db.Model):
    """
    Songs Model
    """
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    artist = db.Column(db.String(128), nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'), nullable=False)
    vote_count = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.title = data.get('title')
        self.artist=data.get('artist')
        self.vote_count = 1
        self.party_id = data.get('party_id')
        self.owner_id = data.get('owner_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.last_seen = datetime.datetime.utcnow()
