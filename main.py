import json
import uuid
import mysql.connector
from flask_json import FlaskJSON, as_json
from flask_cors import CORS, cross_origin
from flask import Flask, redirect, url_for, request, make_response, send_file, jsonify

app = Flask(__name__)

cors = CORS(app)
json = FlaskJSON(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_AS_ASCII'] = False
app.config['JSON_ADD_STATUS'] = False



cnx = mysql.connector.connect(user='user', password='6re7u89uj.mljl',
                              host='158.160.19.129',
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


    elif realPasswd == passwd:
        user_uuid = uuid.uuid4()
        response = {'uuid': f'{str(user_uuid)}'}

    else:
        response = {
            "success": False,
            "exception": {
                "message": "Nickname or password is incorrect"
            }
        }
        # return response
        return response, 401


    # return response
    return response, 200






if __name__=='__main__':
    app.run(host="0.0.0.0", debug=False)





