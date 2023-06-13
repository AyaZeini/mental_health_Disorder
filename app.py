import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import hydralit_components as hc
from streamlit_lottie import st_lottie
import requests

st.set_page_config(
    page_title="Mental Health",
    page_icon= "🧠",
    initial_sidebar_state="auto",
    layout="wide")

# Display lottie animations
def load_lottieurl(url):

    # get the url
    r = requests.get(url)
    # if error 200 raised return Nothing
    if r.status_code !=200:
        return None
    return r.json()

lottie1 = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_tcsrkUkhKh.json")
lottie2=load_lottieurl('https://assets7.lottiefiles.com/packages/lf20_UepHvaXIU4.json')

df=pd.read_csv('data/mental_substance_disorder.csv')
df1=pd.read_csv('data/disorder_type.csv')
df3=pd.read_csv('data/Dalys.csv')
df4=pd.read_csv('data/mentalhealth_perGender.csv')
df5=pd.read_csv('data/Age-mental.csv')



# Merge the datasets based on the common columns
merged_df = pd.merge(df, df1, on=['country', 'code', 'year'])
merged_df=pd.merge(merged_df, df4, on=['country', 'code', 'year'])


# Navigation Bar Design
menu_data = [
{'label':"Home", 'icon': "bi bi-house"},
{'label':"Overview", 'icon': "bi bi-graph-up-arrow"},
{'label':'Disease Burden', 'icon' : "File earmark medical"}
]

# Set the Navigation Bar
menu_id = hc.nav_bar(menu_definition = menu_data,
                    sticky_mode = 'sticky',
                    sticky_nav = False,
                    hide_streamlit_markers = False,
                    override_theme = {'txc_inactive': 'white',
                                        'menu_background' : '#6B3E99',
                                        'txc_active':'#6B3E99',
                                        'option_active':'white'})

if menu_id == "Home":

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("<h1 style='font-size: 50px; text-transform: uppercase;'>MENTAL HEALTH</h1>", unsafe_allow_html=True)
        
        markdown_text = """
        <p style='font-family: Arial, sans-serif; text-align: justify; font-size: 15px;'>Mental health is essential for individuals to navigate life, 
        reach their potential, and contribute to society. It influences decision-making, relationships, and overall well-being. 
        Mental health is a human right, crucial for personal, community, and socio-economic development. 
        It encompasses a spectrum of experiences, difficulties, and outcomes, beyond the absence of disorders. 
        Mental health conditions include disorders, disabilities, and distressing states. 
        </p>
        """
        st.markdown(markdown_text, unsafe_allow_html=True)
        
        # Display customer churn animation
        st_lottie(lottie1, key="mental1")

    with col2:
        # Display the header
        st.markdown("<center><span style='font-size: 40px;'>More Common than You Think</span></center>", unsafe_allow_html=True)

        # Display customer churn animation
        st_lottie(lottie2, key="mental")

     

    with col3:

        # Display the second line
        st.markdown("<span style='font-size: 60px;'><b><span style='color: purple;'>1 in 8</span> people</b></span> <span style='font-size: 20px;'>experienced one or more <span style='color: purple;'>mental health concerns</span>.</span>", 
            unsafe_allow_html=True)




        text = '''
        <span style="font-size: 15px;">The number of mental health disorders has been increasing from year to year, and in this project, we are going to focus on a few of them, notably:</span>

        <ul>
          <li><span style="font-size: 15px;">Schizophrenia (which involves a breakdown between thoughts, emotions, and behavior)</span></li>
          <li><span style="font-size: 15px;">Bipolar disorder (characterized by changes in energy, mood, and activity levels)</span></li>
          <li><span style="font-size: 15px;">Anxiety (persistent feeling of fear)</span></li>
          <li><span style="font-size: 15px;">Depression (persistent feeling of sadness)</span></li>
          <li><span style="font-size: 15px;">Eating disorders (such as anorexia, bulimia, and binge eating)</span></li>
          <li><span style="font-size: 15px;">Drug use disorder (drug addiction)</span></li>
          <li><span style="font-size: 15px;">Alcohol use disorder (alcoholism, binge drinking, etc.)</span></li>
        </ul>
        '''

        st.markdown(text, unsafe_allow_html=True)


