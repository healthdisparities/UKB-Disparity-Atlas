# Dash imports
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html

# Local imports
import components


def get_tab_content(view_data, plotting_data, disp_type):
    return html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(id="disease_text" + disp_type), 
                                        ],
                                        className="mini_container",
                                        style = {'text-align' : 'center'}
                                    ),

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H6(id="caseText" + disp_type), 
                                                    html.P("Cases")
                                                ],
                                                id="cases" + disp_type,
                                                className="pretty_container four columns",
                                                style = {'text-align' : 'center'}
                                            ),
                                            html.Div(
                                                [
                                                    html.H6(id="controlText" + disp_type), 
                                                    html.P("Controls")
                                                ],
                                                id="controls" + disp_type,
                                                className="pretty_container four columns",
                                                style = {'text-align' : 'center'}
                                            ),
                                            html.Div(
                                                [
                                                    html.H6(id="prevalenceText" + disp_type), 
                                                    html.P("Prevalence")
                                                ],
                                                id="prevalence" + disp_type,
                                                className="pretty_container four columns",
                                                style = {'text-align' : 'center'}
                                            )
                                        ],
                                        className="row container-display"
                                    ),

                                ],
                                className="pretty_container",
                                style = {'align-items' : 'center'},
                                # id="cross-filter-options" ,
                            ),

                            html.Div(
                                [                                    
                                    html.Div(
                                        [
                                            html.H5(
                                                "Disease Prevalence Disparities",
                                                className="control_label",
                                            ),
                                            html.P(
                                                "Disparities defined by variance and maximum difference of prevalence values.",
                                                className="control_label",
                                            ),
                                            html.Br(),
                                            # Reading in table from our component library
                                            components.get_dash_table(view_data, disp_type)

                                        ],
                                        className="pretty_container",
                                        style = {
                                            'borderStyle' : 'none',
                                        }
                                    ),

                                    html.Br()
                                ],
                                className="pretty_container",
                                style = {'align-items' : 'center'},
                                # id="cross-filter-options" ,
                            ),
                        ],
                        className = 'container eight columns'
                    ),

                    html.Div(
                        [
                            
                            html.Div(
                                [
                                    dcc.Graph(
                                        id = "disp_graph" + disp_type,
                                        animate = True
                                    )
                                ],
                                id="countGraphContainer" + disp_type,
                                className="pretty_container",
                            ),
                        ],
                        id="right-column" + disp_type,
                        className="six columns",
                    ),
                ],
                className="row flex-display",
            )