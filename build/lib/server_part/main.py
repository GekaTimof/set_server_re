import json
from server_part import create_deck
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
                              host='158.160.10.161',
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
        cursor.execute(f"select nickname from tokens where token = '{accessToken}';")

        nickname = None
        for nickname_arr in cursor:
            nickname = nickname_arr[0]

        if nickname:
            result = func(*args, **kwargs)
        else:
            raise Exception("accessToken not exist")

        return result

    wrapper.__name__ = func.__name__
    return wrapper


def not_in_game(func):
    def wrapper(*args, **kwargs):
        user_token = request.args.get('accessToken')

        cursor.execute(
            f"select count(*) from games where "
            f"(token_1 = '{user_token}' or token_2 = '{user_token}') and (status = 'ongoing' or status = 'starting');")

        game_count = None
        for game_count_arr in cursor:
            game_count = game_count_arr[0]

        if game_count == 0:
            result = func(*args, **kwargs)
        else:
            raise Exception("user already played")

        return result

    wrapper.__name__ = func.__name__
    return wrapper

def in_game(func):
    def wrapper(*args, **kwargs):
        user_token = request.args.get('accessToken')

        cursor.execute(
            f"select count(*) from games where "
            f"(token_1 = '{user_token}' or token_2 = '{user_token}') and (status = 'ongoing' or status = 'starting');")

        game_count = None
        for game_count_arr in cursor:
            game_count = game_count_arr[0]

        if game_count > 0:
            result = func(*args, **kwargs)
        else:
            raise Exception("user not in play")

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
@not_in_game
def game_start():
    accessToken = request.args.get('accessToken')

    # check token
    cursor.execute(f"select nickname FROM tokens Where token='{accessToken}';")
    nickname = None
    for nickname_arr in cursor:
        nickname = nickname_arr[0]

    # game accessToken
    game_accessToken = uuid.uuid4()

    deck = create_deck.create_deck()

    field = deck[:12*8-1]
    deck = deck[12*8:]

    # create a new game
    cursor.execute(f"INSERT INTO games (game_accessToken, field, deck, nickname_1, token_1, status) Values "
                   f"('{str(game_accessToken)}', '{field}', '{deck}', '{nickname}', '{accessToken}' , 'starting');")
    cnx.commit()

    # return game accessToken
    response = {
        "success": True,
        "exception": None,
        "gameId": game_accessToken
    }

    return response, 200


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
@not_in_game
def game_enter():
    user_token = request.args.get('accessToken')
    gameId = request.args.get('gameId')

    cursor.execute(f"select nickname from tokens where token='{user_token}';")

    nickname = None
    for nickname_arr in cursor:
        nickname = nickname_arr[0]

    cursor.execute(f"UPDATE games SET status = 'in_play', token_2 = '{user_token}', nickname_2 = '{nickname}' WHERE "
                   f"game_accessToken = '{gameId}' LIMIT 1;")
    cnx.commit()

    response = {
        "success": True,
        "exception": None,
        "gameId": gameId
    }

    return response, 200


@app.route('/set/field', methods=['GET'])
@cross_origin()
@as_json
@errors
@token_checker
@in_game
def game_field():
    user_token = request.args.get('accessToken')

    cursor.execute(
        f"select field, token_1, token_2, score_1, score_2  from games where token_1 = '{user_token}' or token_2 = '{user_token}';")

    data = cursor.fetchone()

    field = data[0]
    tokens = data[1:3]
    scores = data[3:5]

    response = {"cards": [],
                 "status": "ongoing",
                 "score": 0 }

    for card in field.split('*'):
        id = card.split('.')[0]
        color = card.split('.')[1][0]
        shape = card.split('.')[1][1]
        fill = card.split('.')[1][2]
        count = card.split('.')[1][3]
        response["cards"].append({"id": id, "color": color, "shape": shape, "fill": fill, "count": count})


    if tokens[0] == user_token:
        response["score"] = scores[0]
    else:
        response["score"] = scores[1]


    if len(response["cards"]) == 0:
        response["status"] = "finished"

    return response, 200

