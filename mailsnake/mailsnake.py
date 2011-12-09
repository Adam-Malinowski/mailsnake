import urllib2 
import requests
try:
    import simplejson as json
except ImportError:
    import json

class MailSnake(object):
    def __init__(self, apikey='', extra_params={}, api='standard', timeout=60):
        """ Cache API key, url and extra params
        
        """
        self.apikey = apikey
        self.default_params = {'apikey': apikey}
        self.default_params.update(extra_params)
        self.api = api
        self.timeout = timeout
        self.dc = 'us1' if '-' not in self.apikey else self.apikey.split('-')[1]
        if self.api == 'export':
            # export api has method as url, not as GET param
            self.api_url = 'https://%s.api.mailchimp.com/export/1.0/' % self.dc
        else:            
            self.api_url = 'https://%s.api.mailchimp.com/1.3/?method=' % self.dc

    def unpack(self, export_data):
        """ Unpack export format to list of dicts
        
        Mailchimp returns a string of json-encoded lists, split by newlines.
        The first line is the keys, the remaining lines are user data.
        
        """
        for i, line in enumerate(export_data.split('\n')):
            if not line: continue
            data = json.loads(line)
            if i == 0:
                keys = data
                continue
            yield dict(zip(keys, data))

    def call(self, method, params):        
        api_url = self.api_url + method        
        if self.api == 'export':
            api_url += '/'
            # note, export api does not accept POST, even though it claims it does
            get_params = '&'.join('%s=%s' % (k,v) for k,v in params.items())
            response = requests.get(api_url + '?' + get_params)            
            return response.content  # raw data to be unpacked
        else:
            headers = {'content-type': 'application/json'}
            post_data = urllib2.quote(json.dumps(params))
            response = requests.post(api_url, data=post_data, headers=headers,
                                     timeout=self.timeout)
            return json.loads(response.content)

    def __getattr__(self, method_name):
        def get(self, *args, **kwargs):
            params = dict((i,j) for (i,j) in enumerate(args))
            params.update(kwargs.items() + self.default_params.items())
            return self.call(method_name, params)
        return get.__get__(self)