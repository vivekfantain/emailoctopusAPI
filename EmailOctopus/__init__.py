_version_ = '1.4'

import requests
from requests.exceptions import ConnectionError
from exception import EODown
import pprint


class client(object):
    API_HOST = 'https://emailoctopus.com'
    API_URL_BASE = 'api/1.4'

    def __init__(self, api_key):
        if api_key:
            self.api_key = api_key
            self.valid_api_key = True  # Assume it will work

    def make_api_url(self, endpoint):
        return self.API_HOST + '/' + self.API_URL_BASE + '/' + endpoint

    def make_host_url(self, endpoint):
        return self.API_HOST + endpoint

    def full_api_params(self, params):
        params.update({'api_key': self.api_key})
        return params

    def call_api(self, url, params):
        try:
            r = requests.get(url, params=params)
            if r.status_code == requests.codes.ok:
                return r.json()
            r.raise_for_status()

        except ConnectionError:
            # email octopus is down
            raise EODown()

    def iter_email_octopus_api(self, url, params=None):
        if params is None:
            params = self.full_api_params({})
        fetch_more = True
        while fetch_more:
            resp = self.call_api(url, params)
            for item in resp['data']:
                yield item
            if 'paging' in resp.keys():
                if 'next' in resp['paging'] and resp['paging']['next']:
                    url = self.make_host_url(resp['paging']['next'])
                    params = {}
                    fetch_more = True
                else:
                    fetch_more = False


class Lists(client):
    def iter_all(self):
        URL_ENDPOINT = 'lists'
        resp = []

        url = self.make_api_url(URL_ENDPOINT)
        params = self.full_api_params({'page': 1, 'limit': 100})

        for item in self.iter_email_octopus_api(url, params):
            yield item

    def get_all(self):
        resp = []

        for item in self.iter_all_lists():
            resp.append(item)

        return resp

    def iter_unsubscribed(self, alist):
        endpoint = 'lists/{0}/contacts/unsubscribed'.format(alist)
        url = self.make_api_url(endpoint)
        for item in self.iter_email_octopus_api(url):
            yield item


class Campaigns(client):
    def iter_all(self):
        URL_ENDPOINT = 'campaigns'
        resp = []

        url = self.make_api_url(URL_ENDPOINT)
        params = self.full_api_params({'page': 1, 'limit': 100})

        for item in self.iter_email_octopus_api(url, params):
            yield item

    def iter_campaign(self, endpoint, acampaign):
        endpoint = endpoint.format(acampaign)
        url = self.make_api_url(endpoint)
        for item in self.iter_email_octopus_api(url):
            yield item

    def iter_bounced(self, acampaign):
        return self.iter_campaign('campaigns/{0}/reports/bounced', acampaign)

    def iter_unsubscribed(self, acampaign):
        return self.iter_campaign('campaigns/{0}/reports/unsubscribed',
                                  acampaign)

    def iter_complained(self, acampaign):
        return self.iter_campaign('campaigns/{0}/reports/complained',
                                  acampaign)

    def iter_opened(self, acampaign):
        return self.iter_campaign('campaigns/{0}/reports/opened', acampaign)

    def iter_sent(self, acampaign):
        return self.iter_campaign('campaigns/{0}/reports/sent', acampaign)
