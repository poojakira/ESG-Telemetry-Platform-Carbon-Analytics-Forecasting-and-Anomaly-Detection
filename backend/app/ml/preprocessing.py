import pandas as pd

def preprocess_data(df: pd.DataFrame):
    """
    Splits the dataframe into X (Features) and y (Target).
    """
    # 1. Define the target column (from your new dataset)
    target = 'total_lifecycle_carbon_footprint'
    
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataset!")

    # 2. Separate X and y
    y = df[target]
    X = df.drop(columns=[target])
    
    # 3. Drop non-training columns if they exist (IDs, dates)
    # Your new dataset doesn't have IDs, but this is safe to keep
    ignore_cols = ['Product_ID', 'Date', 'Compliance_Status']
    X = X.drop(columns=[c for c in ignore_cols if c in X.columns])
    
    return X, y