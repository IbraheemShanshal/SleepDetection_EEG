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
            dbc.Col(
                [
                    html.Img(src='../assets/bci3.png', style={'width': '100%','marginLeft': '280px','marginTop': '10px'})
                ], xs=1, sm=1, md=1, lg=1, xl=1, xxl=1),
            dbc.Col(
                [

                ], xs=1, sm=1, md=1, lg=1, xl=1, xxl=1),
            dbc.Col(
                [
                    html.H1("SLEEP STAGES CLASSIFICATION APP", style={'textAlign': 'center','marginTop': '30px','font-family': 'Georgia','textShadow': '2px 2px 4px #ffc0cb'}, className='header')
                ], xs=7, sm=7, md=9, lg=9, xl=9, xxl=9),

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
                    ], xs=1, sm=1, md=1, lg=1, xl=1, xxl=1),
                dbc.Col(
                    [
                        dash.page_container
                    ], xs=7, sm=7, md=9, lg=9, xl=9, xxl=9),

            ]
        )

    ], fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=True)