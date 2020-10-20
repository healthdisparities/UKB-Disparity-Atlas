# Python imports
## General libraries
import pathlib
import os
import math
from random import randint
import pandas as pd

# Plotting bits
import plotly.express as px

## Dash components
import dash
import dash_table
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

# Deployment
import flask

# Local imports
import components
import tab_populator

## App setup
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
# server = app.server

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))


###############################################################################
#################################  MODEL   ####################################
###############################################################################

# Getting paths
# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

'''
First, we'll process the view tables ( these tables will populate the searchable 
tables from which a trait will be chosen ).

This will have to be done for each type of disparity.
'''

## Grouping - Sex
sex_table_data = pd.read_csv(DATA_PATH.joinpath("sex_selection_table.txt"), sep = '\t')
sex_table_data.loc[:, 'Variance'] = 0.5*(sex_table_data['Difference'] ** 2)
sex_table_data.loc[:, 'Variance'] = sex_table_data.loc[:, 'Variance'].round(2)

sex_table_data.loc[:, 'Difference'] = sex_table_data.loc[:, 'Difference'].round(2)
sex_table_data['id'] = sex_table_data['Phenotype']
sex_table_data.set_index('id', inplace = True, drop = False)
sex_table_data = sex_table_data.sort_values(by = ['Variance'], ascending = False)

## Grouping - Age
age_table_data = pd.read_csv(DATA_PATH.joinpath("age_selection_table.txt"), sep = '\t')
age_table_data.loc[:, 'Maximum Difference'] = age_table_data.loc[:, 'Maximum Difference'].round(2)
age_table_data['id'] = age_table_data['Phenotype']
age_table_data.set_index('id', inplace = True, drop = False)
age_table_data = age_table_data.sort_values(by = ['Variance'], ascending = False)

## Grouping - Ethnic Group
ethnic_table_data = pd.read_csv(DATA_PATH.joinpath("ethnic_selection_table.txt"), sep = '\t')
ethnic_table_data.loc[:, 'Maximum Difference'] = ethnic_table_data.loc[:, 'Maximum Difference'].round(2)
ethnic_table_data['id'] = ethnic_table_data['Phenotype']
ethnic_table_data.set_index('id', inplace = True, drop = False)
ethnic_table_data = ethnic_table_data.sort_values(by = ['Variance'], ascending = False)

## Grouping - Socio-economic status
ses_table_data = pd.read_csv(DATA_PATH.joinpath("ses_selection_table.txt"), sep = '\t')
ses_table_data.loc[:, 'Maximum Difference'] = ses_table_data.loc[:, 'Maximum Difference'].round(2)
ses_table_data['id'] = ses_table_data['Phenotype']
ses_table_data.set_index('id', inplace = True, drop = False)
ses_table_data = ses_table_data.sort_values(by = ['Variance'], ascending = False)

'''
Next, we'll process data for the prevalence tables
'''
## Grouping - Sex
sex_prev_data = pd.read_csv(DATA_PATH.joinpath("sex_prev_table.txt"), sep = '\t')
sex_prev_data['id'] = sex_prev_data['Phenotype']
sex_prev_data.set_index('id', inplace = True, drop = False)

## Grouping - Age
age_prev_data = pd.read_csv(DATA_PATH.joinpath("age_prev_table.txt"), sep = '\t')
age_prev_data['id'] = age_prev_data['Phenotype']
age_prev_data.set_index('id', inplace = True, drop = False)

## Grouping - Ethnic Group
ethnic_prev_data = pd.read_csv(DATA_PATH.joinpath("ethnic_prev_table.txt"), sep = '\t')
ethnic_prev_data['id'] = ethnic_prev_data['Phenotype']
ethnic_prev_data.set_index('id', inplace = True, drop = False)

