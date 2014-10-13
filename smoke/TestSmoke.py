#!/usr/local/bin/python

import unittest
import urllib2
import json
import datetime
from urllib import urlencode

class TestSmoke(unittest.TestCase):

    def _request_TV_API(self, url_to_request):
        response = urllib2.urlopen(url_to_request)
        self.assertTrue(response.getcode() == 200, url_to_request + ' status code ' + str(response.getcode()))
        return json.loads(response.read())


    def test_integration_all_platform(self):
        tv_api_base_url = 'http://localhost:9000'
        tv_api_providers = tv_api_base_url + '/providers/channels'
        tv_api_providers_json = self._request_TV_API(tv_api_providers)

        for provider in tv_api_providers_json:
            if provider['provider'] == 'UNKOWN':
                continue

            print "provider: " + provider['provider']
            provider_encoded = urllib2.quote((str(provider['provider']).encode("utf8")))
            channels_by_provider_url = tv_api_base_url + '/channels/provider/' + provider_encoded
            channels_by_provider_json = self._request_TV_API(channels_by_provider_url.encode())
            for channel_json in channels_by_provider_json:
                if 'UNKNOWN' in channel_json['provider']:
                    print channel_json['name'] + ' DISCARDED becuase provider UNKNOWN'
                    continue
                content_channel_url_today = tv_api_base_url + channel_json['uriToday']
                json_tv_content_today = self._request_TV_API(content_channel_url_today.encode())
                # for json_tv_content in json_tv_content_today:
                    # start_datetime = datetime.strstrptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
                    # end_datetime = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')



if __name__ == '__main__':
    unittest.main()