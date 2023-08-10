import plotly.graph_objects as go


def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    rgba_color = f"rgba{rgb_color + (alpha,)}"
    return rgba_color


COLOR_PALETTE = {
    'dark-pink': '#AB6C82',
    'pink': '#D8737F',
    'coral-pink': '#E84A5F',
    'yellow': '#FCBB6D',
}

GRAY_BG = '#2A363B'
PURPLE_BG = '#685D79'
TEXT_COLOR = '#FEFAD4'

COLOR_PALETTE_RGBA = {color: hex_to_rgba(hex_color, 0.7) for color, hex_color in COLOR_PALETTE.items()}
PURPLE_BG_RGBA = hex_to_rgba(PURPLE_BG, 0.8)

MAP_HEIGHT = 999


def plot_pie(labels, values, title=None, to_html=True):
    num_segments = len(labels)
    colors = [COLOR_PALETTE_RGBA[color] for color in
              list(COLOR_PALETTE_RGBA) * (num_segments // len(COLOR_PALETTE_RGBA) + 1)]

    figure = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(
                colors=colors,
                line=dict(color=TEXT_COLOR, width=1),
            ),
        ),
        layout=go.Layout(
            title={
                'text': title.upper(),
                'x': 0.5,
                'font': {'color': TEXT_COLOR}
            },
            hoverlabel={
                'font_size': 16
            },
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            width=500
        )
    )

    figure.update_traces(
        showlegend=False,
        textinfo='percent+label',
        textfont_color=TEXT_COLOR,
        textfont_size=14
    )

    if to_html:
        figure = figure.to_html(full_html=False)
    return figure


def plot_scatter(x, y, name, color):
    figure = go.Scatter(
        x=x,
        y=y,
        name=name,
        mode='lines+markers',
        marker={
            'size': 15,
            'color': color
        },
        line={
          'width': 3,
          'color': color
        }
    )
    return figure


def plot_indicator(value, param_name, to_html=True):
    figure = go.Figure(
        go.Indicator(
            mode="number",
            value=value,
            title={"text": param_name, 'font': {'color': TEXT_COLOR}},
            number={'font': {'color': COLOR_PALETTE_RGBA['yellow']}},
        ),
        layout=go.Layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
            height=MAP_HEIGHT // 3.5
        )
    )

    if to_html:
        figure = figure.to_html(full_html=False)
    return figure


def plot_scattermapbox(lon, lat, text, color, name=None):
    figure = go.Scattermapbox(
        lon=lon,
        lat=lat,
        text=text,
        hoverinfo='lat+lon+text',
        hovertemplate="%{text}",
        mode='markers',
        marker={
            'size': 15,
            'color': color
        },
        name=name
    )
    return figure


def plot_map_figure(data, to_html=True):
    figure = go.Figure(data=data)
    figure.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                # "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
                ]
            }
        ],
        mapbox_zoom=6,
        mapbox_center=dict(lat=42.930, lon=26.027),
        width=1000,
        height=MAP_HEIGHT,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin={'l': 6, 'r': 6, 't': 6, 'b': 6},
        legend={
            'x': 0,
            'y': 1,
            'xanchor': 'left',
            'yanchor': 'top',
            'orientation': 'h',
            'bgcolor': PURPLE_BG_RGBA,
            'font': {'color': TEXT_COLOR, 'size': 16},
        },
    )

    figure.update_traces(
        hovertemplate=None
    )

    if to_html:
        figure = figure.to_html()
    return figure


def plot_figure(data, axis_title: tuple, title=None, to_html=True):
    xaxis_title, yaxis_title = axis_title
    figure = go.Figure(
        data=data,
        layout=go.Layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': "center"
            },
            xaxis={
                'title': xaxis_title.upper(),
                'gridcolor': PURPLE_BG,
                'tickfont': {'color': COLOR_PALETTE['yellow']}
            },
            yaxis={
                'title': yaxis_title.upper(),
                'gridcolor': PURPLE_BG,
                'tickfont': {'color': COLOR_PALETTE['yellow']}
            },
            xaxis_title_font={'color': TEXT_COLOR, 'size': 16},
            yaxis_title_font={'color': TEXT_COLOR, 'size': 16},
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            legend={
                'x': 0.5,
                'y': 1.2,
                'xanchor': 'center',
                'yanchor': 'top',
                'orientation': 'h',
                'bgcolor': PURPLE_BG_RGBA,
                'font': {'color': TEXT_COLOR, 'size': 16},
            },
        )
    )

    if to_html:
        figure = figure.to_html()
    return figure
