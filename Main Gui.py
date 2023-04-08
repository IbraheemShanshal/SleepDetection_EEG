from dash import Dash, html, dcc
import dash

#RUN THIS FILE FOR GUI

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Sleep Stages App example'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page['path']
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
