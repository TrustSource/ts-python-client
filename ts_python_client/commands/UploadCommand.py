import enum
import json
import requests
import click

from pathlib import Path
from typing import Callable, Optional

from . import Command


class UploadCommand(Command):
    # Impl = Callable[[dict, ...], None]

    baseUrl = 'https://app.trustsource.io'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__impl = None
        self.__preprocess = None

        self.tool_name = 'ts-python-client'
        self.tool_version = '2.0.0'

    def impl(self, impl) -> 'UploadCommand':
        self.__impl = impl
        return self

    # def override(self, impl) -> 'UploadCommand':
    #     self.__impl = impl
    #     self.params = [p for p in self.params if not isinstance(p, click.Option)]
    #     return self

    def run(self, path: Path, project_name: str, base_url: str, api_key: str, *args, **kwargs):
        with path.open('r') as fp:
            if data := json.load(fp):
                data['project'] = project_name
            else:
                print("Cannot load scan data")
                exit(2)

        if impl := self.__impl:
            impl(data, base_url, api_key, *args, **kwargs)
        else:
            self.default(data, base_url, api_key)


    def default(self, data: dict, base_url: str, api_key: str, *args, **kwargs):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': f'{self.tool_name}/{self.tool_version}',
            'X-APIKEY': api_key
        }

        response = requests.post(base_url + '/api/v1/scans', json=data, headers=headers)

        if response.status_code == 201:
            print("Transfer success!")
            return
        else:
            print(json.dumps(response.text, indent=2))
            exit(2)
