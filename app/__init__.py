
import os
from sys import flags
from urllib import response

from flask import Flask, Response, make_response, render_template, render_template_string, request
from dotenv import load_dotenv
from peewee import *
import datetime
import re
from playhouse.shortcuts import model_to_dict




load_dotenv()
app = Flask(__name__)


if os.getenv("TESTING") == "true":

    print ( "Running in test mode")
    mydb=SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:

    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )




class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


@app.route("/")
def index():
    return render_template("index.html", title="Home", url=os.getenv("URL"))


@app.route("/professionalinfo")
def professionInfo():
    return render_template(
        "prof.html", title="Education/Experience", url=os.getenv("URL")
    )


@app.route("/hobbies")
def portfolio():
    return render_template("hobbies.html", title="Hobbies", url=os.getenv("URL"))


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():

    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name or name == '' or name is None:
        return "Invalid name", 400

    elif not email or email == '' or email is None or re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(.[A-Z|a-z]{2,})+", email) == None:
        return "Invalid email", 400

    elif not content or content == '' or content is None:
        return "Invalid content", 400

    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route("/api/timeline_post", methods=["DELETE"])
def delete_time_line_post():
    id = request.form["id"]
    TimelinePost.delete_by_id(id)
    return render_template("timeline.html")


@app.route("/timeline")
def timeline():
    template_data = get_time_line_post()
    return render_template("timeline.html", data=template_data)




