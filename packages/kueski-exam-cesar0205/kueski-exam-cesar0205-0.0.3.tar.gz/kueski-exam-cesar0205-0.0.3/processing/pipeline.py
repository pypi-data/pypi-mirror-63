"""
Creates a pipeline according to configuration variables and external parameters
"""
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from processing import preprocessors as pp
import logging
from processing import config


_logger = logging.getLogger(__name__)

class PipelineBuilder():
    @staticmethod
    def create(model):
        """Creates an estimator pipeline and as argument we pass the model that will
        fit the data"""

        price_pipe = Pipeline(
            [
                ('feature_selector',
                    pp.FeatureSelector(variables=config.FEATURES)),
                ('categorical_imputer',
                    pp.CategoricalImputer(variables=config.CATEGORICAL_VARS_WITH_NA)),
                ('numerical_inputer',
                    pp.NumericalImputer(variables=config.NUMERICAL_VARS_WITH_NA)),
                ('rare_label_encoder',
                    pp.RareLabelCategoricalEncoder(
                        tol=0.01,
                        variables=config.CATEGORICAL_VARS)),
                ('categorical_encoder',
                    pp.CategoricalEncoder(variables=config.CATEGORICAL_VARS)),
                ('log_transformer',
                    pp.LogTransformer(variables=config.NUMERICALS_LOG_VARS)),
                ('scaler', MinMaxScaler()),
                ('Linear_model', model),
            ]
        )

        return price_pipe
