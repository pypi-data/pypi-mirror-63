## Installation

Install with
```sh
pip3 install lg-linter
```

## How to use
Inside your git repo run
```sh
init-lg-linter
```

The linter is now active and will be run before every commit.
If you want to remove the linter from your repo use
```
deinit-lg-linter
```

**Pro Tip**
If the linter complains about stuff which clearly is wrong you can override him with
```
git commit --no-verify
```
Use with care, with great power comes great responsibility!
