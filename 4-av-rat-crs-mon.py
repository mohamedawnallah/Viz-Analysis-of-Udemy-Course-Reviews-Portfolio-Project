import justpy as jp
import pandas as pd
from datetime import datetime
from pytz import utc

df = pd.read_csv("reviews.csv",parse_dates=['Timestamp'])


df['Month'] = df['Timestamp'].dt. strftime('%Y-%m')
month_course_average = df.groupby(['Month','Course Name']).count().unstack()

chart_def=""" 
{
  chart: {
    type: 'spline'
  },
  title: {
    text: 'Average fruit consumption during one week'
  },
  legend: {
    layout: 'vertical',
    align: 'left',
    verticalAlign: 'top',
    x: 150,
    y: 100,
    floating: false,
    borderWidth: 1,
    backgroundColor:'#FFFFFF'
  },
  xAxis: {
    categories: [
      'Monday',
      'Tuesday',
      'Wednesday',
      'Thursday',
      'Friday',
      'Saturday',
      'Sunday'
    ],
    plotBands: [{ // visualize the weekend
      from: 4.5,
      to: 6.5,
      color: 'rgba(68, 170, 213, .2)'
    }]
  },
  yAxis: {
    title: {
      text: 'Fruit units'
    }
  },
  tooltip: {
    shared: true,
    valueSuffix: ' units'
  },
  credits: {
    enabled: false
  },
  plotOptions: {
    areaspline: {
      fillOpacity: 0.5
    }
  },
  series: [
  ]
}
"""

def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp, text="Analysis of Course Reviews",classes="text-h3 text-center q-pa-md")
    p1 = jp.QDiv(a=wp, text="These graphs represent course review analysis")
    
    hc = jp.HighCharts(a=wp,options=chart_def)

    hc.options.xAxis.categories = list(month_course_average.index)

    hc_data = [{"name":crs_name,"data":[v2 for v2 in month_course_average.Rating[crs_name]]} for crs_name in month_course_average.Rating]
    hc.options.series = hc_data
    return wp

jp.justpy(app)