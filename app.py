import streamlit as st
import pandas as pd
import preprocess
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go


athletes = pd.read_csv('https://docs.google.com/spreadsheets/d/1bX3jNTylBusiLw8NmIvYJMf8t0x5I8DtJRUoMJEBZwE/edit?usp=sharing')

regions = pd.read_csv('https://docs.google.com/spreadsheets/d/1FjF0EbBp98SmeprvA35uI4dK4ktllU3S4JmfhkPu1Ws/edit?usp=sharing')

summer_df, winter_df = preprocess.preprocesser(athletes, regions)

st.sidebar.image('https://assets.editorial.aetnd.com/uploads/2010/01/gettyimages-466313493-2.jpg')
st.sidebar.title('''



Olympics (1900 - 2016) Analysis



''')
radio_btn = st.sidebar.radio(
	'Select An Option',
	('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athlete-wise-analysis')
)

if radio_btn == 'Medal Tally':
	st.sidebar.markdown('<h1 style="text-align: center;">Medal Tally for Summer olympics</h1>', unsafe_allow_html=True)

	years, countries = helper.year_country(summer_df)
	selected_year = st.sidebar.selectbox('Select Year', years)
	selected_country = st.sidebar.selectbox('Select Country', countries)

	if selected_country == 'Overall' and selected_year == 'Overall':
		st.title('Overall Medal Tally')
	elif selected_country != 'Overall' and selected_year == 'Overall':
		st.title(f'Overall Medal Tally for {selected_country}')
	elif selected_country == 'Overall' and selected_year != 'Overall':
		st.title(f'Overall Medal Tally in {selected_year}')
	elif selected_country != 'Overall' and selected_year != 'Overall':
		st.title(f'Performance of {selected_country} in  {selected_year} ')

	summer_medal_tally, winter_medal_tally = helper.medal_tally(summer_df, winter_df,  year=selected_year, country=selected_country)
	st.title('Summer Games')
	st.table(summer_medal_tally)

	st.title('Winter Games')
	st.table(winter_medal_tally)

if radio_btn == 'Overall Analysis':

	st.markdown('<h1 style="text-align: center; color: red;">Overall Statistics of Summer Games</h1>', unsafe_allow_html=True)

	num_games = summer_df['Games'].unique().shape[0]-1
	num_cities = summer_df['City'].unique().shape[0]
	num_sports = summer_df['Sport'].unique().shape[0]
	num_events = summer_df['Event'].unique().shape[0]
	num_players = summer_df['Name'].unique().shape[0]
	num_country = summer_df['region'].unique().shape[0]

	col1, col2, col3 = st.columns(3)
	with col1:
		st.header('Editions')
		st.title(num_games)
	with col2:
		st.header('Cities')
		st.title(num_cities)
	with col3:
		st.header('Sports')
		st.title(num_sports)

	col4, col5, col6 = st.columns(3)
	with col4:
		st.header('Events')
		st.title(num_events)
	with col5:
		st.header('Total-Players')
		st.title(num_players)
	with col6:
		st.header('Countries')
		st.title(num_country)

	st.markdown('<h1 style="text-align: center; color: green;">Overall Statistics of Winter Games</h1>',
				unsafe_allow_html=True)

	num_winter_games = winter_df['Games'].unique().shape[0] - 1
	num_winter_cities = winter_df['City'].unique().shape[0]
	num_winter_sports = winter_df['Sport'].unique().shape[0]
	num_winter_events = winter_df['Event'].unique().shape[0]
	num_winter_players =  winter_df['Name'].unique().shape[0]
	num_winter_country = winter_df['region'].unique().shape[0]

	col1, col2, col3 = st.columns(3)
	with col1:
		st.header('Editions')
		st.title(num_winter_games)
	with col2:
		st.header('Cities')
		st.title(num_winter_cities)
	with col3:
		st.header('Sports')
		st.title(num_winter_sports)

	col4, col5, col6 = st.columns(3)
	with col4:
		st.header('Events')
		st.title(num_winter_events)
	with col5:
		st.header('Total-Players')
		st.title(num_winter_players)
	with col6:
		st.header('Countries')
		st.title(num_winter_country)

	pot, cot, eot = helper.graph_df(summer_df, winter_df)
	#
	st.markdown('<h1 style="text-align: center; color: red;">Summer Athletes Over Years</h1>', unsafe_allow_html=True)
	st.plotly_chart(helper.plot(pot[0], 'participants'))

	st.markdown('<h1 style="text-align: center; color: red;">Winter Athletes Over Years</h1>', unsafe_allow_html=True)
	st.plotly_chart(helper.plot(pot[1], 'participants'))
	#
	st.markdown('<h1 style="text-align: center; color: red;">Summer Participants Countries Over Years</h1>', unsafe_allow_html=True)
	st.plotly_chart(helper.plot(cot[0], 'countries'))

	st.markdown('<h1 style="text-align: center; color: red;">Winter Participants Countries Over Years</h1>', unsafe_allow_html=True)
	st.plotly_chart(helper.plot(cot[1], 'countries'))
	#
	st.markdown('<h1 style="text-align: center; color: red;">Summer number of Events Over Time</h1>', unsafe_allow_html=True)
	st.plotly_chart(helper.plot(eot[0], 'events'))

	st.markdown('<h1 style="text-align: center; color: red;">Winter number of Events Over Time</h1>', unsafe_allow_html=True)
	st.plotly_chart(helper.plot(eot[1], 'events'))
	#
	summer_grid, winter_grid = helper.grid(summer_df, winter_df)
	#
	st.title('No. of Summer events over time(Every Sport)')
	fig1, ax1 = plt.subplots(figsize=(16, 16))
	fig1.set_facecolor('lightgray')
	ax1 = sns.heatmap(summer_grid, cmap='viridis', linewidths=2, annot=True, fmt=".0f", cbar_kws={'format': '%.0f'}, ax=ax1)
	st.pyplot(fig1)

	st.title('No. of Winter events over time(Every Sport)')
	fig2, ax2 = plt.subplots(figsize=(16, 16))
	fig2.set_facecolor('lightgray')
	ax2 = sns.heatmap(winter_grid, cmap='viridis', linewidths=2, annot=True, fmt=".0f", cbar_kws={'format': '%.0f'}, ax=ax2)
	st.pyplot(fig2)

	summer_msa, winter_msa = helper.most_successful_athlete(summer_df, winter_df)

	st.title('Most successful athletes over history(Summer Games)')
	st.table(summer_msa)

	st.title('Most successful athletes over history(Winter Games)')
	st.table(winter_msa)
