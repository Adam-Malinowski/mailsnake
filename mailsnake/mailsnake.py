import urllib2 
import requests
try:
    import simplejson as json
except ImportError:
    import json


class MailSnake(object):
    def __init__(self, apikey='', extra_params={}):
        """
        Cache API key and address.
        """
        self.apikey = apikey

        self.default_params = {'apikey': apikey}
        self.default_params.update(extra_params)

        dc = 'us1'
        if '-' in self.apikey:
            dc = self.apikey.split('-')[1]
        self.base_api_url = 'https://%s.api.mailchimp.com/1.3/?method=' % dc

    def call(self, method, params):
        headers = {'content-type': 'application/json'}
        post_data = urllib2.quote(json.dumps(params))
        api_url = self.base_api_url + method
        response = requests.post(api_url, data=post_data, headers=headers)
        return json.loads(response.content)

    def __getattr__(self, method_name):

        def get(self, *args, **kwargs):
            params = dict((i,j) for (i,j) in enumerate(args))
            params.update(kwargs.items() + self.default_params.items())
            return self.call(method_name, params)

        return get.__get__(self)
