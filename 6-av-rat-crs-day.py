import justpy as jp
import pandas as pd
from datetime import datetime
from pytz import utc

df = pd.read_csv("reviews.csv",parse_dates=['Timestamp'])


df['Weekday'] = df['Timestamp'].dt.strftime('%A')
df['Daynumber'] = df['Timestamp'].dt.strftime('%w')
weekday_average = df.groupby(['Weekday','Daynumber']).mean()
weekday_average = weekday_average.sort_values('Daynumber')

chart_def=""" 
 {
    chart: {
        type: 'spline',
        inverted: false
    },
    title: {
        text: 'Atmosphere Temperature by Altitude'
    },
    subtitle: {
        text: 'According to the Standard Atmosphere Model'
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Altitude'
        },
        labels: {
            format: '{value} km'
        },
        accessibility: {
            rangeDescription: 'Range: 0 to 80 km.'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Temperature'
        },
        labels: {
            format: '{value}°'
        },
        accessibility: {
            rangeDescription: 'Range: -90°C to 20°C.'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.x} km: {point.y}°C'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Temperature',
        data: [[0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
            [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]]
    }]
}
"""

def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp, text="Analysis of Course Reviews",classes="text-h3 text-center q-pa-md")
    p1 = jp.QDiv(a=wp, text="These graphs represent course review analysis")
    
    hc = jp.HighCharts(a=wp,options=chart_def)

    hc.options.xAxis.categories = list(weekday_average.index.get_level_values(0))

    hc.options.series[0].data = list(weekday_average.Rating)

    return wp

jp.justpy(app)