import args as sut


def test__parse_args__required_and_optional_flags():
    test_args = [
        "--results-dir",
        "/path/to/results",
        "--task",
        "/path/to/task.json",
        "--agent-dir",
        "/path/to/agent",
        "--keep",
    ]

    result = sut.parse_args(test_args)

    assert "/path/to/results" == result.results_dir
    assert "/path/to/task.json" == result.task
    assert "/path/to/agent" == result.agent_dir
    assert True == result.keep
