#!/usr/bin/env python3

import requests as req
import plotly.graph_objects as pgo
import pandas as pd

POPULATION_API = "https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest"
CUR_YEAR=""

## Runs the program
def main():
    #getDataFrame returns a pandas dataframe
    df =  getDataFrame()
    #passing the data to generateMap function
    generateMap(df)

"""
Get population data of all 50 states
Assign cur data year to the CUR_YEAR var
Add each population to a list, return the list
Excludes Puerto Rico and District of Columbia from results
"""
def getStateData():
    global CUR_YEAR
    population = []
    statePop = req.get(POPULATION_API).json().get("data")
    CUR_YEAR = statePop[0].get("Year")

    for stateData in statePop:
        state = stateData.get("State")
        if state != "Puerto Rico" and state != "District of Columbia":
           #appending population to list
           population.append(stateData.get("Population"))
    
    #return the population list
    return population

"""
Reads data from a csv containing States and their abbreviations
Utilizes getStateData() to get list of populations of each state,
population list is added to the pandas df, all columns are converted to str
The df is then returned 
"""
def getDataFrame():
    #creating initial df of state,code: state name and abbreviation
    df = pd.read_csv('statecodes.csv')
    #getting list of populations by state
    statePops = getStateData()

    #create new column population - populated by list of populations
    df['population'] = statePops
    
    #ensuring each column is converted to str to be used by plotly
    for col in df.columns:
        df[col] = df[col].astype(str)
    
    return df

"""
Utilizing plotly to create an interactive map of the US
showing state population data
resulting map is then launched for viewing in browser
NOTE: If enviornment is not setup to launch browser, uncomment the line that can 
write to html and choose a file location to save the html for viewing
"""
def generateMap(df):
    # formatting df on how hover text should display
    df['text'] = 'State: ' + df['state'] + '<br>' + 'Population: ' + df['population']

    # Setting up the map
    # locations utilizes state abbr
    # z=specifies the first line on hover will display population number as int
    # locationmode specifies it will be US states map
    # colorscale sets the coloring
    #text= will set the hover text
    #colorbar_title will set title for the bar graph 
    stateMap = pgo.Figure(data=pgo.Choropleth(
        locations = df['code'],
        z=df['population'].astype(int),
        locationmode = 'USA-states',
        colorscale = 'Reds',
        autocolorscale = False,
        text= df['text'],
        marker_line_color = 'white',
        colorbar_title = "Population in Millions"
    ))

    # Setting layout of the map
    # title_text sets the title
    # geo = is setting scope of map to be usa only
    # projection= type='albers usa' moves alaska and hawaii to be closer to lower 48 states
    stateMap.update_layout(title_text = CUR_YEAR +' US Population by State', geo = dict(scope='usa',
        projection= pgo.layout.geo.Projection(type = 'albers usa'),
        showlakes=True,
        lakecolor='rgb(255,255,255)'),
     )

    ##writing the map to html file for viewing
    ##uncomment below 2 lines and add file path of your choice
    #fileUrl = "/path/to/file/<yourfilename>"
    #stateMap.write_html(fileUrl)

    ##To open the map up uncomment the line below
    stateMap.show()


if __name__ == "__main__":
    main()
