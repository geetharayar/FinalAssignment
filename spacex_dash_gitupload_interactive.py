# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("../spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

spacex_df['booster_color'] =  spacex_df['Booster Version Category']

# Function to assign color to launch outcome
def assign_marker_color(launch_booster):
    if launch_booster == 'B4':
        return 'Green' 
    elif  launch_booster == 'B5':
        return 'Blue'
    elif  launch_booster == 'FT':
        return 'Yellow'
    elif  launch_booster == 'v1.0':
        return 'Red'
    elif  launch_booster == 'v1.1':
        return 'White'

spacex_df['booster_color'] = spacex_df['Booster Version Category'].apply(assign_marker_color)
#print(spacex_df.head())

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            ],
                                            value='ALL',
                                            placeholder="Select Launch Site",
                                            searchable=True
                                            ),
                                html.Br(),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                #  TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[500, 8000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_fig1(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df
        fig1 = px.pie(filtered_df, values='class',names='Launch Site',title='All success-pie-chart')      
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site']==str(entered_site)]
        freq_df=filtered_df['class'].value_counts().to_frame()
        freq_df['count'] = freq_df['class']
        freq_df['class'] = freq_df.index  
        fig1 = px.pie(freq_df , values='count',names='class',title= entered_site)
    return fig1

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))


def get_fig2(entered_site,payload):
  
    filtered_df = spacex_df.loc[spacex_df['Payload Mass (kg)'] >= payload[0]]
    filpay_df = filtered_df.loc[filtered_df['Payload Mass (kg)'] <= payload[1]]
    if entered_site == 'ALL':
        fig2 = px.scatter(filpay_df , x="Payload Mass (kg)", y="class",color="Booster Version Category")
        fig2.update_layout(title='All site success-payload-scatter-chart', xaxis_title='Payload Mass(kg)', yaxis_title='class')
    else:
        # return the outcomes piechart for a selected site
        filpaysite_df = filpay_df[filpay_df['Launch Site']==str(entered_site)]
        fig2 = px.scatter(filpaysite_df, x="Payload Mass (kg)", y="class",color="Booster Version Category")
        title_sel = entered_site + " success-payload-scatter-chart"
        fig2.update_layout(title = title_sel, xaxis_title='Payload Mass(kg)', yaxis_title='Class')
    return fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
