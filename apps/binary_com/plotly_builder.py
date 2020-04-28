#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import plotly.offline as offline
import plotly.graph_objects as go
from matplotlib import pyplot

def save_with_plotly(ticks: list = None, image: str = None):
    """Сохранение графика-отчета
       https://pyprog.pro/mpl/mpl_plot.html
       :param ticks: тики, массивом (время, значение, боллинджер)
       :param image: сохранить как изображение ='png'
    """
    contracts_trace = {
        "x": ["2017-02-13", "2017-02-14", "2017-02-15"],
        "y": [1.2, 1.5, 1.3],
        "mode": "markers",
        "type": "scatter",
        "name": "Contract",
        "text": ["contract1", "contract2", "contract3"],
        "marker": {
          "size":30,
          "color":["rgba(204,204,204,1)", "rgba(222,45,38,0.8)", "rgba(204,204,204,1)"]
        },
        ###"yaxis": "y2",
    }
    fractals_trace = {
        "x": ["2017-02-13", "2017-02-14", "2017-02-15"],
        "y": [2.2, 2.5, 2.3],
        "mode": "markers",
        "type": "scatter",
        "name": "Fractals",
        #"text": ["fractal1", "fractal2', 'fractal3'],
        "marker": {
            "size":12,
            #"color":["rgba(204,204,204,1)", "rgba(222,45,38,0.8)", "rgba(204,204,204,1)"],
            "symbol": ["circle", "square", "diamond"],
        },
    }
    contracts_helpers = {
        "x": ["2017-02-13", "2017-02-14", "2017-02-15"],
        "y": [1.3, 1.4, 1.6],
        #"mode": "markers",
        "type": "scatter",
        "name": "Helpers",
        "text": ["helper1", "helper2", "helper3"],
        "marker": {
            "size":12,
            "color":["rgba(204,204,204,1)", "rgba(222,45,38,0.8)", "rgba(204,204,204,1)"]
        },
    }
    rsi_trace = {
        "x": ["2017-02-13", "2017-02-14", "2017-02-15"],
        "y": [20, 35, 80],
        "opacity": 0.5,
        "name": "RSI",
        "yaxis": "y3",
        "type": "scatter",
    }
    ao_trace = {
        "x": ["2017-02-13", "2017-02-14", "2017-02-15"],
        "y": [0.5, 1, -1],
        "opacity": 0.5,
        "marker":{
            "color": ["rgba(204,204,204,1)", "rgba(222,45,38,0.8)", "rgba(204,204,204,1)"]
        },
        "name": "AO",
        "yaxis": "y2",
        "type": "bar",
    }
    ac_trace = {
        "x": ["2017-02-13", "2017-02-14", "2017-02-15"],
        "y": [0.7, 0.3, -0.4],
        "opacity": 0.5,
        "marker":{
            "color": ["rgba(104,204,104,1)", "rgba(242,15,18,0.8)", "rgba(104,204,104,1)"]
        },
        "name": "AC",
        "yaxis": "y2",
        "type": "bar",
    }
    bollinger_middle = {
        "name": "BB_Middle",
        "line": {"color": "rgba(143,115,220,0.5)"},
        "y": [80, 50, 70],
        "x": ["2017-01-04", "2017-01-05", "2017-01-06"],
        "type": "scatter",
    }
    bollinger_top = {
        "name": "BB_Top",
        "line": {"color": "rgba(243,15,120,0.2)"},
        "y": [85, 55, 75],
        "x": ["2017-01-04", "2017-01-05", "2017-01-06"],
        "type": "scatter",
    }
    bollinger_bottom = {
        "name": "BB_Bottom",
        "line": {"color": "rgba(243,15,120,0.2)"},
        "fillcolor": "rgba(143,115,220,0.05)",
        "y": [75, 45, 65],
        "x": ["2017-01-04", "2017-01-05", "2017-01-06"],
        "fill": "tonexty",
        "type": 'scatter',
    }
    alligator1 = {
        "name": "Alligator Lips",
        "line": {"color": "rgba(0,255,0,0.8)"},
        "y": [110, 120, 90],
        "x": ["2017-01-04", "2017-01-05", "2017-01-06"],
        "type": "scatter",
    }
    alligator2 = {
        "name": "Alligator Teeth",
        "line": {"color": "rgba(255,0,0,0.8)"},
        "y": [90, 105, 110],
        "x": ['2017-01-04', '2017-01-05', '2017-01-06'],
        "type": "scatter",
    }
    alligator3 = {
        "name": "Alligator Jaw",
        "line": {"color": "rgba(0,0,255,0.8)"},
        "y": [100, 104, 99],
        "x": ["2017-01-04", "2017-01-05", "2017-01-06"],
        "type": "scatter"
    }
    candles_trace = {
        "name": "",
        "x": ['2017-01-04', '2017-01-05', '2017-01-06', '2017-01-09', '2017-01-10', '2017-01-11', '2017-01-12', '2017-01-13', '2017-01-17', '2017-01-18', '2017-01-19', '2017-01-20', '2017-01-23', '2017-01-24', '2017-01-25', '2017-01-26', '2017-01-27', '2017-01-30', '2017-01-31', '2017-02-01', '2017-02-02', '2017-02-03', '2017-02-06', '2017-02-07', '2017-02-08', '2017-02-09', '2017-02-10', '2017-02-13', '2017-02-14', '2017-02-15'],
        "close": [116.019997, 116.610001, 117.910004, 118.989998, 119.110001, 119.75, 119.25, 119.040001, 120, 119.989998, 119.779999, 120, 120.080002, 119.970001, 121.879997, 121.940002, 121.949997, 121.629997, 121.349998, 128.75, 128.529999, 129.080002, 130.289993, 131.529999, 132.039993, 132.419998, 132.119995, 133.289993, 135.020004, 135.509995],
        "decreasing": {"line": {"color": '#ca2612'}},
        "high": [116.510002, 116.860001, 118.160004, 119.43, 119.379997, 119.93, 119.300003, 119.620003, 120.239998, 120.5, 120.089996, 120.449997, 120.809998, 120.099998, 122.099998, 122.440002, 122.349998, 121.629997, 121.389999, 130.490005, 129.389999, 129.190002, 130.5, 132.089996, 132.220001, 132.449997, 132.940002, 133.820007, 135.089996, 136.270004],
        "increasing": {"line": {"color": "#4cb104"}},
        "line": {"color": "rgba(31,119,180,1)"},
        "low": [115.75, 115.809998, 116.470001, 117.940002, 118.300003, 118.599998, 118.209999, 118.809998, 118.220001, 119.709999, 119.370003, 119.730003, 119.769997, 119.5, 120.279999, 121.599998, 121.599998, 120.660004, 120.620003, 127.010002, 127.779999, 128.160004, 128.899994, 130.449997, 131.220001, 131.119995, 132.050003, 132.75, 133.25, 134.619995],
        "open": [115.849998, 115.919998, 116.779999, 117.949997, 118.769997, 118.739998, 118.900002, 119.110001, 118.339996, 120, 119.400002, 120.449997, 120, 119.550003, 120.419998, 121.669998, 122.139999, 120.93, 121.150002, 127.029999, 127.980003, 128.309998, 129.130005, 130.539993, 131.350006, 131.649994, 132.460007, 133.080002, 133.470001, 135.520004],
        "type": "candlestick",
        "xaxis": "x",
        "yaxis": "y",
    }

    layout = {
        "dragmode": "zoom",
        "barmode": "relative",
        "margin": {
            "r": 10,
            "t": 25,
            "b": 40,
            "l": 50,
        },
        "showlegend": False,
        "xaxis": {
            "autorange": True,
            "domain": [0, 1],
            "title": "Date",
            "type": "date",
        },
        "yaxis": {
            "autorange": True,
            "anchor": "free",
        },
        "yaxis2":{
            "autorange": True,
            "title": "AO/AC",
            "titlefont": {"color": "rgb(148, 103, 189)"},
            "tickfont": {"color": "rgb(148, 103, 189)"},
            "overlaying": "y",
            "side": "right"
        },
        "yaxis3":{
            "autorange": True,
            "title": "RSI",
            "titlefont": {"color": "rgb(48, 93, 89)"},
            "tickfont": {"color": "rgb(48, 93, 89)"},
            "overlaying": "y",
            "side": "right"
        },
    }
    data = [contracts_trace, bollinger_middle, bollinger_top, bollinger_bottom]

    fname = '%s.html' % datetime.datetime.today().strftime('%Y_%m_%d_%H_%M')
    path = '../../media/%s' % fname

    if image:
        path = path.replace('.html', '.%s' % image)

        epoch = [data[0] for data in ticks]
        pyplot.plot(epoch, [data[1] for data in ticks], color = '#0a0b0c')
        pyplot.plot(epoch, [data[2][0] for data in ticks], color = '#0a0b0c')
        pyplot.plot(epoch, [data[2][1] for data in ticks], color = '#0a0b0c')
        pyplot.plot(epoch, [data[2][2] for data in ticks], color = '#0a0b0c')
        pyplot.savefig(
            fname = path,
        )
    else:
        offline.plot({'data':data, 'layout':layout}, filename=path, auto_open=False, show_link=False)

    return path

