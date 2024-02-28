import json
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
                              host='84.201.164.226',
                              database='myDatabase')
cursor = cnx.cursor()


def token_checker(func):
    def wrapper(*args, **kwargs):
        accessToken = request.args.get('accessToken')

        print(accessToken)
        # check token
        cursor.execute(f"select *  from tokens;")

        tokens = None
        for tokens_arr in cursor:
            tokens = tokens_arr[0]
        print(tokens)

        if accessToken in tokens.keys():
            result =  func(*args, **kwargs)
        else:
            raise Exception("accessToken not exist")
        return result

   wrapper.__name__ = func.__name__
   return wrapper



"""def args(func):
   def wrapper(*args, **kwargs):
       tokens = ['token123', 'test', 'qwerty']  # массив с токенами
       token = request.args.get('token')  # получаем токен из запроса
       if token in tokens:
           result = func(*args, **kwargs)
       else:
           raise AuthError('Пользователь не авторизованн - токен не подошел')# возвращаем данны
       return result


   wrapper.__name__ = func.__name__
   return wrapper

"""

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
    for realPasswd_arr in cursor:
        realPasswd = realPasswd_arr[0]

    if realPasswd == None:
        # create and save user in database
        cursor.execute(f"INSERT INTO users  (user_login, user_passwd) VALUES ('{nickname}', '{passwd}');")
        cnx.commit()

        user_accessToken = uuid.uuid4()

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
        user_accessToken = uuid.uuid4()
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
@token_checker
def game_start():
    # game accessToken
    game_accessToken = uuid.uuid4()

    # create a new game
    cursor.execute(f"INSERT INTO games  (game_accessToken) VALUES ('{game_accessToken}');")

    # return game accessToken
    response = {
        "success": True,
        "exception": None,
        "gameId": game_accessToken
    }

    return response, 200

'''

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
        "gameId": cursor.fetchone()
    }

'''











if __name__=='__main__':
    app.run(host="0.0.0.0", debug=False)





