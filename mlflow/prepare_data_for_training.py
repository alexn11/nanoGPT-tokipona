import argparse
import os
import shutil
import subprocess

from mlflow_lib import MLFlowTracking

data_prep_folder = 'data/toki_pona'
data_prep_folder_rel = os.path.join('..', data_prep_folder)

tracker = MLFlowTracking(run_path='train/data-prep')

print(f'downloading prepared data file')
data_prep_run_id = tracker.find_latest_run(run_path='data-prep/default/')
tracker.download_artifact(run_id=data_prep_run_id,
                          artifact_path='toki-ale.txt',
                          dest_path=data_prep_folder_rel)

shutil.move(os.path.join(data_prep_folder_rel, 'toki-ale.txt',),
            os.path.join(data_prep_folder_rel, 'input.txt'))

print('tokenisation & train-eval-test split')

data_prep_run = tracker.client.get_run(run_id=data_prep_run_id)
data_prep_name: str = data_prep_run.info.run_name
data_prep_sources = data_prep_run.data.params['sources']
tracker.log_params({
    'data_prep_name': data_prep_name.split('/')[-2],
    'data_prep_sources': data_prep_sources,
})

artifact_paths = [
    os.path.join(data_prep_folder_rel, artifact)
    for artifact in [ 'meta.pkl', 'train.bin', 'val.bin', 'test.bin' ]
]

for artifact_path in artifact_paths:
    if(os.path.exists(artifact_path)):
        os.remove(artifact_path)


command_line = [
    'python',
    os.path.join(data_prep_folder, 'prepare.py'),
]
command_outcome = subprocess.call(command_line, cwd='..')
tracker.log_params({
    'process_command_line': command_line,
    'process_return_code': command_outcome,
})
if(command_outcome == 0):
    for artifact_path in artifact_paths:
        if(os.path.exists(artifact_path)):
            tracker.log_artifact(artifact_path)
