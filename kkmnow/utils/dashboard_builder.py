from kkmnow.utils.general_chart_helpers import *
from kkmnow.utils.chart_builder import *
import os

'''
Segregates chart types,
into respective chart builders
'''

def build_chart(chart_type, data) :
    variables = data['variables']
    input_file = os.path.join(os.getcwd(), 'KKMNOW_SRC/kkmnow-data-main') + '/' + data['input']

    match chart_type : 
        case 'bar_chart' :
            return bar_chart(input_file, variables)
        case 'heatmap_chart' :
            return heatmap_chart(input_file, variables)
        case 'timeseries_chart' : 
            return timeseries_chart(input_file, variables)
        case 'bar_meter' :
            return bar_meter(input_file, variables)
        case 'custom_chart' :
            return custom_chart(input_file, variables)
        case 'snapshot_chart' :
            return snapshot_chart(input_file, variables)
        case 'waffle_chart' :
            return waffle_chart(input_file, variables)
        case 'helpers_custom' :
            return helpers_custom(input_file)
        case 'map_lat_lon' : 
            return map_lat_lon(input_file, variables)
        case _:
            return {}