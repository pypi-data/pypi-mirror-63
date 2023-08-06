import os
import re
import subprocess


def site_dir(config_file=None):
    if not config_file:
        return 'site'
    return os.path.join(os.path.dirname(config_file), 'site')


def build(config_file=None, verbose=True):
    command = (
        ['mkdocs', 'build', '--clean'] +
        (['--config-file', config_file] if config_file else [])
    )

    if verbose:
        subprocess.check_call(command)
    else:
        subprocess.check_output(command, stderr=subprocess.STDOUT)


def version():
    output = subprocess.check_output(
        ['mkdocs', '--version'], universal_newlines=True
    ).rstrip()
    m = re.search('^mkdocs, version (\\S*)', output)
    return m.group(1)
