from app import app, db, mail
from flask import render_template, redirect, url_for, flash, request
from models import User, Group, Prompt, Response
from forms import RegistrationForm, LoginForm, GroupForm, PromptForm, ResponseForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    groups = current_user.groups
    return render_template('dashboard.html', groups=groups)

@app.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data)
        group.members.append(current_user)
        db.session.add(group)
        db.session.commit()
        flash('Group created successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_group.html', form=form)

@app.route('/group/<int:group_id>')
@login_required
def group_detail(group_id):
    group = Group.query.get_or_404(group_id)
    prompts = group.prompts
    return render_template('group_detail.html', group=group, prompts=prompts)

@app.route('/group/<int:group_id>/add_prompt', methods=['GET', 'POST'])
@login_required
def add_prompt(group_id):
    form = PromptForm()
    if form.validate_on_submit():
        prompt = Prompt(content=form.content.data, group_id=group_id)
        db.session.add(prompt)
        db.session.commit()
        flash('Prompt added!', 'success')
        return redirect(url_for('group_detail', group_id=group_id))
    return render_template('add_prompt.html', form=form)

@app.route('/prompt/<int:prompt_id>/submit_response', methods=['GET', 'POST'])
@login_required
def submit_response(prompt_id):
    form = ResponseForm()
    if form.validate_on_submit():
        response = Response(answer=form.answer.data, prompt_id=prompt_id, user_id=current_user.id)
        db.session.add(response)
        db.session.commit()
        flash('Response submitted!', 'success')
        check_and_send_newsletter(prompt_id)
        return redirect(url_for('dashboard'))
    return render_template('submit_response.html', form=form)

def check_and_send_newsletter(prompt_id):
    prompt = Prompt.query.get(prompt_id)
    group = prompt.group
    group_member_ids = [member.id for member in group.members]
    prompt_response_user_ids = [response.user_id for response in prompt.responses]
    if set(group_member_ids) == set(prompt_response_user_ids):
        # All members have responded; send the newsletter
        send_newsletter(group, prompt)

def send_newsletter(group, prompt):
    recipients = [member.email for member in group.members]
    msg = Message(f'Newsletter: {group.name}', sender='noreply@example.com', recipients=recipients)
    msg.body = render_template('newsletter_email.html', group=group, prompt=prompt)
    mail.send(msg)
    flash('Newsletter sent!', 'success')
