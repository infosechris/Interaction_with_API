from code_challenge import InteractJsonApi
import pytest
import datetime

url = "https://jsonplaceholder.typicode.com/posts/"

payload = {
    "Title": "Security Post",
    "UserID": "500",
    "Body": "This is an insertion test with a known API"
    }


def test_status_code():
    connect = InteractJsonApi(url, 99)
    test_status = connect.get_response()
    assert test_status.status_code == 200


def test_title():
    connect = InteractJsonApi(url, 99)
    test_title = connect.title()
    assert test_title == ("temporibus sit alias delectus "
                          "eligendi possimus magni")


def test_inject():
    connect = InteractJsonApi(url, 99)
    test_inject = connect.inject_time()
    now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
    assert test_inject['userId'] == 10
    assert test_inject['id'] == 99
    assert test_inject['time'] == now


def test_post_content():
    connect = InteractJsonApi(url, 99)
    test_post_content = connect.get_posted_content(payload)
    assert test_post_content == (101, 201, 'Express')


def test_deleted_content():
    connect = InteractJsonApi(url, 99)
    test_deleted_content = connect.get_deleted_content()
    assert test_deleted_content == (200, 'nosniff')
