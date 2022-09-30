from kfp.components import OutputPath,InputPath
from typing import NamedTuple

def featureengineering(output_dir_path:OutputPath(),input_dir_path:InputPath(),datasetName:str):

    from sklearn.model_selection import train_test_split
    import pandas as pd
    import os
    
    #Commom Steps start here
    os.makedirs(output_dir_path, exist_ok=True)
    df=pd.read_csv(os.path.join(input_dir_path,datasetName))
    #Common Steps Ends here
    
    
    df.dropna(axis=0, subset=['SalePrice'], inplace=True)
    y = df.SalePrice
    X = df.drop(['SalePrice'], axis=1).select_dtypes(exclude=['object'])
    train_X, test_X, train_y, test_y = train_test_split(X.values,
                                                        y.values,
                                                        test_size=0.25,
                                                        shuffle=False)
    
    #Common Steps Starts here
    train_X=pd.DataFrame(train_X)
    train_X.to_csv(os.path.join(output_dir_path,"train_X.csv"))

    train_y=pd.DataFrame(train_y)
    train_y.to_csv(os.path.join(output_dir_path,"train_y.csv"))

    test_X=pd.DataFrame(test_X)
    test_X.to_csv(os.path.join(output_dir_path,"test_X.csv"))

    test_y=pd.DataFrame(test_y)
    test_y.to_csv(os.path.join(output_dir_path,"test_y.csv"))
    #Coomon Steps Ends Here






