import streamlit as st

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from database import Report
from visualization import plot, plotBar
from AnalyseData import Analyse

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

analysis = Analyse()

st.title('EDA on Data Analysts Job Listings')
sidebar = st.sidebar

def viewForm():

    st.plotly_chart(plot())

    title = st.text_input("Report Title")
    desc = st.text_area('Report Description')
    btn = st.button("Submit")

    if btn:
        report1 = Report(title = title, desc = desc, data = "")
        sess.add(report1)
        sess.commit()
        st.success('Report Saved')

def analyse():
    data = analysis.getCategories()
    st.plotly_chart(plotBar(data.index, data.values))

def analyseSalary():
    data = analysis.getSalaryEstimates()
    st.plotly_chart(plotBar(data.index, data.values))

def analyseRating():
    data = analysis.getRatingCount()
    st.plotly_chart(plotBar(data.index, data.values))

def viewReport():
    reports = sess.query(Report).all()
    titlesList = [ report.title for report in reports ]
    selReport = st.selectbox(options = titlesList, label="Select Report")
    
    reportToView = sess.query(Report).filter_by(title = selReport).first()

    markdown = f"""
        ## {reportToView.title}
        ### {reportToView.desc}
        
    """

    st.markdown(markdown)

sidebar.header('Choose Your Option')
options = [ 'View Database', 'Analyse Salary','Analyse Rating', 'View Report' ]
choice = sidebar.selectbox( options = options, label="Choose Action" )

if choice == options[0]:
    viewForm()
elif choice == options[1]:
    analyseSalary()
elif choice == options[2]:
    analyseRating()