import pandas as pd
import json, joblib

CURRENT_YEAR = 2025
TRAIN_COLUMNS = json.load(open("models/train_columns.json"))
SCALER = joblib.load("models/house_scaler.pkl")

def prepare_features_from_raw(record: dict) -> pd.DataFrame:
    
    size = float(record.get("Size_sqft", 0))
    bedrooms = float(record.get("Bedrooms", 0))
    bathrooms = float(record.get("Bathrooms", 0))
    year_built = int(record.get("YearBuilt", CURRENT_YEAR))
    location = str(record.get("Location", "City"))
    
    HouseAge = CURRENT_YEAR - year_built
    Rooms_per_1000sqft = (bedrooms + bathrooms) / (size / 1000) if size > 0 else 0.0
    Size_per_Bedroom = size / bedrooms if bedrooms > 0 else 0.0
    Is_City = 1 if location.lower() == "City" else 0
    
    row = {col: 0.0 for col in TRAIN_COLUMNS}

    for name, val in [
        ("Size_sqft", size),
        ("Bedrooms", bedrooms),
        ("Bathrooms", bathrooms),
        ("YearBuilt", year_built),
        ("HouseAge", HouseAge),
        ("Rooms_per_1000sqft", Rooms_per_1000sqft),
        ("Size_per_Bedroom", Size_per_Bedroom),
        ("Is_City", Is_City),
    ]:
        if name in row:
            row[name] = float(val)

    loc_col = f"Location_{location}"
    if loc_col in row:
        row[loc_col] = 1.0
    


    df_one = pd.DataFrame([row], columns=TRAIN_COLUMNS)

    
    if hasattr(SCALER, "feature_names_in_"):
        cols_to_scale = list(SCALER.feature_names_in_)
        df_one[cols_to_scale] = SCALER.transform(df_one[cols_to_scale])

    return df_one