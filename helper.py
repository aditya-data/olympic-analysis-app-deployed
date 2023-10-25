import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
import seaborn as sns


def medal_tally(summer_df, winter_df, country, year):
	flag = 0
	if (country == 'Overall') and (year == 'Overall'):
		filter_summer = summer_df
		filter_winter = winter_df
	elif (country != 'Overall') and (year == 'Overall'):
		flag = 1
		filter_summer = summer_df[summer_df['region'] == country]
		filter_winter = winter_df[winter_df['region'] == country]
	elif (country == 'Overall') and (year != 'Overall'):
		filter_summer = summer_df[summer_df['Year'] == int(year)]
		filter_winter = winter_df[winter_df['Year'] == int(year)]
	elif (country != 'Overall') and (year != 'Overall'):
		filter_summer = summer_df[(summer_df['Year'] == int(year)) & (summer_df['region'] == country)]
		filter_winter = winter_df[(winter_df['Year'] == int(year)) & (winter_df['region'] == country)]

	s_medallers = filter_summer[filter_summer['Medal'].isin(['Gold', 'Silver', 'Bronze'])]
	s_medallers = s_medallers.drop_duplicates(subset=['Year', 'Event', 'Medal', 'region'])

	w_medallers = filter_winter[filter_winter['Medal'].isin(['Gold', 'Silver', 'Bronze'])]
	w_medallers = w_medallers.drop_duplicates(subset=['Year', 'Event', 'Medal', 'region'])

	if flag == 0:
		summer_medal_tally = s_medallers.groupby(['region'])[['Gold', 'Silver', 'Bronze']].sum().sort_values(
			by=['Gold', 'Silver', 'Bronze'], ascending=[False, False, False])
		winter_medal_tally = w_medallers.groupby(['region'])[['Gold', 'Silver', 'Bronze']].sum().sort_values(
			by=['Gold', 'Silver', 'Bronze'], ascending=[False, False, False])
	else:
		summer_medal_tally = s_medallers.groupby(['Year'])[['Gold', 'Silver', 'Bronze']].sum().sort_index()
		winter_medal_tally = w_medallers.groupby(['Year'])[['Gold', 'Silver', 'Bronze']].sum().sort_index()

	return summer_medal_tally, winter_medal_tally


def year_country(df):
	years = df['Year'].unique().tolist()
	years.remove(1906)
	years.sort()
	years.insert(0, 'Overall')
	country = df['region'].dropna().unique().tolist()
	country.sort()
	country.insert(0, 'Overall')
	return years, country


def graph_df(summer_df, winter_df):
	summer_participants_over_time = summer_df.groupby('Year')[['ID']].count().rename(
		columns={'Year': 'Editions', 'ID': 'num_of_participants'})
	summer_countries_over_time = summer_df.groupby('Year')[['region']].nunique().rename(
		columns={'Year': 'Editions', 'region': 'num_of_countries'})
	summer_events_over_time = summer_df.groupby('Year')[['Event']].nunique().rename(
		columns={'Year': 'Editions', 'Event': 'num_of_events'})

	winter_participants_over_time = winter_df.groupby('Year')[['ID']].count().rename(
		columns={'Year': 'Editions', 'ID': 'num_of_participants'})
	winter_countries_over_time = winter_df.groupby('Year')[['region']].nunique().rename(
		columns={'Year': 'Editions', 'region': 'num_of_countries'})
	winter_events_over_time = winter_df.groupby('Year')[['Event']].nunique().rename(
		columns={'Year': 'Editions', 'Event': 'num_of_events'})

	return (summer_participants_over_time, winter_participants_over_time), (
		summer_countries_over_time, winter_countries_over_time), (summer_events_over_time, winter_events_over_time)


def plot(df, yaxis):
	fig = px.line(df, x=df.index, y=f'num_of_{yaxis}')
	fig.update_traces(line=dict(color='green', width=5))
	fig.update_layout(
		title_text=f"{yaxis.capitalize()} Over Time", title_font=dict(color='red'),
		paper_bgcolor="lightgray",  # Change background color
		plot_bgcolor="lightgray",  # Change plot area background color
		font=dict(family=" Lato", size=14, color="black"),  # Change font settings
		xaxis=dict(showgrid=False, tickfont=dict(color="black")),
		yaxis=dict(showgrid=False, tickfont=dict(color="black"))
	)
	return fig


def grid(summer_df, winter_df):
	summer_df = summer_df.drop_duplicates(subset=['Year', 'Sport', 'Event'])
	summer_grid = summer_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='size', fill_value=0)

	winter_df = winter_df.drop_duplicates(subset=['Year', 'Sport', 'Event'])
	winter_grid = winter_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='size', fill_value=0)

	return summer_grid, winter_grid


def center_content(content):
	return f"""
    <div style="display: flex; justify-content: center;">
        <div style="text-align: center;">
            {content}
        </div>
    </div>
    """


