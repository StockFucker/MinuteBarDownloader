# -*- coding: utf-8 -*-

import sys
import pandas as pd
import math
import json
from datetime import datetime
from threading import Timer
import easyquotation
import time




def stockFilter(stock):
    head = stock[:1]
    return head == "0" or head == "3" or head == "6"

def calculateDailyTotalValue():
    quotation = easyquotation.use('qq')
    data = quotation.all
    df = pd.DataFrame(data)
    df = df.T
    to_drop = list(df.columns)
    to_drop.remove("now")
    to_drop.remove("涨跌(%)")
    to_drop.remove("总市值")
    to_drop.remove("name")
    to_drop.remove("unknown")
    df = df.drop(pd.Index(to_drop),1)

    stocks = filter(stockFilter,list(df.index))
    df = df[df.index.isin(stocks) == True] 
    df.columns = ["name","price","unknown","total_value","changepercent"]

    print(df)


def filterST(df):
    st_names = []
    for name in df['name']:
        if name.find("S") >= 0:
            st_names.append(name)
    df = df[df['name'].isin(st_names) == False]
    risk_notification = ['300028','300022','300143','300372','300126','300399','300380','300135','600656']
    df = df[df.index.isin(risk_notification) == False]
    return df

def scheduleTask():
    x=datetime.today()
    y=x.replace(day=x.day, hour=14, minute=55, second=30, microsecond=0)
    delta_t=y-x

    secs=delta_t.seconds+1

    t = Timer(secs, calculateDailyTotalValue)
    t.start()

calculateDailyTotalValue()