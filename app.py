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

## Grouping - Age
age_table_data = pd.read_csv(DATA_PATH.joinpath("age_selection_table.txt"), sep = '\t')
age_table_data.loc[:, 'Maximum Difference'] = age_table_data.loc[:, 'Maximum Difference'].round(2)
age_table_data['id'] = age_table_data['Phenotype']
age_table_data.set_index('id', inplace = True, drop = False)

## Grouping - Ethnic Group
ethnic_table_data = pd.read_csv(DATA_PATH.joinpath("ethnic_selection_table.txt"), sep = '\t')
ethnic_table_data.loc[:, 'Maximum Difference'] = ethnic_table_data.loc[:, 'Maximum Difference'].round(2)
ethnic_table_data['id'] = ethnic_table_data['Phenotype']
ethnic_table_data.set_index('id', inplace = True, drop = False)

## Grouping - Socio-economic status
ses_table_data = pd.read_csv(DATA_PATH.joinpath("ses_selection_table.txt"), sep = '\t')
ses_table_data.loc[:, 'Maximum Difference'] = ses_table_data.loc[:, 'Maximum Difference'].round(2)
ses_table_data['id'] = ses_table_data['Phenotype']
ses_table_data.set_index('id', inplace = True, drop = False)


'''
Next, we process data for visualization.
'''

## Grouping - Sex
sex_plotting_data = pd.read_csv(DATA_PATH.joinpath("sex_plotting.txt"), sep = '\t')
sex_plotting_data['id'] = sex_plotting_data['Phenotype']
sex_plotting_data.set_index('id', inplace = True, drop = False)
sex_plotting_data.columns = ['PheCode', 'Phenotype', 'Trait', 'Prevalence', 'Cases', 'Controls', 'id']
sex_plotting_data = sex_plotting_data.astype({'Cases': 'int32', 'Controls' : 'int32'})
sex_plotting_data['Pretty_cases'] = sex_plotting_data['Cases'].map("{:,}".format)
sex_plotting_data['Pretty_controls'] = sex_plotting_data['Controls'].map("{:,}".format)

