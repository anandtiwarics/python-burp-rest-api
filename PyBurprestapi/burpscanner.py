#!/usr/bin/env python

__author__ = "Anand Tiwari (http://twitter.com/anandtiwarics)"
__contributors__ = ["Anand Tiwari"]
__status__ = "Production"
__license__ = "MIT"

import requests
import json


class BurpApi(object):
    def __init__(self, host, ):

        self.host = host

    def burp_scope(self, data):
        """
        :return: Add scope in Burp.
        """
        return self._request('GET', '/burp/target/scope?url=%s' % data)

    def burp_scope_add(self, url):
        """
        :param url:
        :return: Add target to Scope
        """
        return self._request('PUT', '/burp/target/scope?url=%s' % url)

    def burp_out_of_scope(self, url):
        """
        Excludes the specified Url from the Suite-wide scope.
        :param url:
        :return:
        """
        return self._request('DELETE', '/burp/target/scope?url=%s' % url)

    def burp_spider(self, data):
        """
        :param data:
        :return: Add target to Spider
        """

        return self._request('POST', '/burp/spider?baseUrl=%s' % data)

    def burp_configuration(self):
        """

        :param data:
        :return: Get the configuration of Burp
        """

        return self._request('GET', '/burp/configuration')

    def burp_configuration_add(self, data):
        """

        :param data: Example: {} #JSON format
        :return: Add Burp Configuration
        """
        return self._request('PUT', '/burp/configuration', data=data)

    def burp_proxy_history(self):
        """

        :return: Returns details of items in Burp Suite Proxy history.
        """
        return self._request('GET', '/burp/proxy/history')

    def scan_report(self, url, reportType):
        """

        :param url: URL prefix in order to extract and include a specific subset of scan issues in the report.
        :param reportType: Format to be used to generate report. Acceptable values are HTML and XML.
        :return: Returns Scan report
        """
        return self._request('GET', '/burp/report?urlPrefix=' + url + '&reportType=' + reportType)

    def burp_reset(self):
        """
        This will restore Burp state with an empty one.
        :return: Clean Burp state
        """
        return self._request('GET', '/burp/reset')

    def burp_issue(self, url):
        """
        Returns all of the current scan issues for URLs matching the specified urlPrefix. Performs a simple
        case-sensitive text match, returning all scan issues whose URL begins with the given urlPrefix. Returns
        all issues if urlPrefix is null.
        :param url: URL prefix in order to extract a specific subset of scan issues.
        :return: Get the current scan issues
        """
        return self._request('GET', '/burp/scanner/issues?urlPrefix=%s' % url)

    def burp_active_scan(self, url):
        """
        Scans through Burp Sitemap and sends all HTTP requests with url starting with baseUrl to Burp Scanner
        for active scan.
        :param url: Base Url to submit for Active scan.
        :return:
        """
        return self._request('POST', '/burp/scanner/scans/active?baseUrl=%s' % url)

    def burp_active_delete(self, ):
        """
        Deletes the scan queue map from memory, not from Burp suite UI.
        :return:
        """
        return self._request('DELETE', '/burp/scanner/scans/active')

    def burp_scan_status(self, ):
        """
        Returns an aggregate of percentage completed for all the scan queue items.
        :return:
        """
        return self._request('GET', '/burp/scanner/status')

    def burp_stop(self):
        """
        This will exit Burp Suite. Use with caution: the API will not work after this endpoint has been called.
        You have to restart Burp from command-line to re-enable te API.
        :return:
        """
        return self._request('GET', '/burp/stop')

    def burp_sitemap(self, url):
        """
        Returns details of items in the Burp suite Site map. urlPrefix parameter can be used to
        specify a URL prefix, in order to extract a specific subset of the site map.
        :return:
        """
        return self._request('GET', '/burp/target/sitemap?urlPrefix=%s' % url)

    def _request(self, method, url, params=None, headers=None, data=None):
        """Common handler for all the HTTP requests."""
        if not params:
            params = {}

        # set default headers
        if not headers:
            headers = {
                'accept': '*/*'
            }
            if method == 'POST' or method == 'PUT':
                headers.update({'Content-Type': 'application/json'})
        try:
            response = requests.request(method=method, url=self.host + url, params=params,
                                        headers=headers, data=data)

            try:
                response.raise_for_status()

                response_code = response.status_code
                success = True if response_code // 100 == 2 else False
                if response.text:
                    try:
                        data = response.json()
                    except ValueError:
                        data = response.content
                else:
                    data = ''

                return BurpResponse(success=success, response_code=response_code, data=data)
            except ValueError as e:
                return BurpResponse(success=False, message="JSON response could not be decoded {}.".format(e))
            except requests.exceptions.HTTPError as e:
                if response.status_code == 400:
                    return BurpResponse(success=False, response_code=400, message='Bad Request')
                else:
                    return BurpResponse(
                        message='There was an error while handling the request. {}'.format(response.content),
                        success=False)
        except Exception as e:
            return BurpResponse(success=False, message='Eerror is %s' % e)


class BurpResponse(object):
    """Container for all Burp REST API response, even errors."""

    def __init__(self, success, message='OK', response_code=-1, data=None):
        self.message = message
        self.success = success
        self.response_code = response_code
        self.data = data

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return self.message

    def data_json(self, pintu=False):
        """Returns the data as a valid JSON String."""
        if pintu:
            return json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self.data)
