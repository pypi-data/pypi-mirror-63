""" Zooper API.

API to unleash data into insights at lightning speed.
"""
import json
import logging
import requests
import http.client
import uuid
import os
import time
import hashlib
from pathlib import Path

from tabulate import tabulate
from urllib.parse import urlencode
from IPython.core.display import display, HTML
from IPython.display import IFrame, Image
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

class Indeks:
    """ Updatable and queryable index. """

    API_ID = "prod_query_api"

    def __init__(self, project_id, account_id='ecommerce', access_creds=None, host='100.24.23.205', port=5000, tag=None):
        self._host = host
        self._port = port
        self._account_id = account_id
        self._project_id = project_id
        self._tag = tag
        self._query_selector = None
        self._query_config = None
        self._access_creds = access_creds
        if self._access_creds is None:
            creds_file = str(Path.home()) + "/.zooper_creds.json"
            if not os.path.exists(creds_file):
                raise ValueError('Unable to find credentials file in the credential store.')
            with open(creds_file, 'r') as f:
                self._access_creds = json.load(f)

        self._token = None

    def query(self, selector, tag=None, config=None):
        """ Query API.

        Perform SQL-like queries against the index.
        """
        self._tag = tag if tag else self._tag
        self._query_selector = selector
        self._query_config = config
        return self

    def plot(self, chart_type="table", format="html", config={}):
        """ Plot API.

        Convert non-visual information into visual insights.
        """

        self.ensure_token()

        # TODO: switch to TLS
        url = "http://{}:{}/api/query/query".format(self._host, self._port)
        params = {
            'account_name': self._account_id,
            'project_name': self._project_id,
            'tag': self._tag,
            'query_text': self._query_selector,
            'plot_type': chart_type,
            'plot_format': format,
            'plot_config': urlencode(config)
        }
        headers = { 'authorization': "Bearer {}".format(self._token.get('access_token')) }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != requests.codes.ok:
            print("Error: {}".format(response.json().get("message")))
            return

        result = response.json().get("result")
        if format == "html":
            if chart_type == "table":
                display(HTML(result))
            else:
                chart_file = "chart_{}.html".format(uuid.uuid4())
                os.makedirs("plots", exist_ok=True)
                with open("plots/" + chart_file, 'w+') as f:
                    f.write(result)
                display(IFrame("plots/" + chart_file, '100%', '600px'))
        elif format == "json":
            return json.loads(result)
        else:
            return result
        return self

    def get_versions(self, tag=None, last_n=None):
        """ Get available index versions.
        """

        raise ValueError("Not yet implemented")

    def __repr__(self):
        return ''

    def ensure_token(self):
        now = time.time()
        if self._token == None:
            # Try to load an existing token from cache
            try:
                with open(self.get_token_cache_file(), 'r') as f:
                    self._token = json.loads(f.read())
            except:
                pass

        if self._token and 'expires_at' in self._token and int(self._token.get('expires_at')) > int(now):
            # Token is still good
            return

        self._token = None
        client = BackendApplicationClient(client_id=self._access_creds.get('key'))
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url='https://dev-q0m6ske4.auth0.com/oauth/token',
                                  client_id=self._access_creds.get('key'),
                                  client_secret=self._access_creds.get('secret_key'),
                                  audience=self.API_ID)

        os.makedirs("{}/.zooper_auth".format(str(Path.home())), exist_ok=True)
        with open(self.get_token_cache_file(), 'w+') as f:
            f.write(json.dumps(token))

        self._token = token

    def get_token_cache_file(self):
        creds = "{}{}".format(self._access_creds.get('key'), self._access_creds.get('secret_key'))
        creds_hash = hashlib.sha256(creds.encode('utf-8')).hexdigest()
        return "{}/.zooper_auth/{}_{}.json".format(str(Path.home()), self._account_id, creds_hash)
