import numpy as np
import pandas as pd
from pandas import DataFrame

INPUT_FILE_NAME = "obs_data_90_1973.txt"

def main():
	print("Run...")
	current_day = 14

	df = pd.read_csv(INPUT_FILE_NAME, delimiter=" ", header=None, low_memory=False,
		names=['stn', 'year', 'month', 'day', 'prcp', 'temp']
	)

	df['rn'] = np.where(df['prcp'] < -900, 0, df['prcp'])
	df['mm'] = np.where(df['day'] >= current_day, df['month'] + 1, df['month'])

	df['yyyy'] = df['year']
	df.yyyy = np.where(df['mm'] > 12, df['yyyy'] + 1, df['yyyy'])
	df.mm = np.where(df['mm'] > 12, 1, df['mm'])

	df['mm'] = df['mm'].map('{:02d}'.format)
	df = df[df.yyyy != 2018]
	#print(df.tail(30))

	groupby_yyyymm = df.groupby(['stn', 'yyyy', 'mm']).sum()
	data = DataFrame(groupby_yyyymm, columns=['rn'])
	data['rn'] = data['rn'].map('{:,.3f}'.format)
	data.to_csv('temp.txt', sep=' ', mode='a', header=False)

if __name__ == "__main__":
	main()
