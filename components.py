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
                                        'borderStyle' : 'none',
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
                        height = 590,
                        plot_bgcolor = '#f9f9f9',
                        paper_bgcolor = '#f9f9f9'
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
                                        'Female', 'Male'][::-1],
                        automargin = True
                    )

    fig.update_xaxes(
                        range = [0, max(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence)],
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
                        # '#006C67', # 30-39
                        '#7AC74F', # Overall  

                        '#FFFFFF', # Blank
                    ]
                )

    fig.update_layout(
                        title = {'x' : 0.5}, 
                        showlegend = False, 
                        autosize = True,
                        # width = 600,
                        height = 590,
                        plot_bgcolor = '#f9f9f9',
                        paper_bgcolor = '#f9f9f9'
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
                                        '70-79', '60-69', '50-59', '40-49'][::-1],
                        automargin = True
                    )

    fig.update_xaxes(
                        range = [0, max(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence)],
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
                        height = 590,
                        plot_bgcolor = '#f9f9f9',
                        paper_bgcolor = '#f9f9f9'
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
                        range = [0, max(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence)],
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
                        height = 590,
                        plot_bgcolor = '#f9f9f9',
                        paper_bgcolor = '#f9f9f9'
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
                        range = [0, max(plotting_data[(plotting_data.Phenotype == active_row_id)].Prevalence)],
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
<br>

Health disparities can be defined as differences in health outcomes between groups of people, where groups (or populations) can be defined in a variety of ways.  We created the UK Health Disparities Browser as a means for researchers to explore the landscape of health disparities in the United Kingdom, for age, ethnicity, sex, and socioeconomic status groups.  The browser includes prevalence data for 1,513 diseases based on a cohort of ~500,000 participants from the [UK Biobank](https://www.ukbiobank.ac.uk/).  Users can browse and sort by disease prevalence, and prevalence differences, to quantify and visualize health disparities for each of these four characteristics.

<br>

Disease cohorts were defined by mapping ICD-10 disease codes from the UK Biobank to phenotype codes (phecodes).  Phecodes aggregate one or more related ICD-10 codes into distinct diseases, and they use both inclusion and exclusion criteria to define disease case and control cohorts.  For each disease phecode, prevalence values were calculated by dividing the number of cases by the sum of the number of cases and controls.  For each of the four groups – age, ethnicity, sex, and socioeconomic status – disease percent prevalence values were computed for all subgroups, and the magnitude of the disparities were calculated by both the variances of the prevalence and the maximum prevalence differences among the subgroups.

<br>

[Age](https://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=21003): The UK Biobank recruited participants aged 40 and over.  Participant ages at the time they attended the assessment centers were divided into four decades – 40-49, 50-59, 60-69, 70-79.

[Ethnicity](https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=21000): UK Biobank participants self-identify as belonging to one of six ethnic groups – Asian, Black, Chinese, Mixed, White, or Other – and a specific ethnic background within each group.

[Sex](https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=31): UK Biobank participant sex – Male or Female – were obtained from the UK National Healthcare Service (NHS) Primary Care Trust registries.    

[Socioeconomic](https://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=189): The Townsend deprivation index, a measure of material deprivation within a population, was used to measure participant socioeconomic status.  Postcode normalized Townsend index values were partitioned into five equal quintiles.

<br>

Developed by [Shashwat Deepali Nagar](http://www.sdnagar.com) from the [Jordan Lab](http://jordan.biology.gatech.edu) at Georgia Tech in collaboration with the Mariño-Ramírez group at the [US National Institute on Minority Health and Health Disparities](https://www.nimhd.nih.gov/).

<br>

All of the health disparities data published here are released freely for the benefit of the research community.  It should be noted that the disease prevalence and disparities values were calculated using the UK Biobank Resource (project ID 65206), and use of these data are subject to the terms of the UK Biobank.
'''