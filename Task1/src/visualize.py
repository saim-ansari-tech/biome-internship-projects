import matplotlib.pyplot as plt
import seaborn as sns


def plot_distribution(df, col):
    fig, ax = plt.subplots()
    sns.histplot(df[col], kde=True, ax=ax)
    ax.axvline(df[col].mean(), color='red', linestyle='--', label='Mean')
    ax.axvline(df[col].median(), color='green', linestyle='--', label='Median')
    ax.set_title(f"Distribution of {col}")
    ax.legend()
    return fig


def plot_boxplot(df, col):
    fig, ax = plt.subplots()
    sns.boxplot(y=df[col], ax=ax)
    ax.set_title(f"Boxplot of {col}")
    return fig


def plot_countplot(df, col):
    fig, ax = plt.subplots()
    sns.countplot(x=col, data=df, ax=ax)
    ax.set_title(f"Count of {col}")
    return fig


def plot_charges_by_smoker(df):
    fig, ax = plt.subplots()
    sns.boxplot(x='smoker', y='charges', data=df, ax=ax)
    ax.set_title("Charges by Smoker Status")
    return fig


def plot_age_vs_charges(df):
    fig, ax = plt.subplots()
    sns.scatterplot(x='age', y='charges', hue='smoker',
                    data=df, ax=ax, alpha=0.6)
    ax.set_title("Age vs Charges (colored by Smoker)")
    return fig


def plot_correlation_heatmap(df):
    df_enc = df.copy()
    df_enc['smoker'] = df_enc['smoker'].map({'yes': 1, 'no': 0})
    corr_cols = ['age', 'bmi', 'children', 'smoker', 'charges']
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(df_enc[corr_cols].corr(), annot=True,
                cmap='coolwarm', fmt='.2f', ax=ax)
    ax.set_title("Correlation Heatmap")
    return fig
