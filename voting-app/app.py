# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from utils import connect_to_redis
import os
import socket
import random
import json

option_a = os.getenv('OPTION_A', u"希拉里")
option_b = os.getenv('OPTION_B', u"川普")
hostname = socket.gethostname()

redis = connect_to_redis("redis")
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = request.cookies.get('vote', '')

    if request.method == 'POST':
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    resp.set_cookie('vote', vote)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
