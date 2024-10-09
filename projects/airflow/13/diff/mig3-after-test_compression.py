import bz2
import errno
import filecmp
import gzip
import shutil
import tempfile

import pytest

from airflow.utils import compression


class TestCompression:
    @pytest.fixture(autouse=True)
    def setup_attrs(self):
        self.file_names = {}
        header = b"Sno\tSome,Text \n"
        line1 = b"1\tAirflow Test\n"
        line2 = b"2\tCompressionUtil\n"
        self.tmp_dir = tempfile.mkdtemp(prefix='test_utils_compression_')
        # create sample txt, gz and bz2 files
        with tempfile.NamedTemporaryFile(mode='wb+', dir=self.tmp_dir, delete=False) as f_txt:
            self._set_fn(f_txt.name, '.txt')
            f_txt.writelines([header, line1, line2])

        fn_gz = self._get_fn('.txt') + ".gz"
        with gzip.GzipFile(filename=fn_gz, mode="wb") as f_gz:
            self._set_fn(fn_gz, '.gz')
            f_gz.writelines([header, line1, line2])

        fn_bz2 = self._get_fn('.txt') + '.bz2'
        with bz2.BZ2File(filename=fn_bz2, mode="wb") as f_bz2:
            self._set_fn(fn_bz2, '.bz2')
            f_bz2.writelines([header, line1, line2])

        yield

        try:
            shutil.rmtree(self.tmp_dir)
        except OSError as e:
            # ENOENT - no such file or directory
            if e.errno != errno.ENOENT:
                raise e