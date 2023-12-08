import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Kline, Grid, Bar, Line,Scatter
from pyecharts.commons.utils import JsCode
import os
color_list = ["#ec0000", "#00da3c",
              "#FFA500", "#8FBC8F",
              "#ec0000", "#00da3c",
              "#ec0000", "#00da3c",
              "#ec0000", "#00da3c",
              "#ec0000", "#00da3c",
              "#ec0000", "#00da3c",
              "#ec0000", "#00da3c",
              ]

def setKlineCtl(kline, count):
    all_opts = []
    all_opts.append(opts.DataZoomOpts(
                             is_show=True,
                             xaxis_index=[0, 1],  # 这里需要修改可缩放的x轴坐标编号
                             type_="slider",
                             pos_top="85%",
                             range_start=98,
                             range_end=100,
                         ))
    for i in range(count*2):
        all_opts.append(
            opts.DataZoomOpts(
                             is_show=False,
                             type_="inside",
                             xaxis_index=[0, i+1],  # 这里需要修改可缩放的x轴坐标编号
                             range_start=98,
                             range_end=100,
                         ))

    kline.set_global_opts(
                     datazoom_opts=all_opts,
                     yaxis_opts=opts.AxisOpts(
                         is_scale=True,
                         splitarea_opts=opts.SplitAreaOpts(
                             is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                         ),
                     ),
                     tooltip_opts=opts.TooltipOpts(
                         trigger="axis",
                         axis_pointer_type="cross",
                         background_color="rgba(245, 245, 245, 0.8)",
                         border_width=1,
                         border_color="#ccc",
                         textstyle_opts=opts.TextStyleOpts(color="#000"),
                     ),
                     axispointer_opts=opts.AxisPointerOpts(
                         is_show=True,
                         link=[{"xAxisIndex": "all"}],
                         label=opts.LabelOpts(background_color="#777"),
                     ),
                     brush_opts=opts.BrushOpts(
                         x_axis_index="all",
                         brush_link="all",
                         out_of_brush={"colorAlpha": 0.1},
                         brush_type="lineX",
                     ),
                     )


