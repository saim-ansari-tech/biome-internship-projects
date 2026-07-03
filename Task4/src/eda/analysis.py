import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(csv_path):
    df = pd.read_csv(csv_path)
    print(df.shape)
    return df


def clean_placeholder(df):

    df = df.replace("?", np.nan, inplace=True)


def dataset_summary(df):

    summary = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Duplicate Rows": df.duplicated().sum(),
        "Total Missing Values": int(df.isnull().sum().sum()),
        "Missing Percentage": round((df.isnull().sum() / df.size) * 100, 2),
    }
    return summary


def feature_summary(df, feature):

    summary = {
        "Feature": feature,
        "Data Type": str(df[feature].dtype),
        "Total Values": len(df),
        "Unique Values": df[feature].nunique(dropna=True),
        "Missing Count": df[feature].isnull().sum(),
        "Missing Percentage": round((df[feature].isnull().
                                    sum() / len(df)) * 100, 2),
        "Question Mark Count": (df[feature] == "?").sum(),
        "Most Frequent Value": (
            df[feature].mode().iloc[0]
            if not df[feature].mode().empty else np.nan
        ),
        "Most Frequent Count": df[feature].value_counts(dropna=False).iloc[0],
    }
    return summary


def missing_value_report(df):

    report = pd.DataFrame(
        {
            "Feature": df.columns,
            "Missing Count": df.isnull().sum().values,
            "Missing Percentage": (
                df.isnull().sum() / len(df) * 100
            ).round(2).values,
        }
    )
    report = report.sort_values(
        by="Missing Percentage",
        ascending=False
    ).reset_index(drop=True)

    return report


def question_mark_report(df):

    report = pd.DataFrame(
        {
            "Feature": df.columns,
            "Question Mark Count": (df == "?").sum().values,
            "Question Mark Percentage": ((df == "?").sum() / len(df) * 100)
            .round(2)
            .values,
        }
    )

    report = report[report["Question Mark Count"] > 0]
    report = (
        report.sort_values(
            by="Question Mark Count",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return report


def duplicated_report(df):

    report = {
        "Total Rows": len(df),
        "Duplicate Rows": df.duplicated().sum(),
        "Duplicate Percentage": round(
            (df.duplicated().sum() / len(df)) * 100,
            2),
    }

    return report


def value_distribution(df, feature):

    counts = df[feature].value_counts(dropna=False)
    percentages = (df[feature].value_counts(dropna=False,
                                            normalize=True) * 100).round(
        2
    )

    report = pd.DataFrame(
        {
            "Value": counts.index,
            "Count": counts.values,
            "Percentage": percentages.values,
        }
    )

    return report


def numerical_summary(df, feature):

    summary = {
        "Feature": feature,
        "Mean": df[feature].mean(),
        "Median": df[feature].median(),
        "Mode": df[feature].mode().iloc[0],
        "Minimum": df[feature].min(),
        "Maximum": df[feature].max(),
        "Standard Deviation": df[feature].std(),
        "Variance": df[feature].var(),
        "Skewness": df[feature].skew(),
        "Kurtosis": df[feature].kurt(),
        "Q1": df[feature].quantile(0.25),
        "Q2": df[feature].quantile(0.50),
        "Q3": df[feature].quantile(0.75),
    }

    return summary


def categorical_summary(df, feature):

    summary = {
        "Feature": feature,
        "dtype": df[feature].dtype(),
        "No of Cat": df[feature].nunique(),
        "Missing count": df[feature].isnull().sum(),
        "Missing Percentage": round(df[feature].isnull().mean() * 100, 2),
        "Mode": df[feature].mode(dropna=True),
        "Mode freq": df[feature].value_counts(dropna=False).iloc[0],
    }
    return summary


def outlier_report(df, feature):

    q1 = df[feature].quantile(0.25)
    q3 = df[feature].quantile(0.75)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    upper = q1 + 1.5 * iqr
    outliers = df[(df[feature] < low) | (df[feature] > upper)]

    summary = {
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "Lower Bound": low,
        "Upper Bound": upper,
        "Outlier Count": len(outliers),
        "Outlier Percentage": round(len(outliers) / len(df) * 100, 2),
    }
    return summary


def correlation_matrix(df):

    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr()

    return corr


def plot_histogram(df, feature):

    plt.Figure(figsize=(5, 5))
    sns.histplot(data=df, x=feature, kde=True)
    plt.show()


def plot_boxplot(df, feature):

    plt.Figure(figsize=(5, 5))
    sns.boxplot(data=df, x=feature)
    plt.show()


def plot_countplot(df, feature):

    plt.Figure(figsize=(5, 5))
    sns.countplot(data=df, x=feature)
    plt.show()


def plot_missing_values(df):

    missing_percentage = (df.isnull().sum() / len(df)) * 100
    missing_percentage = missing_percentage[missing_percentage > 0]
    missing_percentage = missing_percentage.sort_values(ascending=False)

    if missing_percentage.empty:
        print("No missing values found in the dataset.")
        return None

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=missing_percentage.index, y=missing_percentage.values, ax=ax)

    ax.set_title("Missing Value Percentage by Feature")
    ax.set_xlabel("Features")
    ax.set_ylabel("Missing Percentage (%)")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    return fig
