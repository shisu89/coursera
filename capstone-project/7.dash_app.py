# Import required libraries
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_site_list = spacex_df['Launch Site'].unique().tolist()
dropdown_options = ['All Sites']+launch_site_list

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(id='site-dropdown', options=dropdown_options, placeholder='Select a Launch Site', value='All Sites', searchable=True),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(id='payload-slider', min=0, max=max_payload, step=1, value=[min_payload, max_payload], marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
        ]
        )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def pie_chart(site_dropdown):
    if site_dropdown == 'All Sites':
        df = spacex_df.groupby(['Launch Site']).sum().reset_index()
        fig = px.pie(df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        
        df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        #show the Success vs. Failed counts for the site
        df = df.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(df, values='class count', names='class', title='Total Success Launches By Site')

        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])
def scatter_chart(site_dropdown, payload_slider):
    if site_dropdown == 'All Sites':
        df = spacex_df
        df = df[(df['Payload Mass (kg)'] >= payload_slider[0]) & (df['Payload Mass (kg)'] <= payload_slider[1])]
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for All Sites')
        return fig
    else:
        df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        df = df[(df['Payload Mass (kg)'] >= payload_slider[0]) & (df['Payload Mass (kg)'] <= payload_slider[1])]
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for All Sites')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)