from kfp.components import OutputPath,InputPath
from typing import NamedTuple

def training(output_dir_path:OutputPath(),input_dir_path:InputPath()):

    from xgboost import XGBRegressor
    import pandas as pd
    import os
    import joblib
    import numpy
    
    os.makedirs(output_dir_path, exist_ok=True)
    train_X=pd.read_csv(os.path.join(input_dir_path,"train_X.csv"))
    train_X=train_X.to_numpy()
    train_y=pd.read_csv(os.path.join(input_dir_path,"train_y.csv"))
    train_y=train_y.to_numpy()
    test_X=pd.read_csv(os.path.join(input_dir_path, "test_X.csv"))
    test_X=test_X.to_numpy()
    test_y=pd.read_csv(os.path.join(input_dir_path, "test_y.csv"))
    test_y=test_y.to_numpy()

    """Train the model using XGBRegressor."""
    model = XGBRegressor(n_estimators=1000,
                             learning_rate=0.1)

    model.fit(train_X,
                  train_y,
                  early_stopping_rounds=40,
                  eval_set=[(test_X, test_y)])

    print("model score:",model.best_score,"At iteration:",model.best_iteration + 1)

    joblib.dump(model, os.path.join(output_dir_path,"model.joblib"))