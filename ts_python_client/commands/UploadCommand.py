import json
import requests

from pathlib import Path
from click import Command

class UploadCommand(Command):
    baseUrl = 'https://api.trustsource.io/v2'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__impl = None
        self.__preprocess = None

        self.tool_name = 'ts-python-client'
        self.tool_version = '2.0.5'

    # Type hint not used due to issues with earlier Python versions
    # Impl = Callable[[Union[List[dict], dict], ...], None]
    def impl(self, impl) -> 'UploadCommand':
        """
        :param impl: Callable[[Union[List[dict], dict], ...], None]
        :return: self
        """
        self.__impl = impl
        return self

    # def override(self, impl) -> 'UploadCommand':
    #     self.__impl = impl
    #     self.params = [p for p in self.params if not isinstance(p, click.Option)]
    #     return self

    def run(self, path: Path, project_name: str, base_url: str, api_key: str, *args, **kwargs):
        if self.__impl:
            impl = lambda _d: self.__impl(_d, base_url, api_key, *args, **kwargs)
        else:
            impl = lambda _d: self.default(_d, base_url, api_key)

        with path.open('r') as fp:
            if data := json.load(fp):
                if type(data) is list:
                    for d in data:
                        d['project'] = project_name
                        impl(d)
                elif type(data) is dict:
                    data['project'] = project_name
                    impl(data)
                else:
                    raise ValueError('Unexpected scan type')
            else:
                print("Cannot load scan data")
                exit(2)


    def default(self, data: dict, base_url: str, api_key: str, *args, **kwargs):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': f'{self.tool_name}/{self.tool_version}',
            'x-api-key': api_key
        }

        response = requests.post(base_url + '/core/scans', json=data, headers=headers)

        if response.status_code == 201:
            print("Transfer success!")
            return
        else:
            print(json.dumps(response.text, indent=2))
            exit(2)
