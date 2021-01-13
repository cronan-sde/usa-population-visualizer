#!/usr/bin/env python3

import requests as req
import plotly.graph_objects as pgo
import pandas as pd

POPULATION_API = "https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest"
STATE_CODES = {}

def main():
#    popDict = getStateData()
    setStateCodes()
    print(STATE_CODES)
   # generateMap(popDict)

## Get population data on all 50 states
## adds each state name as key and pop as value to data dictionary
## returns dictionary
def getStateData():
    data = {}
    statePop = req.get(POPULATION_API).json().get("data")

    for stateData in statePop:
        state = stateData.get("State")
        if state != "Puerto Rico" and state != "District of Columbia":
            data[state] = int(stateData.get("Population"))


    return data


def setStateCodes():
    global STATE_CODES
    stateCodeData = pd.read_csv('statecodes.csv', index_col=0)
    STATE_CODES = stateCodeData.to_dict()


if __name__ == "__main__":
    main()
