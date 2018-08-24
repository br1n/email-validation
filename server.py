from flask import Flask, redirect, request, session, render_template, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "henlo"
mysql = MySQLConnector(app,'validemaildb')

@app.route('/')
def index():
    return render_template('index.html', title = "Email Validation")

@app.route('/create_user', methods=["POST"])
def createuser():
    form = request.form
    errors = False
    #validation of email format
    if not EMAIL_REGEX.match(form['email']):
        print "emailemail"
        errors = True
        flash("Must be a valid email")

    #checking for existing email address
    query = "SELECT * FROM emails WHERE email_address = :email"
    data = {"email":form['email']}
    emails = mysql.query_db(query, data)
    
    if len(emails) > 0:
      errors = True
      flash("Email already exists")

    if errors:
        return redirect('/')

    else:
        query = "INSERT INTO emails (email_address, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {"email":form['email']}
        mysql.query_db(query, data)
        flash("Success! Thanks for your add!")
        return redirect('/success')


@app.route('/success')
def sucess():
    emails_query = "SELECT * FROM emails"
    emails = mysql.query_db(emails_query)
    return render_template('success.html', title="Success", emails=emails)
    
app.run(debug=True)