import os
import sys
import subprocess


def lint_cpp_file(file_path):
    os.system(f'clang-format -i {file_path}')
    completed_process = subprocess.run(['cppcheck', file_path],
                                       stdout=subprocess.PIPE)

    if completed_process.returncode is 0:
        return True, ''
    else:
        return False, completed_process.stdout.decode('utf-8')


def lint_python_file(file_path):
    os.system(f'yapf -i {file_path}')
    completed_process = subprocess.run(['pylint', file_path],
                                       stdout=subprocess.PIPE)

    if completed_process.returncode is 0:
        return True, ''
    else:
        return False, completed_process.stdout.decode('utf-8')


def lint_shell_file(file_path):
    completed_process = subprocess.run(['shellcheck', file_path],
                                       stdout=subprocess.PIPE)

    if completed_process.returncode is 0:
        return True, ''
    else:
        return False, completed_process.stdout.decode('utf-8')