## Grouping - Socio-economic status
ses_prev_data = pd.read_csv(DATA_PATH.joinpath("ses_prev_table.txt"), sep = '\t')
ses_prev_data.columns = ['Phenotype', 'PheCode', 'First Quintile of Deprivation', 'Second Quintile of Deprivation', 'Third Quintile of Deprivation', 'Fourth Quintile of Deprivation' ,'Fifth Quintile of Deprivation']
ses_prev_data['id'] = ses_prev_data['Phenotype']
ses_prev_data.set_index('id', inplace = True, drop = False)

'''
Fianlly, we process data for visualization.
'''

## Grouping - Sex
sex_plotting_data = pd.read_csv(DATA_PATH.joinpath("sex_plotting.txt"), sep = '\t')
sex_plotting_data['id'] = sex_plotting_data['Phenotype']
sex_plotting_data.set_index('id', inplace = True, drop = False)
sex_plotting_data.columns = ['PheCode', 'Phenotype', 'Trait', 'Prevalence', 'Cases', 'Controls', 'id']
sex_plotting_data = sex_plotting_data.astype({'Cases': 'int32', 'Controls' : 'int32'})
sex_plotting_data['Pretty_cases'] = sex_plotting_data['Cases'].map("{:,}".format)
sex_plotting_data['Pretty_controls'] = sex_plotting_data['Controls'].map("{:,}".format)
sex_plotting_data.loc[sex_plotting_data['Trait'] == 'Total', 'Trait'] = 'Overall'

## Grouping - Age
age_plotting_data = pd.read_csv(DATA_PATH.joinpath("age_plotting.txt"), sep = '\t')
age_plotting_data['id'] = age_plotting_data['Phenotype']
age_plotting_data.set_index('id', inplace = True, drop = False)
age_plotting_data.columns = ['PheCode', 'Phenotype', 'Trait', 'Prevalence', 'Cases', 'Controls', 'id']
age_plotting_data = age_plotting_data.astype({'Cases': 'int32', 'Controls' : 'int32'})
age_plotting_data['Pretty_cases'] = age_plotting_data['Cases'].map("{:,}".format)
age_plotting_data['Pretty_controls'] = age_plotting_data['Controls'].map("{:,}".format)
age_plotting_data.loc[age_plotting_data['Trait'] == 'Total', 'Trait'] = 'Overall'

## Grouping - Ethnic Group
ethnic_plotting_data = pd.read_csv(DATA_PATH.joinpath("ethnic_plotting.txt"), sep = '\t')
ethnic_plotting_data['id'] = ethnic_plotting_data['Phenotype']
ethnic_plotting_data.set_index('id', inplace = True, drop = False)
ethnic_plotting_data.columns = ['PheCode', 'Phenotype', 'Trait', 'Prevalence', 'Cases', 'Controls', 'id']
ethnic_plotting_data = ethnic_plotting_data.astype({'Cases': 'int32', 'Controls' : 'int32'})
ethnic_plotting_data['Pretty_cases'] = ethnic_plotting_data['Cases'].map("{:,}".format)
ethnic_plotting_data['Pretty_controls'] = ethnic_plotting_data['Controls'].map("{:,}".format)
ethnic_plotting_data.loc[ethnic_plotting_data['Trait'] == 'Any other white background', 'Trait'] = 'Other White'
ethnic_plotting_data.loc[ethnic_plotting_data['Trait'] == 'Any other mixed background', 'Trait'] = 'Other Mixed'
ethnic_plotting_data.loc[ethnic_plotting_data['Trait'] == 'Any other Black background', 'Trait'] = 'Other Black'
ethnic_plotting_data.loc[ethnic_plotting_data['Trait'] == 'Any other Asian background', 'Trait'] = 'Other Asian'
ethnic_plotting_data = ethnic_plotting_data.loc[~ethnic_plotting_data['Trait'].isin(['Prefer not to answer', 'Do not know', 'Other ethnic group', 'Chinese (all)']),:]
ethnic_plotting_data.loc[ethnic_plotting_data['Trait'] == 'Total', 'Trait'] = 'Overall'

