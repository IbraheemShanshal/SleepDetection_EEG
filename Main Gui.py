from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

#RUN THIS FILE FOR GUI

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical="true",
    pills="true",
)

app.layout = html.Div([
    dbc.Row(
        html.H1('Sleep Stages App example'),
    ),

    # html.Div(
    #     [
    #         html.Div(
    #             dcc.Link(
    #                 f" [{page['name']}] ", href=page['path']
    #             )
    #         )
    #         for page in dash.page_registry.values()
    #     ]
    # ),
    dbc.Row(
        dash.page_container
    ),
    html.Hr(),
    dbc.Row(
        sidebar,
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
