from flask import Flask, redirect, url_for, request, make_response, send_file, jsonify
from flask_json import FlaskJSON, as_json


def token_checker(func):
    def wrapper(*args, **kwargs):
        accessToken = request.args.get('accessToken')

        # check token
        cursor.execute(f"select count(*)  from tokens t \
        WHERE token ='{accessToken}';")

        tokenCount = None
        for tokenCount in cursor:
            tokenCount = tokenCount[0]

        if tokenCount >= 0:
            return func(*args, **kwargs)
        else:
            raise Exception("accessToken not exist")