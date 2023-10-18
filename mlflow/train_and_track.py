import argparse
import json
import os
import subprocess

from mlflow_lib import MLFlowTracking

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--config-module', type=str, default='train_toki_pona')
parsed_args = arg_parser.parse_args()

config_module = 'config/train_toki_pona.py'
config_module = f'config/{parsed_args.config_module}.py'


try: # this is only here for VS Code syntax highlighter
    from ..config.train_toki_pona import out_dir, eval_interval, eval_iters, log_interval
    from ..config.train_toki_pona import always_save_checkpoint, dataset, gradient_accumulation_steps
    from ..config.train_toki_pona import batch_size, block_size, n_layer, n_head, n_embd, dropout
    from ..config.train_toki_pona import learning_rate, max_iters, lr_decay_iters, min_lr, beta2, warmup_iters
except ImportError:
    pass

exec(open(os.path.join('..', config_module)).read())
params = {
  'out_dir': out_dir,
  'eval_interval': eval_interval,
  'eval_iters': eval_iters,
  'log_interval': log_interval,
  'always_save_checkpoint': always_save_checkpoint,
  'dataset': dataset,
  'gradient_accumulation_steps': gradient_accumulation_steps,
  'batch_size': batch_size,
  'block_size': block_size,
  'n_layer': n_layer,
  'n_head': n_head,
  'n_embd': n_embd,
  'dropout': dropout,
  'learning_rate': learning_rate,
  'max_iters': max_iters,
  'lr_decay_iters': lr_decay_iters,
  'min_lr': min_lr,
  'beta2': beta2,
  'warmup_iters': warmup_iters,
}

tracker = MLFlowTracking(run_path='train/train')

data_prep_run_id = tracker.find_latest_run(run_path='train/data-prep')
data_prep_run = tracker.client.get_run(data_prep_run_id)
tracker.log_params({
    'data_prep_name': data_prep_run.data.params['data_prep_name'],
    'data_prep_sources': data_prep_run.data.params['data_prep_sources'],
})

tracker.log_params({
    'config_module': config_module,
})
tracker.log_params(params)

command_line = [
    'python', 'train.py', config_module
]
tracker.log_params({
    'process_command_line': command_line,
})
command_outcome = subprocess.call(command_line, cwd='..')
tracker.log_params({
    'process_return_value': command_outcome,
})

if(command_outcome == 0):
    with open(os.path.join('..', out_dir, 'loggings.json'), 'r') as loggings_file:
        loggings = json.load(loggings_file)
    for log_entry in loggings:
        tracker.log_metrics(log_entry, step=log_entry['iter'])
    tracker.log_artifact(os.path.join('..', out_dir, 'ckpt.pt'))