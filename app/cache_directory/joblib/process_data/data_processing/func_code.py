# first line: 8
@memory.cache
def data_processing():
    # Read the three CSV files
    df1 = pd.read_csv('./life_expectancy_years.csv')
    df2 = pd.read_csv('./population_total.csv')
    df3 = pd.read_csv('./ny_gnp_pcap_cn.csv')

    # Forward fill the missing data
    df1 = df1.ffill()
    df2 = df2.ffill()
    df3 = df3.ffill()

    # Reshape each dataframe into tidy format
    df1 = pd.melt(df1, id_vars=['country'], var_name='year', value_name='life_expectancy')
    df2 = pd.melt(df2, id_vars=['country'], var_name='year', value_name='population')
    df3 = pd.melt(df3, id_vars=['country'], var_name='year', value_name='gni_per_capita')

    # Merge the three dataframes into one
    merged_df = pd.merge(df1, df2, on=['country', 'year'], how='outer')
    merged_df = pd.merge(merged_df, df3, on=['country', 'year'], how='outer')

    return merged_df
