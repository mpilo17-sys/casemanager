from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RSP79Form
from forms import RSP76Form, RSP79Form, RSP77Form, ContinuationForm
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)


# Form navigation sequence
FORM_SEQUENCE = ['RSP76', 'RSP79', 'RSP77', 'CONTINUATION']

# Mock user database
users = {
    'officer': {
        'password': 'police123',
        'name': 'Investigating Officer',
        'station': 'Main Station',
        'rank': 'Sergeant'
    }
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/case', methods=['GET', 'POST'])
@login_required
def case_form():
    form_type = session.get('current_form', 'RSP76')
    form_class = {
        'RSP76': RSP76Form,
        'RSP79': RSP79Form,
        'RSP77': RSP77Form,
        'CONTINUATION': ContinuationForm
    }[form_type]
    
    form = form_class()
    
    if form.validate_on_submit():
        session[form_type] = form.data
        if 'submit_next' in request.form:
            session['current_form'] = get_next_form(form_type)
        elif 'submit_prev' in request.form:
            session['current_form'] = get_prev_form(form_type)
        else:
            return redirect(url_for('case_submit'))
        return redirect(url_for('case_form'))
    
    # Load existing data
    if form_type in session:
        for field in form:
            if field.id in session[form_type]:
                field.data = session[form_type][field.id]
    
    return render_template(f'form_{form_type.lower()}.html', form=form, form_type=form_type)

def get_next_form(current):
    try:
        return FORM_SEQUENCE[FORM_SEQUENCE.index(current) + 1]
    except IndexError:
        return current

def get_prev_form(current):
    index = FORM_SEQUENCE.index(current)
    return FORM_SEQUENCE[index - 1] if index > 0 else current

@app.route('/case/submit')
@login_required
def case_submit():
    case_data = {form: session.get(form) for form in FORM_SEQUENCE}
    session.clear()
    return render_template('submit.html', case_data=case_data)

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        return None
    user = User()
    user.id = user_id
    return user

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        if username in users and form.password.data == users[username]['password']:
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user data safely
    user_data = users.get(current_user.id, {})
    return render_template('dashboard.html', user=user_data)

@app.route('/statement', methods=['GET', 'POST'])
@login_required
def statement():
    form = RSP79Form()
    user_data = users.get(current_user.id, {})  # Add this line
    if form.validate_on_submit():
        flash('Statement submitted successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('statement_form.html', form=form, user=user_data)  # Pass user here

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
