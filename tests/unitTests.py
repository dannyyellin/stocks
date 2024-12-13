# This is main test file for testing the Stocks application.  It can easily be customized to test other
# microservices by changing a few lines of code and variable names.
# Additionally, service-specific tests must be modified
# The complete set of files required for testing are unitTests.py, stockTests.py. stockDatabase.py, RESTtests.py,
# and serviceController.py
# To invoke this test module, you need to pass in two parameters:
# The first parameter is the directory to print results to.
# The second parameter is the name of the microservice being tested.

import sys
from datetime import datetime
import random
import RESTtests
import serviceController
from stockTests import test_post_item1, get_item1, test_post_item2, test_put_item1, \
    test_put_item1_updated_correctly, test_get_all_items, test_get_all_valid_items,  \
    test_delete_item2, test_not_found_item2, test_post_item3, test_post_item4, \
    test_get_with_query_string_for_item3, test_post_invalid_media_type_item, \
    test_post_missing_parm_item, test_get_stock_price_stock_3, test_get_portfolio_value
from assertions import assert_ret_value_not_empty, assert_collection_contains_field_values

# docker-compose up -d
# docker-compose kill
# docker-compose rm -f
# docker volume prune -f

SERVER_IP = "http://127.0.0.1"

PORTFOLIO_SERVICE_PORT = 5001
PORTFOLIO_RESOURCE_NAME = "/stocks"
PORTFOLIO_SERVICE_URL = f"{SERVER_IP}:{PORTFOLIO_SERVICE_PORT}{PORTFOLIO_RESOURCE_NAME}"
STOCK_VALUE_RESOURCE_NAME = "/stock-value"
STOCK_VALUE_SERVICE_URL = f"{SERVER_IP}:{PORTFOLIO_SERVICE_PORT}{STOCK_VALUE_RESOURCE_NAME}"
PORTFOLIO_VALUE_RESOURCE_NAME = "/portfolio-value"
PORTFOLIO_VALUE_SERVICE_URL = f"{SERVER_IP}:{PORTFOLIO_SERVICE_PORT}{PORTFOLIO_VALUE_RESOURCE_NAME}"

FAKE_ID = "946aa7909878999123abc23f"


