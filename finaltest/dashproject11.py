from dash import Dash
import dash
from dash import dcc
from dash import html
# import dash_html_components as html
# import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd



# Load data
data = pd.read_csv("./datasets/reports_data.csv") #import dataset

# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div(
    children=[
        html.H1("Data Visualization for Emergency Response Management Services in Zimbabwe"),
        html.Div(
            children=[
                html.Label("Select a chart type:"),
                dcc.Dropdown(
                    id="chart-type",
                    options=[
                        {"label": "Bar Chart - Incidents by Type", "value": "bar"},
                        {"label": "Line Chart - Incidents over Time", "value": "line"},
                        {"label": "Pie Chart - Top 5 Incidents", "value": "pie"},
                        {"label": "Histogram - Incidents by Hour", "value": "histogram"},
                    ],
                    value="bar",
                ),
            ],
        ),
        dcc.Graph(id="chart"),
        # dcc.Graph(id="map"),
    ]
)

# Define callback function to update the chart based on user selection
@app.callback(
    dash.dependencies.Output("chart", "figure"),
    [dash.dependencies.Input("chart-type", "value")]
)
def update_chart(chart_type):
    if chart_type == "bar":
        # Create a bar chart of incidents by type
        incidents_by_type = data["title"].value_counts().reset_index()
        incidents_by_type.columns = ["Incident Type", "Count"]
        figure = px.bar(incidents_by_type, x="Incident Type", y="Count", color="Incident Type")
    elif chart_type == "line":
        # Create a line chart of incidents over time
        data["timeStamp"]=pd.to_datetime(data["timeStamp"], format="mixed")
        incidents_over_time = data.groupby(pd.to_datetime(data["timeStamp"]).dt.date).size().reset_index()
        incidents_over_time.columns = ["Date", "Count"]
        figure = px.line(incidents_over_time, x="Date", y="Count")
    elif chart_type == "pie":
        # Create a pie chart of top 5 incidents
        top_5_incidents = data["title"].value_counts().nlargest(5)
        figure = px.pie(top_5_incidents, names=top_5_incidents.index, values=top_5_incidents.values)
    elif chart_type == "histogram":
        # Create a histogram of incidents by hour
        data["timeStamp"]=pd.to_datetime(data["timeStamp"], format="mixed")
        data["Hour"] = pd.to_datetime(data["timeStamp"]).dt.hour
        figure = px.histogram(data, x="Hour", nbins=24)
    else:
        figure = go.Figure()

    return figure

# Define callback function to update the map based on user selection
# @app.callback(
#     dash.dependencies.Output("map", "figure"),
#     [dash.dependencies.Input("chart-type", "value")]
# )
# def update_map(chart_type):
#     if chart_type == "map":
#         # Create a map visualization of incidents
#         figure = px.scatter_mapbox(data, lat="lat", lon="lng", color="title", hover_data=["desc"],
#                                    zoom=10, height=500)
#         figure.update_layout(mapbox_style="open-street-map")
#         figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#     else:
#         figure = go.Figure()

#     return figure

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
