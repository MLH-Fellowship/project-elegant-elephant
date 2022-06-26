import os
from shutil import register_unpack_format
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import*
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb=MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                    user=os.getenv("MYSQL_USER"),
                    password=os.getenv("MYSQL_PASSWORD"),
			        host=os.getenv("MYSQL_HOST"),
                    port=3306)
print(mydb)

class TimeLinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimeLinePost])


@app.route('/')
def index():
    return render_template('index.html', title="Home", url=os.getenv("URL"))

@app.route('/professionalinfo')
def professionInfo():
    return render_template('prof.html', title="Education/Experience", url=os.getenv("URL"))

@app.route('/hobbies')
def portfolio():
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimeLinePost.create(name=name, email=email,content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return{
        'timeline_posts': [
            model_to_dict(p)
            for p in
TimeLinePost.select().order_by(TimeLinePost.created_at.desc())
        ]
    }


##HOLA