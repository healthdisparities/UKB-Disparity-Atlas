# Dash imports
import dash_table

# Plotting bits
import plotly.express as px

def get_dash_table(view_data, disp_type):
    my_table = dash_table.DataTable(
                                    # ID
                                    id = 'datatable-row-ids' + disp_type,

                                    # Data
                                    data = view_data.to_dict('records'),
                                    columns = [
                                                {'name': i, 'id': i, 'deletable': False} for i in view_data.columns
                                                # omit the id column
                                                if i != 'id'
                                            ],
                                    # Options
                                    editable = False,
                                    sort_action="native",
                                    sort_mode='single',
                                    page_action='native',
                                    filter_action = 'native',
                                    page_current= 0,
                                    page_size= 5,
                                    virtualization=True,

                                    style_cell={
                                        'height': '4me',
                                        # all three widths are needed
                                        'minWidth': '2em', 
                                        'width': '2em', 
                                        'maxWidth': '2em',
                                        'whiteSpace': 'normal',
                                        'text-align' : 'center',
                                        'fontSize': 12, 
                                        'font-family': ["Open Sans", "HelveticaNeue", "Helvetica Neue", 'Helvetica', 'Arial', 'sans-serif']
                                    },
                                )
    
    return my_table

def get_sex_disp_plot(plotting_data, active_row_id):
    fig = px.bar(
                    plotting_data[(plotting_data.Phenotype == active_row_id)], 
                    y = 'Trait', 
                    x = 'Prevalence',
                    hover_data = ['Pretty_cases', 'Pretty_controls'],
                    color='Trait', 
                    template = "plotly_white", 
                    orientation='h',
                    color_discrete_sequence = [
                        
                        '#FC737A', # Female
                        '#1C77C3', # Male
                        '#39393A', # Overall
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
                        categoryarray = ['Overall', 
                                        ' ',
                                        'Male', 'Female'][::-1],
                        automargin = True
                    )

    fig.update_xaxes(
                        range = [min(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence), max(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence)],
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


def get_age_disp_plot(plotting_data, active_row_id):
    
    fig = px.bar(
                    plotting_data[(plotting_data.Phenotype == active_row_id)], 
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
                        '#7AC74F', # Overall  

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
                        categoryarray = ['Overall', 
                                        ' ',
                                        '70-79', '60-69', '50-59', '40-49', '30-39', 
                                        '  ',
                                        'Black (all)', 'African', 'Caribbean', 'Other Black'][::-1],
                        automargin = True
                    )

    fig.update_xaxes(
                        range = [min(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence), max(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence)],
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


def get_ethnic_disp_plot(plotting_data, active_row_id):
    fig = px.bar(
                    plotting_data[(plotting_data.Phenotype == active_row_id)], 
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
                        '#EDADC7', # Other ethnic group
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
                        '#C47B7F', # Pakistani
                        '#F1C9A9', # White and Asian
                        '#EFBE96', # White and Black African
                        '#F0C4A0', # White and Black Caribbean
                        '#7AC74F', # Overall  

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
                        categoryarray = ['Overall', 
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
                                        'Other'][::-1],
                        automargin = True
                    )

    fig.update_xaxes(
                        range = [min(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence), max(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence)],
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

def get_ses_disp_plot(plotting_data, active_row_id):
    fig = px.bar(
                    plotting_data[(plotting_data.Phenotype == active_row_id)], 
                    y = 'Trait', 
                    x = 'Prevalence',
                    hover_data = ['Pretty_cases', 'Pretty_controls'],
                    color='Trait', 
                    template = "plotly_white", 
                    # title = f"Trait: {active_row_id}",
                    orientation='h',
                    color_discrete_sequence = [
                        
                        '#7AC74F', # Overall  

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
                        categoryarray = ['Overall', 
                                        ' ',
                                        'First Quintile of Deprivation<br>(Least Deprived)', 
                                        'Second Quintile of Deprivation',
                                        'Third Quintile of Deprivation',
                                        'Fourth Quintile of Deprivation',
                                        'Fifth Quintile of Deprivation<br>(Most Deprived)'][::-1],
                        automargin = True
                    )

    fig.update_xaxes(
                        range = [min(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence), max(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence)],
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

ABOUT_US = '''
### Welcome to the UK Biobank Health Disparities Atlas!

#### Health Disparities

Health Disparities are defined as differences in health ourcomes between different groups of people.  


##### Grouping systems

These groups can be defined in many different ways &ndash; here, we defined groups based on 

(1) Sex,  (2) Age,  (3) Ethnicity, and (4) Socio-economic status


#### _Browser name_
For _Browser name_, we measure health disparities as the difference in the prevalence of diseases across these different grouping systems.  This is a tool for investigators to explore the landscape of health disparities across different grouping schemes to identifiy the largest disprities in disease prevalence between groups.  Identification of large health disparities will enable investigators to work towards ameliorating them.



#### About Us
Developed by [Shashwat Deepali Nagar](www.sdnagar.com), under the tutelage of Prof. [I. King Jordan](jordan.biology.gatech.edu) at Georgia Tech in collaboration with Prof. [Leonardo Mariño-Ramírez](https://scholar.google.com/citations?user=GQIBkAcAAAAJ&hl=en&oi=ao) at the 
[National Institute on Minority Health and Health Disparities](https://www.nimhd.nih.gov/).
'''