import plotly.express as px


def pie_chart(df, values: str, names: str, title: str = ''):
    return px.pie(df, values=values, names=names, title=title)