def getKline(data, index,buy_points=[],sell_points=[]):
    sell_base = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAADuElEQVR4nO2aSahcRRSGT6z/r37tBIoTRFB0ISIoiuLCoIs8EIkTqKBRQVwE1E02Wah7h03A4LAR0a0DOOCACoI+I+L4VBIw6kJEjKA+Cfi6z7m+ktN2VJ6SW327bvdF8kNt69R361Sdoa7IYf1PlUROthivMfJ+Jd8wYFmBb5U8oKQq+YMBe41cMnJXRW5NCwunSReURGIV4w2+cCXXjEwNxodKbksiR80FoiJvVXJ/w8X/a/iOVeRNMwNI/f6pSr5aCuA/gF5LIie2CjEkz1Py+7Yg7OAA9qR+f2MrEKu93hmjA9s2BP+C+SaJnFAUIonQyA9mBsGxmwHPFgVRYPsEX/IzBXYosMl9PYn0xuMUC2HRyAcU+C53vorcWgTCF5FzO3m88Jssc84FBe5V0jI+zHIREIvx+gwI8x2YeO4QrvRgmeFim6YHAZ7IcIFdTef3ncmY/+ESIJ9mfLELm84/crM61wU+mhpEyZU6kCRy9DQ2jHy0xnVXSoBY2yAKXKrkr4ew8XYJkB9rfTiERem6DFjOOIxLSQTSZVmN//7jwL+QRI6TrspC2JwbhT0X86jeevbaRElkg5Hv5sKMgX43crcC9wzJC5JIkC5oSJ6v5GASmHVgXu6+ZeR9FuPVSeSkucFYjNcpWTWFWQe2ZsDnRj5kMV7l+dw8YFZKwKwD+8nIx9wNZwaz2uudOXaTojAHd0qB54fkuTMDshAuH7d22gAyvyiSyBEzAxrEeNboEP/p86WBXp75+XF5FViRNxv5iAEfZxVOdTDAc3O/vr3ppsBlCtyt5CtK/tYQ5k7pkpLIkV4V+g01ye2n5M+dTX+SyLHjPnGW+w3J26XLshC2ZNbtL0rXZeSDtbsCfCld1yDGszPOyYHGBox85xATr1bkjSVAPFZkgAwaG1DylxoDu4uA9PsbM0D2NzZg5Ps1k695h35akCF5W8bNtTQNyM4MA+9Nk0Ykkf74Sa7Ozs7GIApckhmwXmrSEvIuvwJPZwXGEDZPV+YCn2QZAr62GK/NzVg9Vc8uoYGvps6ELYQrsoz9bXTfKC6EsGW11zs9iRzji/CGhBdOCtyh5JuTPJ5W5C1SQgo8NRFM+TfFDUVARgdywk5KkQHsK96o8MzV850ZQuxt7YcCL3BGT2cZSd5U7gQ8k0SOl1nkRkq+3sIufOHtIZm1huQ54x1q/GztOdsoloSwWOxQN5V34hW4yK9WAx73aO8+PuoFkwMvcUc/GgB7xq3UJxW4S4GL/cVqros/LGlHfwCXq0xbmFSh+QAAAABJRU5ErkJggg=="
    buy_base = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAACVUlEQVR4nO3Zv4sTURAH8NHMd3aPM3iiWAj+aCwU0UZtLBWsRK4U/wULwUIQtBALucJCsdc/wMJOK8EjtRaiIKecNnpaeB5qkpnAyEtOFAX3QXY3b48MTDvLJ/Nm33sbomlMYzIhho4YfOxUDETxGcavoXgCw4KYzJNTuy6IV5qKNTHclZ7sbzbkN6grypfJqdVsyHpC+QE5ceMhMuwO39sYEAspZzcEBMZLpS6xmIf+t4BTPuMzu8TkTFgyoujFYjJrnUwH8ne9nhyE8au4ruBOspAQuee7RfElonYnaciwrvK1iDl5kzwEfRwurK1YTR5CTlsKO6L8vgmQdjEEj5OHoI8jxUuLr6QPMdwomI9B1s32JQ2RnhwQxfeCbtwvDVEFJLPWKSg+FMzGyqzTznQgTkJO21n5eKZ8QQxPI165P1j5RKmIWEhZCcVKJYhaIYpPYXYqQdQKGWG6MNyq5INErRD7tcR4GX0cajxERt1ZDeex5kNs2Jl35DRXG6SwiNNc7vnezFqnYbgO45fRGMPtdCD/wjZhgPOi+BqxxPqlbI6VQNaDlY9G3eGVLyYNCQHDzYhZeZg+JOI4D+Xl5CHkNBsxJ9+aANm6ISCsfKz4FcxLyUPC2SriGYtJQ8I9JewTxR3BQsob4rmoDdHgpdxRSoE4tcOH7HDNFeWrYvwipq6M5uMtOW2uBVJtyvzYiElDoHhUCmKyEH5OTtuaDumQ047SELVDtMK/qGuahY/hFJx7vqd0wB+QxRJ/8bVwkhXjZ+H/dFG+NNwjnFAZYBrToLHiJ8jJWRYo5NnpAAAAAElFTkSuQmCC"
    kline = (
        Kline(init_opts=opts.InitOpts(width="1800px", height="1000px"))
        .add_xaxis(xaxis_data=list(data['candle_begin_time']))
        .add_yaxis(
            series_name=data.iloc[0]['symbol'],
            y_axis=data[["open", "close", "low", "high"]].values.tolist(),
            # itemstyle_opts=opts.ItemStyleOpts(color=color_list[0], color0=color_list[0]),
            xaxis_index=1, yaxis_index=1
        )
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False, pos_top=3, pos_left=100 + 110 * index,selected_mode='single'))
    )
    # 创建 Line 图来标记买卖点
    scatter = Scatter()
    scatter.add_xaxis(xaxis_data=data['candle_begin_time'].tolist())
    # 假设 buy_points 是时间戳列表

    scatter.add_yaxis(series_name=data.iloc[0]['symbol'],
                   y_axis=[data[data['candle_begin_time'] == time]['low'].values[0] if time in buy_points else None for time in
                  data['candle_begin_time']], symbol=f"image://data:image/png;base64,{buy_base}",
                   symbol_size=15,color="green"
    )
    # 将卖出点标记为倒三角形
    scatter.add_yaxis(series_name = data.iloc[0]['symbol'],
                   y_axis=[data[data['candle_begin_time'] == time]['high'].values[0] if time in sell_points else None for time in
                  data['candle_begin_time']],
                   symbol=f"image://data:image/png;base64,{sell_base}", symbol_size=15,color="red"
    )

    # 将 Line 图叠加在 Kline 图上
    kline.overlap(scatter)
    return kline


