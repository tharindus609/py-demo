import subprocess
import logging
import shlex


def execute(command):
    _logger = logging.getLogger(__name__)
    _logger.debug("Executing command: {0}".format(command))

    cmd_args = shlex.split(command)
    try:
        proc = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_data, stderr_data = proc.communicate()
        ret_code = proc.returncode
    except Exception as _ex:
        _logger.exception("Unhandled exception: {0}".format(_ex))
        return 1, None, None

    return ret_code, stdout_data.decode(), stderr_data.decode()


def execute_remote(host, command):
    _logger = logging.getLogger(__name__)
    _logger.debug("Executing command on host: {0}".format(host))

    ssh_command = "ssh -o ConnectionAttempts=3 -o stricthostkeychecking=no {0} '{1}'".format(host, command)
    return execute(ssh_command)


def execute_remote_as(user, host, command):
    _logger = logging.getLogger(__name__)
    _logger.debug("Executing command on host: {0} as {1}".format(host, user))

    ssh_command = "ssh -o ConnectionAttempts=3 -o stricthostkeychecking=no {0}@{1} '{2}'".format(user, host, command)
    return execute(ssh_command)

