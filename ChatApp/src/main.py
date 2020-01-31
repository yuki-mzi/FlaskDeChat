from flask import Flask, render_template
from flask_socketio import SocketIO
import codecs
import sqlite3
from contextlib import closing



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
dbname = 'chat_database'
table_name = "test"



user_list = []
mes_list = []
wadai_judge = []


@app.route('/')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):

    if "user_name" in json:
        user_name = codecs.decode(json["user_name"].replace("%", "\\"), 'unicode-escape')
        message = codecs.decode(json["message"].replace("%", "\\"), 'unicode-escape')
        wadai = int(json["wadai"])
        time = json["now_time"]
        user_list.append(user_name)
        mes_list.append(message)
        wadai_judge.append(wadai)

        #databaseにアクセス
        with closing(sqlite3.connect(dbname)) as conn:
            con = conn.cursor()
            create_table = '''create table if not exists {} (user_n varchar(64), user_utter varchar(64), judge_continue int,now_time varchar(64))'''.format(table_name)
            con.execute(create_table)
            sql = 'insert into {} (user_n, user_utter, judge_continue,now_time) values (?,?,?,?)'.format(table_name)
            con.execute(sql,(user_name,message,wadai,time))
            conn.commit()
            select_sql = 'select * from {}'.format(table_name)
            for row in con.execute(select_sql):
                print(row)

        print(len(mes_list))

        socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app,host="localhost")

#Ctrl + Fn + F5