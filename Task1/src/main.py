import data_profiling as dp
import pandas as pd
import visualize as vz
import matplotlib.pyplot as plt
from pathlib import Path

data = pd.read_csv(Path("biome-internship-projects/Task1/data/insurance.csv"))

# for age:
age_mean = dp.cal_mean(data, 'age')
age_median = dp.cal_median(data, 'age')
age_min = dp.cal_min(data, 'age')
age_max = dp.cal_max(data, 'age')
age_quantile_q1 = dp.cal_quantile(data, 'age', 0.25)
age_quantile_q3 = dp.cal_quantile(data, 'age', 0.75)

# for bmi:
bmi_mean = dp.cal_mean(data, 'bmi')
bmi_median = dp.cal_median(data, 'bmi')
bmi_min = dp.cal_min(data, 'bmi')
bmi_max = dp.cal_max(data, 'bmi')
bmi_quantile_q1 = dp.cal_quantile(data, 'bmi', 0.25)
bmi_quantile_q3 = dp.cal_quantile(data, 'bmi', 0.75)

# for children:
children_mean = dp.cal_mean(data, 'children')
children_median = dp.cal_median(data, 'children')
children_min = dp.cal_min(data, 'children')
children_max = dp.cal_max(data, 'children')
children_quantile_q1 = dp.cal_quantile(data, 'children', 0.25)
children_quantile_q3 = dp.cal_quantile(data, 'children', 0.75)

# for gender:
gender_count = data['sex'].value_counts()
gender_mode = dp.cal_mode(data, 'sex')

# for smoker:
smoker_count = data['smoker'].value_counts()
smoker_mode = dp.cal_mode(data, 'smoker')

# for region:
region_count = data['region'].value_counts()
region_mode = dp.cal_mode(data, 'region')

# for charges:
charges_mean = dp.cal_mean(data, 'charges')
charges_median = dp.cal_median(data, 'charges')
charges_min = dp.cal_min(data, 'charges')
charges_max = dp.cal_max(data, 'charges')
charges_quantile_q1 = dp.cal_quantile(data, 'charges', 0.25)
charges_quantile_q3 = dp.cal_quantile(data, 'charges', 0.75)


numeric_cols = ['age', 'bmi', 'children', 'charges']

for col in numeric_cols:
    fig = vz.plot_distribution(data, col)
    plt.show()

    fig = vz.plot_boxplot(data, col)
    plt.show()


categorical_cols = ['sex', 'smoker', 'region']

for col in categorical_cols:
    fig = vz.plot_countplot(data, col)
    plt.show()
