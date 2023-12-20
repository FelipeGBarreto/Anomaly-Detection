def _calc_anomaly_(
    base = df,
    country_currency = 'Brazilian real',
    rolling_window = 60
):
    """"
    Needed to manipulate the data to fit with this format
    df: name of dataframe
    country_currency: name of the column that have the currency to be analyzed
    rolling_window: rolling window to be analyzed each point of the day

    date: name of the column in pandas datetime
    """"
    df_currency = base[['date',country_currency]]
    df_currency[country_currency] = df_currency[country_currency]

    df_currency = df_currency.sort_values(by=['date'], ascending = True)

    rolling_window = 60

    # Calcule Q1, Q2 e Q3 com base nos valores dos 60 dias anteriores, excluindo a linha atual
    df_add = df_currency.copy()
    df_add['Q1'] = df_add[country_currency].rolling(window=rolling_window, min_periods=1).quantile(0.25)
    df_add['Q2'] = df_add[country_currency].rolling(window=rolling_window, min_periods=1).quantile(0.50)
    df_add['Q3'] = df_add[country_currency].rolling(window=rolling_window, min_periods=1).quantile(0.75)
    df_add = df_add.sort_values(by=['date'], ascending=False)

    df_add_quantiles = df_add[1:].drop(
        ['date',country_currency], axis=1
    )

    df_add_quantiles = pd.concat(
        [df_add_quantiles, df_add_quantiles.iloc[-1:]]
        , ignore_index=True, axis=0
    )

    df_currency = df_currency.sort_values(by=['date'], ascending=False).reset_index().drop('index',axis=1)

    df_final = pd.concat(
        [df_currency,df_add_quantiles]
        ,ignore_index = True
        ,axis = 1
    )

    df_final.columns = ['date',country_currency,'Q1','Q2','Q3']

    df_final['IQR'] = df_final.Q3 - df_final.Q1
    df_final['lower_bound'] = df_final.Q1 - 1.5 * df_final.IQR
    df_final['upper_bound'] = df_final.Q1 + 1.5 * df_final.IQR
    df_final['outlier_neg'] = df_final[country_currency] < df_final['lower_bound']
    df_final['outlier_pos'] = df_final[country_currency] > df_final['upper_bound']
    df_final['is_outlier'] = (df_final.outlier_neg == True) | (df_final.outlier_pos == True)

    return df_final