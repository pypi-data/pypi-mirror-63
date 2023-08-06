import requests

class Client(object):

	def __init__(self, host=None, path=None, token=None):
		self.host = host
		self.path = path
		self.token = token

	def data(self, text, *args, **kwargs):
		text = str(text)

		if args:
			text += ' ' + ' '.join(args)

		return {'text': text, 'meta': kwargs}

	def post(self, text, *args, path=None, **kwargs):
		json = self.data(text, *args, **kwargs)
		json.update({'token': self.token})
		return requests.post(f'{self.host}{path or self.path}', json=json)
