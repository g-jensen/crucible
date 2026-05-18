import pytest
import task as sut


def test__load_task__valid_task_with_all_fields(fs):
    fs.create_file(
        "/path/to/task.yml",
        contents="""\
id: example_task
name: Example Task
description: Basic task
docker_image: python:3.11-slim
seed_path: ./seed
prompt: "Do something"
""",
    )

    result = sut.load_task("/path/to/task.yml")

    assert "example_task" == result["id"]
    assert "Example Task" == result["name"]
    assert "Basic task" == result["description"]
    assert "python:3.11-slim" == result["docker_image"]
    assert "./seed" == result["seed_path"]
    assert "Do something" == result["prompt"]


def test__validate_task__missing_required_field():
    task = {"docker_image": "python:3.11-slim", "prompt": "Do something"}

    with pytest.raises(ValueError):
        sut.validate_task(task)


def test__validate_task__missing_docker_image():
    task = {"id": "example_task", "prompt": "Do something"}

    with pytest.raises(ValueError):
        sut.validate_task(task)


def test__validate_task__missing_prompt():
    task = {"id": "example_task", "docker_image": "python:3.11-slim"}

    with pytest.raises(ValueError):
        sut.validate_task(task)


def test__resolve_seed_path__relative_to_task_file(fs):
    fs.create_file(
        "/project/task.yml",
        contents="""\
id: example_task
docker_image: python:3.11-slim
seed_path: ./seed
prompt: "Do something"
""",
    )

    result = sut.resolve_seed_path("/project/task.yml", "./seed")

    assert "/project/seed" == result


def test__validate_seed_path__raises_when_path_missing(fs):
    with pytest.raises(ValueError):
        sut.validate_seed_path("/path/to/nonexistent/seed")
