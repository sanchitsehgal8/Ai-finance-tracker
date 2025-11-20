import plotly.express as px

# Use a dark template by default for Plotly charts so they display nicely
# on the dark Streamlit background.
try:
    px.defaults.template = 'plotly_dark'
except Exception:
    pass


def pie_chart(df, values: str, names: str, title: str = ''):
    return px.pie(df, values=values, names=names, title=title)
