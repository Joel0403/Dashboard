# Import necessary libraries
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('DASHBOARD_DATA.csv')  # Adjust the path to your dataset

# Preprocessing functions
def preprocess_data_for_timeline(df):
    df['StartDate'] = pd.to_datetime(df['StartDate'], errors='coerce')
    df['ActualFinished'] = pd.to_datetime(df['ActualFinished'], errors='coerce')
    filtered_df = df.dropna(subset=['StartDate', 'ActualFinished'])
    filtered_df = filtered_df.sort_values(by='StartDate')
    return filtered_df

def preprocess_data_for_performance(df):
    performance_df = df.groupby('AssignTo').agg({'Total Cost': 'sum'}).reset_index()
    return performance_df

def preprocess_data_for_efficiency(df):
    df['Efficiency'] = df['Total Cost'] / df['Estimates']
    efficiency_df = df[['Sprint', 'Module', 'Efficiency']].dropna()
    return efficiency_df

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Dropdown(
        id='project-selector',
        options=[{'label': i, 'value': i} for i in df['Sprint'].unique()],
        value=df['Sprint'].unique()[0]
    ),
    dcc.Graph(id='project-timeline'),
    dcc.Graph(id='team-performance'),
    dcc.Graph(id='efficiency-metrics'),
])

# Callbacks for updating the visualizations
@app.callback(
    Output('project-timeline', 'figure'),
    [Input('project-selector', 'value')]
)
def update_project_timeline(selected_sprint):
    filtered_df = preprocess_data_for_timeline(df[df['Sprint'] == selected_sprint])
    fig = px.timeline(filtered_df, x_start='StartDate', x_end='ActualFinished', y='Module', color='Priority', title='Project Timeline')
    return fig

@app.callback(
    Output('team-performance', 'figure'),
    [Input('project-selector', 'value')]
)
def update_team_performance(selected_sprint):
    filtered_df = preprocess_data_for_performance(df[df['Sprint'] == selected_sprint])
    fig = px.bar(filtered_df, x='AssignTo', y='Total Cost', title='Team Performance')
    return fig

@app.callback(
    Output('efficiency-metrics', 'figure'),
    [Input('project-selector', 'value')]
)
def update_efficiency_metrics(selected_sprint):
    filtered_df = preprocess_data_for_efficiency(df[df['Sprint'] == selected_sprint])
    fig = px.scatter(filtered_df, x='Module', y='Efficiency', color='Sprint', title='Efficiency Metrics')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
