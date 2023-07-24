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
    "databaseURL" : "https://example-e3547-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('add_tweet'))
    except:
        error = "Authentication failed"
        return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
    try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        UID = login_session['user']['localId']
        user = {"name": fullname, "email": email, "username" : username, "bio" : bio}
        db.child("Users").child(UID).set(user)
        return redirect(url_for('add_tweet'))
    except:
        error = "Authentication failed"
        return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['tweet_text']
    try:
        UID = login_session['user']['localId']
        tweet = {"tweettitle": title, "tweettext": text, "uid" : UID}
        db.child("Tweets").push(tweet)
        return redirect(url_for('add_tweet'))
    except:
        error = "Authentication failed"
        return render_template("add_tweet.html")

@app.route('/all_tweets', methods = ['GET', 'POST'])
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("tweets.html", all_tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True)