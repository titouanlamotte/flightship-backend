#needed for Heroku test purposes, server.py fork
from flask import Flask
import json
from base import comeflywithme
from flask import request

app = Flask(__name__)

#@app.route("/api/0.1/create", methods=['POST', 'GET'])
#def hello():
#    
#    j = json.loads(request.get_data())
#    fly = comeflywithme()
#
#    data =fly.create(j['cities'], j['inbounddate'], j['outbounddate'])
#
#    
#    return json.dumps(data)

#@app.route("/api/0.1/display", methods=['POST', 'GET'])
#def hallo():
#    
#    j = json.loads(request.get_data())
#    fly = comeflywithme()
#
#    data =fly.display(j['id'])
#
#    
#    return json.dumps(data)



#if __name__ == "__main__":
#    app.run(host="0.0.0.0",port="5000")
