from __future__ import print_function
import csv
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Bonjour {}'.format(
            form.username.data))
        return redirect(url_for('timeline'))
    return render_template('login.html', title='Sign In', form=form)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 299
    response.headers.add('Access-Control-Allow-Origin', 'http://pythonanywhere.com')
    return response

@app.route('/gaz', methods=['GET', 'POST'])
def save_gazouille():
    if request.method == 'POST':
        moderationliste = ['barre']
        if any(word in request.form['user-text'] for word in moderationliste):
            print('pas bon')
            return render_template('formulaire.html')
        else:
            print(request.form)
            dump_to_csv(request.form)
            return redirect(url_for('timeline'))
    if request.method == 'GET':
        return render_template('formulaire.html')

@app.route('/timeline', methods=['GET'])
def timeline():
    gaz = parse_from_csv()
    return render_template("timeline.html", gaz=gaz)

def parse_from_csv():
    gaz = []
    with open('./gazouilles.csv', 'r') as lire:
        reader = csv.reader(lire)
        for row in reader:
            gaz.append({"user":row[0], "text":row[1]})
    return gaz

def dump_to_csv(don):
    donnees = [don["user-name"], don["user-text"]]
    new_donnees = map(lambda x: x[:280], donnees)
    with open('./gazouilles.csv', 'a', newline='', encoding='utf-8') as lire:
        writer = csv.writer(lire)
        writer.writerow(new_donnees)

@app.route('/timeline/<username>/')
def profile(username):
    gaz = []
    with open('./gazouilles.csv', 'r') as lire:
        lire = csv.reader(lire)
        for message in lire:
            if message[0] == username:
                gaz.append({"user":message[0], "text":message[1]})
        return render_template("timeline.html", gaz=gaz)
