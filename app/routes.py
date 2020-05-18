
from app import app, db, login_manager, bcrypt
from datetime import datetime
from .forms import EventForm, LoginForm, CreateUserForm
from .models import Events, Users
from flask import redirect, request, render_template
from flask_login import login_user, current_user, login_required, logout_user


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.filter_by(user_email=user_id).first()


@app.route('/')
def index():
    posts = Events.query.all()
    users = Users.query.all()

    return render_template('index.html',posts=posts, users=users, current_user = current_user)


@app.route('/event', methods=['POST', 'GET'])
@login_required
def event():
    event_form = EventForm()

    if request.method == 'POST':

        if event_form.validate_on_submit():
            end_date = request.form.get('end_date')
            topic = request.form.get('topic')
            text = request.form.get('text')
            end_date_format = datetime.strptime(end_date, '%Y-%m-%d')
            event = Events(creator_id=current_user._id, date_start=datetime.now(), date_end=end_date_format, topic = topic, text = text)
            db.session.add(event)
            db.session.commit()
            return redirect('/')
        error = "Form was not validated:"
        return render_template('error.html',form=event_form,error = error, current_user = current_user)

    return render_template('add_event.html', form=event_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(user_email=form.email.data).first()

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect("/")
    return render_template("login.html", form=form)


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        if Users.query.filter_by(user_email=form.email.data).first():
            error = "User exists!"
            return render_template('error.html',form=form,error = error, current_user = current_user)
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users(user_email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("create_user.html", form=form)


@app.route('/getmyevents')
def getmyevents():
    posts = Events.query.filter_by(creator_id=current_user._id)
    return render_template('myevents.html',posts=posts, current_user = current_user)


@app.route('/delete/<id>')
@login_required
def delete_event(id):
    event = Events.query.filter_by(_id=id).first()
    if current_user._id == event.creator_id:
        db.session.delete(event)
        db.session.commit()
        return redirect("/getmyevents")
    error = "You do not have rights to delete this event:"
    return render_template('error.html',form=event_form,error = error, current_user = current_user)


@app.route('/edit/<id>', methods=["GET", "POST"])
@login_required
def edit_event(id):
    event = Events.query.filter_by(_id=id).first()
    event_form = EventForm(obj = event, end_date = event.date_end, topic = event.topic, text = event.text)
    if current_user._id == event.creator_id:
        if request.method == 'POST':
            if event_form.validate_on_submit():
                end_date = request.form.get('end_date')
                event.topic = request.form.get('topic')
                event.text = request.form.get('text')
                event.date_end = datetime.strptime(end_date, '%Y-%m-%d')
                db.session.commit()
                return redirect('/getmyevents')
        else:
            return render_template('edit_event.html', form=event_form)

    error = "Access denied"
    return render_template('error.html',form=event_form,error = error, current_user = current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
