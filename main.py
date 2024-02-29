import json
import create_deck
from functools import reduce
from random import shuffle
import uuid
import mysql.connector
from flask_json import FlaskJSON, as_json
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, url_for, request, make_response, send_file, jsonify
import set


app = Flask(__name__)

cors = CORS(app)
myjson = FlaskJSON(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_AS_ASCII'] = False
app.config['JSON_ADD_STATUS'] = False



cnx = mysql.connector.connect(user='user', password='6re7u89uj.mljl',
                              host='84.201.165.194',
                              database='setDatabase')
cursor = cnx.cursor()


def errors(func):
   def wrapper(*args, **kwargs):
       try:
           result = func(*args, **kwargs)
           print(result)
       except Exception as err:
           response = {'error': str(err)}
           return response, 400
       return result
   wrapper.__name__ = func.__name__
   return wrapper

def token_checker(func):
    def wrapper(*args, **kwargs):
        accessToken = request.args.get('accessToken')

        # check token
        cursor.execute(f"select count(*) from tokens where accessToken = '{accessToken}';")

        token_count = None
        for token_count_arr in cursor:
            token_count = token_count_arr[0]
        print(token_count)

        if token_count and token_count > 0:
            result = func(*args, **kwargs)
        else:
            raise Exception("accessToken not exist")

        return result

    wrapper.__name__ = func.__name__
    return wrapper

# registration function
@app.route('/user/register', methods=['GET'])
@cross_origin()
@as_json
@errors
def register():
    # check parameters
    nickname = request.args.get('nickname')
    passwd = request.args.get('password')

    # get passwd for nickname
    cursor.execute(f"select u.user_passwd  from users u \
    WHERE u.nickname ='{nickname}';")

    # get real user password
    realPasswd = None
    for realPasswd_arr in cursor:
        realPasswd = realPasswd_arr[0]

    if realPasswd == None:
        # create and save user in database
        cursor.execute(f"INSERT INTO users  (nickname, user_passwd) VALUES ('{nickname}', '{passwd}');")
        cnx.commit()

        user_accessToken = uuid.uuid4()

        # add token in database
        cursor.execute(f"insert into tokens (nickname, token) Values ('{nickname}', '{user_accessToken}');")
        cnx.commit()

        response = {
            'nickname': f'{str(nickname)}',
            'accessToken': f'{str(user_accessToken)}'
        }

        # return response
        return response, 200

    else:
        response = {
            "success": False,
            "exception": {
                "message": "User already exist"
            }
        }
        # return response
        return response, 401




# logining function
@app.route('/user/login', methods=['GET'])
@cross_origin()
@as_json
@errors
def login():
    # check parameters
    nickname = request.args.get('nickname')
    passwd = request.args.get('password')

    # get passwd for nickname
    cursor.execute(f"select u.user_passwd  from users u \
    WHERE u.nickname ='{nickname}';")

    # get real user password
    realPasswd = None
    for realPasswd_arr in cursor:
        realPasswd = realPasswd_arr[0]


    if realPasswd == passwd:
        user_accessToken = uuid.uuid4()

        # add token in database
        cursor.execute(f"insert into tokens (nickname, token) Values ('{nickname}', '{user_accessToken}');")
        cnx.commit()

        response = {
            'nickname': f'{str(nickname)}',
            'accessToken': f'{str(user_accessToken)}'
        }
        # return response
        return response, 200

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
@errors
@token_checker
def game_start():
    accessToken = request.args.get('accessToken')

    # check token
    cursor.execute(f"select nickname FROM tokens Where token='{accessToken}';")
    nickname = None
    for nickname_arr in cursor:
        nickname = nickname_arr[0]

    if nickname:
        # game accessToken
        game_accessToken = uuid.uuid4()

        deck = create_deck.create_deck()

        field = deck[:12*7-1]
        deck = deck[12*7:]

        # create a new game
        cursor.execute(f"INSERT INTO games (game_accessToken, field, deck, nickname_1, status) Values ('{str(game_accessToken)}', '{str(field)}', '{str(deck)}', '{str(nickname)}', 'starting');")
        cnx.commit()

        # return game accessToken
        response = {
            "success": True,
            "exception": None,
            "gameId": game_accessToken
        }

        return response, 200
    else:
        response = {
            "success": False,
            "exception": {
                "message": "false token"
            }
        }
        # return response
        return response, 401


# function to get the list of games
@app.route('/set/room/list', methods=['GET'])
@cross_origin()
@as_json
@errors
@token_checker
def game_list():
    # create a new game
    cursor.execute(f"select game_accessToken from games where status = 'starting';")

    dict_game = {'games':[]}

    # get games from cursor
    for games_arr in cursor:
        dict_game['games'].append({"id": str(games_arr[0])})

    # return game accessToken
    response = dict_game

    return response



# enter game function
@app.route('/set/room/enter', methods=['GET'])
@cross_origin()
@as_json
@errors
@token_checker
#@game_token_checker
def game_enter():
    user_token = request.args.get('accessToken')
    gameId = request.args.get('game_accessToken')

    cursor.execute(f"select nickname from tokens where token='{user_token}';")

    nickname = None
    for nickname_arr in cursor:
        nickname = nickname_arr[0]

    cursor.execute(f"update games set nickname_2='{nickname}', status='in_play' where game_accessToken = '{gameId}';)")
    cnx.commit()

    response = {
        "success": True,
        "exception": None,
        "gameId": gameId
    }

    return response, 200



if __name__=='__main__':
    app.run(host="0.0.0.0", debug=False)





