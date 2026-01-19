import boto3
from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def list_files(self, prefix=""):
        """Lists files and 'folders' (common prefixes) in S3."""
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, Delimiter='/')
        files = response.get('Contents', [])
        folders = response.get('CommonPrefixes', [])
        return files, folders

    def upload_file(self, file_obj, filename):
        self.s3.upload_fileobj(file_obj, self.bucket_name, filename)

    def delete_object(self, key):
        self.s3.delete_object(Bucket=self.bucket_name, Key=key)

    def copy_move_file(self, source_key, dest_key, delete_source=False):
        copy_source = {'Bucket': self.bucket_name, 'Key': source_key}
        self.s3.copy(copy_source, self.bucket_name, dest_key)
        if delete_source:
            self.s3.delete_object(Bucket=self.bucket_name, Key=source_key)

    def create_folder(self, folder_name):
        if not folder_name.endswith('/'):
            folder_name += '/'
        self.s3.put_object(Bucket=self.bucket_name, Key=folder_name)