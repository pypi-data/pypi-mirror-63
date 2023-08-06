import os
import pathlib
import logging


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / 'trained_models'
DATASET_DIR = PACKAGE_ROOT / 'data'

print("This is {}-{}".format(TRAINED_MODEL_DIR, DATASET_DIR))

# data
ORIGINAL_DATA_FILE = 'listings_reduced.csv'
TRAIN_DATA_FILE = 'train_set.csv'
DEV_DATA_FILE = 'dev_set.csv'
TEST_DATA_FILE = 'test_set.csv'

TARGET = 'price'

# variables
FEATURES = ['host_id', 'latitude', 'accommodates', 'minimum_nights',
       'maximum_nights', 'availability_90', 'number_of_reviews',
       'review_scores_cleanliness', 'review_scores_location']


# numerical variables with NA in train set
NUMERICAL_VARS_WITH_NA = ['review_scores_cleanliness', 'review_scores_location']

# categorical variables with NA in train set
CATEGORICAL_VARS_WITH_NA = []

TEMPORAL_VARS = 'YearRemodAdd'

# variables to log transform
NUMERICALS_LOG_VARS = ['latitude', 'minimum_nights', 'maximum_nights',
                        'availability_90', 'number_of_reviews']

# categorical variables to encode
CATEGORICAL_VARS = []

NUMERICAL_NA_NOT_ALLOWED = [
    feature for feature in FEATURES
    if feature not in CATEGORICAL_VARS + NUMERICAL_VARS_WITH_NA
]

CATEGORICAL_NA_NOT_ALLOWED = [
    feature for feature in CATEGORICAL_VARS
    if feature not in CATEGORICAL_VARS_WITH_NA
]


PIPELINE_NAME = 'lasso_regression'
PIPELINE_SAVE_FILE = f'{PIPELINE_NAME}_output_v'

# used for differential testing
ACCEPTABLE_MODEL_DIFFERENCE = 0.05
