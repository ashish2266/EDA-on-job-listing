import streamlit as st

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from database import Report
from visualization import *
from AnalyseData import Analyse

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

analysis = Analyse()

st.title('EDA on Data Analysts Job Listings')
sidebar = st.sidebar
# st.image('image_path')

st.markdown("# this is a heading")

def viewDataset():
    st.header('Data Used in Project')
    dataframe = analysis.getDataframe()

    with st.spinner("Loading Data..."):
        st.dataframe(dataframe)

        st.markdown('---')
        cols = st.beta_columns(4)
        cols[0].markdown("### No. of Rows :")
        cols[1].markdown(f"# {dataframe.shape[0]}")
        cols[2].markdown("### No. of Columns :")
        cols[3].markdown(f"# {dataframe.shape[1]}")
        st.markdown('---')

        st.header('Summary')
        st.dataframe(dataframe.describe())
        st.markdown('---')

        types = {'object': 'Categorical',
                 'int64': 'Numerical', 'float64': 'Numerical'}
        types = list(map(lambda t: types[str(t)], dataframe.dtypes))
        st.header('Dataset Columns')
        for col, t in zip(dataframe.columns, types):
            st.markdown(f"### {col}")
            cols = st.beta_columns(4)
            cols[0].markdown('#### Unique Values :')
            cols[1].markdown(f"# {dataframe[col].unique().size}")
            cols[2].markdown('#### Type :')
            cols[3].markdown(f"## {t}")


def analyseSalary():
    data = analysis.getSalaryEstimates()
    st.plotly_chart(plotBar(data, 'Salary Estimate', 'Job Title'))
    st.text("description here")

def analyseCompany():

    st.header('Top Companys')
    n = st.select_slider(
        options=[5, 10, 50, 100, 200], label='Select No. of Companys')

    st.plotly_chart(plotBar(analysis.getCompanyCount(n),
                            'Company Name', 'Job Title'))

    st.header("Popular locations of Data Analytics Jobs")
    st.image('plotImages/locations_bar.png')

    st.header("Popular states of Data Analytics Jobs")
    st.image('plotImages/state_bar.png')

    st.header("Popular industry of Data Analytics Jobs")
    st.image('plotImages/industry_bar.png')

    st.header("Popular Sector of Data Analytics Jobs")
    st.image('plotImages/sector_bar.png')

    st.header("Section for Data Analytics Jobs")
    st.image('plotImages/sector_pie.png')

    st.header("Ownership of Data Analytics Jobs")
    st.image('plotImages/ownership_bar.png')

    st.header("Easy Apply for Data Analytics Jobs")
    st.image('plotImages/easy_bar.png')

    st.header("Ratings for Data Analytics Jobs")
    st.image('plotImages/rating_bar.png')


def analyseListingData():
    st.header('Most Common word in listings')
    st.image('plotimages/cloud1.png')

    st.header("Title for Data Analytics Jobs")
    st.image('plotImages/title_bar.png')

    st.header("Languages for Data Analytics Jobs")
    st.image('plotImages/language_bar.png')


def analyseRating():

    st.header("")
    n = st.select_slider(
        options=[5, 10, 50, 100, 200], label='Select No. of Companys')
    st.plotly_chart(plotBar(analysis.getRatingAvg(
        n), 'Company Name', 'Rating', title=""))


sidebar.header('Choose Your Option')
options = ['View Dataset', 'Analyse Salary',
           'Analyse Company', 'Analyse Rating']
choice = sidebar.selectbox(options=options, label="Choose Action")

if choice == options[0]:
    viewDataset()
elif choice == options[1]:
    analyseSalary()
elif choice == options[2]:
    analyseCompany()
elif choice == options[3]:
    analyseRating()
