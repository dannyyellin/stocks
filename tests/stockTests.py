import sys
import stockDatabase
import serviceController
import RESTtests
from _datetime import datetime
import copy
from assertions import assert_successfully_added_resource, assert_status_code, assert_collection_contains_field_values, \
    assert_fields_equal
import json
import dotenv
import requests
import os

# to add: multiple copies of books.   if POST same ISBN number must state that it is an additional copy.   keep track of
# number of copies.   can only check out a book if the # of copies is > 0


#cids and some othervars needed to be global scope
item1_id = None  # Google
item2_id = None  # Apple
item3_id = None  # NVIDIA
item4_id = None  # Tesla
item1 = None   # this is the item json for item1
item1_updated = None   # this is the updated item1 json sent in the PUT request (test_put_item1)
put_item1_response = None  # response returned from PUT request (test_put_item1)
item2 = None
allItemRecords = None  # response returned from test_get_all
portfolio_stocks = []
portfolio_shares = {}


# # dates used for borrows requests.  ddObject is the datetime object. dd is the string representation of that date.
# todayObject = datetime.date.today()
# today = todayObject.strftime('%d-%m-%Y')
# yesterdayObject = datetime.date.today() - datetime.timedelta(1)
# yesterday = yesterdayObject.strftime('%d-%m-%Y')
# weekAgoObject = datetime.date.today() - datetime.timedelta(7)
# weekAgo = weekAgoObject.strftime('%d-%m-%Y')
# DaysAgo29Object = datetime.date.today() - datetime.timedelta(29)
# DaysAgo29 = DaysAgo29Object.strftime("%d-%m-%Y")
# sixtyDaysAgoObject = datetime.date.today() - datetime.timedelta(60)
# sixtyDaysAgo = sixtyDaysAgoObject.strftime("%d-%m-%Y")
# ninetyDaysAgoObject = datetime.date.today() - datetime.timedelta(90)
# ninetyDaysAgo = ninetyDaysAgoObject.strftime("%d-%m-%Y")

def convert_object_to_date_string(date_object: datetime):
    date_string = datetime.strftime(date_object, '%d-%m-%Y')  # turn into string
    return date_string


# tests for item microservice
# post_item
def test_post_item1(resourceURL):
    global item1, item1_id, portfolio_stocks, portfolio_shares
    item1 = stockDatabase.Google
    portfolio_stocks.append(item1['symbol'])
    portfolio_shares[item1['symbol']] = item1['shares']
    # print("libraryTests:test_post.  item1 = ", item1)
    success, msg, item1_id = RESTtests.test_post(resourceURL, item1)
    # print(f"LibraryTests:test_post_item1: item1_id = {str(item1_id)}")
    # print(f"test_post_item1:  returning {success} and {msg}. item1_id = {item1_id}")
    sys.stdout.flush()
    return success, msg  #, item1_id, item1


# post 2nd item
def test_post_item2(resourceURL):
    global item2, item2_id, portfolio_stocks, portfolio_shares
    item2 = stockDatabase.Apple
    portfolio_stocks.append(item2['symbol'])
    portfolio_shares[item2['symbol']] = item2['shares']
    success, msg, item2_id = RESTtests.test_post(resourceURL, item2)
    # print(f"item2_id = {item2_id}")
    return success, msg  #, item2_id


# post 3rd item
def test_post_item3(resourceURL):
    global item3_id, portfolio_stocks, portfolio_shares
    item3 = stockDatabase.NVIDIA
    portfolio_stocks.append(item3['symbol'])
    portfolio_shares[item3['symbol']] = item3['shares']
    success, msg, item3_id = RESTtests.test_post(resourceURL, item3)
    return success, msg #, item3_id


# post 4th item
def test_post_item4(resourceURL):
    global item4_id, portfolio_stocks, portfolio_shares
    item4 = stockDatabase.Tesla
    portfolio_stocks.append(item4['symbol'])
    portfolio_shares[item4['symbol']] = item4['shares']
    success, msg, item4_id = RESTtests.test_post(resourceURL, item4)
    return success, msg  # , item4_id


def get_item1(resourceURL):
    global item1_id, item1
    # print(f"LibraryTests:get_item1: item1_id = {item1_id}")
    success, msg, response = RESTtests.test_get(resourceURL, item1_id, item1)
    return success, msg

def test_put_item1(resourceURL):
    global item1_id, item1_updated
    item1_updated = copy.deepcopy(stockDatabase.Google)
    # print("LibraryTests: PUT, item1 = ", item1 )
    # print("LibraryTests: PUT, item1 deepcopy = ", item1_updated)
    # print("type of deepcopy = ", type(item1_updated))
    # print("item1_id = ", item1_id)
    item1_updated["id"] = item1_id
    item1_updated["shares"] = 22
    # print("LibraryTests: PUT, item1 updated = ", item1_updated)
    success, msg, response = RESTtests.test_put(resourceURL, item1_id, item1_updated)
    return success, msg  #, item1_id


