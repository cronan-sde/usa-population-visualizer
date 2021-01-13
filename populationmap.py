#!/usr/bin/env python3

import requests as req
import plotly.graph_objects as pgo
import pandas as pd
import os
import subprocess as sp

POPULATION_API = "https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest"
CUR_YEAR=""

## Runs the program
def main():
    #getDataFrame returns a pandas dataframe
    df =  getDataFrame()
    #passing the data to generateMap function
    generateMap(df)

## Get population data on all 50 states
## adds each state name as key and pop as value to data dictionary
## returns dictionary
def getStateData():
    global CUR_YEAR
    data = {}
    statePop = req.get(POPULATION_API).json().get("data")
    CUR_YEAR = statePop[0].get("Year")

    for stateData in statePop:
        state = stateData.get("State")
        if state != "Puerto Rico" and state != "District of Columbia":
            data[state] = stateData.get("Population")


    return data

#TODO: figure out how to get state accessable from df, comment code, refactor
#TODO: potentially only need to get population from getStateData as a list and add to df
##Reads data from a csv containing States and their abbreviations
##creates a population list that contains the population for all 50 states
##population list is added to the pandas df, all columns are converted to str
##The df is then returned 
def getDataFrame():
    df = pd.read_csv('statecodes.csv')
    statePops = getStateData()
    
    population = []

    for state in statePops:
        population.append(statePops.get(state))

    df['population'] = population
    
    for col in df.columns:
        df[col] = df[col].astype(str)
    
    return df

##Utilizing plotly to create an interactive map of the US
##shows state population data
## resulting map is then saved to an html file to be viewed
def generateMap(df):
    df['text'] = 'State: ' + df['state'] + '<br>' + 'Population: ' + df['population']

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

    stateMap.update_layout(title_text = CUR_YEAR +' US Population by State', geo = dict(scope='usa',
        projection= pgo.layout.geo.Projection(type = 'albers usa'),
        showlakes=True,
        lakecolor='rgb(255,255,255)'),
        )

    #writing the map to html file for viewing
    #fileUrl = "/home/student/static/population_map.html"
    #stateMap.write_html(fileUrl)

    ##To open the map up uncomment the line below
    stateMap.show()


if __name__ == "__main__":
    main()
