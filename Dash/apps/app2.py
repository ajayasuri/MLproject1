import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_table

from app import app

SIDEBAR_STYLE = {"position": "fixed", "top": 0, "left": 0,"bottom": 0,
    "width": "16rem", "padding": "2rem 1rem","background-color": "#f8f9fa",}


CONTENT_STYLE = {"margin-left": "18rem", "margin-right": "2rem", "padding": "2rem 1rem",}
Padded_STYLE = {"margin-left": "-1rem", "margin-right": "2rem","padding": "2rem 1rem",}

sidebar = html.Div([
        html.H3("Housing Prices in Ames, Iowa", style={'textAlign': 'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Introduction", href="/apps/app1", active="exact"),
                dbc.NavLink("Project", href="/apps/app2", active="exact"),
                dbc.NavLink("Pricing Model", href="/apps/app3", active="exact"),
                dbc.NavLink("Real Estate Handbook", href="/apps/app4", active="exact"),
                dbc.NavLink("Miscellaneous", href="/apps/app5", active="exact"),
            ], vertical=True, pills=True
        )
    ],
    style=SIDEBAR_STYLE,
)

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])



## Content is your new 'layout'


content = html.Div([

    html.Div([
        html.Div([html.H3('Project Overview'),
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Background', value='tab-1'),
        dcc.Tab(label='Models', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content', style=Padded_STYLE)
])

], style=CONTENT_STYLE)])


## This is how the sidebar and content is displayed together
layout = html.Div([sidebar, content])

df=pd.read_csv('All_housess_coords_4map.csv')
fig=px.scatter_mapbox(df, lat="Lat", lon="Long")
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


model_table=pd.DataFrame({'Model':['Lasso','Stepwise','Random Forest','SVR'],'Features Used':['Lasso','Stepwise','Tree','SVM'],'Train R2':['Lasso','Stepwise','Tree','SVM'],'Test R2':['Lasso','Stepwise','Tree','SVM']},index=['Lasso','Stepwise','Random Forest','SVM'])



@app.callback(
    Output('app-2-display-value', 'children'),
    Input('app-2-dropdown', 'value'))
@app.callback(Output('tabs-example-content', 'children'),
    Input('tabs-example', 'value'))
def display_value(value):
    if value=='tab-1':
        return (html.Div([
            html.H3('Welcome To Ames, Iowa:',style={'font-weight': 'bold'}),
            ]),dcc.Markdown('''For this assignment, we analyzed a data set of housing prices in and around Ames, Iowa. With over 2,500 rows of data pertaining to house sale records between 2006 - 2010, we took it upon ourselves to thoroughly clean, analyze, and create machine learning models to answer a handful of questions our team found beneficial from both a business and consumer perspective. This dataset includes numerous features to work with in order to come to the most optimal resolutions to the questions we looked to resolve. As visualized in the map below, the area of housing that our data focuses on is around Iowa State University.
            '''),
            dcc.Graph(id="choropleth",figure=fig),
            html.Hr(),html.Div([
            html.H3('Our Business Angle:',style={'font-weight': 'bold'}),]),
            dcc.Markdown('''We chose to investigate the Ames, Iowa housing market from the perspective of a data scientist working at Zillow Offers, Zillow's service line that purchases homes directly from individuals. Zillow Offers is an instant buying service provided to individual homeowners. Simply fill out a short online form about your home and Zillow will send an offer to purchase in just two business days, contingent upon an inspection. You have five days to accept the offer, which is finalized after an in-person inspection. You don't have to show your home, don't have to prep it for sale, can set your own move-out date, and have surety of payment. Also, if you choose not to sell your home to Zillow you can list it through a Zillow Premier Agent.
            This is primarily offered as a service to home sellers and is a way to drive volume into Zillow's other businesses. Zillow isn't flipping homes at a significant profit or renovating homes (just performing light, make-ready repairs), and runs its Offers business at 'razor-thin' margins. A 2019 analysis of instant home buyers (competitors include OpenDoor and OfferPAD) showed an average profit over cost of renovations of just 1.3%. Zillow bought 4,162 homes in 2020, with the Offers service currently available in 25 metro areas across the country.
            Zillow specifically cites its "superior data science and technology" as a competitive advantage, making this business angle chosen for our project particularly relevant. We decided to tackle two significant business problems for Zillow Offers as it hypothetically expands into Ames, Iowa; accurately predicting home prices and maintaining positive relations with the existing real estate industry in the area. The second point can be particularly difficult for Zillow as it continues to make inroads into the home buying industry. To provide incentive for real estate agents to work with Zillow rather than isolate the company, we will assemble a handbook for Zillow Premier Agents that provides useful data-driven insights into the local housing market in Ames, Iowa. This information will help agents provide more value to their clients and encourage them to work with Zillow, not against it.
            '''))
    else:
        return (html.Div([
            html.H3('Data Preproccessing:',style={'font-weight': 'bold'}),
            ]),dcc.Markdown('''
            #### Attribute Creation
            After cleaning, pruning and dummifying necessary features, we created two columns from the existing data we hypothesized would be more useful in our modeling. One column we created was the ‘RemodelYrsAftBuilt’ which is how long after being built a house was remodeled. If the year it was built was different than the year a house was remodeled, then the house was deemed to be remodeled and this column is the difference between those years.
            A second feature we created was neighborhood clusters. Instead of dummifying the neighborhood category which had almost 30 unique values, we wanted to extract the most important neighborhoods. However, each neighborhood was unique and we did not want to lose information by combining dissimilar values. We performed hierarchical clustering on each neighborhood as an instance to find which neighborhoods were highly dissimilar and which could be combined. As a result we combined the most similar neighborhoods and formed five clusters. More about this can be found in the Real Estate Handbook.
            #### Row Selection
            With so many different rows and columns, as well as various types of information included in our data, a huge task in our cumulative process was creating the most ideal dataset to work with. This meant transforming our data to fit the needs of our research and our machine learning models. For example, when it came to certain features of type categories, we decided to create binarized versions of those columns so that they may be interpretable by our models. As we aimed to be as specific as possible with our research, many columns and rows found themselves to be unnecessary to our cause and therefore were dropped altogether, but not before they received a thorough analysis to confirm their value.
            #### Dropped Attributes
            After extensive analysis, one of the few setbacks we experienced happened to revolve around one column: ‘LndAc_S’. A column that was received separate from what was provided to us through Kaggle, this feature showed the highest level of value to our dataset with a feature importance score of 87%. Although its relation to the rest of the data was predominant, due to our lack of knowledge on what it informed us of and multicolinearity, we had no choice but to drop this column entirely.
            '''), html.Hr(),html.Div([
            html.H3('Our Models:',style={'font-weight': 'bold'}),
            ]),dcc.Markdown('''Because we had over 100 attributes after dummifying necessary columns, feature selection was highly important in creating an explainable, properly fit model. To do so we employed Lasso Regression and Stepwise Feature Selection. The Stepwise was most successful in whittling the number of used features while maintaining stellar training and testing R2 values. Below is a summary of the models we tried on our data and their performance. An in depth analysis of the best performing model can be found in the Pricing Model tab.
            '''),dash_table.DataTable(
            id='Model_table',
            columns=[{"name": i, "id": i}
                 for i in model_table.columns],
                 data=model_table.to_dict('records'),
                 style_cell=dict(textAlign='left')))#,
        #style_header=dict(backgroundColor="paleturquoise"),
        #style_data=dict(backgroundColor="lavender")
