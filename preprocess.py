import pandas as pd
import numpy as np


def helper(row):
	if pd.isna(row['region']):
		if row['NOC'] == 'SGP':
			return 'Singapore'
		elif row['NOC'] == 'ROT':
			return 'Refugee Olympic Team'
		elif row['NOC'] == 'TUV':
			return 'Tuvalu'
		else:
			return 'Unknown'
	else:
		return row['region']


def preprocesser(athletes, regions):
	athletes = pd.merge(athletes, regions, how='left', on=['NOC'])
	athletes = athletes.drop(columns=['notes'])
	athletes['region'] = athletes.apply(helper, axis=1)
	athletes['Medal'] = athletes['Medal'].replace({np.nan: "Didn't win"})
	new_data_types = {'NOC': 'category', 'Games': 'category', 'Season': 'category', 'Medal': 'category'}
	athletes = athletes.astype(new_data_types)
	summer_df = athletes[athletes['Season'] == 'Summer']
	winter_df = athletes[athletes['Season'] == 'Winter']
	summer_df.drop_duplicates(inplace=True)
	summer_df = pd.concat([summer_df, pd.get_dummies(summer_df['Medal'])], axis=1)

	winter_df.drop_duplicates(inplace=True)
	winter_df = pd.concat([winter_df, pd.get_dummies(winter_df['Medal'])], axis=1)

	return summer_df, winter_df
