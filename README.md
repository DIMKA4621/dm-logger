# DM-Logger

## Urls

* [PyPI](https://pypi.org/project/dm-logger/)
* [GitHub](https://github.com/DIMKA4621/dm-logger)

## Parameters

### _Options for creating individual loggers_

| Parameter    | Type   | Default Value | Description                                  |
|--------------|--------|---------------|----------------------------------------------|
| `name`       | `str`  | (required)    | The name associated with the class instance. |
| `level`      | `str`  | `"DEBUG"`     | The logging level (e.g., "DEBUG", "INFO").   |
| `write_logs` | `bool` | `True`        | Whether to write logs to a file.             |
| `print_logs` | `bool` | `True`        | Whether to print logs to the console.        |

### _Common class parameters for all loggers_

| Parameter             | Type           | Default Value | Description                                           |
|-----------------------|----------------|---------------|-------------------------------------------------------|
| `logs_dir_path`       | `str`          | `"logs"`      | Path to the directory where the logs will be stored.  |
| `file_name`           | `str`          | `"main.log"`  | The name of the log file.                             |
| `write_mode`          | `"a" \| "w"`   | `"w"`         | File write mode ('a' for append, 'w' for overwrite).  |
| `max_MB`              | `int`          | `5`           | Maximum size of the log file in MB.                   |
| `max_count`           | `int`          | `10`          | Maximum number of log files.                          |
| `show_name_label`     | `bool`         | `False`       | Whether to display the name label in log entries.     |
| `show_location_label` | `bool \| None` | `False`       | Whether to display the location label in log entries. |
| `format_string`       | `str`          | `None`        | The format string of the log.                         |

## Usage

### Setup class options

_This options usage for all loggers_

```python
from dm_logger import DMLogger

DMLogger.options.show_name_label = True
DMLogger.options.max_count = 5
```

### Record

```python
from dm_logger import DMLogger

logger = DMLogger("main")

logger.info("test message", tag="test tag")
logger.debug("new message", id=123312)
logger.info("only mess")
logger.critical(env="production")
logger.warning({"key": "value"})
logger.error(["item1", "item2", 3])
logger.info()
```

Output

```textmate
19-11-2023 00:49:03.406 [INFO] {tag: 'test tag'} -- test message
19-11-2023 00:49:03.406 [DEBUG] {id: 123312} -- new message
19-11-2023 00:49:03.407 [INFO] -- only mess
19-11-2023 00:49:03.407 [CRITICAL] (test.<module>:8) {env: 'production'}
19-11-2023 00:49:03.408 [WARNING] -- {'key': 'value'}
19-11-2023 00:49:03.408 [ERROR] (test.<module>:10) -- ['item1', 'item2', 3]
19-11-2023 00:49:03.409 [INFO]
```

### Several loggers

_All loggers will write to one file_

```python
from dm_logger import DMLogger

DMLogger.options.show_name_label = True

logger = DMLogger("main", level="INFO")
debugger = DMLogger("debugger", print_logs=False)

logger.info("Start app")
debugger.debug(process_id=123123)
logger.error("App crashed!")
```

Output

```textmate
19-11-2023 00:56:36.879 [INFO] [main] -- Start app
19-11-2023 00:56:36.880 [ERROR] [main] (test.<module>:10) -- App crashed!
```

Log file

```textmate
19-11-2023 00:56:36.879 [INFO] [main] -- Start app
19-11-2023 00:56:36.880 [DEBUG] [debugger] {process_id: 123123}
19-11-2023 00:56:36.880 [ERROR] [main] (test.<module>:10) -- App crashed!
```

## Requirements

Python 3.7 or higher.
