from pathlib import Path
import boto3
import click
import sys

s3 = boto3.client('s3')

@click.command('upload')
@click.option('--path-prefix', default=Path(__file__).parent)
@click.argument('path')
def upload(path_prefix, path):
    absolute_path = Path(path).expanduser().resolve()

    print(f'Preparing {absolute_path} for upload')

    absolute_prefix_path = Path(path_prefix).expanduser().resolve()

    relative_path = absolute_path.relative_to(absolute_prefix_path)

    bucket_name = relative_path.parts[0]
    upload_path = Path(*relative_path.parts[1:])

    ack_path = absolute_path.with_suffix('.ACK')

    assert absolute_path.exists(), f'{absolute_path} not found'
    assert not ack_path.exists(), f'{ack_path} found. Aborting upload.'
    print(f'Uploading s3://{bucket_name}/{upload_path}')

    with absolute_path.open('rb') as f:
        response = s3.put_object(
            Body=f,
            Bucket=bucket_name,
            Key=str(upload_path),
        )
        ack_path.touch()
        absolute_path.unlink()



if __name__ == '__main__':
    upload()
