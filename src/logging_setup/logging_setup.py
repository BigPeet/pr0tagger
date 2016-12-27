import os
import json
import logging.config

MODULES = ["__main__",
           "pr0gramm",
           "data_collection",
           "annotation",
           "logging_setup",
           "net"]


class Whitelist(logging.Filter):

    def __init__(self, whitelist):
        self.whitelist = [logging.Filter(name) for name in whitelist]

    def filter(self, record):
        return any(f.filter(record) for f in self.whitelist)


def setup_logging(path="../etc/logging.json",
        log_file=None,
        file_handler="file_handler",
        default_level=logging.INFO):
    """
    Setup logging configuration
    """

    # read json config file
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)

        # replace the log file of the file handler, if another file is given
        if log_file:
            config["handlers"][file_handler]["filename"] = log_file

        # init the logging framework with the config
        logging.config.dictConfig(config)
    else:
        # use fallback config
        logging.basicConfig(level=default_level)

    # filter out logging messages from modules that are not whitelisted
    for handler in logging.root.handlers:
        handler.addFilter(Whitelist(MODULES))
