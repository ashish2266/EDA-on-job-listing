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


def viewDataset():
    st.header('Data Used in this Analysis')
    st.dataframe(analysis.getDataframe())


def viewForm():

    st.plotly_chart(plot())

    title = st.text_input("Report Title")
    desc = st.text_area('Report Description')
    btn = st.button("Submit")

    if btn:
        report1 = Report(title=title, desc=desc, data="")
        sess.add(report1)
        sess.commit()
        st.success('Report Saved')


def analyseSalary():
    data = analysis.getSalaryEstimates()
    st.plotly_chart(plotBar(data.index, data.values))


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
    st.plotly_chart(plotBar(analysis.getRatingAvg(n), 'Company Name', 'Rating', title=""))


def viewReport():
    reports = sess.query(Report).all()
    titlesList = [report.title for report in reports]
    selReport = st.selectbox(options=titlesList, label="Select Report")

    reportToView = sess.query(Report).filter_by(title=selReport).first()

    markdown = f"""
        ## {reportToView.title}
        ### {reportToView.desc}
        
    """

    st.markdown(markdown)


sidebar.header('Choose Your Option')
options = ['View Dataset', 'Analyse Salary',
           'Analyse Company', 'Analyse Rating', 'View Report']
choice = sidebar.selectbox(options=options, label="Choose Action")

if choice == options[0]:
    viewDataset()
elif choice == options[1]:
    analyseSalary()
elif choice == options[2]:
    analyseCompany()
elif choice == options[3]:
    analyseRating()
