import sys
import click
import pathlib

from .commands.ScanCommand import ScanCommand
from .commands.UploadCommand import UploadCommand

@click.group()
@click.version_option()
def start():
    pass


@start.command(cls=ScanCommand)
@click.option('-o', '--output', 'output_path', required=False, type=click.Path(path_type=pathlib.Path), help='Output path for the scan')
@click.argument('path', type=click.Path(exists=True, path_type=pathlib.Path), nargs=-1)
def scan(path, output_path, *args, **kwargs):
    if not (paths := list(path)):
        for line in sys.stdin:
            p = pathlib.Path(line.rstrip('\n'))
            if p.exists():
                paths.append(p)

    scan.run(paths, output_path, *args, **kwargs)


@start.command(cls=UploadCommand)
@click.option('--project-name', 'project_name', type=str, required=True, help='Project name')
@click.option('--base-url', 'base_url', default=UploadCommand.baseUrl, help='TrustSource API base URL')
@click.option('--api-key', 'api_key', type=str, required=True, help='TrustSource API Key')
@click.argument('path', type=click.Path(exists=True, path_type=pathlib.Path))
def upload(project_name: str, base_url: str, api_key: str, path: pathlib.Path, *args, **kwargs):
    upload.run(path, project_name, base_url, api_key, *args, **kwargs)