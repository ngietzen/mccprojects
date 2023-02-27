########################################
# api_demo.py
# ITCC 2100
# Nikolaus Gietzen
# 02/24/2023
########################################

# imports
import requests
import json
from requests import RequestException


# GET function
def invoke_http_get(url):
	# call requests.get to get the json placeholder data
	r = requests.get(url)
	
	# create a JSON object from the data
	obj = r.json()
	
	# iterate through the data and print each item
	for o in obj:
		print('userId : ' + str(o['userId']))
		print('id : ' + str(o['id']))
		print('title : ' + o['title'])
		print('body : ' + o['body'])


# POST function
def invoke_http_post(url):
	# sample data
	sample_post = {
		'userId': 1,
		'title': 'Test Post Title',
		'body': 'This is the body of the test post!'
	}
	
	# call requests.post using the URL and the sample data
	r = requests.post(url, data=json.dumps(sample_post))
	
	# print the status code
	print('Returned status code : ' + str(r.status_code))
	
	
# main function, runs the other two functions
def main():
	# HTTP GET
	print('Invoking HTTP GET')
	try:
		invoke_http_get('https://jsonplaceholder.typicode.com/posts')
	except RequestException as e:
		print('An error occurred!')
	
	# HTTP POST
	print('Invoking HTTP POST')
	try:
		invoke_http_post('https://jsonplaceholder.typicode.com/posts')
	except RequestException as e:
		print('An error occurred!')


if __name__ == '__main__':
	main()

