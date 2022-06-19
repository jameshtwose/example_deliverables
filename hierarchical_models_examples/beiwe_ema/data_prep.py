#%%
import pandas as pd
import numpy as np
from glob import glob
import seaborn as sns
import matplotlib.pyplot as plt

#%%
if "jms_style_sheet" in plt.style.available:
    plt.style.use("jms_style_sheet")

# %%
csv_list = glob("UT1000_ema/*/*/*/daily_emas*.csv")
# %%
df_long = (pd.concat([pd.read_csv(x, index_col=[0]) for x in csv_list])
           .assign(**{"date": lambda d: pd.to_datetime(d["survey.date"])}))
# %%
df_wide = df_long.pivot_table(index=["pid", "survey.date"], columns="variable")
df_wide.columns=df_wide.columns.get_level_values(level=1)
# %%
display(df_wide.head()); df_wide.info()

#%%
display(df_long.head()); df_long.info()

# %%
def jitter(values,j):
    return values + np.random.normal(j,0.1,values.shape)
plot_df = df_long.assign(**{"answer_jitter": lambda d: jitter(d["answer"], 3)})
_ = plt.figure(figsize=(20, 5))
_ = sns.scatterplot(data=plot_df, x="date", 
                    y="answer_jitter", hue="variable",
                    alpha=0.8)

# %%
df_wide.to_csv("data/UT1000_ema_wide.csv")
df_long.to_csv("data/UT1000_ema_long.csv")
# %%
