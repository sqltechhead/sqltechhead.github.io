import plotly.express as px
import plotly.io as pio

df = px.data.gapminder()
df_2007 = df.query("year==2007")

fig = px.scatter(df_2007,
                 x="gdpPercap", y="lifeExp", size="pop", color="continent",
                 log_x=True, size_max=60,
                 template="plotly_dark", title="Gapminder 2007: '%s' theme" % "plotly_dark")

pio.write_html(fig, file='figure.html', auto_open=False)