## Grouping - Age
age_plotting_data = pd.read_csv(DATA_PATH.joinpath("age_plotting.txt"), sep = '\t')
age_plotting_data['id'] = age_plotting_data['Phenotype']
age_plotting_data.set_index('id', inplace = True, drop = False)
age_plotting_data.columns = ['PheCode', 'Phenotype', 'Trait', 'Prevalence', 'Cases', 'Controls', 'id']
age_plotting_data = age_plotting_data.astype({'Cases': 'int32', 'Controls' : 'int32'})
age_plotting_data['Pretty_cases'] = age_plotting_data['Cases'].map("{:,}".format)
age_plotting_data['Pretty_controls'] = age_plotting_data['Controls'].map("{:,}".format)

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
ethnic_plotting_data = ethnic_plotting_data.loc[~ethnic_plotting_data['Trait'].isin(['Prefer not to answer', 'Do not know', 'Other', 'Chinese (all)']),:]

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
                        html.H5(
                            '''
                            This is our about tab.
                            '''
                        )
                    ]
                ),
                dcc.Tab(
                    label = 'Sex Disparities',
                    value = 'sex_tab',
                    children = tab_populator.get_tab_content(sex_table_data, sex_plotting_data, 'Sex')
                ),
                dcc.Tab(
                    label = 'Age Disparities',
                    value = 'age_tab',
                    children = tab_populator.get_tab_content(age_table_data, age_plotting_data, 'Age')
                ),
                dcc.Tab(
                    label = 'Ethnic Disparities',
                    value = 'ethnic_tab',
                    children = tab_populator.get_tab_content(ethnic_table_data, ethnic_plotting_data, 'Ethnic')
                ),
                dcc.Tab(
                    label = 'Socio-economic Disparities',
                    value = 'ses_tab',
                    children = tab_populator.get_tab_content(ses_table_data, ses_plotting_data, 'SES')
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
    cases = sex_plotting_data[(sex_plotting_data.Phenotype == active_row_id) & (sex_plotting_data.Trait == "Total")].Cases.unique()[0]
    return human_format(int(cases))

@app.callback(
    Output('controlTextSex', 'children'),
    [Input('datatable-row-idsSex', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Inguinal hernia'
    controls = sex_plotting_data[(sex_plotting_data.Phenotype == active_row_id) & (sex_plotting_data.Trait == "Total")].Controls.unique()[0]
    return human_format(int(controls))

@app.callback(
    Output('prevalenceTextSex', 'children'),
    [Input('datatable-row-idsSex', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Inguinal hernia'
    prevalence = sex_plotting_data[(sex_plotting_data.Phenotype == active_row_id) & (sex_plotting_data.Trait == "Total")].Prevalence.unique()[0]
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
    cases = age_plotting_data[(age_plotting_data.Phenotype == active_row_id) & (age_plotting_data.Trait == "Total")].Cases.unique()[0]
    return human_format(int(cases))

@app.callback(
    Output('controlTextAge', 'children'),
    [Input('datatable-row-idsAge', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Essential hypertension'
    controls = age_plotting_data[(age_plotting_data.Phenotype == active_row_id) & (age_plotting_data.Trait == "Total")].Controls.unique()[0]
    return human_format(int(controls))

@app.callback(
    Output('prevalenceTextAge', 'children'),
    [Input('datatable-row-idsAge', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Essential hypertension'
    prevalence = age_plotting_data[(age_plotting_data.Phenotype == active_row_id) & (age_plotting_data.Trait == "Total")].Prevalence.unique()[0]
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
    cases = ethnic_plotting_data[(ethnic_plotting_data.Phenotype == active_row_id) & (ethnic_plotting_data.Trait == "Total")].Cases.unique()[0]
    return human_format(int(cases))

@app.callback(
    Output('controlTextEthnic', 'children'),
    [Input('datatable-row-idsEthnic', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    controls = ethnic_plotting_data[(ethnic_plotting_data.Phenotype == active_row_id) & (ethnic_plotting_data.Trait == "Total")].Controls.unique()[0]
    return human_format(int(controls))

@app.callback(
    Output('prevalenceTextEthnic', 'children'),
    [Input('datatable-row-idsEthnic', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    prevalence = ethnic_plotting_data[(ethnic_plotting_data.Phenotype == active_row_id) & (ethnic_plotting_data.Trait == "Total")].Prevalence.unique()[0]
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
    cases = ses_plotting_data[(ses_plotting_data.Phenotype == active_row_id) & (ses_plotting_data.Trait == "Total")].Cases.unique()[0]
    return human_format(int(cases))

@app.callback(
    Output('controlTextSES', 'children'),
    [Input('datatable-row-idsSES', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    controls = ses_plotting_data[(ses_plotting_data.Phenotype == active_row_id) & (ses_plotting_data.Trait == "Total")].Controls.unique()[0]
    return human_format(int(controls))

@app.callback(
    Output('prevalenceTextSES', 'children'),
    [Input('datatable-row-idsSES', 'active_cell')]
    )
def update_disease_title(active_cell):
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    prevalence = ses_plotting_data[(ses_plotting_data.Phenotype == active_row_id) & (ses_plotting_data.Trait == "Total")].Prevalence.unique()[0]
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
    
    fig = px.bar(
                    sex_plotting_data[(sex_plotting_data.Phenotype == active_row_id)], 
                    y = 'Trait', 
                    x = 'Prevalence',
                    hover_data = ['Pretty_cases', 'Pretty_controls'],
                    color='Trait', 
                    template = "plotly_white", 
                    orientation='h',
                    color_discrete_sequence = [
                        
                        '#1C77C3', # Male
                        '#FC737A', # Female
                        '#39393A', # Total
                    ]
                )

    fig.update_layout(
                        title = {'x' : 0.5}, 
                        showlegend = False, 
                        autosize = True,
                        height = 600
                    )

    for a in fig.layout.annotations:
        a.text = ""
        
    fig.update_yaxes(
                        matches = None,
                        title_text = '', 
                        tickmode = 'linear',
                        categoryorder = 'array',
                        categoryarray = ['Total', 
                                        ' ',
                                        'Male', 'Female'][::-1],
                        automargin = True
                    )

    fig.update_xaxes(
                        range = [min(sex_plotting_data[(sex_plotting_data.Phenotype == active_row_id)].Prevalence), max(sex_plotting_data[(sex_plotting_data.Phenotype == active_row_id)].Prevalence)],
                        title_text = "Percent Prevalence",
                        automargin = True
                    )
    
    fig.update_traces(
                        hovertemplate=
                                    "<b>%{y}</b><br><br>" +
                                    "%{customdata[0]} cases<br>" +
                                    "%{customdata[1]} controls<br>" +
                                    "<b>Prevalence:</b> %{x}%" +
                                    "<extra></extra>",
    )

    return fig

# Age
@app.callback(
    Output('disp_graphAge', 'figure'),
    [Input('datatable-row-idsAge', 'active_cell')]
    )
def make_figure(active_cell):

    # Setting default value
    active_row_id = active_cell['row_id'] if active_cell else 'Essential hypertension'
    
    fig = px.bar(
                    age_plotting_data[(age_plotting_data.Phenotype == active_row_id)], 
                    y = 'Trait', 
                    x = 'Prevalence',
                    hover_data = ['Pretty_cases', 'Pretty_controls'],
                    color='Trait', 
                    template = "plotly_white", 
                    # title = f"Trait: {active_row_id}",
                    orientation='h',
                    color_discrete_sequence = [

                        '#A22A31', # 70-79
                        '#214084', # 60-69
                        '#EDB88B', # 40-49
                        '#FAA51A', # 50-59
                        '#006C67', # 30-39
                        '#7AC74F', # Total  

                        '#FFFFFF', # Blank
                    ]
                )

    fig.update_layout(
                        title = {'x' : 0.5}, 
                        showlegend = False, 
                        autosize = True,
                        # width = 600,
                        height = 600
                    )

    for a in fig.layout.annotations:
        a.text = ""
        
    fig.update_yaxes(
                        matches = None,
                        title_text = '', 
                        tickmode = 'linear',
                        categoryorder = 'array',
                        categoryarray = ['Total', 
                                        ' ',
                                        '70-79', '60-69', '50-59', '40-49', '30-39', 
                                        '  ',
                                        'Black (all)', 'African', 'Caribbean', 'Other Black'][::-1],
                        automargin = True
                    )

    fig.update_xaxes(
                        range = [min(age_plotting_data[(age_plotting_data.Phenotype == active_row_id)].Prevalence), max(age_plotting_data[(age_plotting_data.Phenotype == active_row_id)].Prevalence)],
                        title_text = "Percent Prevalence",
                        automargin = True
                    )
    
    fig.update_traces(
                        hovertemplate=
                                    "<b>%{y}</b><br><br>" +
                                    "%{customdata[0]} cases<br>" +
                                    "%{customdata[1]} controls<br>" +
                                    "<b>Prevalence:</b> %{x}%" +
                                    "<extra></extra>",
    )

    return fig

# Ethnic

@app.callback(
    Output('disp_graphEthnic', 'figure'),
    [Input('datatable-row-idsEthnic', 'active_cell')]
    )
def make_figure(active_cell):

    # Setting default value
    active_row_id = active_cell['row_id'] if active_cell else 'Type 2 diabetes'
    
    fig = px.bar(
                    ethnic_plotting_data[(ethnic_plotting_data.Phenotype == active_row_id)], 
                    y = 'Trait', 
                    x = 'Prevalence',
                    hover_data = ['Pretty_cases', 'Pretty_controls'],
                    color='Trait', 
                    template = "plotly_white", 
                    # title = f"Trait: {active_row_id}",
                    orientation='h',
                    color_discrete_sequence = [

                        '#A22A31', # Asian Total
                        '#214084', # Black Total
                        '#EDB88B', # Mixed Total
                        '#FAA51A', # White Total
                        '#5075AC', # African
                        '#D69B9F', # Asian, other
                        '#B5CDE1', # Black other
                        '#F2CEB1', # Mixed Other
                        '#F4D6AF', # White Other
                        '#AB3E45', # Bangladeshi
                        '#F3C88B', # British
                        '#839FC6', # Caribbean
                        '#006C67', # Chinese
                        '#B95F65', # Indian
                        '#F8C16F', # Irish
                        '#EDADC7', # Other ethnic group
                        '#C47B7F', # Pakistani
                        '#F1C9A9', # White and Asian
                        '#EFBE96', # White and Black African
                        '#F0C4A0', # White and Black Caribbean
                        '#7AC74F', # Total  

                        '#FFFFFF', # Blank
                        '#FFFFFF', # Blank
                        '#FFFFFF', # Blank
                        '#FFFFFF', # Blank
                        '#FFFFFF', # Blank
                        '#FFFFFF', # Blank  
                    ]
                )

    fig.update_layout(
                        title = {'x' : 0.5}, 
                        showlegend = False, 
                        autosize = True,
                        # width = 600,
                        height = 600
                    )

    for a in fig.layout.annotations:
        a.text = ""
        
    fig.update_yaxes(
                        matches = None,
                        title_text = '', 
                        tickmode = 'linear',
                        categoryorder = 'array',
                        categoryarray = ['Total', 
                                        ' ',
                                        'Asian (all)', 'Bangladeshi', 'Indian', 'Pakistani', 'Other Asian', 
                                        '  ',
                                        'Black (all)', 'African', 'Caribbean', 'Other Black', 
                                        '   ', 
                                        'Chinese', 
                                        '    ', 
                                        'Mixed (all)', 'White and Black African', 'White and Black Caribbean', 'White and Asian', 'Other Mixed', 
                                        '     ',
                                        'White (all)', 'Irish', 'British', 'Other White', 
                                        '      ', 
                                        'Other ethnic group'][::-1],
                        automargin = True
                    )

    fig.update_xaxes(
                        range = [min(ethnic_plotting_data[(ethnic_plotting_data.Phenotype == active_row_id)].Prevalence), max(ethnic_plotting_data[(ethnic_plotting_data.Phenotype == active_row_id)].Prevalence)],
                        title_text = "Percent Prevalence",
                        automargin = True
                    )
    
    fig.update_traces(
                        hovertemplate=
                                    "<b>%{y}</b><br><br>" +
                                    "%{customdata[0]} cases<br>" +
                                    "%{customdata[1]} controls<br>" +
                                    "<b>Prevalence:</b> %{x}%" +
                                    "<extra></extra>",
    )

    return fig

# Socio-economic status

@app.callback(
    Output('disp_graphSES', 'figure'),
    [Input('datatable-row-idsSES', 'active_cell')]
    )
def make_figure(active_cell):

    # Setting default value
    active_row_id = active_cell['row_id'] if active_cell else 'Essential hypertension'
    
    fig = px.bar(
                    ses_plotting_data[(ses_plotting_data.Phenotype == active_row_id)], 
                    y = 'Trait', 
                    x = 'Prevalence',
                    hover_data = ['Pretty_cases', 'Pretty_controls'],
                    color='Trait', 
                    template = "plotly_white", 
                    # title = f"Trait: {active_row_id}",
                    orientation='h',
                    color_discrete_sequence = [
                        
                        '#7AC74F', # Total  

                        '#A22A31', # 1
                        '#214084', # 2
                        '#EDB88B', # 3
                        '#FAA51A', # 4
                        '#006C67', # 5

                        '#FFFFFF', # Blank
                    ]
                )

    fig.update_layout(
                        title = {'x' : 0.5}, 
                        showlegend = False, 
                        autosize = True,
                        # width = 600,
                        height = 600
                    )

    for a in fig.layout.annotations:
        a.text = ""
        
    fig.update_yaxes(
                        matches = None,
                        title_text = '', 
                        tickmode = 'linear',
                        categoryorder = 'array',
                        categoryarray = ['Total', 
                                        ' ',
                                        'First Quintile of Deprivation<br>(Least Deprived)', 
                                        'Second Quintile of Deprivation',
                                        'Third Quintile of Deprivation',
                                        'Fourth Quintile of Deprivation',
                                        'Fifth Quintile of Deprivation<br>(Most Deprived)'][::-1],
                        automargin = True
                    )

    fig.update_xaxes(
                        range = [min(ses_plotting_data[(ses_plotting_data.Phenotype == active_row_id)].Prevalence), max(ses_plotting_data[(ses_plotting_data.Phenotype == active_row_id)].Prevalence)],
                        title_text = "Percent Prevalence",
                        automargin = True
                    )
    
    fig.update_traces(
                        hovertemplate=
                                    "<b>%{y}</b><br><br>" +
                                    "%{customdata[0]} cases<br>" +
                                    "%{customdata[1]} controls<br>" +
                                    "<b>Prevalence:</b> %{x}%" +
                                    "<extra></extra>",
    )

    return fig

# Main
if __name__ == '__main__':
    app.run_server(host = '127.0.0.1', port = '8080', debug=True)
