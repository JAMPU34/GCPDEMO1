from kfp.components import OutputPath
from typing import NamedTuple

def download_dataset(query: str, project_id: str,
                   output_dir_path: OutputPath()):

    from google.cloud import bigquery
    import pandas
    import os

    os.makedirs(output_dir_path, exist_ok=True)
    op_model_path = output_dir_path

    client = bigquery.Client(location="us-east1", project=project_id)
    #query = """SELECT * FROM `basic-radius-362010.lakshmi.lakshmidemo` LIMIT 10 """
    query=query
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="us-east1",
    )  # API request - starts the query

    df = query_job.to_dataframe()
    df.to_csv(op_model_path+"lakshmidemo.csv",index=False)





