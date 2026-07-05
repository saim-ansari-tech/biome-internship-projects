from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
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
        self.scaled_x_test = self.scaler.fit_transform(self.x_test)

    def train_LR(self):
        self.lr = LogisticRegression()
        self.lr.fit(self.scaled_x_train, self.y_train)

        self.lr_prediction = self.lr.predict(self.scaled_x_test)

    def train_RF(self, no_trees, random_state_val):
        self.rf = RandomForestClassifier(
            n_estimators=no_trees, random_state=random_state_val
        )
        self.rf.fit(self.x_train, self.y_train)

        self.rf_prediction = self.rf.predict(self.x_test)

    def train_XGB(self, evl_metric, random_state_val):
        self.xgb = XGBClassifier(eval_metric=evl_metric,
                                 random_state=random_state_val)
        self.xgb.fit(self.x_train, self.y_train)

        self.xgb_prediction = self.xgb.predict(self.x_test)

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
