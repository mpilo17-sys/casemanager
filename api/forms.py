from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length

class MultiForm(FlaskForm):
    submit_next = SubmitField('Next →')
    submit_prev = SubmitField('← Previous')
    submit_final = SubmitField('Submit Case')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# RSP 76 - Docket Form
class RSP76Form(MultiForm):
    police_region = StringField('Police Region', validators=[DataRequired()])
    station = StringField('Station', validators=[DataRequired()])
    rcci_no = StringField('R.C.C.I. NO')
    ob_no = StringField('O.B. NO')
    traffic_offence = StringField('Registration Traffic Offence')
    court_case_no = StringField('Court Case NO')
    accused_info = TextAreaField('Accused Full Details')
    charges = TextAreaField('Charges (Section of Law)')
    property_stolen = StringField('Value of Property Stolen (E)')
    property_recovered = StringField('Value of Property Recovered (E)')

# RSP 79 - Statement Form
class RSP79Form(MultiForm):
    statement_name = StringField('Statement of (full name)', validators=[DataRequired()])
    occupation = StringField('Occupation')
    employer = StringField('Employed by')
    work_phone = StringField('Work Telephone No')
    residential_address = TextAreaField('Residential Address')
    nationality = StringField('Nationality')
    chief = StringField('Chief')
    statement_content = TextAreaField('Statement Content', validators=[DataRequired()])

# RSP 77 - Police Report
class RSP77Form(MultiForm):
    report_no = StringField('Report Number', validators=[DataRequired()])
    officer_rank = StringField('Rank')
    officer_name = StringField('Name')
    ref_no = StringField('Reference Number')
    report_subject = TextAreaField('Subject of Report')
    report_date = DateField('Date', validators=[DataRequired()])

# Continuation Form
class ContinuationForm(MultiForm):
    continuation_ref = StringField('Continuation of Reference', validators=[DataRequired()])
    continuation_content = TextAreaField('Continued Statement', validators=[DataRequired()])