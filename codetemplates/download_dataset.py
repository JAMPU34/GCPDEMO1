from kfp.components import OutputPath,InputPath
from typing import NamedTuple

def download_dataset(input_dir_path:InputPath(),query: str, project_id: str,
                   output_dir_path: OutputPath()):

    from google.cloud import bigquery
    import pandas
    import os
    
    #Commom Steps Starts Here
    os.makedirs(output_dir_path, exist_ok=True)

    client = bigquery.Client(location="us-central1", project=project_id)
    query=query
    query_job = client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location="us-central1",
    )  # API request - starts the query

    df = query_job.to_dataframe()
    df.to_csv(os.path.join(output_dir_path,"lakshmidemo.csv"),index=False)
    print(os.listdir(output_dir_path))
    
    #Common Steps Ends here





