import os
import sys
import getopt
import json
import requests


class TSClient:
    def usage(self):
        print('usage: {} <project folder>'.format(self._tool_name))

    def __init__(self, tool_name, Scanner):
        self._tool_name = tool_name
        self._scan_path = os.getcwd()
        
        self._userName = ''
        self._apiKey = ''
        self._projectName = ''
        self._skipTransfer = False
        self._baseUrl = 'https://app.trustsource.io'
        self._scanner = Scanner(self)

    @property
    def projectName(self):
        return self._projectName

    @property
    def scanPath(self):
        return self._scan_path

    def run(self, args):
        try:
            opts, args = getopt.getopt(args, '', [])
        except getopt.GetoptError:
            self.usage()
            sys.exit(2)

        if len(args) > 1:
            self.usage()
            exit(2)
        elif len(args) == 1:
            self._scan_path = args[0]

        if not os.path.isdir(self._scan_path):
            print('\'' + self._scan_path + '\'' + ' is not a folder')
            self.usage()
            exit(2)

        # Do the actual scan
        scanInfo = self._scanner.run()

        settings_path = os.path.join(self._scan_path, 'ts-plugin.json')
        if not os.path.exists(settings_path) or not os.path.isfile(settings_path):
            print(json.dumps(scanInfo, indent=2))
            return

        settings = {}
        with open(settings_path) as settings_file:
            try:
                settings = json.load(settings_file)
            except Exception as err:
                print('Cannot read \'ts-plugin.json\'')
                print(err)
                exit(2)

        self._baseUrl = settings.get('baseUrl', 'https://app.trustsource.io')
        self._skipTransfer = settings.get('skipTransfer', False)
        self._projectName = settings.get('project', '')
        self._userName = settings.get('userName', '')
        self._apiKey = settings.get('apiKey', '')

        if self._apiKey == '':
            credentials_path = settings.get('credentials', None)
            if credentials_path is not None:
                try:
                    with open(os.path.join(self._scan_path, credentials_path)) as credentials_file:
                        credentials = json.load(credentials_file)
                        # self._userName = credentials.get('userName', ''), removed by jTh 02/2020
                        self._apiKey = credentials.get('apiKey', '')
                except Exception as err:
                    print(err)

        if not self._skipTransfer:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': '%/1.0.0'.format(self._tool_name),
                # 'X-USER': self._userName, removed by jTh 02/2020
                'X-APIKEY': self._apiKey
            }

            response = requests.post(self._baseUrl + '/api/v1/scans', json=scanInfo, headers=headers)

            if response.status_code == 201:
                print("Transfer success!")
                return
            else:
                print(json.dumps(response.content, indent=2))
                exit(2)
        else:
            print(json.dumps(scanInfo, indent=2))