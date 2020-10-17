import src.session.session as session
from flask import Flask, render_template, request, make_response, redirect
from src.db.db import DB
from src.msg.msg import MH
app = Flask(__name__)


@app.route('/')
def hello_world():
    login = request.cookies.get('login')
    uid = -1
    username = ''
    user_roles = []
    MH.update_messages()

    if login:
        user_rec = session.get_user_rec_by_login(login)
        if user_rec:
            uid = user_rec[0]
            username = user_rec[1]
            user_roles = session.get_rids_by_uid(uid)

    return render_template(
        'index.html',
        data={
            'uid': uid,
            'uid_rids': user_roles,
            'username': username,
            'messages': MH.messages
        })


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
    response.set_cookie('login', user_rec[1], samesite='Strict')
    return response


@app.route('/delmsg', methods=['GET'])
def delete_message_handler():
    user_rec = session.get_user_rec_by_login(request.cookies.get('login'))

    if not user_rec:
        return '', 500

    message_id = int(request.args.get('id'))

    message = next((x for x in MH.messages if x[0] == message_id))

    if not (user_rec[0] == 1 or user_rec[0] == message[1]):
        return '', 500

    MH.delete_message(message_id)
    return make_response(redirect('/'))
