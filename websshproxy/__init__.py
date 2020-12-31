# coding=utf-8
from flask import Flask
from flask import render_template

# flask
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