if menu_id == 'Overview':
    col = st.columns(2)

    with col[0]:
        selected_year = st.slider(
            'Select Year',
            min_value=1990,
            max_value=2019,
            value=1990,
            step=1,
            key='year_slider',
            help='Drag the slider to change the year'
        )

    with col[1]:
        all_countries_option = 'All Countries'
        country_options = merged_df['country'].unique().tolist()
        country_options.insert(0, all_countries_option)
        selected_country = st.selectbox('Select Country', country_options)

    # Filter the DataFrame for the selected year, country, and gender
    if selected_country == all_countries_option:
        filtered_df = merged_df[merged_df['year'] == selected_year]
    else:
        filtered_df = merged_df[(merged_df['year'] == selected_year) & (merged_df['country'] == selected_country)]



    # Calculate the total number of mental disorder cases for the selected year
    total_schizophrenia = filtered_df['schizophrenia'].mean()
    total_bipolar_disorder = filtered_df['bipolar_disorder'].mean()
    total_eating_disorders = filtered_df['eating_disorders'].mean()
    total_anxiety_disorders = filtered_df['anxiety_disorders'].mean()
    total_drug_use_disorders = filtered_df['drug_use_disorders'].mean()
    total_depression = filtered_df['depression'].mean()
    total_alcohol_use_disorders = filtered_df['alcohol_use_disorders'].mean()


    col1, col2 = st.columns(2, gap="large")

    with col1:

        # Create the dynamic title
        title = f"Mental Disorder by Country ({selected_year})"
        st.markdown(f"### {title}")

        markdown_text = """
        <div style="font-family: Arial, sans-serif; font-size: 12px; text-align: justify;">
            The share of the population with any mental health disorder in the selected year. 
            The mental health disorders included are <span style="color: #6B3E99;">depression, anxiety, bipolar disorder, eating disorders, and schizophrenia.</span>
        </div>
        """

        st.write(markdown_text, unsafe_allow_html=True)

        # map visualization
        fig = px.choropleth(
            filtered_df,
            locations="code",
            color="mental_disorder",
            hover_name="country",
            color_continuous_scale=px.colors.sequential.Purples
        )

        fig.update_geos(showframe=False, showcoastlines=True)
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)'
        )

        # Display the choropleth map
        st.plotly_chart(fig)


        # bar chart

        # bar chart title:

        disorder_options = ["depressive", "anxiety", "bipolar", "eating", "schizophrenia"]
        selected_disorder = st.selectbox("Select Disorder", disorder_options)


        # Create the dynamic title
        title = f"Gender Disparity in the Prevalence of {selected_disorder} Disorder: Share of Population ({selected_year})"
        st.markdown(f"#### {title}")

        markdown_text = """
        <div style="font-family: Arial, sans-serif; font-size: 12px; text-align: justify;">
            The visualization contrasts the prevalence of mental health disorders among men and women. 
            It illustrates that women are more likely than men to suffer from depression, anxiety, eating disorders, and bipolar disorder. 
            However, the prevalence of schizophrenia varies by country, with men being more likely to be diagnosed. 
        </div>
        """

        st.write(markdown_text, unsafe_allow_html=True)


        def plot_bar_chart(year, country, disorder):
            if selected_country == all_countries_option:
                filtered_df = merged_df[merged_df['year'] == selected_year]
            else:
                filtered_df = merged_df[(merged_df['year'] == selected_year) & (merged_df['country'] == selected_country)]
            
            disorder_cols = [f"{disorder}_male", f"{disorder}_female"]
            disorder_names = ["Male", "Female"]
            disorder_values = filtered_df[disorder_cols].values.flatten()
            disorder_values_formatted = [format(value, ".2f") for value in disorder_values]
            
            colors=['purple', 'mediumpurple']

            fig = go.Figure(data=[
                go.Bar(x=disorder_names, y=disorder_values,               
                marker=dict(color=colors),
                text= disorder_values_formatted,
                textposition='outside'
            )
            ])
            
            fig.update_layout(
                xaxis=dict(visible=True, showgrid=False),
                yaxis=dict(showticklabels=False, showgrid=False),
                margin=dict(l=20, r=20, t=50, b=20),
                plot_bgcolor='rgba(255, 255, 255, 0)',
                paper_bgcolor='rgba(255, 255, 255, 0)'
            )
            
            st.plotly_chart(fig)


        # Call the plot_bar_chart function with the selected filters
        plot_bar_chart(selected_year, selected_country, selected_disorder)



    # add line
    st.markdown("""<style>.divider{border-top: 3px solid #6B3E99;}</style>""", unsafe_allow_html=True)
    st.markdown("""<div class="divider"></div>""", unsafe_allow_html=True)


    with col2:


        # Create the dynamic title
        title = f"Exploring the Prevalence of Mental Health Disorders by Disorder Type"
        st.markdown(f"#### {title}")

        markdown_text = """
        <div style="font-family: Arial, sans-serif; font-size: 12px; text-align: justify;">
            In 2019, it is estimated that 1 billion people worldwide suffered from a mental or substance use problem. 
            Anxiety disorders were the most common, affecting approximately 4% of the population.
        </div>
        """
        st.write(markdown_text, unsafe_allow_html=True)


        # Define the data for the horizontal bar chart
        labels = [
            'Schizophrenia',
            'Bipolar Disorder',
            'Eating Disorders',
            'Anxiety Disorders',
            'Drug Use Disorders',
            'Depression',
            'Alcohol Use Disorders'
        ]
        values = [
            total_schizophrenia,
            total_bipolar_disorder,
            total_eating_disorders,
            total_anxiety_disorders,
            total_drug_use_disorders,
            total_depression,
            total_alcohol_use_disorders
        ]

        # Sort the labels and values in descending order
        sorted_values, sorted_labels = zip(*sorted(zip(values, labels), reverse=False))



        # Create the horizontal bar chart trace
        trace = go.Bar(
            x=sorted_values,
            y=sorted_labels,
            orientation='h',
            marker=dict(color='purple'),
            text=[f'{value:.2f}%' for value in sorted_values],
            textposition='outside'
        )

        # Create the figure
        fig = go.Figure(data=[trace])

        # Customize the layout
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(showticklabels=True),
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)'
        )

        st.plotly_chart(fig)



