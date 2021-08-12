#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import datetime
import json


class InteractJsonApi:
    """
    Using the API to interact with the JSONPlaceholder website,
    accomplishing the six goals of the coding chanllenge.

    ...

    Attributes
    ----------
    url : str
        JSONPlaceholder website for the API interaction
    header : dict
        generic headers to use for calls
    post_num : int
        post number equivalent to the id
    payload : dict
        payload for post entry
    """

    def __init__(self, url, post_num=1):
        """Initialize with headers, url, and post numnber(optional)"""
        self.headers = {"Content-type': 'application/json; charset=UTF-8"}
        self.url = url
        self.post_num = str(post_num)

    def get_response(self):
        """Returns response for /Get with post number."""
        post_url = self.url + self.post_num
        try:
            response = requests.get(post_url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response

    def title(self):
        """Returns the value of the title."""
        return self.get_response().json()["title"]

    def inject_time(self):
        """Injects current UTC time and returns JSON record."""
        time_with_post = self.get_response().json()
        now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
        time_with_post["time"] = now
        return time_with_post

    def post_entry(self, payload):
        """Returns response for /post with a payload."""
        try:
            response = requests.post(
                self.url, json.dumps(payload), self.headers)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response

    def get_posted_content(self, payload):
        """
        Posts with given payloadand returns tuple if successful.
        If post failed, returns comment with status code.
        """
        response = self.post_entry(payload)
        status_code = response.status_code
        if (status_code == 201):
            id = response.json()["id"]
            header_powered_by = response.headers["x-Powered-By"]
            return (id, status_code, header_powered_by)
        else:
            return "Post Failed with status code " + str(status_code)

    def delete_entry(self):
        """Returns response for /delete."""
        url = self.url + self.post_num
        try:
            response = requests.delete(url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response

    def get_deleted_content(self):
        """
        Delete the record and
        returns the status code and x-content-type-options.
        """
        response = self.delete_entry()
        content_type = response.headers["x-content-type-options"]
        return response.status_code, content_type


def main():
    url = "https://jsonplaceholder.typicode.com/posts/"

    # Goal #1: Print the value of the title for post number 99.
    goal_one = InteractJsonApi(url, 99)
    print("Goal #1:", goal_one.title())

    # Goal #2: Inject a field called time into the results for post number 100
    # and print the whole JSON record.
    goal_two = InteractJsonApi(url, 100)
    print("Goal #2:", goal_two.inject_time())

    # Goal #3: Create a new /posts entry which the following values.
    # Goal #4: If post was successful, create a tuple.
    payload = {
        "Title": "Security Interview Post",
        "UserID": "500",
        "Body": "This is an insertion test with a known API"
    }

    goal_three_four = InteractJsonApi(url)
    goal_five = goal_three_four.get_posted_content(payload)

    # Goal #5: Print the tuple from #4.
    print("Goal #5:", goal_five)

    # Goal #6: Delete the record you created in #3,
    # by referencing the new “id”.
    # Print the return status code and the x-content-type-options
    # from the returned object.
    goal_six = InteractJsonApi(url, 101)
    print("Goal #6:", goal_six.get_deleted_content())


if __name__ == "__main__":
    main()
