import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from dash import dash_table
import pandas as pd
import plotly.express as px

# Set token
with open('/etc/secrets/mapbox_token', 'r') as f:
    token = f.read().strip()

# Read data and create scatter mapbox chart
coordinates_df = pd.read_csv('spa_location_coordinates.csv')
zip_code_df = pd.read_csv("zip_code_df.csv")[['zipcode', 'population', 'population_density', 'spas_per_cap', 'spas_per_zip']]
zip_code_df_2 = zip_code_df.copy(deep=True)
zip_code_df_2.columns = ['Zip Code', 'Population', 'Population Density (People / Sq Mi)', 'Spas per Capita', 'Spas per Zip Code']
zip_code_df['zipcode'] = zip_code_df['zipcode'].astype('str')
zip_table = zip_code_df_2.to_dict('records')
zip_table_columns = [{'name': col, 'id': col} for col in zip_code_df_2.columns]



fig1 = px.scatter_mapbox(coordinates_df, lat='lattitude', lon='longitude',
                         hover_name='BusinessName', hover_data=['BusinessName', 'ZIP', 'location'],
                         color_discrete_sequence=['navy'], opacity=.75, zoom=10, height=750)
fig1.update_layout(mapbox_style='mapbox://styles/nystrategy/clfczy9ld006a01p59bwlo8xt/draft',
                  mapbox_accesstoken=token, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

fig2 = px.bar(zip_code_df.sort_values("population_density", ascending=False), x='zipcode',
              y='population_density',
              title='Population Density by Zip Code',
              labels={"zipcode": "Zip Code", "population_density": "Population Density (people per sq mi)"},
              template="plotly_dark")

fig3 = px.scatter_mapbox(coordinates_df, lat='lattitude', lon='longitude',
                         hover_name='BusinessName', hover_data=['BusinessName', 'ZIP', 'location'],
                         color_discrete_sequence=['navy'], opacity=.75, zoom=10, height=750)
fig3.update_layout(mapbox_style='mapbox://styles/nystrategy/clffx8ozt001901nnm5i4pptw/draft',
                  mapbox_accesstoken=token, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

fig4 = px.bar(zip_code_df.sort_values("spas_per_cap", ascending=False), x='zipcode',
              y='spas_per_cap',
              title='Spas per Capita by Zip Code',
              labels={"zipcode": "Zip Code", "spas_per_cap": "Spas per Capita"},
              template="plotly_dark")

fig5 = px.bar(zip_code_df.sort_values("spas_per_zip", ascending=False), x='zipcode',
              y='spas_per_zip',
              title='Spas by Zip Code',
              labels={"zipcode": "Zip Code", "spas_per_zip": "Spas per Zip Code"},
              template="plotly_dark")

style_data_conditional = [
    {'if':
        {'row_index': 'odd'},
        'backgroundColor': 'rgba(101, 110, 242, .25)'},
    {'if':
        {'row_index': 'even'}, 
        'backgroundColor': 'rgba(17, 17, 17, .25)'}]
style_cell = {
    'fontFamily': 'sans-serif',
    'color': 'white'
}
style_header = {
    'backgroundColor': 'rgb(60, 60, 60)',
    'color': 'white',
    'fontWeight': 'bold'
}

fig6 = dash_table.DataTable(
                    id='zip-code-table',
                    columns=zip_table_columns,
                    data=zip_table,
                    sort_action='native',
                    sort_mode='multi',
                    page_size=20,
                    style_data_conditional=style_data_conditional,
                    style_cell=style_cell,
                    style_header=style_header
                )

# Define the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
])
server = app.server

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Las Vegas Demographic and Spa Location Report', className='page-title'), width=12)
    ], className='header mb-4'),

    # First map and bar chart
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H2('Population Density & Spa Locations', className='card-title chart-title'),
                    html.P('The map shows population density mapped as a filler color, with navy dots representing individual medspas.', className='card-text chart-subtitle'),
                    html.P('The bar chart beneath it ranks zip codes according to population density.', className='card-text chart-subtitle')
                ]),
                dbc.CardBody([
                    dcc.Graph(figure=fig1, className='card-img-top chart-img'),
                    html.Br(),
                    dcc.Graph(figure=fig2, className='card-img-top chart-img')
                ])
            ], className='chart-container mb-4')
        ], width=12),
    ]),

    # Second map and bar charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H2('Med Spas per Capita by Zip Code', className='card-title chart-title'),
                    html.P('The map shows spa concentration as a measure of spas per capita within each zip code mapped as a filler color, with navy dots representing individual medspas.'),
                    html.P('It is worth observing that the deep red zip codes reflecting the highest concentration of spas per capita are two zip codes in the heart of the famed Vegas Strip. As seen in the map above, this area does not have a high population density. The combination of these observations is easily attributable to the strong correlation of tourism in the area, rather than an appeal of commercial activities to primarily local residents which may be more prevalent farther from the Strip.', className='card-text chart-subtitle'),
                    html.P('The first bar chart ranks zip codes according to this same measure of medspas per capita.', className='card-text chart-subtitle'),
                    html.P('The second bar chart ranks zip codes according to the absolute number of spas per zip code.', className='card-text chart-subtitle')
                ]),
                dbc.CardBody([
                    dcc.Graph(figure=fig3, className='card-img-top chart-img'),
                    html.Br(),
                    dcc.Graph(figure=fig4, className='card-img-top chart-img'),
                    html.Br(),
                    dcc.Graph(figure=fig5, className='card-img-top chart-img')
                ])
            ], className='chart-container mb-4')
        ], width=12),
    ]),

    # Third row
    dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.H2('Zip Code Comparison of People and Spa Concentration', className='card-title chart-title'),
                html.P('This table lists details by zip code pertaining to demographics and spa availability across Las Vegas, NV.', className='card-text chart-subtitle'),
                html.P('The data in this table can be downloaded using the button below.', className='card-text chart-subtitle')
            ]),
            dbc.CardBody([
                fig6,
                html.Br(),
                html.Div(
                    [
                        dbc.Button("Download this Data", color="primary", id="btn_csv_dbc", className="mr-2"),
                        dcc.Download(id="download-dataframe-csv"),
                    ],
                    className="d-grid gap-2 col-6 mx-auto",
                )
            ])
        ], className='chart-container mb-4')
    ])
]),

    dbc.Row([
        dbc.Col([
            html.P([
                'Copyright © 2023 ',
                html.A('NY Strategy.', href='https://nystrategy.com')
            ], className='text-center')
        ], width=12)
    ], className='footer mt-4')
], fluid=True)


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv_dbc", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(zip_code_df_2.to_csv, "zipcode_data.csv")


if __name__ == '__main__':
    app.run_server(debug=True)