import bz2
import errno
import filecmp
import logging
import shutil
import unittest
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


class TestS3ToHiveTransfer(unittest.TestCase):
    def setUp(self):
        self.file_names = {}
        self.task_id = 'S3ToHiveTransferTest'
        self.s3_key = 'S32hive_test_file'
        self.field_dict = OrderedDict([('Sno', 'BIGINT'), ('Some,Text', 'STRING')])
        self.hive_table = 'S32hive_test_table'
        self.delimiter = '\t'
        self.create = True
        self.recreate = True
        self.partition = {'ds': 'STRING'}
        self.headers = True
        self.check_headers = True
        self.wildcard_match = False
        self.input_compressed = False
        self.kwargs = {
            'task_id': self.task_id,
            's3_key': self.s3_key,
            'field_dict': self.field_dict,
            'hive_table': self.hive_table,
            'delimiter': self.delimiter,
            'create': self.create,
            'recreate': self.recreate,
            'partition': self.partition,
            'headers': self.headers,
            'check_headers': self.check_headers,
            'wildcard_match': self.wildcard_match,
            'input_compressed': self.input_compressed,
        }
        try:
            header = b"Sno\tSome,Text \n"
            line1 = b"1\tAirflow Test\n"
            line2 = b"2\tS32HiveTransfer\n"
            self.tmp_dir = mkdtemp(prefix='test_tmps32hive_')
            # create sample txt, gz and bz2 with and without headers
            with NamedTemporaryFile(mode='wb+', dir=self.tmp_dir, delete=False) as f_txt_h:
                self._set_fn(f_txt_h.name, '.txt', True)
                f_txt_h.writelines([header, line1, line2])
            fn_gz = self._get_fn('.txt', True) + ".gz"
            with GzipFile(filename=fn_gz, mode="wb") as f_gz_h:
                self._set_fn(fn_gz, '.gz', True)
                f_gz_h.writelines([header, line1, line2])
            fn_gz_upper = self._get_fn('.txt', True) + ".GZ"
            with GzipFile(filename=fn_gz_upper, mode="wb") as f_gz_upper_h:
                self._set_fn(fn_gz_upper, '.GZ', True)
                f_gz_upper_h.writelines([header, line1, line2])
            fn_bz2 = self._get_fn('.txt', True) + '.bz2'
            with bz2.BZ2File(filename=fn_bz2, mode="wb") as f_bz2_h:
                self._set_fn(fn_bz2, '.bz2', True)
                f_bz2_h.writelines([header, line1, line2])
            # create sample txt, bz and bz2 without header
            with NamedTemporaryFile(mode='wb+', dir=self.tmp_dir, delete=False) as f_txt_nh:
                self._set_fn(f_txt_nh.name, '.txt', False)
                f_txt_nh.writelines([line1, line2])
            fn_gz = self._get_fn('.txt', False) + ".gz"
            with GzipFile(filename=fn_gz, mode="wb") as f_gz_nh:
                self._set_fn(fn_gz, '.gz', False)
                f_gz_nh.writelines([line1, line2])
            fn_gz_upper = self._get_fn('.txt', False) + ".GZ"
            with GzipFile(filename=fn_gz_upper, mode="wb") as f_gz_upper_nh:
                self._set_fn(fn_gz_upper, '.GZ', False)
                f_gz_upper_nh.writelines([line1, line2])
            fn_bz2 = self._get_fn('.txt', False) + '.bz2'
            with bz2.BZ2File(filename=fn_bz2, mode="wb") as f_bz2_nh:
                self._set_fn(fn_bz2, '.bz2', False)
                f_bz2_nh.writelines([line1, line2])
        # Base Exception so it catches Keyboard Interrupt
        except BaseException as e:
            logging.error(e)
            self.tearDown()

    def tearDown(self):
        try:
            shutil.rmtree(self.tmp_dir)
        except OSError as e:
            # ENOENT - no such file or directory
            if e.errno != errno.ENOENT:
                raise e