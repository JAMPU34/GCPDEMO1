from kfp.components import OutputPath,InputPath
from typing import NamedTuple

def evaluate(input_dir_path:InputPath(),input_dir_path1:InputPath()):
    import joblib
    import os
    import pandas as pd
    from sklearn.metrics import mean_absolute_error

    model=joblib.load(os.path.join(input_dir_path,"model.joblib"))
    test_X=pd.read_csv(os.path.join(input_dir_path1, "test_X.csv"))
    test_X=test_X.to_numpy()
    test_y=pd.read_csv(os.path.join(input_dir_path1, "test_y.csv"))
    test_y=test_y.to_numpy()

    predictions = model.predict(test_X)
    print("Mean Absolute Error:",mean_absolute_error(predictions, test_y))


