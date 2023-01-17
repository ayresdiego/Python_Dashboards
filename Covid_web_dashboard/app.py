import pandas as pd
import numpy as np

import dash # good framework for analytical applications # Web-development # Based on HTML, CSS, JavaScript and Plotly.
# Creates a simple HTTP Server where the dash is displayed

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

# ps -fA | grep python - shows the existing process that should be killed
# kill -9 pid  or kill -9
# flask run

def get_covid_data():

    df_x = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
        sep=",")
    # df_x.to_csv('corona_virus_data.csv')
    # print(df_x.columns) # 'Province/State', 'Country/Region', 'Lat', 'Long',
    # print(df_x.head())
    # print(df_x['Country/Region'].unique())
    # df_x = df_x['Congo (Brazzaville)']
    # 'Congo (Kinshasa)'

    # input()
    ## group by country, sum and transpose
    df_x = df_x.drop(['Province/State', 'Lat', 'Long'], axis=1)
    df_x = df_x.rename(columns={'Country/Region': 'test'})

    df_x = df_x.replace({'Taiwan*': 'Taiwan',
                         'Burma' : 'Myanmar',
                         'Turkmenia' : 'Turkmenia',
                         'Czechia': 'Czech Republic',
                         'US': 'United States',
                         'United States of America': 'United States',
                         'Cabo Verde': 'Cape Verde',
                         'Korea, South': 'South Korea',
                         'Timor-Leste': 'East Timor',
                         'North Macedonia': 'Macedonia',
                         'Dominican Rep.': 'Dominican Republic',
                         'Bosnia and Herz.': 'Bosnia and Herzegovina',
                         'Central African Rep.': 'Central African Republic',
                         'Dem. Rep. Congo': 'Democratic Republic of the Congo',
                         'Congo, Dem. Rep.': 'Democratic Republic of the Congo',
                         'Congo (Kinshasa)': 'Democratic Republic of the Congo',
                         'Congo (Brazzaville)': 'Republic of the Congo',
                         'Congo, Rep.': 'Republic of the Congo',
                         'Eq. Guinea': 'Equatorial Guinea',
                         'Falkland Is.': 'Falkland Islands',
                         'Côte d\'Ivoire': 'Ivory Coast',
                         'Cote d\'Ivoire': 'Ivory Coast',
                         'Congo': 'Republic of the Congo',
                         'Solomon Is.': 'Solomon Islands',
                         'S. Sudan': 'South Sudan',
                         'eSwatini': 'Swaziland',
                         'W. Sahara': 'Western Sahara',
                         'Russian Federation': 'Russia',
                         'Egypt, Arab Rep.': 'Egypt',
                         'Slovak Republic': 'Slovakia',
                         'Yemen, Rep.': 'Yemen',
                         'Venezuela, RB': 'Venezuela',
                         'Puerto Rico': 'Puerto Rico',
                         'Korea, Rep.': 'South Korea',
                         'Bahamas, The': 'Bahamas',
                         'Lao PDR': 'Laos',
                         'Iran, Islamic Rep.': 'Iran',
                         'Syrian Arab Republic': 'Syria',
                         'Fr. S. Antarctic Lands': 'Antarctic',
                         'Brunei Darussalam': 'Brunei'
                         })

    df_x = df_x.groupby("test").sum().T
    df_x.index = pd.to_datetime(df_x.index, infer_datetime_format=True)  ## convert index to datetime
    df_x = df_x.sort_index(ascending=True)  # by index        # inplace=True


    df_x.reset_index(inplace=True)

    df_x = df_x.rename(columns={'index': 'date'})

    df_x.to_csv("data_covid.csv")

    return df_x


def get_data():
    df_1 = pd.read_csv("data_covid.csv")
    df_1 = df_1.drop(['Unnamed: 0'], axis=1)

    return df_1


def adjust_data(df_1):
    df_1 = pd.melt(df_1,
                   id_vars=['date'],
                   var_name=['country'],
                   value_name='total_number')

    df_1["date"] = pd.to_datetime(df_1["date"])  # , format="%Y-%m-%d"
    # print(type(df_1["date"]))
    # print((df_1["date"].dtypes))
    # df_1.sort_values("date", inplace=True, ascending=True)
    df_1.sort_values(["country", "date"], inplace=True, ascending=True)
    df_1 = df_1.dropna(how='any')
    df_1["new_cases"] = df_1["total_number"] - df_1["total_number"].shift(1)

    # print(df_1.head(50).to_string())
    df_1.set_index("date", inplace=True)
    df_1.loc[df_1.index.min(), "new_cases"] = 0  # np.nan

    df_1.reset_index(inplace=True)
    df_1.sort_values("date", inplace=True)
    df_1 = df_1[df_1["new_cases"] > int(0)]


    # print(df_1.columns)
    # print(df_1[df_1["country"]=="Brazil"].to_string())

    return df_1


try:
    df_1 = get_covid_data() # scrape_web_data
except:
    print("Error Scraping Data: Data for previous available date")
    df_1 = get_data() # In case of error get the saved one

df_1 = adjust_data(df_1)

# column_x2 =
column_y1 = "total_number" # Axis y columns
column_y2 = "new_cases" # Axis y columns
column_x1 = "date"  # date filter columns
column_f1 = "country" # categorical filter columns
# column_f2 = "type"  # categorical filter columns


