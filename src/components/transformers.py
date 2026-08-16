from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class RatioFeatureEngineering(BaseEstimator,TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self,X,y=None):
        
        return self
    
    def transform(self,X):
        X=X.copy()
    
        X['Balance_to_Salary'] = X['balance'] / (X['estimated_salary'] + 1e-6)
        X['Tenure_to_Age'] = X['tenure'] / X['age']
        X['Active_Product_Multiplier'] = X['active_member'] * X['products_number']
        X['Credit_Score_per_Age'] = X['credit_score'] / X['age']
        
        return X
        
        
        