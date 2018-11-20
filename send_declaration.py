#!/usr/bin/env python

import json
import os
import sys

import requests
import yaml


class ApiWrapper(object):
    def __init__(self, api_url=None, api_username=None, api_password=None):
        if not api_url or not api_username or not api_password:
            raise ValueError("Please provide API url, username and password")
        else:
            self.api_url = api_url
            self.api_username = api_username
            self.api_password = api_password

    def post(self, endpoint, payload):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        response = requests.post('{}{}'.format(self.api_url, endpoint),
                                 auth=(self.api_username, self.api_password),
                                 headers=headers, data=payload, verify=False)

        response.raise_for_status()

        return response


class F5Handler(object):
    def __init__(self, f5_address=None, api_username=None, api_password=None):
        if not f5_address or not api_username or not api_password:
            raise ValueError(
                "Please provide API address, username and password")
        else:
            self.api_wrapper = ApiWrapper(api_url=f5_address,
                                          api_username=api_username,
                                          api_password=api_password)

    def send_declaration(self, payload):
        endpoint = 'mgmt/shared/appsvcs/declare'

        self.api_wrapper.post(endpoint, json.dumps(payload))


def main():
    ###
    #   Initialize F5 Handler
    ###
    f5_device = F5Handler(
        f5_address='https://{}:8443/'.format(os.environ.get('IPADDR')),
        api_username='admin',
        api_password=os.environ.get('PASSWORD'))

    ###
    #   Read declared configuration
    ###
    with open('declaration.yml') as yml:
        declaration_data = yaml.load(yml)

    ###
    #   Switch to dry-run mode if needed
    ###
    if int(os.environ.get('DRYRUN', 0)) == 1:
        declaration_data['action'] = 'dry-run'

    ###
    #   Send the declaration
    ###
    f5_device.send_declaration(declaration_data)


if __name__ == '__main__':
    sys.exit(main())
