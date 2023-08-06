"""
Module to experiment with different models and parameters.
Uses MlFlow as a experiment Framework to create, track and serve pipelines
"""

import numpy as np
import argparse
import mlflow
import mlflow.sklearn
from processing.pipeline import PipelineBuilder
from processing import config
from processing.data_management import load_dataset
from processing.utils import eval_metrics, clean_money_format, print_learning_curve, print_validation_curve
import logging
from processing.model_builder import ModelBuilder


_logger = logging.getLogger(__name__)

TRAIN_DATA_FILE = "train_set_03162020_015253.csv"
DEV_DATA_FILE = "dev_set_03162020_015253.csv"
TEST_DATA_FILE = "test_set_03162020_015253.csv"

RANDOM_STATE = 142

def run_training() -> None:
    """Train the model."""

    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-mode', action='store', type=str, required=True)
    my_parser.add_argument('-model', action='store', type=str)
    my_parser.add_argument('-params', action='store', type=str)

    args = my_parser.parse_args()
    mode = args.mode
    model_name = args.model
    params = eval(args.params)

    # read training/dev/test data
    train_set = load_dataset(file_name=TRAIN_DATA_FILE)
    y_train = clean_money_format(train_set, "price")


    if(mode == "train"):
        test_set = load_dataset(file_name=DEV_DATA_FILE)
    elif(mode == "test"):
        test_set = load_dataset(file_name=TEST_DATA_FILE)

    y_test = clean_money_format(test_set, "price")

    #Creates an estimator instance depending on the model_name
    model_builder = ModelBuilder()
    model = model_builder.create(model_name, params, RANDOM_STATE)

    #The next code is partly based on the MLFlow tutorial
    with mlflow.start_run():

        pipeline = PipelineBuilder.create(model)
        pipeline.fit(train_set, y_train)

        test_pred = pipeline.predict(test_set)

        (rmse, mae, r2) = eval_metrics(y_test, test_pred)

        print("{} model ({}):".format(model_name, params))
        print("  RMSE {}: {}".format(mode, rmse))
        print("  MAE {}: {}".format(mode, mae))
        print("  R2 {}: {}".format(mode, r2))

        mlflow.log_param("model", model_name)
        mlflow.log_param("params", params)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(pipeline, "model")

        #Print learning curves, optionally we could also use validation
        #curves
        print_learning_curve(pipeline, train_set, y_train)


if __name__ == '__main__':
    run_training()



