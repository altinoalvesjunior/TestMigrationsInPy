import bz2
import errno
import filecmp
import logging
import shutil
from collections import OrderedDict
from gzip import GzipFile
from itertools import product
from tempfile import NamedTemporaryFile, mkdtemp
from unittest import mock

import pytest

from airflow.exceptions import AirflowException
from airflow.providers.apache.hive.transfers.s3_to_hive import S3ToHiveOperator

try:
    import boto3
    from moto import mock_s3
except ImportError:
    mock_s3 = None


class TestS3ToHiveTransfer:
    @pytest.mark.skipif(mock is None, reason='mock package not present')
    @pytest.mark.skipif(mock_s3 is None, reason='moto package not present')
    @mock.patch('airflow.providers.apache.hive.transfers.s3_to_hive.HiveCliHook')
    @mock_s3
    def test_execute_with_select_expression(self, mock_hiveclihook):
        conn = boto3.client('s3')
        conn.create_bucket(Bucket='bucket')

        select_expression = "SELECT * FROM S3Object s"
        bucket = 'bucket'

        # Only testing S3ToHiveTransfer calls S3Hook.select_key with
        # the right parameters and its execute method succeeds here,
        # since Moto doesn't support select_object_content as of 1.3.2.
        for (ext, has_header) in product(['.txt', '.gz', '.GZ'], [True, False]):
            input_compressed = ext.lower() != '.txt'
            key = self.s3_key + ext

            self.kwargs['check_headers'] = False
            self.kwargs['headers'] = has_header
            self.kwargs['input_compressed'] = input_compressed
            self.kwargs['select_expression'] = select_expression
            self.kwargs['s3_key'] = f's3://{bucket}/{key}'

            ip_fn = self._get_fn(ext, has_header)

            # Upload the file into the Mocked S3 bucket
            conn.upload_file(ip_fn, bucket, key)

            input_serialization = {'CSV': {'FieldDelimiter': self.delimiter}}
            if input_compressed:
                input_serialization['CompressionType'] = 'GZIP'
            if has_header:
                input_serialization['CSV']['FileHeaderInfo'] = 'USE'

            # Confirm that select_key was called with the right params
            with mock.patch(
                'airflow.providers.amazon.aws.hooks.s3.S3Hook.select_key', return_value=""
            ) as mock_select_key:
                # Execute S3ToHiveTransfer
                s32hive = S3ToHiveOperator(**self.kwargs)
                s32hive.execute(None)

                mock_select_key.assert_called_once_with(
                    bucket_name=bucket,
                    key=key,
                    expression=select_expression,
                    input_serialization=input_serialization,
                )