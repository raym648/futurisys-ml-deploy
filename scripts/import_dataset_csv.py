# futurisys-ml-deploy/scripts/import_dataset_csv.py

from src.data.loader import load_csv_to_db

if __name__ == "__main__":
    load_csv_to_db("data/processed/e01_df_central_left_clean.csv")
