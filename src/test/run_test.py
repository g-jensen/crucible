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
