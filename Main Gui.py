from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE])
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
    vertical=True,
    pills=True,
    className='body',
)

app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.H1("Sleep Stages App example", style={'textAlign': 'center'}, className='header')),
        ]),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        sidebar
                    ], xs=2, sm=2, md=1, lg=1, xl=1, xxl=1, style={'height': '99%'}),
                dbc.Col(
                    [
                        dash.page_container
                    ], xs=9, sm=9, md=11, lg=11, xl=11, xxl=11)
            ]
        )

    ], fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=True)
