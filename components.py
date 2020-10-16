# Dash imports
import dash_table

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
                                        'height': 'auto',
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