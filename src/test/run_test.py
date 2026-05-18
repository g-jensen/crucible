import os
import re
import run as sut


def test__create_run_dir__creates_directory_with_timestamp(fs):
    fs.create_dir("/results")

    result = sut.create_run_dir("/results", "example_task")

    files = os.listdir("/results")
    assert 1 == len(files)

    dir_name = files[0]
    pattern = r"example_task_\d{14}_[a-z0-9]{4,8}"
    assert re.match(pattern, dir_name)
    assert f"/results/{dir_name}" == result


def test__copy_seed_to_workspace__copies_files_recursively(fs):
    fs.create_file("/seed/test.txt", contents="hello")
    fs.create_file("/seed/subdir/nested.txt", contents="world")
    fs.create_dir("/run/workspace")

    sut.copy_seed_to_workspace("/seed", "/run/workspace")

    assert os.path.exists("/run/workspace/test.txt")
    assert "hello" == open("/run/workspace/test.txt").read()
    assert os.path.exists("/run/workspace/subdir/nested.txt")
    assert "world" == open("/run/workspace/subdir/nested.txt").read()
