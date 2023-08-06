
"""
Utility functions to format and plot some graphs
"""
from sklearn.model_selection import learning_curve, validation_curve
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

def eval_metrics(actual, pred):
    """Basic evaluation metrics por regression tasks"""
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def clean_money_format(data_set, variable):
    """Removes commas and money symbol from string"""
    return data_set.apply(lambda x: float(x[variable].\
                            replace("$", "").\
                            replace(",", "")), axis = 1)

def print_learning_curve(model, X, y, train_sizes = [200, 400, 600, 800, 1000], cv = 5, title = "Learning curve", scoring = "neg_mean_squared_error"):
    """Prints the learning curve given an estimator and the data sizes"""
    train_sizes, train_scores, valid_scores = learning_curve(model, 
                                                             X, 
                                                             y, 
                                                             train_sizes= train_sizes, 
                                                             cv=cv, 
                                                             scoring = scoring)
    
    train_scores_mean = np.mean(np.sqrt(-train_scores), axis = 1)
    valid_scores_mean = np.mean(np.sqrt(-valid_scores), axis = 1)
    
    plt.plot(train_sizes, train_scores_mean, c= "b", label = "Training")
    plt.plot(train_sizes, valid_scores_mean, c= "r", label = "Validation")
    plt.legend(loc = "best")
    plt.title("Learning curve (" + title + ")")
    plt.xlabel("Training size")
    plt.ylabel("RMSE")
    plt.show()

def print_validation_curve(model, X, y, param_name, param_range, cv = 5, title = "Validation curve", scoring = "neg_mean_squared_error"):
    """Prints the learning curve given an estimator and hyperparameters"""
    train_scores, valid_scores = validation_curve(model, 
                                                X, 
                                                y, 
                                                param_name= param_name,
                                                param_range = param_range,
                                                cv = cv, 
                                                scoring = scoring)

    
    train_scores_mean = np.mean(np.sqrt(-train_scores), axis = 1)
    valid_scores_mean = np.mean(np.sqrt(-valid_scores), axis = 1)
    
    plt.plot(param_range, train_scores_mean, c= "b", label = "Training")
    plt.plot(param_range, valid_scores_mean, c= "r", label = "Validation")
    plt.legend(loc = "best")
    plt.title("Validation_curve (" + title + ")")
    plt.xlabel("Parameter ({})".format(param_name))
    plt.ylabel("RMSE")
    plt.show()


#print_validation_curve(pipeline, train_set, y_train, "Linear_model__alpha", [0.1, 0.5, 1, 10, 100, 1000, 10000])
