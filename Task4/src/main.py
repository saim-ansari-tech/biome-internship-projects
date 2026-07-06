from preprocessing import Preprocessing
from encoding import Encoding
from feature_engineering import FeatureEngineering
from model import Model
import pandas as pd


def main():
    df = pd.read_csv(
        (
            "biome-internship-projects\\Task4\\data\\diabetic_data.csv"
        )
    )
    preproc = Preprocessing(df)
    preproc.clean_placeholder()
    preproc.transform_target()
    preproc.drop_cols(["encounter_id", "patient_nbr", "weight"])
    preproc.drop_category_rows("gender", "Unknown/Invalid")
    preproc.drop_rows_by_values("discharge_disposition_id", [11, 19, 20])
    preproc.handle_categorical_missing_vals(["payer_code"], "Unknown")
    preproc.handle_categorical_missing_vals(["medical_specialty"], "Unknown")
    preproc.handle_categorical_missing_vals(["race"], "Unknown")
    preproc.handle_rare_categories(cols=["medical_specialty"], min_count=100)
    preproc.handle_rare_categories(cols=["payer_code"], min_count=150)
    preproc.handle_rare_categories(cols=["admission_source_id"], min_count=20)
    preproc.convert_dtype_category(
        [
            "admission_type_id", "discharge_disposition_id",
            "admission_source_id"
        ]
    )
    pre_process_df = preproc.df

    fn = FeatureEngineering(pre_process_df)

    fn.transform_age()
    fn.total_visits()
    fn.long_stay()
    fn.high_medications()
    fn.multiple_diagnoses()
    fn.engineer_diagnosis_groups()
    fn.drop_original_diagnosis_cols()

    feature_engineered_df = fn.df

    encoder = Encoding(feature_engineered_df)

    one_hot_cols = [
        "race",
        "admission_type_id",
        "discharge_disposition_id",
        "admission_source_id",
        "payer_code",
        "medical_specialty",
        "diag_1_group",
        "diag_2_group",
        "diag_3_group",
        "max_glu_serum",
        "A1Cresult",
        "metformin",
        "repaglinide",
        "nateglinide",
        "chlorpropamide",
        "glimepiride",
        "acetohexamide",
        "glipizide",
        "glyburide",
        "tolbutamide",
        "pioglitazone",
        "rosiglitazone",
        "acarbose",
        "miglitol",
        "troglitazone",
        "tolazamide",
        "examide",
        "citoglipton",
        "insulin",
        "glyburide-metformin",
        "glipizide-metformin",
        "glimepiride-pioglitazone",
        "metformin-rosiglitazone",
        "metformin-pioglitazone",
    ]
    encoder.one_hot_encode(cols=one_hot_cols)
    encoder.binary_encode("gender", {"Male": 1, "Female": 0})
    encoder.binary_encode("change", {"Ch": 1, "No": 0})
    encoder.binary_encode("diabetesMed", {"Yes": 1, "No": 0})

    encoded_df = encoder.df

    model = Model(encoded_df)
    model.split_data(test_size=0.2, random_state=42)
    model.scale_data()
    print("Logistic Regression")
    model.train_LR()
    model.evaluate_model(model.y_test, model.lr_prediction)

    print("Random Forest")
    model.train_RF(no_trees=100, random_state_val=42)
    model.evaluate_model(model.y_test, model.rf_prediction)

    print("XGBoosting")
    model.train_XGB(evl_metric="logloss", random_state_val=42)
    model.evaluate_model(model.y_test, model.xgb_prediction)
    model.explain_model()


if __name__ == "__main__":
    main()
