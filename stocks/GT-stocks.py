# This is example REST API server code for HW #1: topic-2 REST APIs
# It uses Flask to build a RESTful service in Python.
# A good introduction is https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f
# See also https://dzone.com/articles/creating-rest-services-with-flask
# To run this program, in terminal window issue the cmd:
#   python3 GT-stocks.py
# alternatively, comment out "app.run..." cmd in __main__ and issue the following cmds
#   export FLASK_APP-"GT-stocks.py"
#   flask run --port 8000     (or whatever port you want to run on.  if no "--port" option specified, it is port 5000)
# flask will return the IP and port the app is running on
# you must install the packages Flask before running this program
import json
# The resources are:
# /stocks             This is a portfolio.of stock objects.   These stocks comprise the portfolio.
# /stocks/{id}        This is the stock object in /stocks with the given id.
# /stock-value/{id}   This is a float.  It is the current share price of the portfolio stock with that id.
# /portfolio-value    This is a float.  It is the current value of the entire portfolio.
# Every stock object must  have a unique id represented by a string.   The id could be simple string representation of
#   integers (“1”, “2”,…) or could be some other UUID (“VT77G8UMQ”).
#   If an object is deleted, its id should not be reused by a new object.
# A stock object is of the form:
# {
#    “id”: string,
#    “name”: string,
#    “symbol”: string,
#    “purchase price”: float,
#    “purchase date”: string,
#    “shares”: int
# }


import sys
# import dotenv
from flask import Flask, jsonify, request, make_response
# from helpers import genID    # generates a unique string ID
import pymongo
from bson import ObjectId
import requests
import os
from datetime import datetime



app = Flask(__name__)  # initialize Flask
client = pymongo.MongoClient('mongodb://mongo:27017/')
db = client['stocks']
portfolio = db['portfolio']
# dotenv.load_dotenv() # will search for .env file in local folder and load variables
NINJA_API_KEY = os.environ.get("NINJA_API_KEY")

def convert_object_to_date_string(date_object: datetime):
    date_string = datetime.strftime(date_object, '%d-%m-%Y')  # turn into string
    return date_string


