import json
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from io import StringIO
import dash_table




# Load the GeoJSON file
with open('tehsil.geojson', 'r') as file:
    geojson_data = json.load(file)

# Assuming df_tehsil_presence is your DataFrame containing the CSV data
# Here, you replace 'path_to_your_csv.csv' with the actual path to your CSV
# df_tehsil_presence = pd.read_csv('path_to_your_csv.csv')
    

# Simulated CSV data creation (You would replace this part with actual data loading)
csv_data = """
Tehsil,Child Stunting Rate (%),Access to Clean Water (%),Basic Healthcare Availability
Mithi,45,60,1
Thatta,40,70,0
Umerkot,50,65,1
Hyderabad,35,75,1
Sukkur,42,68,1
Larkana,48,62,0
Mirpurkhas,38,69,1
Nawabshah,41,67,0
Jacobabad,49,61,1
Shikarpur,47,63,0
Khairpur,43,70,1
Badin,36,72,1
Tando Allahyar,39,71,1
Tando Muhammad Khan,44,66,0
Ghotki,37,74,1
Sanghar,46,64,0
Naushahro Feroze,51,60,1
Dadu,34,73,0
Jamshoro,52,59,1
Kashmore,53,58,0
Tharparkar,54,57,1
Umarkot,55,56,0
Sujawal,33,76,1
Matli,31,77,0
Hala,32,78,1
Digri,29,79,0
Kot Ghulam Muhammad,30,80,1
Shahdadkot,28,81,0
Kandhkot,27,82,1
Rohri,26,83,0
"""

# Partner activity data (simplified for demonstration)
partner_data = {
    'Tehsil': ['Dadu', 'Kotri', 'Shikarpur', 'Thatta', 'Umerkot'],
    'Partner Activity': [1, 1, 1, 1, 1]  # 1 indicates active partner project
}

df_partner_activity = pd.DataFrame(partner_data)

# Convert CSV string to DataFrame
df_tehsil_stats = pd.read_csv(StringIO(csv_data))

# Merge KPI data with partner activity data
df_merged = pd.merge(df_tehsil_stats, df_partner_activity, on='Tehsil', how='left')
df_merged['Partner Activity'] = df_merged['Partner Activity'].fillna(0)  # Fill NaN with 0 for tehsils without partner activity

# Use StringIO to simulate reading the CSV content
# data = StringIO(csv_data)

# Creating a choropleth map for Child Stunting Rate
# Update choropleth map to highlight tehsils with partner activities
fig_map = px.choropleth_mapbox(df_merged, 
                               geojson=geojson_data, 
                               locations='Tehsil', 
                               color='Child Stunting Rate (%)',
                               featureidkey="properties.ADM3_EN", 
                               hover_data=['Tehsil', 'Partner Activity'],
                               mapbox_style="carto-positron", 
                               zoom=5, 
                               center={"lat": 30.3753, "lon": 69.3451}, 
                               opacity=0.5)

# Creating a bar chart for Child Stunting Rate by Tehsil
fig_bar = px.bar(df_tehsil_stats, x='Tehsil', y='Child Stunting Rate (%)', title="Child Stunting Rate by Tehsil")

# Creating a pie chart for Access to Clean Water
fig_pie = px.pie(df_tehsil_stats, names='Tehsil', values='Access to Clean Water (%)', title="Access to Clean Water by Tehsil")

app = dash.Dash(__name__)
server = app.server
# App layout
app.layout = html.Div([
    html.H1('Child Stunting Dashboard', style={'textAlign': 'center'}),
    html.P('This dashboard provides an overview of Child stunting and EUD Programme activities for Improved Nutrition in Sindh.', style={'textAlign': 'center'}),
    html.Div(style={'display': 'flex', 'flexDirection': 'row'}, children=[
        html.Div(style={'width': '50%', 'paddingRight': '20px'}, children=[
            html.Div([
                html.H3('Controls', style={'padding': '10px', 'backgroundColor': '#f0f0f0', 'borderRadius': '5px', 'textAlign': 'center'}),
                dcc.Dropdown(
                    id='filter_dropdown',
                    options=[{'label': 'Access to Clean Water', 'value': 'OPT1'}, {'label': 'Basic Healthcare Availability', 'value': 'OPT2'}],
                    placeholder='Select a KPI...',
                    style={'marginBottom': '20px', 'width': '90%'}
                )
            ], style={'marginBottom': '20px'}),
            dcc.Graph(figure=fig_bar, style={'height': '30vh'}),
            dash_table.DataTable(
                id='partner_activity_table',
                columns=[{"name": i, "id": i} for i in df_merged.columns],
                data=df_merged.to_dict('records'),
                style_cell={'padding': '5px'},
                style_as_list_view=True,
                style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},
                style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}],
                style_table={'overflowX': 'auto', 'height': '30vh'}
            )
        ]),
        html.Div(style={'width': '50%'}, children=[
            dcc.Graph(figure=fig_map, style={'height': '90vh'})
        ])
    ])
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'height': '100vh', 'boxSizing': 'border-box'})




if __name__ == '__main__':
    app.run_server(debug=True)