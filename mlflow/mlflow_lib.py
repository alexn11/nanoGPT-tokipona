import mlflow

class MLFlowTracking:
    def __init__(self,
                 tracking_uri='http://localhost:5000',
                 experiment_name='tokipona',
                 run_path=''):
        self.experiment_name = experiment_name
        self.run_path = run_path
        self.client = mlflow.client.MlflowClient(tracking_uri=tracking_uri)
        self.experiment = self.client.get_experiment_by_name(experiment_name)
        run = self.client.create_run(experiment_id=self.experiment.experiment_id)
        self.run_id = run.info.run_id
        if('run_path' == ''):
            self.run_name = run.info.run_name
        else:
            self.run_name = f'{run_path}/{run.info.run_name}'
            self.client.set_tag(self.run_id, 'mlflow.runName', self.run_name)
    
    def find_latest_run(self, experiment_ids=[], run_path='',):
        if(experiment_ids == []):
            experiment_ids = [ self.experiment.experiment_id, ]
        results = self.client.search_runs(experiment_ids=experiment_ids,
                                          # NOTE: happy SQL injections - not intended for use in the wild:
                                          filter_string=f"attributes.run_name like '{run_path}%'",
                                          order_by=[ 'Created DESC', ],
                                          max_results=1)
        if(len(results) == 0):
            return None
        return results[0].info.run_id
    
    def download_artifact(self, artifact_path='', run_id=None, dest_path=None):
        if(run_id is None):
            run_id = self.run_id
        self.client.download_artifacts(run_id=run_id, path=artifact_path, dst_path=dest_path)

    def log_params(self, params: dict):
        for param_name, param_value in params.items():
            self.client.log_param(self.run_id, param_name, param_value)

    def log_metrics(self, metrics: dict, step=None):
        for metric_name, metric_value in metrics.items():
            self.client.log_metric(run_id=self.run_id,
                                   key=metric_name,
                                   value=metric_value,
                                   step=step)
    
    def log_artifact(self, artifact_path):
        self.client.log_artifact(run_id=self.run_id, local_path=artifact_path,)

    def end(self):
        self.client.set_terminated(self.run_id)
