#imports statements
import google.cloud.aiplatform as aip
from kfp import dsl
from kfp.v2 import compiler
from kfp import components
import warnings
from codetemplates import download_dataset,featureengineering,training,hypertuning,evaluation

experiment_name = 'test1'
BASE_IMAGE = "python:3.8-slim"

warnings.filterwarnings('ignore')

pipeline_root="gs://lakshmiqwiklabs-gcp-03-8b866aa182e2aip-20220915080528/pipeline_root/intro"

#Pipeline Orchastration
@dsl.pipeline(name='lakshmipipeline8',description="A simple intro pipeline",pipeline_root=pipeline_root)
def pipeline(query:str="""SELECT * FROM `qwiklabs-gcp-03-8b866aa182e2.lakshmi.lakshmidemo` LIMIT 10 """
             ,datasetName:str="lakshmidemo.csv",project_id:str="qwiklabs-gcp-03-8b866aa182e2"):

    #Components Creation
    download_dataset_opp=components.create_component_from_func(download_dataset.download_dataset,base_image=BASE_IMAGE,
                                                    packages_to_install=['google-cloud-bigquery[pandas]==2.34.3','pandas'])
    featureengineering_opp=components.create_component_from_func(featureengineering.featureengineering,base_image=BASE_IMAGE,
                                                    packages_to_install=['sklearn','pandas'])
    training_opp=components.create_component_from_func(training.training,base_image=BASE_IMAGE,
                                                    packages_to_install=['sklearn','xgboost','pandas','joblib','numpy'])

    evaluation_opp=components.create_component_from_func(evaluation.evaluate,base_image=BASE_IMAGE,
                                                    packages_to_install=['sklearn','pandas','joblib','xgboost'])

    hypertuning_opp=components.create_component_from_func(hypertuning.hypertuning,base_image=BASE_IMAGE,
                                                    packages_to_install=[])



    #Building pipeline or stitching the components in order
    download_dataset_opp_final=download_dataset_opp(project_id=project_id,query=query)
    featureengineering_opp_final=featureengineering_opp(download_dataset_opp_final.output,datasetName)
    training_opp_final=training_opp(featureengineering_opp_final.output)
    evaluation_opp_final=evaluation_opp(training_opp_final.output,featureengineering_opp_final.output)




def main(project_id2:str,staging_bucket:str,package_fileandpathname:str,display_name:str,pipeline_root:str):
    # Intializining Vertex Ai
    aip.init(project=project_id2, staging_bucket=staging_bucket)

    #Compile the Pipeline
    compiler.Compiler().compile(pipeline_func=pipeline, package_path=package_fileandpathname)

    #Preparining the pipeline to submit to VertexAI
    job = aip.PipelineJob(
        display_name=display_name,
        template_path=package_fileandpathname,
        pipeline_root=pipeline_root,
    )

    #Submitting the Pipeline to VertexAI
    job.run()


if __name__ == '__main__':
    main(project_id2="qwiklabs-gcp-03-8b866aa182e2",staging_bucket="gs://lakshmiqwiklabs-gcp-03-8b866aa182e2aip-20220915080528",package_fileandpathname="lakshmi.json",display_name="lakshmihelloworld",pipeline_root=pipeline_root)




