from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
    "apiKey": "AIzaSyAuR1Q6vXLX5wXyHVED0iI4mX0ptLphFMQ",
    "authDomain": "example-e3547.firebaseapp.com",
    "projectId": "example-e3547",
    "storageBucket": "example-e3547.appspot.com",
    "messagingSenderId": "958026672525",
    "appId": "1:958026672525:web:14bcc94c8c613461d4f5c4",
    "databaseURL" : ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        return redirect(url_for('home'))
    except:
        error = "Authentication failed"
        return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)