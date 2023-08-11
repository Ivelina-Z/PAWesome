import pandas as pd
import plotly.graph_objects as go

from PAWesome.animal.models import Animal, AdoptedAnimalsArchive
from PAWesome.volunteering.models import FosterHome, DonationTickets


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


def plot_pie(labels, values, title='', to_html=True):
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
            # title={
            #     'text': title,
            #     'x': 0.5,
            #     'xanchor': "center"
            # },
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


def dashboard_plots_context(organization):
    try:
        all_animals = pd.DataFrame(Animal.objects.filter(organization=organization.pk).all().values())
    except Animal.DoesNotExist:
        all_animals = pd.DataFrame()

    try:
        animals_by_type_data = all_animals['animal_type'].value_counts()
        animal_type_pie = plot_pie(
            animals_by_type_data.index,
            animals_by_type_data.values,
            'Брой животни по вид'
        )
    except KeyError:
        animal_type_pie = None

    try:
        animals_by_current_residence_data = all_animals['current_residence'].value_counts()
        animal_current_type_pie = plot_pie(
            animals_by_current_residence_data.index,
            animals_by_current_residence_data.values,
            'Брой животни по настояща локация'
        )
    except KeyError:
        animal_current_type_pie = None

    try:
        all_archived_animal = pd.DataFrame(
            AdoptedAnimalsArchive.objects.filter(organization=organization.pk).all().values())
    except AdoptedAnimalsArchive.DoesNotExist:
        all_archived_animal = pd.DataFrame()

    try:
        all_foster_homes = pd.DataFrame(FosterHome.objects.all().values())
    except FosterHome.DoesNotExist:
        all_foster_homes = pd.DataFrame()

    try:
        foster_homes_by_animal_type = pd.DataFrame({
            'cats': [all_foster_homes['cat_available_spots'].sum()],
            'dogs': [all_foster_homes['dog_available_spots'].sum()],
            'bunnies': [all_foster_homes['bunny_available_spots'].sum()]
        })
        foster_home_pie = plot_pie(
            foster_homes_by_animal_type.columns,
            *foster_homes_by_animal_type.values,
            'Брой приемни домове по вид животно'
        )
    except KeyError:
        foster_home_pie = None

    try:
        animal_by_date_of_publication_data = all_animals['date_of_publication'].value_counts()
        adopted_animal_by_date_of_adoption_data = all_archived_animal['date_of_adoption'].value_counts()
    except KeyError:
        animal_by_date_of_publication_data = None
        adopted_animal_by_date_of_adoption_data = None

    try:
        time_series_data = [
            plot_scatter(
                animal_by_date_of_publication_data.index,
                animal_by_date_of_publication_data.values,
                'Животни за осиновяване',
                COLOR_PALETTE_RGBA['pink'],

            ),
            plot_scatter(
                adopted_animal_by_date_of_adoption_data.index,
                adopted_animal_by_date_of_adoption_data.values,
                'Осиновени животни',
                COLOR_PALETTE_RGBA['coral-pink'],
            )
        ]
        animal_by_date_of_publication_time_series = plot_figure(time_series_data, ('Дата', 'Брой'))
    except AttributeError:
        animal_by_date_of_publication_time_series = None

    try:
        all_donation_tickets = pd.DataFrame(
            DonationTickets.objects.filter(created_by=organization.pk).all().values())
        donation_tickets_indicator = plot_indicator(all_donation_tickets.shape[0], 'ИСКАНИЯ ЗА ДАРЕНИЕ')
    except DonationTickets.DoesNotExist:
        donation_tickets_indicator = None

    try:
        all_animals[['latitude', 'longitude']] = pd.DataFrame(all_animals['location'].to_list(),
                                                              index=all_animals.index)
        all_foster_homes[['latitude', 'longitude']] = pd.DataFrame(all_foster_homes['location'].to_list(),
                                                                   index=all_foster_homes.index)
        all_foster_homes['hover_text'] = ('Кучета: ' + all_foster_homes["dog_available_spots"].astype(str) +
                                          ' Котки: ' + all_foster_homes["cat_available_spots"].astype(str) +
                                          ' Зайчета: ' + all_foster_homes["bunny_available_spots"].astype(str))
        all_foster_homes_scatter = plot_scattermapbox(
            all_foster_homes['longitude'],
            all_foster_homes['latitude'],
            all_foster_homes['hover_text'],
            COLOR_PALETTE_RGBA['yellow'],
            'Приемни домове'
        )
        all_animals_scatter = plot_scattermapbox(
            all_animals['longitude'],
            all_animals['latitude'],
            all_animals['name'],
            COLOR_PALETTE_RGBA['pink'],
            'Животни, чакащи осиновител'
        )
        animals_foster_homes_map = plot_map_figure(data=[all_animals_scatter, all_foster_homes_scatter])
    except KeyError:
        animals_foster_homes_map = None

    foster_homes_indicator = plot_indicator(all_foster_homes.shape[0], 'ПРИЕМНИ ДОМОВЕ')
    animals_indicator = plot_indicator(all_animals.shape[0], 'ЖИВОТНИ')

    plots_for_context = {
        'map': animals_foster_homes_map,
         'animal_type_pie': animal_type_pie,
         'animal_current_type_pie': animal_current_type_pie,
         'foster_home_pie': foster_home_pie,
         'animal_by_date_of_publication_time_series': animal_by_date_of_publication_time_series,
         'foster_homes_indicator': foster_homes_indicator,
         'animals_indicator': animals_indicator,
         'donation_tickets_indicator': donation_tickets_indicator
    }

    return plots_for_context
