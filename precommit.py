import os
import subprocess
import platform
import json
import logging

#
# Strip out the output section for all the tracked ipynb filees under the
# current git branch
#
# Add 'no_strip' to the notebook's metadata (Edit -> Edit Notebook Metadata)
# to exclude the notebook from strip out the output section
#

def normalize_path(git_path):
    if 'windows' in platform.system().lower():
        return git_path.replace('/', '\\\\')
    else:
        return git_path

def strip_output(ipynb):
    path = normalize_path(ipynb)
    output_cnt = 0
    with open(path, 'r') as f:
        j = json.load(f)
        meta = j['metadata']
        if 'no_strip' in meta.keys() and meta['no_strip'] == True:
            logging.info(f'skip {path} based on the notebook metadata')
            return

        for cell in filter(lambda c: c['cell_type'] == 'code', j['cells']):
            if cell['outputs'] != []:
                output_cnt += 1
                cell['outputs'] = []
            if cell['execution_count'] != None:
                cell['execution_count'] = None
    logging.info(f'Striping outputs for {path}, cnt={output_cnt}')
    with open(path, 'w') as f:
        f.write(json.dumps(j, indent=1))

def run_git(*args):
    cmd = ['git']
    cmd.extend(args)
    return subprocess.check_output(cmd).decode('utf-8')

def get_current_branch():
    return run_git('branch', '--show-current')

def main():

    branch = get_current_branch().strip()
    files = run_git('ls-tree', '-r', branch, '--name-only')

    # output = subprocess.check_output(get_param_all_files('master'))
    for l in filter(lambda f: '.ipynb' in f, files.split('\n')):
        strip_output(l)

if __name__ == '__main__':
    main()