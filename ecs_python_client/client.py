import os, sys, getopt, json, requests

class ECSClient:
    def usage(self):
        print 'usage: {} <project folder>'.format(self._tool_name)

    def __init__(self, tool_name, Scanner):
        self._tool_name = tool_name
        self._scan_path = os.getcwd()

        self._userName = ''
        self._apiKey = ''
        self._projectName = ''
        self._skipTransfer = False

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

        settings_path = os.path.join(self._scan_path, 'ecs-plugin.json')
        if not os.path.exists(settings_path) or not os.path.isfile(settings_path):
            print('Cannot find project settings \'ecs-plugin.json\' in \'' + settings_path + '\'')
            exit(2)

        settings = {}
        with open(settings_path) as settings_file:
            try:
                settings = json.load(settings_file)
            except Exception as err:
                print('Cannot read \'ecs-plugin.json\'')
                if err.message != '':
                    print(err.message)
                exit(2)

        self._skipTransfer = settings.get('skipTransfer', False)
        self._projectName = settings.get('project', '')
        self._userName = settings.get('userName', '')
        self._apiKey = settings.get('apiKey', '')

        if (self._userName == '') and (self._apiKey == ''):
            credentials_path = settings.get('credentials', None)
            if credentials_path is not None:
                try:
                    with open(os.path.join(self._scan_path, credentials_path)) as credentials_file:
                        credentials = json.load(credentials_file)
                        self._userName = credentials.get('userName', '')
                        self._apiKey = credentials.get('apiKey', '')
                except Exception as err:
                    if err.message != '':
                        print(err.message)

        scanInfo = self._scanner.run()

        if not self._skipTransfer:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': '%/0.1.0'.format(self._tool_name),
                'X-USER': self._userName,
                'X-APIKEY': self._apiKey
            }

            response = requests.post('https://ecs-app.eacg.de/api/v1/scans', json=scanInfo, headers=headers)

            if response.status_code == 201:
                exit(0)
            else:
                print(json.dumps(response.content, indent=2))
                exit(2)
        else:
            print(json.dumps(scanInfo, indent=2))