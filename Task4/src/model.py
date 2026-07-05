from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import shap
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    f1_score,
    recall_score,
    confusion_matrix,
    classification_report,
)


class Model:

    def __init__(self, df):
        self.df = df
        self.x = self.df.drop(columns=["readmitted"])
        self.y = self.df["readmitted"]

    def split_data(self, test_size, random_state):
        self.x_train, self.x_test, self.y_train,
        self.y_test = train_test_split(
            self.x,
            self.y,
            test_size=test_size,
            random_state=random_state,
            stratify=self.y,
        )

    def scale_data(self):
        self.scaler = StandardScaler()
        self.scaled_x_train = self.scaler.fit_transform(self.x_train)
        self.scaled_x_test = self.scaler.transform(self.x_test)

    def train_LR(self):
        self.lr = LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=42
        )
        self.lr.fit(self.scaled_x_train, self.y_train)

        self.lr_prediction = self.lr.predict(self.scaled_x_test)

    def train_RF(self, no_trees, random_state_val):
        self.rf = RandomForestClassifier(
            n_estimators=no_trees,
            class_weight="balanced",
            random_state=random_state_val,
        )
        self.rf.fit(self.x_train, self.y_train)

        self.rf_prediction = self.rf.predict(self.x_test)

    def train_XGB(self, evl_metric, random_state_val):
        scale_pos_weight = len(self.y_train[self.y_train == 0]) / len(
            self.y_train[self.y_train == 1]
        )
        self.xgb = XGBClassifier(
            scale_pos_weight=scale_pos_weight,
            eval_metric=evl_metric,
            random_state=random_state_val,
        )
        self.xgb.fit(self.x_train, self.y_train)

        self.xgb_prediction = self.xgb.predict(self.x_test)

    def explain_model(self):
        explainer = shap.Explainer(self.xgb)

        shap_values = explainer(self.x_test)
        shap.plots.beeswarm(shap_values, max_display=20)

    def evaluate_model(self, y_true, y_pred):
        print(f"Accuracy : {accuracy_score(y_true, y_pred):.4f}")
        print(f"Precision: {precision_score(y_true, y_pred,
                                            zero_division=0):.4f}")
        print(f"Recall   : {recall_score(y_true, y_pred,
                                         zero_division=0):.4f}")
        print(f"F1 Score : {f1_score(y_true, y_pred, zero_division=0):.4f}")

        print("\nClassification Report")
        print(classification_report(y_true, y_pred))

        print("\nConfusion Matrix")
        print(confusion_matrix(y_true, y_pred))
