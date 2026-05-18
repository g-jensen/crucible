from unittest.mock import MagicMock
import crucible as sut


def test__run__orchestrates_full_flow(fs, mocker):
    fs.create_file(
        "/tasks/task.yml",
        contents="id: test_task\ndocker_image: python:3.11\nprompt: test prompt\nseed_path: ./seed",
    )
    fs.create_file("/tasks/seed/file.txt", contents="seed content")
    fs.create_file("/agents/test_agent/init.sh", contents="#!/bin/bash")
    fs.create_file(
        "/agents/test_agent/docker/docker-compose.yml",
        contents="services:\n  agent:\n    image: test",
    )
    fs.create_dir("/results")

    mock_run_init = mocker.patch("crucible.run_init_sh", return_value=0)
    mock_run_compose = mocker.patch("crucible.run_docker_compose", return_value=0)
    mock_run_compose_down = mocker.patch("crucible.run_docker_compose_down")

    args = MagicMock()
    args.results_dir = "/results"
    args.task = "/tasks/task.yml"
    args.agent_dir = "/agents/test_agent"
    args.keep = False

    sut.run(args)

    mock_run_init.assert_called_once()
    init_call_args = mock_run_init.call_args
    assert "/agents/test_agent" == init_call_args[0][0]

    mock_run_compose.assert_called_once()
    compose_call_args = mock_run_compose.call_args
    assert "/agents/test_agent" == compose_call_args[0][0]
    assert "python:3.11" == compose_call_args[0][2]
    assert "test prompt" == compose_call_args[0][3]

    mock_run_compose_down.assert_called_once_with("/agents/test_agent")
