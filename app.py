from flask import Flask, render_template, request, make_response, redirect
from src.db.db import DB
from src.msg.msg import MH
app = Flask(__name__)


@app.route('/')
def hello_world():
    login = request.cookies.get('login')
    username = ''

    if login:
        names_logins = DB.execute_select_query('SELECT name, login FROM User')
        user_rec = next(filter(lambda x: x[1] == login, names_logins))
        if user_rec:
            username = user_rec[0]

    return render_template(
        'index.html', username=username, messages=MH.messages)


@app.route('/login', methods=['POST'])
def login_handler():
    login = request.form.get('login')
    password = request.form.get('password')

    if not all([login, password]):
        return '', 500

    user_table_recs = DB.execute_select_query(
        'SELECT name, login, password FROM User')

    user_rec = next(filter(lambda x: x[1] == login, user_table_recs))

    if not user_rec:
        return '', 500

    if user_rec[2] != password:
        return '', 500

    response = make_response(redirect('/'))
    response.set_cookie('login', user_rec[1])
    return response