if __name__ == '__main__':
    print("entered UnitTests.py")
    # Check if file path provided as input.  If it is, then write output to that file.  Otherwise use default file.
    if len(sys.argv) > 2:
        base_dir = str(sys.argv[1])  # 1st parm is directory to print to
        ms_name = str(sys.argv[2])   # 2nd parm is the name of the microservice code file without the extension.
    else:
        base_dir = "/Users/danielyellin/PycharmProjects/stocks"
        ms_name = "stocks"
    log_name = base_dir + "/" + ms_name + "-test_log.txt"
    err_file = base_dir + "/" + ms_name + "-test-errors.txt"
    # excp_file = base_dir + "/" + ms_name + "-test-exceptions.txtf"
    dateObj = datetime.today()
    print("Running tests on ", datetime.strftime(dateObj, '%d-%m-%Y'))
    h = open(err_file, "w")
    h.write(f"The following unit tests failed when testing the {ms_name} microservice:\n")
    # this file will be writtent to below for failed tests

    testsPassed = []
    testsFailed = []
    RESTexceptions = []
    ALL_TESTS = [
        "",   # just here for alignment - so that next element is ALL_TESTS[1], not ALL_TESTS[0]
        f"1: Test GET {PORTFOLIO_RESOURCE_NAME}.  This test checks that the collection resource is initially empty",
        f"2: Test POST {PORTFOLIO_RESOURCE_NAME}",
        f"3: Test GET {PORTFOLIO_RESOURCE_NAME}. This test checks that the previous POST request returned the correct ID",
        f"4: Test PUT {PORTFOLIO_RESOURCE_NAME}",
        f"5: Test PUT {PORTFOLIO_RESOURCE_NAME}. This test checks that the previous PUT request correctly updated the resource",
        f"6: Test GET ALL {PORTFOLIO_RESOURCE_NAME}",
        f"7: Test to validate that the previous GET all {PORTFOLIO_RESOURCE_NAME} returned the correct resources",
        f"8: Test DELETE {PORTFOLIO_RESOURCE_NAME}",
        f"9: Test GET {PORTFOLIO_RESOURCE_NAME}. This test checks that the correct status code is returned when the resource is not found",
        f"10: Test GET {PORTFOLIO_RESOURCE_NAME}. This test checks that the correct resources are returned when a Query String is included in the request",
        f"11: Test POST {PORTFOLIO_RESOURCE_NAME}. This test checks that the correct status code is returned when the request includes an invalid media type",
        f"12: Test POST {PORTFOLIO_RESOURCE_NAME}. This test checks that the correct status code is returned when the request has a missing parameter",
        f"13: Test GET {PORTFOLIO_RESOURCE_NAME}. This test checks that the correct status code is returned when the request has an incorrect ID",
    ]

    STOCK_SPECIFIC_TESTS = [
        f"14. Test GET {STOCK_VALUE_RESOURCE_NAME}",   # number 0 in Stock_Specific_Tests
        f"15. Test GET {PORTFOLIO_VALUE_RESOURCE_NAME}"
    ]

    print(f"\nTESTS {PORTFOLIO_RESOURCE_NAME} microservice")
    # TESTS ON CARDHOLDERS microservice, test 1-14

    # test #1
    #print(\n1. Test GET ALL testing empty collection")
    text = ALL_TESTS[1]
    print(text)
    try:
        success, msg, response = RESTtests.test_empty_collection_resource(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(1)
        else:
            testsFailed.append(1)
            # h.write(f"Unit test GET request to the item service checking that the /items resource is initially "
            #         f"empty failed with the message: {msg}\n")
            h.write(f"{text}.  This test failed with the message: {msg}\n")
    except Exception as e:   # REST threw exception
        RESTexceptions.append(1)
        testsFailed.append(1)
        print(f"{text}.  This test raised the exception {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        sys.stdout.flush()


    # print("\n2. Test POST item1")
    text = ALL_TESTS[2]
    print(text)
    item1_id = None
    item1 = None
    text = ALL_TESTS[2]
    try:
        success, msg = test_post_item1(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(2)
        else:
            testsFailed.append(2)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test POST request to the item service failed with the message: {msg}\n")
    except Exception as e:   # REST threw exception
        print("unitTests: TEST POST item1. exception: raised")
        RESTexceptions.append(2)
        testsFailed.append(2)
        print(f"{text}.  This test raised the exception {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        sys.stdout.flush()

    # 3. GET <id1>:  test that that posted resource is returned.  2 & 3 test POST completely
    # print("\n3. Test GET item1")
    sys.stdout.flush()
    text = ALL_TESTS[3]
    print(text)
    try:
        success, msg = get_item1(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(3)
        else:
            testsFailed.append(3)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test GET ID request to the item service checking that the previous POST request returned "
            #         f"the correct ID failed with the message: {msg}\n")
    except Exception as e:  # REST threw exception
        RESTexceptions.append(3)
        testsFailed.append(3)
        print(f"{text}.  This test raised the exception {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        # h.write(f"Unit test GET ID request to the item service checking that the previous POST request returned"
        #     f"the correct ID raised the exception: {str(e)}\n")
        sys.stdout.flush()

    # 4. PUT <id1>: test that PUT returns the correct status code
    # print("\n4. Test PUT item1")
    text = ALL_TESTS[4]
    print(text)
    try:
        success, msg = test_put_item1(PORTFOLIO_SERVICE_URL)
        # returns response from GET
        if success:
            testsPassed.append(4)
        else:
            testsFailed.append(4)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test PUT request to the item service failed with the message: {msg}\n")
    except Exception as e:
        RESTexceptions.append(4)
        testsFailed.append(4)
        print(f"{text}.  This test raised the exception {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        # h.write(f"Unit test PUT request to the item service raised the exception: {str(e)}\n")
        sys.stdout.flush()

    # 5. GET <id1>: test that updated resource is returned.  4 & 5 test PUT completely
    # print("\n5. Test that PUT item1 updated correctly")
    text = ALL_TESTS[5]
    print(text)
    try:
        success, msg = test_put_item1_updated_correctly(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(5)
        else:
            testsFailed.append(5)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test GET request to the item service validating that the previous PUT request "
            #         f"correctly updated the resource failed with the message: {msg}\n")
    except Exception as e:
        RESTexceptions.append(5)
        testsFailed.append(5)
        print(f"{text}.  This test raised the exception {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        # h.write(f"Unit test GET request to the item service validating that the previous PUT request "
        #         f"correctly updated the resource raised the exception: {str(e)}\n")
        sys.stdout.flush()

    # X. POST: a second resource.   already tested POST in #2 so this one not counted
    print("\n  Test POST item2")
    print("\n This test not counted in success/failure count as already tested POST")
    sys.stdout.flush()
    try:
        success, msg = test_post_item2(PORTFOLIO_SERVICE_URL)
    except Exception as e:
        print(f"{text}.  This test raised the exception {str(e)}\n")
        sys.stdout.flush()

    # 6. GET all:  test that GET returns correct status code
    # print("\n6. Test GET all items")
    text = ALL_TESTS[6]
    print(text)
    try:
        success, msg = test_get_all_items(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(6)
        else:
            testsFailed.append(6)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test GET (ALL) request to the item service failed with the message: {msg}\n")
    except Exception as e:
        RESTexceptions.append(6)
        testsFailed.append(6)
        print(f"{text}.  This test raised the exception {str(e)}\n")
        # h.write(f"Unit test GET (ALL) request to the item service raised the exception: {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        sys.stdout.flush()

    # 7. Check that both item1 and item2 resources are returned in previous call.
    # n7 checks that there exists records r1 and r2 in the result such that r1["id"] = item1_id, and
    # r2["id"] = item2_id.
    # tests #6 and #7 test Get all completely.
    # print("\n7. Validate results from previous GET all items")
    text = ALL_TESTS[7]
    print(text)
    try:
        success, msg = test_get_all_valid_items(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(7)
        else:
            testsFailed.append(7)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test The test to validate that the previous GET (ALL) request to the item service "
            #         f"returned the correct resources failed with the message: {msg}\n")
    except Exception as e:
        #  If have an exception: here not due to REST request (as there is no REST request)
        testsFailed.append(7)
        print(f"{text}.  This test raised the exception {str(e)}\n")
        # h.write(f"Unit test The test to validate that the previous GET (ALL) request to the item service "
        #         f"returned the correct resources raised the exception: {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        sys.stdout.flush()

    # 8. DELETE <id2>: test that DELETE returns the correct status code
    # print("\n8. Test DELETE item2")
    text = ALL_TESTS[8]
    print(text)
    try:
        success, msg = test_delete_item2(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(8)
        else:
            testsFailed.append(8)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test DELETE ID request to the item service failed with the message: {msg}\n")
    except Exception as e:
        # REST request threw exception
        RESTexceptions.append(8)
        testsFailed.append(8)
        print(f"{text}.  This test raised the exception {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        # h.write(f"Unit test DELETE ID request to the item service raised the exception: {str(e)}\n")
        sys.stdout.flush()


    # 9. GET <id2>:  test that correct status code is returned (NOT FOUND).    #8 & #9 test DELETE completely
    # print("\n9. Test that GET item2 is NOT FOUND")
    text = ALL_TESTS[9]
    print(text)
    try:
        success, msg = test_not_found_item2(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(9)
        else:
            testsFailed.append(9)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test GET request with an invalid ID to the item service failed with the f"
            #         f"message: {msg}\n")
    except Exception as e:
        # REST request threw exception
        RESTexceptions.append(9)
        testsFailed.append(9)
        print(f"{text}.  This test raised the exception {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        # h.write(f"Unit test GET request with an invalid ID to the item service raised the exception: {str(e)}\n")
        sys.stdout.flush()

    # X. POST: 3rd resource.   already tested POST in #2 so this one not counted
    print("\n Test POST item3")
    # print("This test not counted in success/failure as already tested POST")
    sys.stdout.flush()
    try:
        success, msg = test_post_item3(PORTFOLIO_SERVICE_URL)
    except Exception as e:
        print("UnitTests.py: Exception = ", str(e))
        sys.stdout.flush()

    # X. POST 4th resource.  already tested POST in #2 so this one not counted
    print("\n Test POST item4")
    # print("\n   This test not counted in success/failure as already tested POST")
    sys.stdout.flush()
    try:
        success = test_post_item4(PORTFOLIO_SERVICE_URL)
    except Exception as e:
        print("UnitTests.py: Exception = ", str(e))
        sys.stdout.flush()

    # 10. GET all with simple equality query string.  Check that status code is correct & correct resource
    # is returned.
    # print("\n10. Test GET items with query string for item3")
    text = ALL_TESTS[10]
    print(text)
    try:
        success, msg = test_get_with_query_string_for_item3(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(10)
        else:
            testsFailed.append(10)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test GET request with a Query String to the item service failed with the "
            #          f"message {msg}\n")
    except Exception as e:
        # REST request threw exception
        RESTexceptions.append(10)
        testsFailed.append(10)
        print(f"{text}.  This test raised the exception {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        # h.write(f"Unit test GET request with a Query String to the item service raised the exception: {str(e)}\n")
        sys.stdout.flush()


    # test_post_invalid_media_type_item checks that wrong media type returns the proper status code.
    # if not, or if exception is raised in REST call, it is counted as a failure.
    # print("\n11. Test POST item with invalid media type")
    text = ALL_TESTS[11]
    print(text)
    try:
        success, msg = test_post_invalid_media_type_item(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(11)
        else:
            testsFailed.append(11)
            h.write(f"{text}. This test failed with the message: {msg}\n")
            # h.write(f"Unit test POST request with an invalid media type to the item service failed with the "
            #         f"message: {msg}\n")
    except Exception as e:
        # REST request threw exception
        RESTexceptions.append(11)
        testsFailed.append(11)
        print(f"{text}. This test raised the exception {str(e)}\n")
        h.write(f"{text}. This test raised the exception {str(e)}\n")
        # h.write(f"Unit test POST request with an invalid media type to the item service raised the exception: {str(e)}\n")
        sys.stdout.flush()


    # performing test_post_missing_parm_item checks that missing parameters returns the proper status code.
    # if not, or if exception is raised in REST call, it is counted as a failure.
    # print("\n12. Test POST item with missing parameter")
    text = ALL_TESTS[12]
    print(text)
    try:
        success, msg = test_post_missing_parm_item(PORTFOLIO_SERVICE_URL)
        if success:
            testsPassed.append(12)
        else:
            testsFailed.append(12)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test POST request to item service with a missing parameter failed with the "
            #         f"message: {msg}\n")
    except Exception as e:
        # REST request threw exception
        RESTexceptions.append(12)
        testsFailed.append(12)
        print(f"{text}. This test raised the exception {str(e)}\n")
        h.write(f"{text}. This test raised the exception {str(e)}\n")
        # h.write(f"Unit test POST request to item service with a missing parameter raised the exception: {str(e)}\n")
        sys.stdout.flush()


    # print("\n13. Test GET item with incorrect ID")
    text = ALL_TESTS[13]
    print(text)
    try:
        # print("UnitTests.py: about to call RESTtests.test_get_not_found(PORTFOLIO_SERVICE_URL, FAKE_ID)")
        success, msg, response = RESTtests.test_get_not_found(PORTFOLIO_SERVICE_URL, FAKE_ID)
        if success:
            testsPassed.append(13)
        else:
            testsFailed.append(13)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test GET request to the item service with an incorrect ID failed with the "
            #         f"message {msg}\n")
    except Exception as e:
        # REST request threw exception
        RESTexceptions.append(13)
        testsFailed.append(13)
        print(f"{text}. This test raised the exception {str(e)}\n")
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        # h.write(f"Unit test GET request to the item service with an incorrect ID raised the exception: {str(e)}\n")
        sys.stdout.flush()

# at this point portfolio contains item1 (modified), item3 and item4
#
#  SERVICE specific tests
#     print("\n14. Test GET /stock-value/{id}")
    text = STOCK_SPECIFIC_TESTS[0]
    try:
        success,msg = test_get_stock_price_stock_3(STOCK_VALUE_SERVICE_URL)
        if success:
            testsPassed.append(14)
        else:
            testsFailed.append(14)
            h.write(f"{text}.  This test failed with the message: {msg}\n")
            # h.write(f"Unit test GET request to the STOCK_VALUE_SERVICE_URL failed with the message {msg}\n")
    except Exception as e:
        # REST request threw exception
        RESTexceptions.append(14)
        testsFailed.append(14)
        print("UnitTests.py: Exception = ", str(e))
        h.write(f"{text}.  This test raised the exception {str(e)}\n")
        # h.write(f"Unit test GET request to the STOCK_VALUE_SERVICE_URL raised the exception: {str(e)}\n")
        sys.stdout.flush()

# print("\n15. Test GET /portfolio-value")
text = STOCK_SPECIFIC_TESTS[1]
print(text)
try:
    success,msg = test_get_portfolio_value(PORTFOLIO_VALUE_SERVICE_URL)
    if success:
        testsPassed.append(15)
    else:
        testsFailed.append(15)
        h.write(f"{text}.  This test failed with the message: {msg}\n")
        # h.write(f"Unit test GET request to the STOCK_VALUE_SERVICE_URL failed with the message {msg}\n")
except Exception as e:
    # REST request threw exception
    RESTexceptions.append(15)
    testsFailed.append(15)
    print(f"{text}. This test raised the exception {str(e)}\n")
    h.write(f"{text}.  This test raised the exception {str(e)}\n")
    # h.write(f"Unit test GET request to the PORTFOLIO_VALUE_SERVICE_URL raised the exception: {str(e)}\n")
    sys.stdout.flush()

h.close()
print("\nTests statistics\n")
print(f"Tests passed = {testsPassed}\nTests failed = {testsFailed}\n")
TestsPassed = testsPassed
TestsFailed = testsFailed
BasicPassed = [x for x in testsPassed if x in range(1,11)]
BasicFailed = [x for x in testsFailed if x in range(1,11)]
ExceptionPassed = [x for x in testsPassed if x in range(11,13)]
ExceptionFailed = [x for x in testsFailed if x in range(11, 13)]
StockSpecificPassed = [x for x in testsPassed if x in range(14, 14)]
StockSpecificFailed = [x for x in testsFailed if x in range(14, 14)]

g = open(log_name, "w")
print("opened log file = ", log_name)
g.write("test\n")
current_time = datetime.now()
formatted_time = current_time.strftime('%d/%m/%Y:%H:%M:%S')
print(formatted_time)
g.write(formatted_time)
g.write("\nf'TESTS STATISTICS for Stocks Service \n")
g.write(f"Tests passed = {testsPassed}\nTests failed = {testsFailed}\n")

g.write("\nSTOCKS MICROSERVICE STATISTICS\n")
g.write(f"Stocks tests passed = {TestsPassed}\nStocks tests failed = {TestsFailed}\n")
g.write(f'Basic Stocks tests passed = {BasicPassed}\nBasic Stocks tests failed = {BasicFailed}\n')
# g.write("Basic Stocks tests includes GET all with simple equality query string (test 10)\n")
g.write(f'Exception Status Stocks tests passed = {ExceptionPassed}\nException Status Stocks tests failed = {ExceptionFailed}\n')
g.write(f'Stocks specific tests passed = {StockSpecificPassed}\nStocks specific tests failed = {StockSpecificFailed}\n')
g.close()