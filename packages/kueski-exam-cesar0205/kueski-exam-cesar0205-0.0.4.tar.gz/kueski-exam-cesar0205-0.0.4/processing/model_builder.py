"""
Buils scikit-learn estimators using a factory
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression
import inspect

class ModelBuilder():
    """ Factory that creates models based on the name key and parameters"""
    def __init__(self):
        self.creator = {}
        self.creator["LinearRegression"] = LinearRegression
        self.creator["RandomForestRegressor"] = RandomForestRegressor
        self.creator["Lasso"] = Lasso


    def create(self, model, params, random_state):
        if "random_state" in inspect.getfullargspec(self.creator[model].__init__).args:
            params.update({"random_state": random_state})
        return self.creator[model](**params)