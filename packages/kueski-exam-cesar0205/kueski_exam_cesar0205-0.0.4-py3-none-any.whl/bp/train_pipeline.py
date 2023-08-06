import numpy as np

import sys

import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from processing.pipeline import PipelineBuilder
from processing import config
from processing.data_management import load_dataset
import logging

_logger = logging.getLogger(__name__)

TRAIN_DATA_FILE = "train_set_03162020_015253.csv"
DEV_DATA_FILE = "dev_set_03162020_015253.csv"
TEST_DATA_FILE = "test_set_03162020_015253.csv"

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def clean_money_format(data_set, variable):
    return data_set.apply(lambda x: float(x[variable].\
                            replace("$", "").\
                            replace(",", "")), axis = 1)


def run_training() -> None:
    """Train the model."""

    # read training/dev/test data
    train_set = load_dataset(file_name=TRAIN_DATA_FILE)
    dev_set = load_dataset(file_name=DEV_DATA_FILE)
    test_set = load_dataset(file_name=TEST_DATA_FILE)

    y_train = clean_money_format(train_set, "price")
    y_dev = clean_money_format(dev_set, "price")
    y_test = clean_money_format(test_set, "price")

    # transform the target
    y_train = np.log(y_train + 1)
    y_dev = np.log(y_dev + 1)
    y_test = np.log(y_test + 1)

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    random_state = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    logging.info("Alpha {}, l1_ratio {}".format(alpha, random_state))

    with mlflow.start_run():

        pipeline = PipelineBuilder.create(alpha, random_state)
        pipeline.fit(train_set, y_train)

        dev_pred = pipeline.predict(dev_set)

        (rmse, mae, r2) = eval_metrics(y_dev, dev_pred)

        print("Lasso model (alpha=%f, random_state=%f):" % (alpha, random_state))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("random_state", random_state)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(pipeline, "model")

    test_pred = pipeline.predict(test_set)
    (rmse, mae, r2) = eval_metrics(y_test, test_pred)
    print("Model evaluated in test set:")
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

if __name__ == '__main__':
    run_training()
