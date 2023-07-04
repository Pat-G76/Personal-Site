
from flask import Flask, render_template, flash, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, URL, Email
import smtplib
from datetime import datetime as date
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Bootstrap(app)


class CreatePostForm(FlaskForm):
    name = StringField("Name ", validators=[DataRequired()])
    email = EmailField("Email ", validators=[DataRequired(), Email()])
    subject = StringField("Subject ", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit Message")


PORT_DETAILS = [
    {
      "name": "Bug Tracker",
      "Description": "Logging and monitoring bugs or errors during software testing",
      "code_url": "https://github.com/Pat-G76/Bug-Tracker",
      "website_url": "https://bugtk.azurewebsites.net/",
      "image_url": "Bug Tracker.png"
    },
    {
      "name": "Personal Website",
      "Description": "The website you are currently on",
      "code_url": "https://github.com/Pat-G76/my_personal_website",
      "website_url": "https://personal-site-5659.onrender.com/",
      "image_url": "Personal Website.png"
    }
  ]


@app.route("/", methods=["POST", "GET"])
def home():

    form = CreatePostForm()

    if form.validate_on_submit():
        with smtplib.SMTP("smtp.gmail.com", 587) as mail:

            mail.starttls()

            email = os.environ.get("EMAIL")
            main_email = os.environ.get("MAIN_EMAIL")
            password = os.environ.get("EMAIL_PASSWORD")

            mail.login(user=email, password=password)

            mail.sendmail(from_addr=email, to_addrs=main_email,
                          msg= f"Subject: {form.subject.data}\n\n "
                               f"Message from : {form.email.data}\n\n"
                               f"{form.message.data}")

            flash("Your message has been received. I will get back to you as soon as possible.", "info")

        return redirect("/")

    projects = PORT_DETAILS

    return render_template("index.html", projects=projects, form=form, year=date.now().year)


@app.route("/download/<path:filename>")
def download(filename):

    return send_from_directory("static/Documents", filename)


if __name__ == "__main__":
    app.run()
