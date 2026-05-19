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


def test__run_docker_compose__executes_with_env_vars(mocker):
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.returncode = 0

    sut.run_docker_compose("/agent", "/result", "python:3.11-slim", "Do the task")

    mock_run.assert_called_once()
    call_args = mock_run.call_args
    assert ["docker", "compose", "up"] == call_args[0][0]
    assert "/agent/docker" == call_args[1]["cwd"]
    assert "python:3.11-slim" == call_args[1]["env"]["IMAGE_NAME"]
    assert "/workspace" == call_args[1]["env"]["WORKING_DIR"]
    assert "/result" == call_args[1]["env"]["ABSOLUTE_RESULT_DIR"]
    assert "Do the task" == call_args[1]["env"]["TASK_PROMPT"]


def test__run_docker_compose_down__executes_in_docker_dir(mocker):
    mock_run = mocker.patch("subprocess.run")

    sut.run_docker_compose_down("/agent", "/result", "python:3.11-slim")

    mock_run.assert_called_once()
    call_args = mock_run.call_args
    assert ["docker", "compose", "down"] == call_args[0][0]
    assert "/agent/docker" == call_args[1]["cwd"]
    assert "python:3.11-slim" == call_args[1]["env"]["IMAGE_NAME"]
    assert "/workspace" == call_args[1]["env"]["WORKING_DIR"]
    assert "/result" == call_args[1]["env"]["ABSOLUTE_RESULT_DIR"]
