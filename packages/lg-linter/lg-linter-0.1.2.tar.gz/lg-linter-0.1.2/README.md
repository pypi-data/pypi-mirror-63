## Installation
Install with
```sh
pip3 install lg-linter
```
**Note:** This will install / overwrite the linter config files in your home directory.

## How to use
Inside your git repo run
```sh
init_lg_linter
```
The linter is now active and will be run before every commit.
If you want to remove the linter from your repo use
```
deinit_lg_linter
```

**Pro Tip:** If the linter complains about stuff which clearly is wrong you can override him with
```
git commit --no-verify
```
Use with care, with great power comes great responsibility!

For feature requests or bugs please drop an issue at https://github.com/lgulich/lg-linter.
