import pytest
import execute as sut


def test__run_init_sh__executes_with_env_var(fs, mocker):
    fs.create_file("/agent/init.sh", contents="#!/bin/bash\nexit 0")
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0

    result = sut.run_init_sh("/agent", "/result")

    assert 0 == result
    mock_run.assert_called_once()
    call_args = mock_run.call_args
    assert ["./init.sh"] == call_args[0][0]
    assert "/agent" == call_args[1]["cwd"]
    assert "/result" == call_args[1]["env"]["ABSOLUTE_RESULT_DIR"]