## Grouping - Socio-economic status
ses_plotting_data = pd.read_csv(DATA_PATH.joinpath("ses_plotting.txt"), sep = '\t')
ses_plotting_data['id'] = ses_plotting_data['Phenotype']
ses_plotting_data.set_index('id', inplace = True, drop = False)
ses_plotting_data.columns = ['PheCode', 'Phenotype', 'Trait', 'Prevalence', 'Cases', 'Controls', 'id']
ses_plotting_data = ses_plotting_data.astype({'Cases': 'int32', 'Controls' : 'int32'})
ses_plotting_data['Pretty_cases'] = ses_plotting_data['Cases'].map("{:,}".format)
ses_plotting_data['Pretty_controls'] = ses_plotting_data['Controls'].map("{:,}".format)
ses_plotting_data.loc[ses_plotting_data['Trait'] == '1', 'Trait'] = 'First Quintile of Deprivation<br>(Least Deprived)'
ses_plotting_data.loc[ses_plotting_data['Trait'] == '2', 'Trait'] = 'Second Quintile of Deprivation'
ses_plotting_data.loc[ses_plotting_data['Trait'] == '3', 'Trait'] = 'Third Quintile of Deprivation'
ses_plotting_data.loc[ses_plotting_data['Trait'] == '4', 'Trait'] = 'Fourth Quintile of Deprivation'
ses_plotting_data.loc[ses_plotting_data['Trait'] == '5', 'Trait'] = 'Fifth Quintile of Deprivation<br>(Most Deprived)'
ses_plotting_data.loc[ses_plotting_data['Trait'] == 'Total', 'Trait'] = 'Overall'

###############################################################################
#################################  VIEW  ######################################
###############################################################################