if menu_id == 'Disease Burden':

    col=st.columns(2)

    with col[0]:
        st.markdown('## Unveiling the Hidden Toll: Mental Health and Substance Use Burden')

        markdown_text = """
        <div style="font-family: Arial, sans-serif; font-size: 18px; text-align: justify;">
            The disease burden, measured in Disability-Adjusted Life Years (DALYs), takes into account not only death but also years lived with impairment or health burden. 
            The map depicts DALYs as a percentage of overall health burden; in 2019, mental and substance use disorders reached up to 10% in various countries. 
            In Australia, Saudi Arabia, and Iran, these disorders contribute the most to the overall health burden.
        </div>
        """
        st.write(markdown_text, unsafe_allow_html=True)


    with col[1]:

        # Create a choropleth map
        fig = px.choropleth(df3, locations='code', color='dalys',
                            hover_data=['country'], animation_frame='year', projection='natural earth', color_continuous_scale=px.colors.sequential.Purples,)

      
        # Customize the map layout
        fig.update_layout(title='DALYs - Mental Disorders',
                          coloraxis_colorbar=dict(title='DALYs (Percent)'),
                          geo=dict(showframe=False, showcoastlines=True))

        # Show the figure
        st.plotly_chart(fig)

    col=st.columns(2)


    with col[0]:
        selected_year = st.slider(
            'Select Year',
            min_value=1990,
            max_value=2019,
            value=1990,
            step=1,
            key='year_slider',
            help='Drag the slider to change the year'
        )


    with col[1]:
        all_countries_option = 'All Countries'
        country_options = df5['country'].unique().tolist()
        country_options.insert(0, all_countries_option)
        selected_country = st.selectbox('Select Country', country_options)

        # Filter the DataFrame for the selected year, country, and gender
        if selected_country == all_countries_option:
            filtered_df1 = df5[df5['year'] == selected_year]
        else:
            filtered_df1 = df5[(df5['year'] == selected_year) & (df5['country'] == selected_country)]




    with col[0]:

        title=f'DALYs -Mental Disorder by Age Group- {selected_country}'
        st.markdown(f"#### {title}")

        # Calculate the sum of DALYs for each age group
        age_groups = ['Anxiety- age: <5', 'Anxiety- age: 5-14', 'Anxiety- age: 15-49', 'Anxiety- age: 50-69', 'Anxiety- age: 70+']
        daly_sum = filtered_df1[age_groups].sum()

        # Create pie chart using Plotly Express
        fig = px.pie(values=daly_sum, names=age_groups, title=f'Anxiety Disorder', 
            color_discrete_sequence=px.colors.sequential.Purples)
        
        # Customize the layout
        fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.5))


        # Show the figure
        st.plotly_chart(fig)


    with col[1]:
        

            # Add space
        st.markdown("<p style='margin-bottom:  70px;'></p>", unsafe_allow_html=True)

        # Calculate the sum of DALYs for each age group
        age_groups = ['depression- age: <5', 'depression- age: 5-14', 'depression- age: 15-49', 'depression- age: 50-69', 'depression- age: 70+']
        daly_sum = filtered_df1[age_groups].sum()

        # Create pie chart using Plotly Express
        fig = px.pie(values=daly_sum, names=age_groups, title=f'Depression Disorder', 
            color_discrete_sequence=px.colors.sequential.Purples)
        
        # Customize the layout
        fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.5))


        # Show the figure
        st.plotly_chart(fig)

    col=st.columns(2)


    with col[0]:

        # Calculate the sum of DALYs for each age group
        age_groups = ['bipolar- age: 5-14', 'bipolar- age: 15-49', 'bipolar- age: 50-69', 'bipolar- age: 70+']
        daly_sum = filtered_df1[age_groups].sum()

        # Create pie chart using Plotly Express
        fig = px.pie(values=daly_sum, names=age_groups, title=f'Bipolar Disorder',
         color_discrete_sequence=px.colors.sequential.Purples)
        
        # Customize the layout
        fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.5))


        # Show the figure
        st.plotly_chart(fig)

    with col[1]:

        # Calculate the sum of DALYs for each age group
        age_groups = ['eating- age: 5-14', 'eating- age: 15-49']
        daly_sum = filtered_df1[age_groups].sum()

        # Create pie chart using Plotly Express
        fig = px.pie(values=daly_sum, names=age_groups, title=f'Eating Disorder', 
            color_discrete_sequence=px.colors.sequential.Purples)

         # Customize the layout
        fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.5))


        # Show the figure
        st.plotly_chart(fig)

    # Calculate the sum of DALYs for each age group
    age_groups = ['Schiz- age: 5-14', 'Schiz- age: 15-49', 'Schiz- age: 50-69', 'Schiz- age: 70+']
    daly_sum = filtered_df1[age_groups].sum()

    # Create pie chart using Plotly Express
    fig = px.pie(values=daly_sum, names=age_groups, title=f'Schizophrenia', 
        color_discrete_sequence=px.colors.sequential.Purples)

    # Customize the layout
    fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.5))


    # Show the figure
    st.plotly_chart(fig)
























