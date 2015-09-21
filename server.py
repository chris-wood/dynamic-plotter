import json
from flask import Flask, jsonify, Response
from functools import wraps
from flask import redirect, request, current_app
from flask import Flask, render_template, abort, request, redirect, url_for, session
app = Flask(__name__)

queryData = {}
x = 1442334403241
y = 0

queryData["lci:/local/forwarder/ContentStore/stat/size"] = []
queryData["lci:/local/forwarder/ContentStore/stat/size"].append((1442334403241, 0))
queryData["lci:/local/forwarder/ContentStore/stat/hits"] = []
queryData["lci:/local/forwarder/ContentStore/stat/hits"].append((1442334403241, 0))
queryData["lci:/local/forwarder/PIT/stat/size"] = []
queryData["lci:/local/forwarder/PIT/stat/size"].append((1442334403241, 0))
queryData["lci:/local/forwarder/PIT/stat/avgEntryLifetime"] = []
queryData["lci:/local/forwarder/PIT/stat/avgEntryLifetime"].append((1442334403241, 0))

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

@app.route("/cache-size", methods=['GET'])
@support_jsonp
def get_data():
    global queryData

    dataTuple = queryData["lci:/local/forwarder/ContentStore/stat/size"][-1]
    p1 = {"time": dataTuple[0], "y": dataTuple[1]}

    dataTuple = queryData["lci:/local/forwarder/ContentStore/stat/hits"][-1]
    p2 = {"time": dataTuple[0], "y": dataTuple[1]}

    dataTuple = queryData["lci:/local/forwarder/PIT/stat/size"][-1]
    p3 = {"time": dataTuple[0], "y": dataTuple[1]}

    dataTuple = queryData["lci:/local/forwarder/PIT/stat/avgEntryLifetime"][-1]
    p4 = {"time": dataTuple[0], "y": dataTuple[1]}

    data = [p1]
    result = Response(json.dumps(data),  mimetype='application/json')

    return result

@app.route("/cache-hits", methods=['GET'])
@support_jsonp
def get_data():
    global queryData

    dataTuple = queryData["lci:/local/forwarder/ContentStore/stat/hits"][-1]
    p2 = {"time": dataTuple[0], "y": dataTuple[1]}

    data = [p2]
    result = Response(json.dumps(data),  mimetype='application/json')

    return result

@app.route("/pit-size", methods=['GET'])
@support_jsonp
def get_data():
    global queryData

    dataTuple = queryData["lci:/local/forwarder/PIT/stat/size"][-1]
    p3 = {"time": dataTuple[0], "y": dataTuple[1]}

    data = [p3]
    result = Response(json.dumps(data),  mimetype='application/json')

    return result

@app.route("/pit-lifetime", methods=['GET'])
@support_jsonp
def get_data():
    global queryData

    dataTuple = queryData["lci:/local/forwarder/PIT/stat/avgEntryLifetime"][-1]
    p4 = {"time": dataTuple[0], "y": dataTuple[1]}

    data = [p4]
    result = Response(json.dumps(data),  mimetype='application/json')

    return result

@app.route("/data", methods=['POST'])
def post_data():
    global queryData
    if request.json:
        data = request.json

        query = data["query"]
        response = data["response"]
        time = response["time"]

        print "RECEIVED QUERY: %s" % (query)
        if (query == "lci:/local/forwarder/ContentStore/stat/size"):
            dataTuple = (int(time), int(response["sizeInBytes"]))
            queryData[query].append(dataTuple)
            print "ADDING ---> " + str(dataTuple)
        elif query == "lci:/local/forwarder/ContentStore/stat/hits":
            dataTuple = (int(time), int(response["numHits"]))
            queryData[query].append(dataTuple)
            print "ADDING ---> " + str(dataTuple)
        elif query == "lci:/local/forwarder/PIT/stat/size":
            dataTuple = (int(time), int(response["numPendingEntries"]))
            queryData[query].append(dataTuple)
            print "ADDING ---> " + str(dataTuple)
        elif query == "lci:/local/forwarder/PIT/stat/avgEntryLifetime":
            dataTuple = (int(time), int(response["avgEntryLifetime"]))
            queryData[query].append(dataTuple)
            print "ADDING ---> " + str(dataTuple)

    else:
        pass # do nothing...

    return jsonify(foo="bar")

@app.errorhandler(404)
def errorHandler(data):
    print data
    return data

if __name__ == "__main__":
    app.run(debug=True)