#
#
if radio_btn == 'Country Wise Analysis':
	year, country = helper.year_country(summer_df)
	country = country[1:]
	selected_country = st.selectbox('Select The country', country)

	st.title(f'Summer Medals won by  {selected_country}')
	fig = helper.country_wise(summer_df, selected_country)
	st.plotly_chart(fig)

	st.title(f'Top most successful Summer games for {selected_country}')
	fig1, ax1 = plt.subplots(figsize=(16, 16))
	fig1.set_facecolor('lightgray')
	ax1 = sns.heatmap(helper.top_games(summer_df, selected_country), cmap='viridis', linewidths=2, annot=True, fmt=".0f", cbar_kws={'format': '%.0f'}, ax=ax1)
	st.pyplot(fig1)
	st.title(f'Top most successful players for {selected_country} in Summer Games')
	st.table(helper.most_successfull_by_country(summer_df, selected_country).set_index('Name'))

	if selected_country in winter_df['region'].unique():
		st.title(f'Winter Medals won by  {selected_country}')
		fig2 = helper.country_wise(winter_df, selected_country)
		st.plotly_chart(fig2)
		st.title(f'Top most successful Winter games for {selected_country}')
		fig3, ax2 = plt.subplots(figsize=(16, 16))
		fig1.set_facecolor('lightgray')
		ax2 = sns.heatmap(helper.top_games(winter_df, selected_country), cmap='viridis', linewidths=2, annot=True,
						  fmt=".0f", cbar_kws={'format': '%.0f'}, ax=ax2)
		st.pyplot(fig3)
		st.title(f'Top most successful players for {selected_country} in Winter Games')
		st.table(helper.most_successfull_by_country(winter_df, selected_country).set_index('Name'))
	else:
		st.title(f'{selected_country} has never participated in Winter Games.')
