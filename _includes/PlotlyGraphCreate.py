import plotly.express as px
import plotly.io as pio
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/sqltechhead/sqltechhead.github.io/master/_includes/Skills.csv')
df.head()



fig = px.line(df,
                 x="Year", y="Level",color="Skill", 
                 log_x=True,
                 template="plotly_dark", title="Skills Over Time (1-10)")

pio.write_html(fig, file='SkillsGraph.html', auto_open=True)