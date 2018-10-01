from app import app,db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, StartAPartyForm, AddASongForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Party, Song
import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    parties = current_user.followed_parties().paginate(page, app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('index', page=parties.next_num) if parties.has_next else None
    prev_url = url_for('index', page=parties.prev_num) if parties.has_prev else None
    #parties = Party.query.join(User).add_columns(User.username, Party.title, Party.created_at).order_by(Party.created_at).limit(10)
    #parties = Party.get_all_parties_with_owner_id()
    #parties = current_user.followed_parties().all()
    return render_template('index.html',title = 'Home', parties = parties.items, next_url = next_url, prev_url=prev_url)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    parties = Party.query.order_by(Party.created_at.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=parties.next_num) if parties.has_next else None
    prev_url = url_for('explore', page=parties.prev_num) if parties.has_prev else None
    #parties = Party.query.order_by(Party.created_at.desc()).all()
    return render_template('index.html', title='Explore', parties=parties.items, next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print('LOOK AT FORM DATA')
        print(type(form.data))
        print(form.data)
        user = User(form.data)
        user.save()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    #parties = Party.query.filter_by(owner_id = user.id).all()
    parties = user.parties.order_by(Party.created_at.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=parties.next_num) if parties.has_next else None
    prev_url = url_for('user', username=user.username, page=parties.prev_num) if parties.has_prev else None
    return render_template('user.html', user=user, parties=parties.items, next_url=next_url, prev_url=prev_url)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your chagnes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/start_a_party', methods=['GET', 'POST'])
@login_required
def start_a_party():
    form = StartAPartyForm()
    if form.validate_on_submit():
        party_data={'owner_id': current_user.id, 'title':form.title.data}
        p = Party(party_data)
        db.session.add(p)
        db.session.commit()
        flash('Your party has been added')
        return redirect(url_for('start_a_party'))
    return render_template('start_a_party.html', title='Start a Party', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/party/<party_id>', methods = ['GET', 'POST'])
@login_required
def view_party(party_id):
    print('LOOOOKKKK EHRERER')
    print(type(party_id))
    party = Party.query.filter_by(id=party_id).first_or_404()
    songs = Song.query.filter_by(party_id=int(party_id)).all()
    form = AddASongForm()
    if form.validate_on_submit():
        song_data={'owner_id': current_user.id, 'title':form.title.data, 'artist': form.artist.data, 'party_id':party_id}
        s = Song(song_data)
        db.session.add(s)
        db.session.commit()
        flash('Your song has been added to the Party')
        return redirect(url_for('view_party', party_id=party_id))

    return render_template('party.html',form=form, party=party,party_id = party_id, songs=songs)

# @app.route('/songs/<party_id>', methods=['GET', 'POST'])
# @login_required
# def add_song(party_id):
#     form = AddASongForm()
#     if form.validate_on_submit():
#         song_data = {'owner_id': current_user.id, 'title':form.title.data,'artist': form.artist.data, 'party_id':party_id, 'vote_count':'1'}
#         s = Song(song_data)
#         db.session.add(p)
#         db.session.commit()
#         flash('Your song has been added to the Party')
#         return redirect(url_for('view_party', party_id))
#
#     return render_template('party.html', party=party,party_id = party_id)