def most_successful_athlete(summer_df, winter_df):
	summer_df = summer_df.dropna(subset='Medal')
	summer_msa = summer_df.groupby(['ID', 'Name'])[['Gold', 'Silver', 'Bronze']].sum().sort_values(
		by=['Gold', 'Silver', 'Bronze'],
		ascending=[False, False,
				   False]).head(
		10).reset_index()
	summer_msa = \
		pd.merge(summer_msa, summer_df, how='inner', on=['ID', 'Name']).drop_duplicates(subset=['ID', 'Sport'])[
			['Name', 'Gold_x', 'Silver_x', 'Bronze_x', 'Sport', 'region']]
	summer_msa = summer_msa.set_index('Name')
	summer_msa = summer_msa.rename(columns={'Gold_x': 'Num_golds', 'Silver_x': 'Num_Silver', 'Bronze_x': 'Num_Bronze'})

	winter_df = winter_df.dropna(subset='Medal')
	winter_msa = winter_df.groupby(['ID', 'Name'])[['Gold', 'Silver', 'Bronze']].sum().sort_values(
		by=['Gold', 'Silver', 'Bronze'],
		ascending=[False, False,
				   False]).head(
		10).reset_index()
	winter_msa = \
		pd.merge(winter_msa, winter_df, how='inner', on=['ID', 'Name']).drop_duplicates(subset=['ID', 'Sport'])[
			['Name', 'Gold_x', 'Silver_x', 'Bronze_x', 'Sport', 'region']]
	winter_msa = winter_msa.set_index('Name')
	winter_msa = winter_msa.rename(columns={'Gold_x': 'Num_golds', 'Silver_x': 'Num_Silver', 'Bronze_x': 'Num_Bronze'})

	return summer_msa, winter_msa


def country_wise(df, country='USA'):
	df1 = df[df['region'] == country]
	df1 = df1.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
	medal_counts = df1.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().reset_index()

	fig = go.Figure()

	# Add traces for Gold, Silver, and Bronze medals
	fig.add_trace(go.Bar(x=medal_counts['Year'], y=medal_counts['Gold'], name='Gold', marker=dict(color='gold'), width=1.5))
	fig.add_trace(go.Bar(x=medal_counts['Year'], y=medal_counts['Silver'], name='Silver', marker=dict(color='white'), width=1.5))
	fig.add_trace(go.Bar(x=medal_counts['Year'], y=medal_counts['Bronze'], name='Bronze', marker=dict(color='peru'), width=1.5))

	# Customize the layout
	fig.update_layout(
		title=f'{country} Medal Tally Over Time',
		xaxis_title='Year',
		yaxis_title='Number of Medals',
		paper_bgcolor='lightgray',
		plot_bgcolor='lightgray',
		xaxis=dict(showgrid=False),
		yaxis=dict(showgrid=False),
	)

	return fig


def top_games(df, country):
	df1 = df[df['region'] == country]
	df1 = df1.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])

	top_10_games = df1.groupby(['Sport'])[['Gold', 'Silver', 'Bronze']].sum().sort_values(
		by=['Gold', 'Silver', 'Bronze'], ascending=[False, False, False]).head(10)

	return top_10_games


def most_successfull_by_country(df, country):
	df1 = df[df['region'] == country]
	# df1 = df1.drop_duplicates(subset=['Medal'])

	df1 = df1.groupby(['ID', 'Name'])[['Gold', 'Silver', 'Bronze']].sum().sort_values(by=['Gold', 'Silver', 'Bronze'],
																					  ascending=[False, False,
																								 False]).head(
		10).reset_index()[['Name', 'Gold', 'Silver', 'Bronze']]

	return df1


def density_plot_helper(summer_df, winter_df):
	summer_df = summer_df.dropna(subset=['Age', 'Height', 'Weight']).astype(
		{'Age': 'int', 'Weight': 'float', 'Height': 'float'})
	winter_df = winter_df.dropna(subset=['Age', 'Height', 'Weight']).astype(
		{'Age': 'int', 'Weight': 'float', 'Height': 'float'})

	summer_gold = summer_df[summer_df['Medal'] == "Gold"]

	summer_silver = summer_df[summer_df['Medal'] == "Silver"]

	summer_bronze = summer_df[summer_df['Medal'] == "Bronze"]

	summer_not_won = summer_df[summer_df['Medal'] == "Didn't win"]

	winter_gold = winter_df[winter_df['Medal'] == "Gold"]

	winter_silver = winter_df[winter_df['Medal'] == "Silver"]

	winter_bronze = winter_df[winter_df['Medal'] == "Bronze"]

	winter_not_won = winter_df[winter_df['Medal'] == "Didn't win"]

	return (summer_gold, winter_gold), (summer_silver, winter_silver), (summer_bronze, winter_bronze), (
	summer_not_won, winter_not_won)
