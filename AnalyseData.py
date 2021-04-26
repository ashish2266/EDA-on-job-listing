import pandas as pd

class Analyse:

    def __init__(self, path = 'datasets/DataAnalyst.csv'):
        self.df = pd.read_csv(path)
        self.cleanData()

    def cleanData(self):
        self.df.drop(columns=[self.df.columns[0]], inplace=True)
        self.df['Salary Estimate'] = self.df['Salary Estimate'].apply(lambda val : val.split()[0])

    def getSalaryEstimates(self):
        return self.df.groupby('Salary Estimate').count()['Job Title']