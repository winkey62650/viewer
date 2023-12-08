import pandas as pd
import pandas as pd
from Functions import plot_kline_trade

trade_df = pd.read_csv('/Users/winkey/Documents/量化/中性策略回测 自用版/indicator_v2/symbol_info.csv', error_bad_lines=False) #输入要复盘的csv
trade_df.columns = ['symbol','当前持仓量','目标下单量','目标下单分数','实际下单量','实际下单资金','candle_begin_time']
trade_df['candle_begin_time'] = pd.to_datetime(trade_df['candle_begin_time'])
trade_df['candle_begin_time'] = trade_df['candle_begin_time'].dt.round('H')
df = trade_df[trade_df['candle_begin_time'] < pd.to_datetime('2023-12-01')]
trade_df = df.copy()
trade_df['symbol'] = trade_df['symbol'].apply(lambda x: x[:-4] + '-' + x[-4:])
coin_list = trade_df['symbol'].unique().tolist()
start_date = trade_df['candle_begin_time'].min()  # 回测开始时间
end_date = trade_df['candle_begin_time'].max()  # 回测结束时间


min_price = 5  # 最小下单金额
coin_list = coin_list[-10:]  # 取多少个币
# coin_list = ['SNT-USDT']
factors = [('alpha', 34)]  # 要查看的因子
coin_path = "/Users/winkey/Documents/量化/中性策略回测 自用版/data/k线数据/"  # 输入1h币对分类的k线数据


if __name__ == "__main__":

    benchmark = pd.DataFrame(pd.date_range(start=start_date, end=end_date, freq='1H'))  # 创建2017-01-01至回测结束时间的1H列表
    benchmark.rename(columns={0: 'candle_begin_time'}, inplace=True)
    all_df = []
    for coin in coin_list:
        _coin_df = pd.read_csv(coin_path + "%s.csv" % coin, skiprows=1, encoding='gbk',
                              parse_dates=['candle_begin_time'])
        # ===与benchmark合并
        coin_df = pd.merge(left=benchmark, right=_coin_df, on='candle_begin_time', how='left', sort=True, indicator=True)
        coin_df.fillna(inplace=True, method='bfill')
        all_df.append(coin_df)

    all_factors = []
    df_factors = pd.DataFrame()
    for factor in factors:
        _cls = __import__('factors.%s' % (factor[0]), fromlist=('',))
        for index, df in enumerate(all_df):
            symbol = df['symbol'].iloc[-1]
            symbol = symbol[:len(symbol) - 5]

            if index == 0:
                df_factors['candle_begin_time'] = df['candle_begin_time']

            df = getattr(_cls, 'signal')(df, factor[1], 0, factor[0] + "_" + symbol)
            all_factors.append(factor[0] + "_" + symbol)
            df_factors = pd.merge(df_factors, df[['candle_begin_time', factor[0] + "_" + symbol]],
                                     on=['candle_begin_time'])
            for ind, row in df.iteritems():
                if ind.startswith('sig_'):
                    all_factors.append(symbol + '_' + ind)
                    df[symbol + '_' + ind] = df[ind]
                    df_factors = pd.merge(df_factors, df[['candle_begin_time', symbol + '_' + ind]],
                                          on=['candle_begin_time'])


    plot_kline_trade(all_df, df_factors, all_factors,trade_df,min_price)
