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


#Pipeline Orchastration
@dsl.pipeline(name='pipelinename',description="A simple intro pipeline",pipeline_root="pipeline_root")
def pipeline(query:str="""SELECT * FROM `basic-radius-362010.lakshmi.lakshmidemo` LIMIT 10 """
             ,datasetName:str="lakshmidemo.csv",project_id:str="basic-radius-362010"):

    #Components Creation
    download_dataset_opp=components.create_component_from_func(download_dataset.download_dataset,base_image=BASE_IMAGE,
                                                    packages_to_install=['google.cloud','pandas'])
    featureengineering_opp=components.create_component_from_func(featureengineering.featureengineering,base_image=BASE_IMAGE,
                                                    packages_to_install=['sklearn','pandas'])
    training_opp=components.create_component_from_func(training.training,base_image=BASE_IMAGE,
                                                    packages_to_install=['xgboost','pandas','joblib'])

    evaluation_opp=components.create_component_from_func(evaluation.evaluate,base_image=BASE_IMAGE,
                                                    packages_to_install=['sklearn','pandas','joblib'])

    hypertuning_opp=components.create_component_from_func(hypertuning.hypertuning,base_image=BASE_IMAGE,
                                                    packages_to_install=[])



    #Building pipeline or stitching the components in order
    download_dataset_opp_final=download_dataset_opp(project_id,query)
    featureengineering_opp_final=featureengineering_opp(download_dataset_opp_final.output,datasetName)
    training_opp_final=training_opp(featureengineering_opp_final.output)
    evaluation_opp_final=training_opp(training_opp_final.output)




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
    main(project_id2="lakshmi",staging_bucket="bucket",package_fileandpathname="lakshmi.json",display_name="helloworld",pipeline_root="pipeline\\root")




