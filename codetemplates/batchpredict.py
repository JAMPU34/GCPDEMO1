from kfp.components import OutputPath,InputPath
from typing import NamedTuple

def batchpredict(input_dir_path:InputPath(),project_id:str):
    
    import google.cloud.aiplatform as aiplatform
    
    models = aiplatform.Model.list(filter=f"display_name=lakshmigcpdemo1")
    model=models[0]
    batch_prediction_job = model.batch_predict(
      job_display_name='lakshmi-batch-prediction-job',
      instances_format='bigquery',
      machine_type='n1-standard-4',
      bigquery_source='bq://qwiklabs-gcp-04-9b56f269a5ed.batchamsdata.batchsource',
      bigquery_destination_prefix='bq://qwiklabs-gcp-04-9b56f269a5ed'
    )
    
    print("Job Completed Successfully and uploaded the results")