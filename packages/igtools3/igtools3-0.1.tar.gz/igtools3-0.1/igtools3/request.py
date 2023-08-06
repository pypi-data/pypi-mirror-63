import requests

def get(url, headers=None, redirect=False):
	r = requests.get(url, headers=headers, allow_redirects=redirect)
	return r

def post(url, headers=None, data=None):
	r = requests.post(url, data=data, headers=headers)
	return r

def sess():
	return requests.Session()
