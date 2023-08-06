from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from processing import preprocessors as pp

import logging
from processing import config


_logger = logging.getLogger(__name__)

class PipelineBuilder():
    @staticmethod
    def create(alpha, random_state):

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
                ('Linear_model', Lasso(alpha=alpha, random_state=random_state))
            ]
        )

        return price_pipe
