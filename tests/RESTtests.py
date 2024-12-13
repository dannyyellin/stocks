# This module provides generic tests for REST application
# All tests return a boolean outcome which is True if the test is successful and False otherwise.   Some tests return
# additional paramters (for example, the id returned from a POST request).

import sys
import serviceController
from assertions import assert_fields_equal, assert_successfully_added_resource, assert_status_code, \
    assert_ret_value_empty, assert_matches_equality_query, \
    assert_request_not_implemented, assert_ret_value_not_empty, get_response_id


# ** NEED TO make sure that if one test fails (e.g., no data returned and request.json() throws exception) the exception is caught

# POST TESTS:
# test_post_and_get(resourceURL,payload, expectedJasonResult)
# test_post_invalid_media_type(resourceURL, resource)
# test_post_missing_or_invalid_parm(resourceURL, invalidResource)

# GET TESTS:
# test_empty_collection_resource(resourceURL)
# test_not_empty_collection_resource(resourceURL)
# test_get_all(resourceURL)
# test_get_with_equality_query(resourceURL, query)
# test_get_with_date_query(resourceURL, query)
# test_get_not_found(resourceURL)

# DELETE TESTS:
# test_delete(resourceURL, resource)
# test_delete_not_supported(resourceURL, resource)

# PUT TESTS
# test_put_and_get(resourceURL, resource, updatedResource)
    # test_put_not_found_<resource_name>
    # test_put_incorrect_parm_<resource_name>


#
# Basic tests and exception tests on Cardholder microservice
#

# breaking the above test_post_and_get into test_post and test_get
# initial test on collection resource to validate that the resource is empty to begin with
def test_empty_collection_resource(resourceURL):
    # print("RESTtests: test_empty_collection_resource")
    response = serviceController.http_get(resourceURL)
    # print("RESTtests: got response")
    # assert response.status_code == 200
    # assert response.json() == []
    outcome1, msg1 = assert_status_code(response, 200)
    outcome2, msg2 = assert_ret_value_empty(response)
    outcome = outcome1 and outcome2
    msg = msg1 + msg2
    return outcome, msg, response

def test_post(resourceURL, payload):
    response = serviceController.http_post(resourceURL, payload)
    # print("RESTtests response = ", response)
    outcome,msg = assert_successfully_added_resource(response)
    sys.stdout.flush()
    # retrieves the id of the posted resource either from response.json()['id'] or from response.text
    post_id = get_response_id(response)
    return outcome, msg, post_id


def test_get(resourceURL, resource_id, expectedJasonResult):
    # print(f"test_get: resourceURL = {resourceURL} resource_id = {resource_id}")
    response = serviceController.http_get(resourceURL + "/" + resource_id)
    # print(f"test_get: response.text = {response.text}")
    outcome1, msg1  = assert_status_code(response, 200)
    outcome2, msg2  = assert_fields_equal(expectedJasonResult, response.json())
    outcome = outcome1 and outcome2
    msg = msg1 + msg2
    return outcome, msg, response


# test PUT request
def test_put(resourceURL, resource_id, updatedResource):
    response = serviceController.http_put(resourceURL + "/" + resource_id, updatedResource)
    print("RESTtests::test_put: response.json() = ", response.json())
    outcome, msg = assert_status_code(response,200)
    return outcome, msg, resource_id


# tests GET All on a collection resource.   Note that it does not test that all the resources are returned.
def test_get_all(resourceURL):
    response = serviceController.http_get(resourceURL)
    outcome, msg = assert_status_code(response, 200)
    # print("RESTtests::get_all: response.json() = ", response.json())
    return outcome, msg, response.json()


def test_not_empty_collection_resource(resourceURL):
    response = serviceController.http_get(resourceURL)
    # assert response.status_code == 200
    # assert response.json() == []
    outcome1, msg1 = assert_status_code(response, 200)
    outcome2, msg2 = assert_ret_value_not_empty(response)
    outcome = outcome1 and outcome2
    msg = msg1 + msg2
    return outcome, msg, response


# just testing delete, without preceding post
def test_delete(resourceURL, resource_id):
    response = serviceController.http_delete(resourceURL + "/" + resource_id)
    outcome, msg = assert_status_code(response, error_code=204)
    return outcome, msg, response


# this tests that the records in the response all satisfy the simple equality query.
# the simple query is assumed to be of the form: field=value
# Note that it does not check that ALL resources that satisfy the query are included in the response.
def test_get_with_equality_query(resourceURL, query):
    response = serviceController.http_get(resourceURL + "?" + query)
    outcome1, msg1 = assert_status_code(response, 200)
    recordsSatisfyingQuery = response.json()
    # print(f'recordsSatisfyingQuery = {recordsSatisfyingQuery}')
    sys.stdout.flush()
    outcome2, msg2 = assert_ret_value_not_empty(recordsSatisfyingQuery)
    outcome3, msg3 = assert_matches_equality_query(query, response)
    outcome = outcome1 and outcome2 and outcome3
    msg = msg1 + msg2 + msg3
    return outcome, msg, response


# exception tests
# resource_id should not exist.   test that REST GET request returns proper error code
def test_get_not_found(resourceURL, resource_id):
    response = serviceController.http_get(resourceURL + "/" + resource_id)
    outcome, msg = assert_status_code(response, error_code=404)
    return outcome, msg, response


def test_post_invalid_media_type(resourceURL, resource):
    response = serviceController.http_post_xml(resourceURL, resource)
    outcome, msg = assert_status_code(response, 415)
    return outcome, msg, response


def test_post_missing_or_invalid_parm(resourceURL, invalidResource):
    # invalid or missing json field
    response = serviceController.http_post(resourceURL, invalidResource)
    outcome, msg = assert_status_code(response, 400)
    return outcome, msg, response


# test_delete_not_supported tests that deleting a resource is not valid.  Should return 405 Method Not Allowed - we will also
# accept error codes 500 or 501.
# (From Mozilla: # The HyperText Transfer Protocol (HTTP) 405 Method Not Allowed response status code indicates that the
# server knows the request method, but the target resource doesn't support this method.)   Even though it states that:
# If the server does recognize the method, but intentionally does not support it, the appropriate response is 405
# Method Not Allowed.
def test_delete_not_supported(resourceURL, id):
    response = serviceController.http_delete(resourceURL + "/" + id)
    outcome, msg = assert_request_not_implemented(response)
    return outcome, msg, response


if __name__ == '__main__':
    #basic tests on cardholders
    print("done")
    sys.stdout.flush()
