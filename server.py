import json
from flask import Flask, jsonify, Response
from functools import wraps
from flask import redirect, request, current_app
from flask import Flask, render_template, abort, request, redirect, url_for, session
app = Flask(__name__)

x = 1441899490
y = 1

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args,**kwargs).data) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@support_jsonp
def get_data():
    global x
    global y

    x = x + 1
    y = (y + 1) % 10

    p1 = {"time": x, "y": y + 1}
    p2 = {"time": x, "y": y + 2}
    p3 = {"time": x, "y": y + 3}
    p4 = {"time": x, "y": y + 4}
    data = [p1,p2,p3,p4]

    print data
    # result = jsonify(json.dumps(data))
    result = Response(json.dumps(data),  mimetype='application/json')
    print result

    return result

    # jsonify(result={"status": 200})
    # return jsonify(foo="bar")

@app.errorhandler(404)
def fuckoff(data):
    print data
    return data

if __name__ == "__main__":
    app.run(debug=True)
