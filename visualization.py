import plotly.graph_objects as go
import plotly.express as px


def plotBar(df, x, y,  title="default title", color_continuous_scale="rainbow", width=1400, height=600):
    fig = px.bar(df,
                 x=x,
                 y=y,
                 #  color=color,
                 color_continuous_scale=color_continuous_scale,
                 title=title,
                 width=width,
                 height=height)
    return fig