# checks that item1 was updated correctly
def test_put_item1_updated_correctly(resourceURL):
    global item1_id, item1_updated
    success, msg, response = RESTtests.test_get(resourceURL, item1_id, item1_updated)
    return success, msg


# test_get_all_items
def test_get_all_items(resourceURL):
    global allItemRecords
    success, msg, allItemRecords = RESTtests.test_get_all(resourceURL)
    # print(f'allItemRecords = {allItemRecords}')
    sys.stdout.flush()
    return success, msg


def test_get_all_valid_items(resourceURL):
    # print(f"libraryTests: test_get_all_vaid: item1_id = {item1_id} and item2_id = {item2_id}")
    success, msg = assert_collection_contains_field_values(allItemRecords, "id", [item1_id, item2_id])
    return success, msg


# test_delete_item2 checks that DELETE returns correct status code
def test_delete_item2(resourceURL):
    global item2_id, item2, portfolio_stocks, portfolio_shares
    success, msg, response = RESTtests.test_delete(resourceURL, item2_id)
    portfolio_stocks.remove(item2['symbol'])
    del portfolio_shares[item2['symbol']]
    return success, msg


# test_not_found_item2 checks that item2 resource no longer found
def test_not_found_item2(resourceURL):
    success, msg, response = RESTtests.test_get_not_found(resourceURL, item2_id)
    return success, msg


# test GET with query string to retrieve only item3.
def test_get_with_query_string_for_item3(resourceURL):
    global item3_id
    queryString = "id=" + item3_id
    success, msg, response = RESTtests.test_get_with_equality_query(resourceURL, queryString)
    return success, msg


# test_post_invalid_media_type_item checks that if media type is not json, correct error code is returned
def test_post_invalid_media_type_item(resourceURL):
    item = stockDatabase.Microsoft  # could use any stock
    success, msg, response = RESTtests.test_post_invalid_media_type(resourceURL, item)
    return success, msg


# test_post_missing_parm_item checks that if a parameter is missing from the payload, correct error code is
# returned
def test_post_missing_parm_item(resourceURL):
    # item missing "symbol" parameter
    item = stockDatabase.missingParmItem
    success, msg, response = RESTtests.test_post_missing_or_invalid_parm(resourceURL, item)
    return success, msg


def test_get_stock_price_stock_3(resourceURL):
    global item3_id
    item3_symbol = stockDatabase.NVIDIA['symbol']
    shares = stockDatabase.NVIDIA['shares']
    api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(item3_symbol)
    NINJA_API_KEY = os.getenv("NINJA_API_KEY")
    # print("stockTests: NINJA_API_KEY=", NINJA_API_KEY)
    response = requests.get(api_url, headers={'X-Api-Key': NINJA_API_KEY})
    if response.status_code == requests.codes.ok:
        # response.text is a string.   can convert it into JSON via json.loads
        # resp = json.loads(response.text)
        # print("type of resp = ", type(resp))
        # price = resp['price']
        # print("price is = ", str(price))
        # print("type of price is = ", type(price))
        # but response.json() retrieves the json directly, so simpler to do the following
        price = round(response.json()['price'])
        value = round(shares*price)
        expectedResult = {
            "symbol": item3_symbol,
            "ticker": price,
            "stock value": value
        }
        success, msg, response = RESTtests.test_get(resourceURL, item3_id, expectedResult)
        return success, msg
    else:
        # print("test_get_stock_price_stock_3 Error calling Ninja API")
        # print("response.text=", response.text)
        return False, "NINJA API error"


def test_get_portfolio_value(resourceURL):
    # allStocks = RESTtests.test_get(resourceURL)
    global portfolio_stocks, portfolio_shares
    date = convert_object_to_date_string(datetime.today())
    value = 0
    for symbol in portfolio_stocks:
        api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
        NINJA_API_KEY = os.getenv("NINJA_API_KEY")
        response = requests.get(api_url, headers={'X-Api-Key': NINJA_API_KEY})
        if response.status_code == requests.codes.ok:
            # print("response.json() = ", response.json())
            price = response.json()['price']
            value = + price * portfolio_shares[symbol]
    exp_obj = {
        "date": date,  # in the format 'DD-MM-YYYY',
        "portfolio value": round(value)
    }
    response = serviceController.http_get(resourceURL)
    print(f"test_get_portfolio: response from application = response.text = {response.text}")
    print(f"computed value of portfolio = {round(value)}")
    outcome1, msg1 = assert_status_code(response, 200)
    outcome2, msg2 = assert_fields_equal(exp_obj,response.json())
    outcome = outcome1 and outcome2
    msg = msg1 + msg2
    return outcome, msg

if __name__ == '__main__':
    #basic tests on items
    print("done")
    sys.stdout.flush()
