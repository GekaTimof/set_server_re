import json
import uuid
import mysql.connector
from flask_json import FlaskJSON, as_json
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, url_for, request, make_response, send_file, jsonify

app = Flask(__name__)

cors = CORS(app)
myjson = FlaskJSON(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_AS_ASCII'] = False
app.config['JSON_ADD_STATUS'] = False



cnx = mysql.connector.connect(user='user', password='6re7u89uj.mljl',
                              host='51.250.102.162',
                              database='myDatabase')
cursor = cnx.cursor()


@app.route('/user/register', methods=['GET'])
@cross_origin()
@as_json
def register():
    # check parameters
    nickname = request.args.get('nickname')
    passwd = request.args.get('password')

    # get passwd for nickname
    cursor.execute(f"select u.user_passwd  from users u \
    WHERE u.user_login ='{nickname}';")

    # get reak user password
    realPasswd=None
    for realPasswd in cursor:
        realPasswd = realPasswd[0]

    if realPasswd == None:
        # create user in database
        cursor.execute(f"INSERT INTO users  (user_login, user_passwd) VALUES ('{nickname}', '{passwd}');")
        # save data in database
        cnx.commit()

        user_uuid = uuid.uuid4()
        response = {'uuid': f'{str(user_uuid)}'}

    else:
        response = {
            "success": False,
            "exception": {
                "message": "User already exist"
            }
        }
        # return response
        return response, 401


    # return response
    return response, 200

@app.route('/user/login', methods=['GET'])
@cross_origin()
@as_json
def login():
    # check parameters
    nickname = request.args.get('nickname')
    passwd = request.args.get('password')

    # get passwd for nickname
    cursor.execute(f"select u.user_passwd  from users u \
    WHERE u.user_login ='{nickname}';")

    # get real user password
    realPasswd = None
    for realPasswd in cursor:
        realPasswd = realPasswd[0]


    if realPasswd == passwd:
        user_uuid = uuid.uuid4()
        response = {'uuid': f'{str(user_uuid)}'}

    elif realPasswd == None:
        response = {
            "success": False,
            "exception": {
                "message": "User not exist"
            }
        }
        # return response
        return response, 401
    else:
        response = {
            "success": False,
            "exception": {
                "message": "password or login is wrong"
            }
        }
        # return response
        return response, 401



if __name__=='__main__':
    app.run(host="0.0.0.0", debug=False)





