import pytest
import agent as sut


def test__validate_agent_dir__missing_init_sh(fs):
    fs.create_file("/agent/docker/docker-compose.yml", contents="")

    with pytest.raises(ValueError):
        sut.validate_agent_dir("/agent")


def test__validate_agent_dir__missing_docker_compose(fs):
    fs.create_file("/agent/init.sh", contents="")

    with pytest.raises(ValueError):
        sut.validate_agent_dir("/agent")
