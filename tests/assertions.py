import requests
import sys
import datetime

# This file contains assertions checking if the results of tests are correct or not.
# The assertion returns True if the assertion is satisfied and False otherwise.


# auxiliary function to allow a resource id to be returned simply as a string value or as a JSON record.   used in
# other modules
def get_response_id(response: requests.Response):
    try:
        # print(f"assertions.py::get_response_id: response.json()['id'] = {response.json()['id']}")
        return response.json()['id']
    except ValueError:
        # no JSON defined, id should be defined as response.txt
        # print("get_response: returning response.text=  ", response.text)
        # print(f"assertions.py::get_response_id: exception.  returning {response.text}")
        return response.text


def assert_status_code(response: requests.Response, error_code: int):
    # assert response.status_code == error_code
    if response.status_code != error_code:
        print("----->  FAILED <----- assert_status_code")
        print(f"Expected status code = {error_code} but received status code = {response.status_code}\n")
        msg = f"Expected status code = {error_code} but received status code = {response.status_code}\n"
        return False,msg
    else:
        print("++++++ passed assert_status_code")
        return True,''


def assert_successfully_added_resource(response: requests.Response):
    # assert response.status_code == 201
    if response.status_code != 201:
        print("----->  FAILED <----- assert_successfully_added_resource")
        print(f"Expected status code = 201 but response error code = {str(response.status_code)}\n")
        return False, f"Expected status code = 201 but response error code = {str(response.status_code)}\n"
    else:
        print("++++++ passed assert_successfully_added_resource")
        return True,''


# I never specified that it should return -1 if not successful post
# def assert_unsuccessful_post_resource(response: requests.Response):
#     # assert response.text == -1
#     if response.text != "-1":
#         print("----->  FAILED <----- unsuccessful_post_resource")
#         print("expecting '-1'.  response.text = ", response.text)
#     else:
#         print("++++++ passed unsuccessful_post_resource")
#     sys.stdout.flush()

# this assertion is used to check that the return code from a request returns an error code indicating that the request
# is not implemented.  For example, some resources do not allow deleting a resource.   If that is the case, the
# request should return 405 Method Not Allowed.
# (From Mozilla: # The HyperText Transfer Protocol (HTTP) 405 Method Not Allowed response status code indicates that the
# server knows the request method, but the target resource doesn't support this method.)   Even though it states that:
# If the server does recognize the method, but intentionally does not support it, the appropriate response is 405
# Method Not Allowed.
# We will also accept error codes 500 or 501 in addition to 405.
def assert_request_not_implemented(response: requests.Response):
    # assert response.status_code is one of [405, 500, 501]  (See testDefns.test_log_delete_invalid)
    if response.status_code not in [405, 500, 501]:
        print("----->  FAILED <----- assert_one_of_several_status_codes")
        print(f"Expected status code = 405 or 500 or 501 but response error code = {str(response.status_code)}\n")
        return False, f"Expected status code = 405 or 500 or 501 but response error code = {str(response.status_code)}\n"
    else:
        print("++++++ passed assert_one_of_several_status_codes")
        # print("allowable codes are 405 (preferred), 500, 501")
        # print("response code = ", response.status_code)
        return True,''


# record2 is returned object.  record1 is expected object.
# check that the fields of record2 match each field of record1. note that record2 may have more fields, such as an
# # "id" field.
# record1 is known to be a dict (a json structure) but record2 needs to be checked
def assert_fields_equal(record1: dict, record2: any):
    if type(record2) != type(record1):  # check that record2 is also a dictionary
        print(f'Returned object is not of type {str(type(record1))}\n')
        print("----->  FAILED <----- assert_fields_equal")
        sys.stdout.flush()
        return False, f'Returned object is not of type {str(type(record1))}\n'
    for field in record1.keys():
        if field not in record2:
            print(f'Expected field named "{field}" in returned object but it was missing. Returned object = {record2}\n')
            print("----->  FAILED <----- assert_fields_equal")
            sys.stdout.flush()
            return False, f'Expected field named "{field}" in returned object but it was missing. Returned object = {record2}\n'
        if record1[field] != record2[field]:
            print(f'Field "{field}" in returned object: {record2[field]} does not match expected value: {record1[field]}')
            print("----->  FAILED <----- assert_fields_equal")
            sys.stdout.flush()
            return False, f'Field "{field}" in returned object: {record2[field]}does not match expected value: {record1[field]}'
    print("++++++ passed assert_fields_equal")
    return True,''


def assert_ret_value_empty(response: requests.Response):
    # assert response.json() == []]
    # print(f"in assert_ret_value_empty")
    if response.json() != []:
        print("----->  FAILED <----- ret_value_empty")
        print(f'Expected empty response but received {response.json()}\n')
        return False, f'Expected empty response but received {response.json()}\n'
    else:
        print("++++++ passed ret_value_empty")
        return True,''


def assert_ret_value_not_empty(records: list):
    # assert response.json() != []
    if records == []:
        print("----->  FAILED <----- ret_value_not_empty")
        print(f'Expected non-empty response but received {records}\n')
        return False, f'Expected non-empty response but received {records}.\n'
    else:
        print("++++++ passed ret_value_not_empty")
        return True,''


# this function assumes that the query is a simple query of the form field-name=value.
# it checks that each record in the response is such that field of the given name equals the given value
def assert_matches_equality_query(query: str, response: requests.Response):
    jresponse = response.json()
    index = query.find("=")
    field = query[:index]
    value = query[index+1:]
    # print(f'field = {field}. value = {value}')
    msg = ''
    correct = True
    if not all(field in record for record in jresponse):
        correct = False
        print(f'Expected field named "{field}" in response object but it is missing.\n')
        msg = f'Expected field named "{field}" in response object but it is missing.\n'
    else:
        if not all(record[field] == value for record in jresponse):
            correct = False
            print(f'Field {field} of response object does not equal its expected value: {value}.\n')
            msg += f'Field {field} of response object does not equal its expected value: {value}.\n'
    if correct:
        print("++++++ passed assert_matches_query")
        return True,''
    else:
        print("----->  FAILED <----- assert_matches_query")
        print(msg)
        return False, msg


# test_collection_contains_field_values checks that given a list of objects, a json field name field, and a list of
# values, for each v in the list of values there exists a record r in coll such that r[field] = v
def assert_collection_contains_field_values(coll: list, field: str, values: list):
    print(f"assert_collection_container_field_values:  coll = {coll}\n field = {field}\n values = {values}")
    for v in values:
        try:
            if not [c for c in coll if c[field] == v]:
                print("----->  FAILED <----- assert_collection_contains_field_values")
                print(f"No object in returned array with {field} == {v}")
                return False, f"No object in returned array with {field} == {v}"
        except Exception as e:
            print("----->  FAILED <----- assert_collection_contains_field_values")
            print("Exception = ", str(e))
            sys.stdout.flush()
            return False, f'Exception raised.  Exception value = {str(e)}\n'
    # otherwise found that the collection satisfies the assertion
    print("++++++ passed assert_collection_contains_field_values")
    # print(f"there are records in the collection for each value v in {values} such that the field {field} equals v")
    return True,''


if __name__ == '__main__':
    # assert_loanDate_matches_query('beginDate=01-08-2020&endDate=22-12-2023', None)
    # assert_loanDate_matches_query('beginDate=01-08-2020', None)
    # assert_loanDate_matches_query('endDate=22-12-2023', None)
    print("ok")