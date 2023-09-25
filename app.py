import streamlit as st
import plotly.express as px
import pandas as pd

def load_data():
    df = pd.read_csv('./World University Rankings 2023.csv')

    # Ensuring that there are no NaN values in the specific columns
    df = df.dropna(subset=['University Rank', 'OverAll Score', 'Research Score', 'Location', 'Name of University'])
    return df

def main():
    st.title("University Rankings Dashboard")
    df = load_data()

    choice = st.sidebar.selectbox('Choose a Visualization:', ('Top Universities by Country', 'Top Universities Based on Score'))

    if choice == 'Top Universities by Country':
        country_rankings = df['Location'].value_counts().reset_index()
        min_universities = st.sidebar.slider('Filter countries with minimum number of universities', 1, 50, 1)
        filtered_countries = country_rankings[country_rankings['Location'] >= min_universities]
        chart_type = st.sidebar.selectbox('Choose a Chart Type:', ('Bar Chart', 'Pie Chart'))

        if chart_type == 'Bar Chart':
            fig = px.bar(filtered_countries, x='index', y='Location', title='Number of Top Universities by Country')
            fig.update_layout(bargap=0.1)
        else:
            fig = px.pie(filtered_countries, names='index', values='Location', title='Distribution of Top Universities by Country')

        st.plotly_chart(fig)

    else:
        top_n = st.sidebar.slider('Select the number of top universities:', min_value=1, max_value=len(df), value=20)
        sort_order = st.sidebar.selectbox('Select sorting order:', ['Ascending', 'Descending'])
        is_ascending = sort_order == 'Ascending'
        top_n_universities = df.head(top_n).sort_values(by='OverAll Score', ascending=is_ascending)

        fig = px.scatter(top_n_universities, x='University Rank', y='OverAll Score',
                         size='Research Score', color='Location',
                         text='Name of University', hover_name='Name of University',
                         title=f'Top {top_n} Universities Based on Overall Score and Research Score')

        st.plotly_chart(fig)

if __name__ == '__main__':
    main()
