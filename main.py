import json
import uuid
import mysql.connector
from flask_json import FlaskJSON, as_json
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, url_for, request, make_response, send_file, jsonify
import set
import decorators


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


# registration function
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

    # get real user password
    realPasswd=None
    for realPasswd in cursor:
        realPasswd = realPasswd[0]

    if realPasswd == None:
        # create user in database
        cursor.execute(f"INSERT INTO users  (user_login, user_passwd) VALUES ('{nickname}', '{passwd}');")
        # save data in database
        cnx.commit()

        user_accessToken = uuid.accessToken4()
        response = {'accessToken': f'{str(user_accessToken)}'}

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


# logining function
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
        user_accessToken = uuid.accessToken4()
        response = {'accessToken': f'{str(user_accessToken)}'}

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


# game starting function
@app.route('/set/room/create', methods=['GET'])
@cross_origin()
@as_json
@token_checker
def game_start():
    # game accessToken
    game_accessToken = uuid.accessToken4()

    # create a new game
    cursor.execute(f"INSERT INTO games  (game_accessToken) VALUES ('{game_accessToken}');")

    # return game accessToken
    response = {
        "success": True,
        "exception": None,
        "gameId": game_accessToken
    }


# function to get the list of games
@app.route('/set/room/list', methods=['GET'])
@cross_origin()
@as_json
@token_checker
def game_list():
    # create a new game
    cursor.execute(f"select game_accessToken from games;")

    # return game accessToken
    response = {
        "games":[]
    }


# enter game function
@app.route('/set/room/enter', methods=['GET'])
@cross_origin()
@as_json
@token_checker
def game_enter():
    # create a new game
    cursor.execute(f"select game_token from games;")




    response = {
        "success": True,
        "exception": None,
        "gameId":
    }













if __name__=='__main__':
    app.run(host="0.0.0.0", debug=False)