image_x = "" # "TEST"  # "🥑" # 🦠
image_filename = 'covid.png' # 'header_image.jpeg' # .ico ; .png ; .jpeg # needs to be in the assets folder

header_text = "Covid"# "Analytics header"
description_text = """
Historical analysis - Covid total cases and daily new cases amount
"""


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap", # get the special font
        "rel": "stylesheet",
    },
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets, # add the external style sheet
    meta_tags=[  # Responsive website
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ],
)
server = app.server # Associating server # important to have

app.title = "Analytics Dashboard" # it it the title in the tab

# app.layout it is created to html and visual structure
app.layout = html.Div(  # DIV for the headers
    children=[
        html.Div(
            children=[
                # html.P(children=image_x, className="header-emoji"), # https://favicon.io/favicon-converter/
                html.Img(src=app.get_asset_url(image_filename), className="header-image"),
                html.H1(
                    children=header_text, className="header-title"
                ),
                html.P(
                    children=description_text,
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div(  # DIV for the menu
            children=[
                html.Div(
                    children=[
                        html.Div(children="Select Country" # add the text to describe the dropbox menu
                                 , className="menu-title"),
                        dcc.Dropdown(# add the dropdown boxes
                            id="filter-1",
                            options=[
                                # what show in the drop box and the value itself
                                {"label": x, "value": x} for x in np.sort(df_1[column_f1].unique()) # create a dictionary
                            ],
                            value="Czech Republic", # str(np.sort(df_1[column_f1].unique())[0]) , # default value
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                # html.Div(
                #     children=[
                #         html.Div(children="Select Type",
                #                  className="menu-title"),
                #         dcc.Dropdown(
                #             id="filter-2",
                #             options=[
                #                 {"label": x, "value": x} for x in df_1[column_f2].unique()
                #             ],
                #             value="organic",
                #             clearable=False,
                #             searchable=False,
                #             className="dropdown",
                #         ),
                #     ],
                # ),
                html.Div(
                    children=[
                        html.Div( # Div for the date range selector
                            children="Select Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange( # add the date selection
                            id="date-range",
                            min_date_allowed=df_1[column_x1].min().date(),
                            max_date_allowed=df_1[column_x1].max().date(),
                            start_date=df_1[column_x1].min().date(), # set the default
                            end_date=df_1[column_x1].max().date(),  # set the default
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div( # DIV add the charts (no data is added - just the frame)
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="chart-line-1", # tha data will be added based on ID
                        config={"displayModeBar": False},
                    ),
                    className="chart order2",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="chart-line-2",
                        config={"displayModeBar": False},
                    ),
                    className="chart order1",
                ),
            ],
            className="container",
        ),
    ]
)

# callback functions: add interactive elements. Set the source data and destination of it
@app.callback( # must have Output and Input
    [ # Output is what will be updated. # the orders matters
        Output("chart-line-1", "figure") # "chart-line-1" = ID , "figure" = property
        , Output("chart-line-2", "figure") # element ID is what will be updated # "figure" is property to be updated
    ],
    [ # Input is what will be the source od data
        Input("filter-1", "value"), # "filter-1" = ID , "value" = property
        # Input("filter-2", "value"),# element ID that will be the source value # "value" ("property") is the selected option
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)

# In the function set the filters in the Data Frame and prepare the figure
# This function always ran when APP opens with default input values from callback
def update_charts(input_1, input_3, input_4): # gets the data from input in callback. If there are 2 inputs. there must be 2 variables
    mask = ( # Set up all the filters to be applied in the DataFrame
        (df_1[column_f1] == input_1)
        # & (df_1[column_f2] == input_2)
        & (df_1[column_x1] >= input_3)
        & (df_1[column_x1] <= input_4)
    )
    filtered_df_1 = df_1.loc[mask, :] # Apply the filter in the DaraFrame

    chart_1 = { # prepare the chart based on the filtered Data. Set "data" and "layout"
        "data": [
            {
                "x": filtered_df_1[column_x1], # X axis data
                "y": filtered_df_1[column_y1], # Y axis data
                "type": "lines", # bar
                "hovertemplate": "%{y:,.0f}<extra></extra>", # $%{y:.0f} # add text when hovering
            },
        ],
        "layout": {
            "title": {
                    "text": filtered_df_1[column_y1].name.capitalize(),
                    "x": 0.05,
                    "xanchor": "left",
                    },
            "xaxis": {"fixedrange": True},
            "yaxis": {
                    # "tickprefix": "$", # add this prefix
                    "fixedrange": True
                    },
            "colorway": ["#DC143C"], # color of the line #  '#DC143C', '#B78511'
        },
    }

    chart_2 = {
        "data": [
            {
                "x": filtered_df_1[column_x1], # x axis
                "y": filtered_df_1[column_y2], # y axis
                "type": "lines", # bar
                "hovertemplate": "%{y:,.0f}<extra></extra>", # $%{y:.0f}
            },
        ],
        "layout": {
            "title": {"text": filtered_df_1[column_y2].name.capitalize(),
                      "x": 0.05 ,
                      "xanchor": "left"
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#B78511"],
        },
    }
    return chart_1, chart_2 # returns the charts


if __name__ == '__main__':
    # # app.run_server(debug=True)
    # app.run_server(debug=True)
    PORT = 8050   # Deployment information

    app.run_server(debug=True
                   # host='0.0.0.0' #, port=8080
                   , port=PORT)  # Starting flask server
