"""
Splits the original dataset into train, test and dev sets
"""

from processing.data_management import load_dataset, save_dataset
from sklearn.model_selection import train_test_split
from processing import config
import logging
import pandas as pd

_logger = logging.getLogger(__name__)

RANDOM_STATE = 0 
SPLIT_PCT = 0.1 #Percetage corresponding to the test and dev sets


def split_data() -> None:

    data = load_dataset(config.ORIGINAL_DATA_FILE)
    data_train, data_test = train_test_split(data, test_size=SPLIT_PCT, random_state=RANDOM_STATE)
    data_train, data_dev = train_test_split(data_train, test_size=SPLIT_PCT, random_state=RANDOM_STATE)

    save_dataset(data_train, config.TRAIN_DATA_FILE)
    save_dataset(data_dev, config.DEV_DATA_FILE)
    save_dataset(data_test, config.TEST_DATA_FILE)

if __name__ == '__main__':
    split_data()