def getVolumeBar(data, index ):
    bar = (
        Bar()
        .add_xaxis(xaxis_data=list(data.candle_begin_time))
        .add_yaxis(
            series_name=data.iloc[0]['symbol'],
            y_axis=data["volume"].tolist(),
            xaxis_index=1,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(
                color=JsCode(
                    """
                function(params) {
                    var colorList;
                    if (barData[params.dataIndex][1] > barData[params.dataIndex][0]) {
                        colorList = '#ec0000';
                    } else {
                        colorList = '#00da3c';
                    }
                    return colorList;
                }
                """
                )
            ),
        )
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False, pos_top=30, pos_left=100 + 150 * index,selected_mode='single'))

    )
    return bar

def plot_kline_trade(all_df, data, factors,trade_df,min_price=50):
    klines = []
    bars = []
    count = len(all_df)
    for i in range(count):
        symbol_condition = trade_df['symbol'] == all_df[i]['symbol'][0]
        buy_condition = trade_df['实际下单资金'] > min_price
        sell_condition = trade_df['实际下单资金'] < -min_price
        # 获取满足条件的行的索引值列表
        buy_points = trade_df[symbol_condition & buy_condition]['candle_begin_time'].tolist()
        sell_points = trade_df[symbol_condition & sell_condition]['candle_begin_time'].tolist()
        kline = getKline(all_df[i], i,buy_points,sell_points)
        klines.append(kline)
        bar = getVolumeBar(all_df[i], i)
        bars.append(bar)

    setKlineCtl(klines[0], count)


    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width="1500px",
            height="800px",
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )

    grid_chart.add_js_funcs(
        "var barData={}".format(all_df[0][["open", "close"]].values.tolist()))  # 导入open、close数据到barData改变交易量每个bar的颜色

    for i in range(count):
        grid_chart.add(
            # overlap_kline_line,
            klines[i],
            grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", pos_top="15%", height='30%'),
        )
    for i in range(count):
        grid_chart.add(
            bars[i],
            grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", pos_top="45%", height='10%'),
        )

    if len(factors) > 0:
        line = (Line()
                .add_xaxis(xaxis_data=list(data.candle_begin_time))
                .set_global_opts(legend_opts=opts.LegendOpts(is_show=True, pos_top=62, pos_left=10,selected_mode='single'))
                )

        for factor in factors:

            line = line.add_yaxis(
                series_name=factor.split('_')[1] + '-USDT',
                y_axis=data[factor].tolist(),
                xaxis_index=1,
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )

        grid_chart.add(
            line,
            grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", pos_top="55%", height='30%'),
        )

    path = './kline_volume.html'
    grid_chart.render(path)

    res = os.system('start ' + path)
    if res != 0:
        os.system('open ' + path)
