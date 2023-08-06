import os
import setuptools

HOME_PATH = os.path.expanduser('~')
CONFIG_PATH = 'lib/lg_linter/config'

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="lg-linter",
    version="v0.1.1-alpha",
    author="Lionel Gulich",
    author_email="lgulich@ethz.ch",
    url="https://github.com/lgulich/lg-linter",
    description="A pre commit linter for cpp, python and sh",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    download_url=
    "https://github.com/lgulich/lg-linter/archive/v0.1.1-alpha.tar.gz",
    install_requires=[
        'gitpython',
        'pylint',
        'yapf',
        'cpplint',
    ],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
    ],
    license="GPL-3.0",
    package_dir={'': 'lib'},
    packages=setuptools.find_packages('lib'),
    include_package_data=True,
    data_files=[('/' + HOME_PATH, [
        os.path.join(CONFIG_PATH, '.clang-format'),
        os.path.join(CONFIG_PATH, '.pylintrc'),
        os.path.join(CONFIG_PATH, 'cpplint.py')
    ])],
    scripts=[
        'lib/lg_linter/scripts/init-lg-linter',
        'lib/lg_linter/scripts/deinit-lg-linter'
    ],
    python_requires=">=3.6",
)
