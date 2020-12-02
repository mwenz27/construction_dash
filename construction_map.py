import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table
import plotly.graph_objects as go

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',  # Default style
]

# Read Data
df = pd.read_csv('perth_projects_2')
headers = ['project_id', 'building_name', 'project', 'cost', 'time_months']
df['label_dash'] = df.apply(
    lambda x: f"Project ID: {x.project_id} <br>"
              f"Building Name: {x.building_name} <br>"
              f"Project: {x.project} <br>"
              f"Cost ${x.cost},  Time {x.time_months} months",
    axis=1)

# Create Map plot
fig = go.Figure(go.Scattermapbox(lat=df.lat,
                                 lon=df.lon,

                                 marker=go.scattermapbox.Marker(
                                     size=30,
                                     color=df.cost,
                                     colorscale='Jet',  # _r reverses the color scale
                                     opacity=0.9,
                                     # showscale=False,
                                     colorbar_x=1,
                                     colorbar_title='Cost',
                                 ),

                                 hovertext=df.label_dash,
                                 ))

fig.update_layout(mapbox_style="stamen-terrain",
                  mapbox_center_lat=-31.949036485381626,
                  mapbox_center_lon=115.85805926727204,
                  mapbox_zoom=8.5,
                  )

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

## Create Month Plot for expenses

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
predicted_list = [
    63823,
    87328,
    66067,
    61513,
    78627,
    80682,
    87360,
    87042,
    60732,
    69672,
    71108,
    66350,
]
actual_list = [88660,
               77595,
               83575,
               73938,
               82357,
               70051,
               82267,
               63781,
               71671,
               69867,
               79168,
               65478,
               ]
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=months,
    y=predicted_list,
    name='Predicted',
    marker_color='indianred'
))
fig_bar.add_trace(go.Bar(
    x=months,
    y=actual_list,
    name='Actual',
    marker_color='lightsalmon'
))

fig_bar.update_layout(barmode='group', xaxis_tickangle=-45)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H3('Construction Projects'),

    dash_table.DataTable(
        id='table',

        columns=[{"name": i.capitalize().replace('_', ' '), "id": i}
                 for i in headers],  # df.columns
        data=df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    ),
    html.H4('Location Map'),
    dcc.Graph(figure=fig),

    html.H4('Operations Chart'),
    dcc.Graph(figure=fig_bar),

])

if __name__ == '__main__':
    app.run_server(port=8888, debug=True)
