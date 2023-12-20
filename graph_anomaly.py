def _graph_anomaly_seaborn(
    base=df,
    country_currency='Brazilian real',
    rolling_window=60
):
    """"
    Needed to manipulate the data to fit with this format
    df: name of dataframe
    country_currency: name of the column that have the currency to be analyzed
    rolling_window: rolling window to be analyzed each point of the day

    date: name of the column in pandas datetime
    """"

    df_final = _calc_anomaly_(
        base=base,
        country_currency=country_currency,
        rolling_window=rolling_window
    )

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_final, x='date', y=country_currency, color='gray', label=country_currency.title())

    # Negative Outlier
    outlier_neg_indices = df_final[df_final['outlier_neg']].index
    sns.scatterplot(x=df_final['date'].iloc[outlier_neg_indices], y=df_final[country_currency].iloc[outlier_neg_indices], color='blue', label='Outlier Negativo')

    for i in outlier_neg_indices:
        plt.text(df_final['date'].iloc[i], df_final[country_currency].iloc[i], f"{df_final[country_currency].iloc[i]:.2f}", color='blue')

    # Positive Outliers
    outlier_pos_indices = df_final[df_final['outlier_pos']].index
    sns.scatterplot(x=df_final['date'].iloc[outlier_pos_indices], y=df_final[country_currency].iloc[outlier_pos_indices], color='red', label='Outlier Positivo')

    for i in outlier_pos_indices:
        plt.text(df_final['date'].iloc[i], df_final[country_currency].iloc[i], f"{df_final[country_currency].iloc[i]:.2f}", color='red')

    # Mean (range)
    rolling_mean = df_final[country_currency].rolling(window=rolling_window).mean()
    sns.lineplot(data=df_final, x='date', y=rolling_mean, color='green', linestyle='--', label=f'Média Móvel ({rolling_window} dias)')

    plt.title(f'Detecção de Anomalias & Média Móvel com range de {rolling_window} dias')
    plt.xlabel('Data')
    plt.ylabel(f'Valor {country_currency.title()}')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.show()
    