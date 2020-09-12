from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    username = request.args.get('user')
    return render_template('index.html', username=username)
