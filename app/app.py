import streamlit as st
#hints for debugging: https://awesome-streamlit.readthedocs.io/en/latest/vscode.html
import plotly.express as px
import pandas as pd
from process_data import data_processing

st.title('Gapminder')

st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

# Example: Display a table with the cached data
st.table(cached_data)
df = st.table(cached_data)


# Read the merged dataframe
df = data_processing()

# Year slider
df_year_min = df['year'].min()
df_year_max = df['year'].max()
year = st.slider('Select Year', min_value=int(df_year_min), max_value=int(df_year_max))

# Multiselect widget for selecting countries
countries = st.multiselect('Select Countries', df['country'].unique())

# Filter the dataframe based on the selected year and countries
filtered_df = df[(df['year'] == str(year)) & (df['country'].isin(countries))]

st.write(filtered_df.head())

df_for_plot = filtered_df.copy()

multipliers = {'k': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12}
def convert_population(population):
    if isinstance(population, str):
        for suffix, multiplier in multipliers.items():
            if population.endswith(suffix):
                return int(float(population[:-1]) * multiplier)
    return population

df_for_plot['population'] = df_for_plot['population'].apply(convert_population)
df_for_plot['year'] = df_for_plot['year'].astype(int)
df_for_plot['life_expectancy'] = df_for_plot['life_expectancy'].astype(int)


st.write(df_for_plot.head())

# Bubble chart
# Check if there are selected countries
df_life_exp_min = df['life_expectancy'].min()
df_life_exp_max = df['life_expectancy'].max()
if len(countries) > 0:
    # Create bubble chart using Plotly Express
    fig = px.scatter(df_for_plot, x='year', y='life_expectancy', size='population', hover_data=['gni_per_capita'], color='country', color_discrete_sequence=['blue'])  

    # Customize the chart layout
    fig.update_layout(title='Life Expectancy vs. Year',
                      xaxis_title='Year',
                      yaxis_title='Life Expectancy',
                      showlegend=True,
                      xaxis_range=[int(df_year_min), int(df_year_max)],
                      yaxis_range=[int(df_life_exp_min),int(df_life_exp_max)]
    )

    # Display the chart
    st.plotly_chart(fig)
else:
    # Display a message if no countries are selected
    st.write('Please select one or more countries.')


