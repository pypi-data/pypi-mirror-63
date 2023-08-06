import pandas as pd
import numpy as np

def central_standard(df):
    """
    Get the centalised and standardised numpy array
    
    Parameters:
     - df: A pandas DataFrame
    """
    x = df.values
    # Centralisation
    y = x - np.mean(x, axis=0)
    # Calculate the covariance matrix
    s = np.dot(np.transpose(y), y) / (x.shape[0] - 1)
    # Standardisation
    d = np.diag(s.diagonal()**(-1 / 2))
    z = np.dot(y, d)
    return z