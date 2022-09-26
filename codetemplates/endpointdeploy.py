from kfp.components import OutputPath,InputPath
from typing import NamedTuple

def endpointdeploy(input_dir_path:InputPath(),project_id:str):
    
    import google.cloud.aiplatform as aiplatform
    
    endpoint = aiplatform.Endpoint.create(
    display_name="lakshmigcpddemo1rock",
    project=project_id,
    location='us-central1'
    )

    print(endpoint)
    
    models = aiplatform.Model.list(filter=f"display_name=lakshmigcpdemo1")
    print("ModelNmae:",models[0])
    model=models[0]
    
    response = endpoint.deploy(
    model=model,
    deployed_model_display_name="xgboostams",
    machine_type='n1-standard-4',
    )

    print(endpoint)
    
    deployed_model_id = endpoint.gca_resource.deployed_models[0].id
    print(deployed_model_id)