@app.route('/stocks', methods=['POST'])
def addStock():
    # print("addStock:")
    try:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify("{error: Expected application/json}"), 415  # 415 Unsupported Media Type
        data = request.json
        # print("type of data = ", type(data))
        # print("data = " , data)
        # Check if required fields are present
        required_fields = ["symbol", "purchase price", "shares"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Malformed data"}), 400
        # newID = genID()      # returns string ID
        if "name" not in data:
            name = "Not Available"
        else:
            name = data["name"]
        if 'purchase date' not in data:
            pd = "Not Available"
        else:
            pd = data["purchase date"]
        stock = {
            "name":name,
            "symbol":data["symbol"],
            "purchase price":data["purchase price"],
            "purchase date":pd,
            "shares":data["shares"]
        }
        result = portfolio.insert_one(stock)
        # Convert ObjectId to string for JSON serialization
        stock_id_str = str(result.inserted_id)
        resp = {"id": stock_id_str}
        # return resp, 201
        return jsonify(resp),201
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


@app.route('/stocks', methods=['GET'])
def getStocks():
    # print("stocks:GET")
    try:
        query_params = request.args.to_dict()
        if query_params:  # query params is not empty
            # print("query_params = ", query_params)
            # convert the string into a mongoDB ID
            query_params['_id'] = ObjectId(query_params["id"])
            del query_params["id"]
        stocks = list(portfolio.find(query_params))
        # print(f"list(portfolio.find(query_params)) =  {stocks}")
        # Convert ObjectId to string for each stock in the list.
        for stock in stocks:
            stock["id"] = str(stock["_id"])
            del stock["_id"]
        return jsonify(stocks), 200
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


@app.route('/stocks/<string:stockid>', methods=['GET'])
def getStock(stockid):
    # print("in getstock(id)")
    try:
        # print("stockid = ", stockid)
        record = portfolio.find_one({"_id": ObjectId(stockid)})
        if record:
            # print("found stock with that id")
            stock = {}
            for field in record:
                if field == "_id":
                    stock['id'] = str(record["_id"])
                else:
                    stock[field] = record[field]
                    # print("field = ", field)
                    # print("stock[field] = ", stock[field])
            return jsonify(stock), 200  # if dict, need to turn into json before returning
        else:
            print("getStock: did NOT find stock with that id")
            return jsonify({"error": "Not found"}), 404
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


@app.route('/stocks/<string:stockid>', methods=['DELETE'])
def delStock(stockid):
    try:
        result = portfolio.delete_one({"_id": ObjectId(stockid)})
        # print("portfolio:DELETE:   result = ", result)
        # print("result.deleted_count = ", str(result.deleted_count))
        if result.deleted_count > 0:
            return '', 204
        else:
            return jsonify({"error": "Not found"}), 404
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


@app.route('/stocks/<string:stockid>', methods=['PUT'])
def update(stockid):
    try:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify({"error":"Expected application/json media type"}), 415  # 415 Unsupported Media Type
        data = request.get_json()
        # Check if required fields are present
        # print("portfolio: PUT:  data = ",data)
        required_fields = ['id','symbol', 'purchase price', 'shares']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Malformed data"}), 400
        result = portfolio.find_one_and_update(
            {"_id": ObjectId(stockid)},
            {"$set": data},
            return_document=pymongo.ReturnDocument.AFTER
        )
        if result.keys():
            resp = {'id': str(result["_id"])}
            return jsonify(resp),200
        else:
            return jsonify({"error": "Not found"}), 404
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


@app.route('/stock-value/<string:stockid>', methods=['GET'])
def get_stock_value(stockid):
    try:
        # I am not certain why I am required to declare NINJA_API_KEY global.   If I do not, then the line:
        # print("NINJA_API_KEY=",NINJA_API_KEY) raises an error that NINJA_API_KEY is undefined.   Maybe whenever
        # passed as am argument to a function, even if not redefined, it needs to global.
        global NINJA_API_KEY
        # print("in get_stock_value")
        # print("get_stock_value: stockid = ", stockid)
        sys.stdout.flush()
        record = portfolio.find_one({"_id": ObjectId(stockid)})
        if record:
            # print("found stock with that id")
            symbol = record['symbol']
            shares = record['shares']
            api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
            response = requests.get(api_url, headers={'X-Api-Key': NINJA_API_KEY})
            if response.status_code == requests.codes.ok:
                # print("response.json() = ", response.json())
                # sys.stdout.flush()
                price = round(response.json()['price'])
                value = round(shares * price)
                priceRec = {
                    "symbol":symbol,
                    "ticker":price,
                    "stock value": value
                }
                return jsonify(priceRec), 200  # if dict, need to turn into json before returning
            else:
                print("Error:", response.status_code, response.text)
                return jsonify({"server error": "API status code " + str(response.status_code)}), 500
                #, "API response": response.text}), 500
        else:
            print("did NOT find stock with that id")
            return jsonify({"error": "Not found"}), 404
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


@app.route('/portfolio-value', methods=['GET'])
def get_portfolio():
    global NINJA_API_KEY
    try:
        # print("get_portfolio (/portfolio-value):")
        query_params = request.args.to_dict()
        stocks = list(portfolio.find(query_params))
        value = 0
        for stock in stocks:
            symbol = stock['symbol']
            shares = stock['shares']
            api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
            response = requests.get(api_url, headers={'X-Api-Key': NINJA_API_KEY})
            if response.status_code == requests.codes.ok:
                # print("response.json() = ", response.json())
                sys.stdout.flush()
                price = response.json()['price']
                value =+ price*shares
            else:
                print("get_portfolio (/portfolio-value): NINJA API error")
                sys.stdout.flush()
                return jsonify({"server error": "API status code " + str(response.status_code)}), 500
        date = convert_object_to_date_string(datetime.today())
        obj = {
            "date": date,  # in the format 'DD-MM-YYYY',
            "portfolio value": round(value)
        }
        return jsonify(obj), 200
    except Exception as e:
        print("Exception: ", str(e))
        return jsonify({"server error":str(e)}),500


if __name__ == '__main__':
    print("running stocks server")
    # run Flask app.   default part is 5000
    app.run(host='0.0.0.0', port=5001, debug=True)
