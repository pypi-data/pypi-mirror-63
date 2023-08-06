import git
import os

from lg_linter.src.file_linters import lint_cpp_file, lint_python_file, lint_shell_file


def print_file_names(files):
    for elem in files:
        print(f'- {elem.a_path}')


def files_were_modified_after_staging(modified_files, staged_files):
    for modified_file in modified_files:
        if modified_file.a_path in [x.a_path for x in staged_files]:
            return True

    return False


def get_file_type(file_path):
    EXTENSIONS = {
        'cpp': ['.h', '.hpp', '.cc', '.cpp'],
        'python': ['.py'],
        'shell': ['.sh', '.bash']
    }

    SHEBANG_KEYWORDS = {
        'cpp': [],
        'python': ['python'],
        'shell': ['sh', 'bash']
    }

    name, extension = os.path.splitext(file_path)

    type_name = None
    if extension:
        for (file_type, extensions_for_type) in EXTENSIONS.items():
            if extension in extensions_for_type:
                type_name = file_type
                break
    else:
        shebang = open(file_path).readline()
        for (file_type, keywords_for_type) in SHEBANG_KEYWORDS.items():
            for keyword in keywords_for_type:
                if keyword in shebang:
                    type_name = file_type
                break

    return type_name


class LgLinter(object):
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = git.Repo(self.repo_path)
        assert not self.repo.bare

    def lint(self):
        """
        Lint all the staged files, return true if successful.
        """
        modified_files = self.repo.index.diff(None)
        staged_files = self.repo.index.diff('HEAD')
        if files_were_modified_after_staging(modified_files, staged_files):
            print(
                'Error: Found files which were modified after staging. Please'
                ' stage all modifications first.')
            return False

        success = True
        outputs = []
        for staged_file in staged_files:
            # Do not lint if the file was deleted. It seems as if pythongit has
            # a bug and has new_file and deleted_file confused.
            if not staged_file.new_file:
                print(f'Linting {staged_file.a_path}... ', end='')
                file_is_ok, stdout = self._lint_file(self.repo_path /
                                                     staged_file.a_path)
                if file_is_ok:
                    print('[\033[92mOK\033[0m]')
                else:
                    print('[\033[91mFAIL\033[0m]')
                    success = False
                    outputs.append(stdout)

        if success:
            print("\nHurray linted succesfully!")
        else:
            print("\nLinter found the following errors:")
            for output in outputs:
                print(output)

        return success

    def _lint_file(self, file_path):
        file_type = get_file_type(file_path)

        if file_type is 'cpp':
            return lint_cpp_file(file_path)
        elif file_type is 'python':
            return lint_python_file(file_path)
        elif file_type is 'shell':
            return lint_shell_file(file_path)
        else:
            return True, f'WARNING: File {file_path} has unknown type and was ignored.'
