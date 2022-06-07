# SPDX-FileCopyrightText: 2020 EACG GmbH
#
# SPDX-License-Identifier: Apache-2.0

import sys
import getopt
import json
import requests

from pathlib import Path
from .scan import Scan

class Scanner(object):
    def __init__(self):
        self._client = None

    @property
    def client(self) -> 'Client':
        return self._client

    @client.setter
    def client(self, value: 'Client'):
        self._client = value

    @property
    def is_folder_scanner(self):
        return True

    def run(self) -> Scan:
        raise NotImplemented()



class Client(object):
    class Settings:
        def __init__(self):
            self.apiKey = ''
            self.projectName = ''
            self.baseUrl = 'https://app.trustsource.io'
            self.skipTransfer = False
            self.data = {}


        def load(self, path: Path):
            if not path.exists():
                return

            try:
                with path.open('r') as fp:
                    self.data = json.load(fp)
            except Exception as err:
                print('Error loading settings file: {}'.format(err))

            self.apiKey = self.data.get('apiKey', self.apiKey)
            self.projectName = self.data.get('project', self.projectName)
            self.baseUrl = self.data.get('baseUrl', self.baseUrl)
            self.skipTransfer = self.data.get('skipTransfer', self.skipTransfer)

            if not self.apiKey:
                credentials = self.data.get('credentials', '')
                if credentials:
                    credentials_path = path / credentials
                    if credentials_path.exists() and credentials_path.is_file():
                        try:
                            with credentials_path.open() as fp:
                                credentials = json.load(fp)
                                self.apiKey = credentials.get('apiKey', self.apiKey)

                        except Exception as err:
                            print('Error loading credentials: {}'.format(err))

    ##############

    def __init__(self, tool_name: str, scanner: Scanner):
        self._path = Path.cwd()
        self._tool_name = tool_name
        self._settings = Client.Settings()

        self._scanner = scanner
        self._scanner.client = self


    @property
    def path(self) -> Path:
        return self._path

    @property
    def settings(self):
        return self._settings


    def run(self, path: str = '', baseUrl='', apiKey = '', projectName = '', skipTransfer = True, settingsFile = '', outputFile = ''):
        if path:
            self._path = Path(path)

        if settingsFile:
            self._settings.load(Path(settingsFile))
        elif self._scanner.is_folder_scanner and self._path.is_dir():
            self._settings.load(self._path / 'ts-plugin.json')

        if baseUrl:
            self._settings.baseUrl = baseUrl

        if apiKey:
            self._settings.apiKey = apiKey

        if projectName:
            self._settings.projectName = projectName

        if skipTransfer:
            self._settings.skipTransfer = skipTransfer


        # Do the actual scan
        scan = None

        try:
            scan = self._scanner.run()
        except ValueError as err:
            print(err)
            exit(2)

        if not scan:
            exit(2)

        scan.project = self._settings.projectName

        # Submit scan info
        if not self._settings.skipTransfer:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': '{}/1.0.0'.format(self._tool_name),
                'X-APIKEY': self._settings.apiKey
            }

            response = requests.post(self._settings.baseUrl + '/api/v1/scans', data=scan.json, headers=headers)

            if response.status_code == 201:
                print("Transfer success!")
                return
            else:
                print(json.dumps(response.text, indent=2))
                exit(2)
        elif outputFile:
            output = Path(outputFile)
            with output.open('w') as fp:
                fp.write(scan.json)
        else:
            print(scan.json)