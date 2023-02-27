##################################
# custom_api_lab.py
# ITCC2100
# Nikolaus Gietzen
# 02/15/2023
##################################

import requests
from requests import RequestException


def main():
    url = "https://hbjsktq9zh.execute-api.us-east-1.amazonaws.com/my-function"

    print("Invoking my HTTP GET function")
    if invoke_my_function(url):
        print("Completed Successfully!")
    else:
        print("An error occurred!")


def invoke_my_function(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print(r)
            return True
        else:
            return False

    except RequestException as e:
        print(e)
        return False


if __name__ == '__main__':
    main()