#
if radio_btn == 'Athlete-wise-analysis':
	gold, silver, bronze, not_won = helper.density_plot_helper(summer_df, winter_df)

	st.title('Overall Age distribution of Summer Athletes')
	fig1, ax1 = plt.subplots(figsize=(10, 10))
	sns.set(style="dark")
	plt.ylim(0, 0.1)
	sns.kdeplot(data=gold[0], x='Age', color='gold', label='Gold Medal', linewidth=4)
	sns.kdeplot(data=silver[0], x='Age', color='gray', label='Silver Medal', linewidth=4)
	sns.kdeplot(data=bronze[0], x='Age', color='peru', label='Bronze Medal', linewidth=4)
	sns.kdeplot(data=not_won[0], x='Age', color='black', label='Not-Won', linewidth=4)
	ax1.legend()
	st.pyplot(fig1)

	st.title('Overall Age distribution of Winter Athletes')
	fig2, ax2 = plt.subplots(figsize=(10, 10))
	sns.set(style="dark")
	plt.ylim(0, 0.1)
	sns.kdeplot(data=gold[1], x='Age', color='gold', label='Gold Medal', linewidth=4)
	sns.kdeplot(data=silver[1], x='Age', color='gray', label='Silver Medal', linewidth=4)
	sns.kdeplot(data=bronze[1], x='Age', color='peru', label='Bronze Medal', linewidth=4)
	sns.kdeplot(data=not_won[1], x='Age', color='black', label='Not-Won', linewidth=4)
	ax2.legend()
	st.pyplot(fig2)

	st.title('Overall Height distribution of Summer Athletes')
	fig3, ax3 = plt.subplots(figsize=(10, 10))
	sns.set(style="dark")
	plt.ylim(0, 0.05)
	sns.kdeplot(data=gold[0], x='Height', color='gold', label='Gold Medal', linewidth=4)
	sns.kdeplot(data=silver[0], x='Height', color='gray', label='Silver Medal', linewidth=4)
	sns.kdeplot(data=bronze[0], x='Height', color='peru', label='Bronze Medal', linewidth=4)
	sns.kdeplot(data=not_won[0], x='Height', color='black', label='Not-Won', linewidth=4)
	ax3.legend()
	st.pyplot(fig3)

	st.title('Overall Height distribution of Winter Athletes')
	fig4, ax4 = plt.subplots(figsize=(10, 10))
	sns.set(style="dark")
	plt.ylim(0, 0.05)
	sns.kdeplot(data=gold[1], x='Height', color='gold', label='Gold Medal', linewidth=4)
	sns.kdeplot(data=silver[1], x='Height', color='gray', label='Silver Medal', linewidth=4)
	sns.kdeplot(data=bronze[1], x='Height', color='peru', label='Bronze Medal', linewidth=4)
	sns.kdeplot(data=not_won[1], x='Height', color='black', label='Not-Won', linewidth=4)
	ax4.legend()
	st.pyplot(fig4)

	st.title('Overall Weight distribution of Summer Athletes')
	fig5, ax5 = plt.subplots(figsize=(10, 10))
	sns.set(style="dark")
	plt.ylim(0, 0.05)
	sns.kdeplot(data=gold[0], x='Weight', color='gold', label='Gold Medal', linewidth=4)
	sns.kdeplot(data=silver[0], x='Weight', color='gray', label='Silver Medal', linewidth=4)
	sns.kdeplot(data=bronze[0], x='Weight', color='peru', label='Bronze Medal', linewidth=4)
	sns.kdeplot(data=not_won[0], x='Weight', color='black', label='Not-Won', linewidth=4)
	ax5.legend()
	st.pyplot(fig5)

	st.title('Overall Weight distribution of Winter Athletes')
	fig6, ax6 = plt.subplots(figsize=(10, 10))
	sns.set(style="dark")
	plt.ylim(0, 0.05)
	sns.kdeplot(data=gold[1], x='Weight', color='gold', label='Gold Medal', linewidth=4)
	sns.kdeplot(data=silver[1], x='Weight', color='gray', label='Silver Medal', linewidth=4)
	sns.kdeplot(data=bronze[1], x='Weight', color='peru', label='Bronze Medal', linewidth=4)
	sns.kdeplot(data=not_won[1], x='Weight', color='black', label='Not-Won', linewidth=4)
	ax6.legend()
	st.pyplot(fig6)

	athletes_summer = summer_df.groupby(['Sex', 'Year'])[['ID']].count()['ID'].reset_index().rename(
		columns={'ID': 'count'})

	athletes_winter = winter_df.groupby(['Sex', 'Year'])[['ID']].count()['ID'].reset_index().rename(
		columns={'ID': 'count'})

	male_summer_athletes = athletes_summer[athletes_summer['Sex'] == 'M']
	female_summer_athletes = athletes_summer[athletes_summer['Sex'] == 'F']
	male_winter_athletes = athletes_winter[athletes_winter['Sex'] == 'M']
	female_winter_athletes = athletes_winter[athletes_winter['Sex'] == 'F']

	fig7 = go.Figure()
	fig7.add_scatter(x=male_summer_athletes['Year'], y=male_summer_athletes['count'], mode='lines', name='Males',
					line=dict(width=5))
	fig7.add_scatter(x=female_summer_athletes['Year'], y=female_summer_athletes['count'], mode='lines', name='Females',
					line=dict(width=5, color='brown'))
	fig7.update_layout(
		title='Male and Female Athletes in Summer Events Over the Years',
		xaxis=dict(title='Year'),
		yaxis=dict(title='Count'),
		xaxis_showgrid=False,  # Remove x-axis gridlines
		yaxis_showgrid=False,  # Remove y-axis gridlines
		plot_bgcolor='lightgray',  # Set the background color
		paper_bgcolor='lightgray',  # Set the paper background color
	)
	st.plotly_chart(fig7)

	fig8 = go.Figure()
	fig8.add_scatter(x=male_winter_athletes['Year'], y=male_summer_athletes['count'], mode='lines', name='Males',
					line=dict(width=5, color='red'))
	fig8.add_scatter(x=female_winter_athletes['Year'], y=female_summer_athletes['count'], mode='lines', name='Females',
					line=dict(width=5, color='black'))
	fig8.update_layout(
		title='Male and Female Athletes in Winter Events Over the Years',
		xaxis=dict(title='Year'),
		yaxis=dict(title='Count'),
		xaxis_showgrid=False,
		yaxis_showgrid=False,  # Remove y-axis gridlines
		plot_bgcolor='lightgray',  # Set the background color
		paper_bgcolor='lightgray',  # Set the paper background color
	)
	st.plotly_chart(fig8)
