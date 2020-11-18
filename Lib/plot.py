import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def plot_lines(
    scale_dict1,
    dict1_x = None,
    dict1_y = None,
    scale_dict2 = None,
    dict2_x = None,
    dict2_y = None
):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    def add_trace_for_dict(dic, x, y, is_secondary):
        for name in dic.keys():
            v = dic[name]
            if isinstance(v, pd.DataFrame) and x != None and y != None:
                fig.add_trace(go.Scatter(x=v[x], y=v[y],
                                    mode='lines',
                                    name=name), secondary_y = is_secondary)
            elif x in v.keys() and y in v.keys():
                fig.add_trace(go.Scatter(x=v['x'],  y=v['y'],
                                    mode='lines',
                                    name=name), secondary_y = is_secondary)
            else:
                raise 'Unknown trace'
    
    add_trace_for_dict(scale_dict1, dict1_x, dict1_y, False)
    if scale_dict2 != None:
        add_trace_for_dict(scale_dict2, dict2_x, dict2_y, True)

    fig.show()

def plot_line(x, y, name = None):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y,
                        mode='lines',
                        name=name))

    fig.show()