app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        
        ## HEADER 

        html.Div(
            [
                html.Div(
                    [
                        # Just padding
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "The Landscape of Health Disparities in the UK Biobank",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Jordan Lab @ GaTech | NIMHD", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        # Just padding
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),

        ## BODY

        dcc.Tabs(
            id = 'disparity_tabs',
            value = 'about_tab',
            children = [
                dcc.Tab(
                    label = 'About',
                    value = 'about_tab',
                    children = [
                        dcc.Markdown(
                            components.ABOUT_US
                        )
                    ]
                ),
                dcc.Tab(
                    label = 'Sex Disparities',
                    value = 'sex_tab',
                    children = [
                        tab_populator.get_tab_content(sex_table_data, sex_plotting_data, 'Sex'),

                        html.Div(
                            [
                                html.H5(
                                    "Phenotype Prevalence",
                                    className="control_label",
                                ),
                                html.Br(),
                                # Reading in table from our component library
                                components.get_dash_table(sex_prev_data, 'SexPrev'),
                            ],
                        
                        className="pretty_container",
                        
                        )
                    ]
                ),
                dcc.Tab(
                    label = 'Age Disparities',
                    value = 'age_tab',
                    children = [
                        tab_populator.get_tab_content(age_table_data, age_plotting_data, 'Age'),

                        html.Div(
                            [
                                html.H5(
                                    "Phenotype Prevalence",
                                    className="control_label",
                                ),
                                html.Br(),
                                # Reading in table from our component library
                                components.get_dash_table(age_prev_data, 'AgePrev'),
                            ],
                        
                        className="pretty_container",
                        
                        )
                    ]
                ),
                dcc.Tab(
                    label = 'Ethnic Disparities',
                    value = 'ethnic_tab',
                    children = [
                        tab_populator.get_tab_content(ethnic_table_data, ethnic_plotting_data, 'Ethnic'),

                        html.Div(
                            [
                                html.H5(
                                    "Disease Prevalence across groups",
                                    className="control_label",
                                ),
                                html.Br(),
                                # Reading in table from our component library
                                components.get_dash_table(ethnic_prev_data, 'EthnicPrev'),
                            ],
                        
                        className="pretty_container",
                        
                        )
                    ]
                ),
                dcc.Tab(
                    label = 'Socio-economic Disparities',
                    value = 'ses_tab',
                    children = [
                        tab_populator.get_tab_content(ses_table_data, ses_plotting_data, 'SES'),

                        html.Div(
                            [
                                html.H5(
                                    "Phenotype Prevalence",
                                    className="control_label",
                                ),
                                html.Br(),
                                # Reading in table from our component library
                                components.get_dash_table(ses_prev_data, 'SESPrev'),
                            ],
                        
                        className="pretty_container",
                        
                        )
                    ]
                ),
            ]
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


###############################################################################
##############################  CONTROLLER   ##################################
###############################################################################


# Helper functions
def human_format(num):
    if num == 0:
        return "0"
    magnitude = int(math.log(num, 1000))
    mantissa = str(int(num / (1000 ** magnitude)))
    return mantissa + ["", "K", "M", "G", "T", "P"][magnitude]



# Populating information tiles
@app.callback(
    Output('disease_textSex', 'children'),
    [
        Input('datatable-row-idsSex', 'active_cell')
    ]
    )
def update_disease_name(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Inguinal hernia'

    return f"{active_row_id}"

@app.callback(
    Output('disease_textAge', 'children'),
    [
        Input('datatable-row-idsAge', 'active_cell')
    ]
    )
def update_disease_name(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Essential hypertension'

    return f"{active_row_id}"

@app.callback(
    Output('disease_textEthnic', 'children'),
    [
        Input('datatable-row-idsEthnic', 'active_cell')
    ]
    )
def update_disease_name(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'

    return f"{active_row_id}"

@app.callback(
    Output('disease_textSES', 'children'),
    [
        Input('datatable-row-idsSES', 'active_cell')
    ]
    )
def update_disease_name(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'

    return f"{active_row_id}"

### Sex
@app.callback(
    Output('caseTextSex', 'children'),
    [
        Input('datatable-row-idsSex', 'active_cell'),
    ]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Inguinal hernia'
    # Null value
    cases = 0
    cases = sex_plotting_data[(sex_plotting_data.Phenotype == active_row_id) & (sex_plotting_data.Trait == "Overall")].Cases.unique()[0]
    return human_format(int(cases))

@app.callback(
    Output('controlTextSex', 'children'),
    [Input('datatable-row-idsSex', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Inguinal hernia'
    controls = sex_plotting_data[(sex_plotting_data.Phenotype == active_row_id) & (sex_plotting_data.Trait == "Overall")].Controls.unique()[0]
    return human_format(int(controls))

@app.callback(
    Output('prevalenceTextSex', 'children'),
    [Input('datatable-row-idsSex', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Inguinal hernia'
    prevalence = sex_plotting_data[(sex_plotting_data.Phenotype == active_row_id) & (sex_plotting_data.Trait == "Overall")].Prevalence.unique()[0]
    return str(prevalence) + "%"


## Age
@app.callback(
    Output('caseTextAge', 'children'),
    [
        Input('datatable-row-idsAge', 'active_cell'),
    ]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Essential hypertension'
    # Null value
    cases = 0
    cases = age_plotting_data[(age_plotting_data.Phenotype == active_row_id) & (age_plotting_data.Trait == "Overall")].Cases.unique()[0]
    return human_format(int(cases))

@app.callback(
    Output('controlTextAge', 'children'),
    [Input('datatable-row-idsAge', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Essential hypertension'
    controls = age_plotting_data[(age_plotting_data.Phenotype == active_row_id) & (age_plotting_data.Trait == "Overall")].Controls.unique()[0]
    return human_format(int(controls))

@app.callback(
    Output('prevalenceTextAge', 'children'),
    [Input('datatable-row-idsAge', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Essential hypertension'
    prevalence = age_plotting_data[(age_plotting_data.Phenotype == active_row_id) & (age_plotting_data.Trait == "Overall")].Prevalence.unique()[0]
    return str(prevalence) + "%"


## Ethnic
@app.callback(
    Output('caseTextEthnic', 'children'),
    [
        Input('datatable-row-idsEthnic', 'active_cell'),
    ]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    # Null value
    cases = 0
    cases = ethnic_plotting_data[(ethnic_plotting_data.Phenotype == active_row_id) & (ethnic_plotting_data.Trait == "Overall")].Cases.unique()[0]
    return human_format(int(cases))

@app.callback(
    Output('controlTextEthnic', 'children'),
    [Input('datatable-row-idsEthnic', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    controls = ethnic_plotting_data[(ethnic_plotting_data.Phenotype == active_row_id) & (ethnic_plotting_data.Trait == "Overall")].Controls.unique()[0]
    return human_format(int(controls))

@app.callback(
    Output('prevalenceTextEthnic', 'children'),
    [Input('datatable-row-idsEthnic', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    prevalence = ethnic_plotting_data[(ethnic_plotting_data.Phenotype == active_row_id) & (ethnic_plotting_data.Trait == "Overall")].Prevalence.unique()[0]
    return str(prevalence) + "%"

## Socio-Economic Status
@app.callback(
    Output('caseTextSES', 'children'),
    [
        Input('datatable-row-idsSES', 'active_cell'),
    ]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    # Null value
    cases = 0
    cases = ses_plotting_data[(ses_plotting_data.Phenotype == active_row_id) & (ses_plotting_data.Trait == "Overall")].Cases.unique()[0]
    return human_format(int(cases))

@app.callback(
    Output('controlTextSES', 'children'),
    [Input('datatable-row-idsSES', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    controls = ses_plotting_data[(ses_plotting_data.Phenotype == active_row_id) & (ses_plotting_data.Trait == "Overall")].Controls.unique()[0]
    return human_format(int(controls))

@app.callback(
    Output('prevalenceTextSES', 'children'),
    [Input('datatable-row-idsSES', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    prevalence = ses_plotting_data[(ses_plotting_data.Phenotype == active_row_id) & (ses_plotting_data.Trait == "Overall")].Prevalence.unique()[0]
    return str(prevalence) + "%"

# Populating graphs

# Sex
@app.callback(
    Output('disp_graphSex', 'figure'),
    [Input('datatable-row-idsSex', 'active_cell')]
    )
def make_figure(active_cell):

    # Setting default value
    active_row_id = active_cell['row_id'] if active_cell else 'Inguinal hernia'

    return components.get_sex_disp_plot(sex_plotting_data, active_row_id)

# Age
@app.callback(
    Output('disp_graphAge', 'figure'),
    [Input('datatable-row-idsAge', 'active_cell')]
    )
def make_figure(active_cell):

    # Setting default value
    active_row_id = active_cell['row_id'] if active_cell else 'Essential hypertension'
    
    return components.get_age_disp_plot(age_plotting_data, active_row_id)

# Ethnic

@app.callback(
    Output('disp_graphEthnic', 'figure'),
    [Input('datatable-row-idsEthnic', 'active_cell')]
    )
def make_figure(active_cell):

    # Setting default value
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    
    return components.get_ethnic_disp_plot(ethnic_plotting_data, active_row_id)

# Socio-economic status

@app.callback(
    Output('disp_graphSES', 'figure'),
    [Input('datatable-row-idsSES', 'active_cell')]
    )
def make_figure(active_cell):

    # Setting default value
    active_row_id = active_cell['row_id'] if active_cell else 'Essential hypertension'
    
    return components.get_ses_disp_plot(ses_plotting_data, active_row_id)

# Main
if __name__ == '__main__':
    # app.run_server(host = '127.0.0.1', port = '8080', debug=True)
    app.run_server()

