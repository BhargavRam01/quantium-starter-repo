import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load processed data
df = pd.read_csv("formatted_output.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"], dayfirst=True)

# Create month column
df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

# Aggregate monthly sales
monthly_sales = (
    df.groupby("month")["Sales"]
    .sum()
    .reset_index()
    .sort_values("month")
)

# Create line chart
fig = px.line(
    monthly_sales,
    x="month",
    y="Sales",
    title="Monthly Pink Morsel Sales Over Time"
)

fig.update_traces(mode="lines")

fig.update_layout(
    template="plotly_white",
    height=600,
    xaxis=dict(
        title="Month",
        tickformat="%b %Y",
        tickangle=45
    ),
    yaxis=dict(
        title="Total Sales ($)",
        tickformat=",.0f"
    )
)

# Add price increase vertical line
price_change = pd.to_datetime("2021-01-15")

fig.add_shape(
    type="line",
    x0=price_change,
    x1=price_change,
    y0=0,
    y1=monthly_sales["Sales"].max(),
    line=dict(color="red", dash="dash")
)

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Dashboard"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)