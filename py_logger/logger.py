import logging.config
import json
import os
from datetime import datetime
from pathlib import Path


def load_json_configs():
    config_file = Path('py_logger/log_config.json')

    with open(config_file, 'r', encoding='utf-8') as _config_file:
        json_config = json.load(_config_file)

    if not json_config['load_config']['full_path_to_file_provided']:
        config_file_name = Path('{0}/{1}.{2}.log'.format(
            str(os.environ['SYSTEM_LOGS']),
            json_config['logger']['handlers']['file']['filename'],
            datetime.now().strftime("%Y%m%d-%H%M%S")))
        json_config['logger']['handlers']['file']['filename'] = config_file_name

    print("Logging to File: {0}".format(Path(json_config['logger']['handlers']['file']['filename'])))
    logging.config.dictConfig(json_config['logger'])