@app.route('/set/pick', methods=['GET'])
@cross_origin()
@as_json
@errors
@token_checker
@in_game
def pick_card():
    user_token = request.args.get('accessToken')

    cards = request.args.get('cards').split("*")
    for i, card in enumerate(cards):
        if len(card) == 1:
            cards[i] = "0" + cards[i]

    cursor.execute(
        f"select field, deck, token_1, token_2, score_1, score_2  from games "
        f"where token_1 = '{user_token}' or token_2 = '{user_token}';")

    data = cursor.fetchone()
    field = data[0]
    deck = data[1]
    tokens = data[2:4]
    scores = data[4:6]

    is_set = True
    set = []
    set_re = []
    for card in field.split("*"):
        if card.split(".")[0] in cards:
            set.append(card.split(".")[1])
            set_re.append(card)

    if len(set) > 0:
        for i in range(len(set[0])):
            if not ((set[0][i] == set[1][i] and set[1][i] == set[2][i]) or int(set[0][i]) + int(set[1][i]) + int(set[2][i]) == 6):
                is_set = False
    else:
        raise Exception("cards not exist")


    if tokens[0] == user_token:
        score = scores[0]
        player = 0
    else:
        score = scores[1]
        player = 1

    deck_re = deck.split("*")
    field_re = []
    if is_set == True:
        for re in field.split("*"):
            if re in set_re:
                if len(field.split("*")) == 12:
                    field_re.append(deck_re.pop())
            else:
                field_re.append(re)

        score = int(score) + 1

        if player == 0:
            cursor.execute(
                f"UPDATE games SET field = '{'*'.join(field_re)}', deck = '{'*'.join(deck_re)}', score_1 = '{score}' "
                f"where token_1 = '{user_token}';")
        else:
            cursor.execute(
                f"UPDATE games SET field = '{'*'.join(field_re)}', deck = '{'*'.join(deck_re)}', score_2 = '{score}' "
                f"where token_2 = '{user_token}';")
        cnx.commit()

    response = {
        "is_set": is_set,
        "score": score
    }
    return response, 200


@app.route('/set/add', methods=['GET'])
@cross_origin()
@as_json
@errors
@token_checker
@in_game
def add_card():
    user_token = request.args.get('accessToken')

    cursor.execute(
        f"select field, deck from games "
        f"where token_1 = '{user_token}' or token_2 = '{user_token}';")

    data = cursor.fetchone()
    field = data[0]
    deck = data[1]

    if len(field.split("*")) == 12 and len(deck.split("*")) >= 3:
        field_re = "*".join(field.split("*") + deck.split("*")[0:4])
        deck_re = "*".join(deck.split("*")[4:])

        # create a new game
        cursor.execute(f" update games set field = '{field_re}', deck = '{deck_re}' "
                       f"where token_1 = '{user_token}' or token_2 = '{user_token}' ;")
        cnx.commit()
    else:
        raise Exception("not possible to add card")

    response = {
        "success": True,
        "exception": None
    }
    return response, 200

@app.route('/set/scores', methods=['GET'])
@cross_origin()
@as_json
@errors
@token_checker
@in_game
def scores():
    user_token = request.args.get('accessToken')

    cursor.execute(
        f"select nickname_1, nickname_2, score_1, score_2  from games "
        f"where token_1 = '{user_token}' or token_2 = '{user_token}';")

    data = cursor.fetchone()
    names = data[0:2]
    scores = data[2:4]

    response = {
                "success": True,
                "exception": None,
                "users": [
                    {
                        "name": names[0],
                        "score": scores[0]
                    },
                    {
                        "name": names[1],
                        "score": scores[1]
                    }
                ]
            }
    return response, 200





if __name__=='__main__':
    app.run(host="0.0.0.0", debug=False)





