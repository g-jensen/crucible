import sys
from unittest.mock import MagicMock

sys.path.insert(0, "/home/greg/programs/container-agent/src")

import main
import args
import crucible


def test__main__calls_run_with_parsed_args(mocker):
    mock_args = MagicMock()
    mock_parse_args = mocker.patch.object(args, "parse_args", return_value=mock_args)
    mock_run = mocker.patch.object(crucible, "run")

    main.main()

    mock_parse_args.assert_called_once()
    mock_run.assert_called_once_with(mock_args)
