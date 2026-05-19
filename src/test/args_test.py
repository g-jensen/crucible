import args as sut


def test__parse_args__uses_sys_argv_when_no_args_provided(mocker):
    mocker.patch(
        "sys.argv",
        [
            "program_name",
            "--results-dir",
            "/mocked/results",
            "--task",
            "/mocked/task.json",
            "--agent-dir",
            "/mocked/agent",
        ],
    )

    result = sut.parse_args()

    assert "/mocked/results" == result.results_dir
    assert "/mocked/task.json" == result.task
    assert "/mocked/agent" == result.agent_dir


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
