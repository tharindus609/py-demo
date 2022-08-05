from ast import Return
import os
import sys

import logging
import logging.handlers

import cx_Oracle

_oracle = None
_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)

class Oracle:
    def __init__(self, db_string):
        _log = logging.getLogger(__name__)
        _log.debug("Connecting to DB: {0}".format(db_string))
        self.db_con = cx_Oracle.connect(db_string)
        _log.debug("Connected to DB: {0}".format(db_string))
        self.db_con.autocommit = True
        self.db_cursor = self.db_con.cursor()
    
    def __del__(self):
        _log = logging.getLogger(__name__)
        _log.debug("Cleaning up DB connection")
        self.db_cursor.close()
        self.db_con.close()
    
    def exec_select(self, query):
        _log = logging.getLogger(__name__)
        _log.debug("Executing: {0}".format(query))
        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()


def _init_logger(log_name, log_level):
    global _log

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_log_handler = logging.FileHandler(log_name)
    file_log_handler.setLevel(logging.DEBUG)
    file_log_handler.setFormatter(formatter)
    _log.addHandler(file_log_handler)

    stream_log_handler = logging.StreamHandler(sys.stdout)
    stream_log_handler.setLevel(log_level)
    _log.addHandler(stream_log_handler)


def check_table_diff(original_table, duplicate_table, db_con):
    _log.info("Checking table differences between: {0} and {1}".format(original_table, duplicate_table))

    ori_table_def = db_con.exec_select("select COLUMN_ID, COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION from USER_TAB_COLUMNS where table_name = '{0}' order by column_id".format(original_table))
    dpl_table_def = db_con.exec_select("select COLUMN_ID, COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION from USER_TAB_COLUMNS where table_name = '{0}' order by column_id".format(duplicate_table))

    if not set(ori_table_def) == set(dpl_table_def):
        _log.error("Table definition mismatch between {0} and {1}".format(original_table, duplicate_table))
        _log.debug("{0} definition".format(original_table))
        _log.debug(ori_table_def)
        _log.debug("{0} definition".format(duplicate_table))
        _log.debug(dpl_table_def)
        return False
    
    _log.info("Table definitions matched")
    return True


def main():
    _db = Oracle(os.environ['ATS_DB_STRING'])

    status = True

    if status:
        status = check_table_diff("ATSD_TCR_COMMON", "ATSH_TCR_COMMON", _db)
    else:
        check_table_diff("ATSD_TCR_COMMON", "ATSH_TCR_COMMON", _db)

    if status:
        status = check_table_diff("ATSD_POS_SETTLEMENT", "ATSH_POS_SETTLEMENT", _db)
    else:
        check_table_diff("ATSD_POS_SETTLEMENT", "ATSH_POS_SETTLEMENT", _db)

    if status:
        status = check_table_diff("ATSD_POS_SETTLEMENT", "ATSH_POS_SETTLEMENT", _db)
    else:
        check_table_diff("ATSD_POS_SETTLEMENT", "ATSH_POS_SETTLEMENT", _db)

    if status:
        status = check_table_diff("ATSD_SIN_SIN", "ATSH_SIN_SIN", _db)
    else:
        check_table_diff("ATSD_SIN_SIN", "ATSH_SIN_SIN", _db)

    if status:
        status = check_table_diff("ATSD_SIF_SI_FEEDBACK", "ATSH_SIF_SI_FEEDBACK", _db)
    else:
        check_table_diff("ATSD_SIF_SI_FEEDBACK", "ATSH_SIF_SI_FEEDBACK", _db)

    if status:
        status = check_table_diff("ATSD_ALC_ALLOCATION", "ATSH_ALC_ALLOCATION", _db)
    else:
        check_table_diff("ATSD_ALC_ALLOCATION", "ATSH_ALC_ALLOCATION", _db)

    if status:
        _log.debug("Done")
    else:
        _log.info("Table definition check failed")
        sys.exit(1)


if __name__ == '__main__':
    _init_logger('script.log', logging.INFO)
    try:
        main()
    except Exception as _ex:
        _log.exception("Exception Occurred")
    _log.info("Exciting script")

