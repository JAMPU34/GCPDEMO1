from kfp.components import OutputPath,InputPath
from typing import NamedTuple

def modelexport(input_dir_path:InputPath(),output_dir_path:OutputPath(),project_id:str,bucket:str):
    
    import os
    import google.cloud.aiplatform as aiplatform
    
    #Common Steps Starts here
    aiplatform.init(project=project_id, location='us-central1')
    model_v1 = aiplatform.Model.upload(
    display_name="lakshmigcpdemo1",
    artifact_uri=bucket+"/models",
    serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-6:latest"
    )
    
    model_v1.wait()
    print(model_v1)
    #Common Steps Ends here
    
    
    