from kfp.components import OutputPath,InputPath
from typing import NamedTuple

def etl_dataproc(output_dir_path:OutputPath()):
    
    from google.cloud import dataproc_v1
    cluster_client = dataproc_v1.ClusterControllerClient(
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format('us-central1')}
    )
    cluster = {
        "project_id": 'qwiklabs-gcp-02-2cabae029b33',
        "cluster_name": 'lakshmi341',
        "config": {
            "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-4"},
            "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2"},
        },
    }
    operation = cluster_client.create_cluster(
        request={"project_id":"qwiklabs-gcp-02-2cabae029b33", "region": "us-central1", "cluster": cluster}
    )
    result = operation.result()
    print("Cluster created successfully: {}".format(result.cluster_name))
    
    # Create the job client.
    job_client = dataproc_v1.JobControllerClient(
    client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format('us-central1')}
    )
    
    gcs_bucket="gs://qwiklabs-gcp-02-2cabae029b33aip-20220927061904/etl"
    spark_filename="dataproc.py"
    # Create the job config.
    job = {
    "placement": {"cluster_name": 'lakshmi341'},
    "pyspark_job": {"main_python_file_uri":"gs://qwiklabs-gcp-02-2cabae029b33aip-20220927061904/etl/dataproc.py" ,"jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest.jar"]
},
        #"jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest.jar"],
        #"args": ["1000"]
    }

    operation = job_client.submit_job_as_operation(
    request={"project_id": 'qwiklabs-gcp-02-2cabae029b33', "region": 'us-central1', "job": job})
    response = operation.result()

    # Dataproc job output is saved to the Cloud Storage bucket
    # allocated to the job. Use regex to obtain the bucket and blob info.
    matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)

    output = (
    storage.Client()
    .get_bucket(matches.group(1))
    .blob(f"{matches.group(2)}.000000000")
    .download_as_string())
    print(f"Job finished successfully: {output}\r\n")
    

    