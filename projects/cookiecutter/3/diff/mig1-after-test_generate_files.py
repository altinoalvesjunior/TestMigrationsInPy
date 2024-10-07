from __future__ import unicode_literals
import os
import io
import pytest

from cookiecutter import generate
from cookiecutter import exceptions
from cookiecutter import utils


@pytest.fixture(scope="function")
def clean_system_remove_additional_folders(request, clean_system):
    """
    Use the global clean_system fixture and run additional teardown code to
    remove some special folders.
    For a better understanding - order of fixture calls:
    clean_system setup code
    clean_system_remove_additional_folders setup code
    clean_system_remove_additional_folders teardown code
    clean_system teardown code
    """
    def remove_additional_folders():
        if os.path.exists('inputpizzä'):
            utils.rmtree('inputpizzä')
        if os.path.exists('inputgreen'):
            utils.rmtree('inputgreen')
        if os.path.exists('inputbinary_files'):
            utils.rmtree('inputbinary_files')
        if os.path.exists('tests/custom_output_dir'):
            utils.rmtree('tests/custom_output_dir')
        if os.path.exists('inputpermissions'):
            utils.rmtree('inputpermissions')
    request.addfinalizer(remove_additional_folders)
    
    @pytest.mark.usefixtures("clean_system_remove_additional_folders")
    def test_generate_files_permissions():
        """
        simple.txt and script.sh should retain their respective 0o644 and
        0o755 permissions
        """
        generate.generate_files(
            context={
                'cookiecutter': {'permissions': 'permissions'}
            },
            repo_dir='tests/test-generate-files-permissions'
        )
        assert os.path.isfile('inputpermissions/simple.txt')
        # simple.txt should still be 0o644
        assert os.stat('tests/test-generate-files-permissions/input{{cookiecutter.permissions}}/simple.txt').st_mode & 0o777 == os.stat('inputpermissions/simple.txt').st_mode & 0o777
        assert os.path.isfile('inputpermissions/script.sh')
        # script.sh should still be 0o755
        assert os.stat('tests/test-generate-files-permissions/input{{cookiecutter.permissions}}/script.sh').st_mode & 0o777 == os.stat('inputpermissions/script.sh').st_mode & 0o777