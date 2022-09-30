from kfp.components import OutputPath,InputPath
from typing import NamedTuple

def batchpredict(input_dir_path:InputPath(),project_id:str):
    
    import google.cloud.aiplatform as aiplatform
    
    #Common Steps starts here
    models = aiplatform.Model.list(filter=f"display_name=lakshmigcpdemo1")
    model=models[0]
    batch_prediction_job = model.batch_predict(
      job_display_name='lakshmi-batch-prediction-job',
      instances_format='bigquery',
      machine_type='n1-standard-4',
      bigquery_source='bq://qwiklabs-gcp-02-2cabae029b33.batchpredictamsdata.batchpredictsource',
      bigquery_destination_prefix='bq://qwiklabs-gcp-02-2cabae029b33'
    )
    
    print("Job Completed Successfully and uploaded the results")
    #Common Steps ends here