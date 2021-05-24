import pandas as pd
import numpy as np


class Analyse:

    def __init__(self, path='datasets/DataAnalyst.csv'):
        self.df = pd.read_csv(path)
        self.cleanData()
        self.df = self.df.head(1000)

    def cleanData(self):
        self.df.drop(columns=[self.df.columns[0]], inplace=True)
        self.df['Salary Estimate'] = self.df['Salary Estimate'].apply(
            lambda val: val.split()[0])
        self.df['Company Name'] = self.df['Company Name'].map(
            lambda name: str(name).split('\n')[0])

        self.df.Rating = self.df.Rating.apply(lambda x: np.nan if x < 0 else x)
        self.df.Founded = self.df.Founded.apply(
            lambda x: np.nan if x < 0 else x)
        self.df = self.df.replace(['-1'], np.nan)

        self.df['Company Name'] = self.df['Company Name'].str.split(
            '\n').str[0]

        self.df["Salary Estimate"] = self.df["Salary Estimate"].str.replace(
            "\(Glassdoor est.\)", "")
        self.df["Salary Estimate"] = self.df["Salary Estimate"].str.replace(
            "K", "")
        # self.df[['Salary Lower bound','Salary Upper bound']] = self.df["Salary Estimate"].str.split("-",expand=True)

        # self.df["Salary Lower bound"] = self.df["Salary Lower bound"].str.replace("$", "")
        # self.df["Salary Upper bound"] = self.df["Salary Upper bound"].str.replace("$", "")

        # self.df["Salary Lower bound"] = pd.to_numeric(self.df["Salary Lower bound"])
        # self.df["Salary Upper bound"] = pd.to_numeric(self.df["Salary Upper bound"])

        self.df[["City", "State", "None"]] = self.df["Location"] = pd.DataFrame(
            self.df.Location.str.split(",", expand=True))

    def getSalaryEstimates(self):
        return self.df.groupby('Salary Estimate', as_index=False).count()

    def getRatingAvg(self, n):
        return self.df.groupby('Company Name', as_index=False).median().sort_values('Rating', ascending=False).head(n)

    def getDataframe(self):
        return self.df

    # def getCompanyRatings(self, company)

    def getCompanyCount(self, n):
        return self.df.groupby('Company Name', as_index=False).count().sort_values('Job Title', ascending=False).head(n)
