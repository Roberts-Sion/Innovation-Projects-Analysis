import streamlit as st
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

st.title("Personal Research Analysis")

#Import the datafile
data = pd.read_excel('snp_dataset_alls.xlsx')
#Extract the required data from the datafile
#Time
start_date = data['Project Start Date']
end_date = data['Project End Date']
status = data['Project Status']
#Funding & Association
budget = data['Project Budget']
owners = data['Owner Network']
collaborators = data['Collaborating Networks']
funding_mechanism = data['Funding Mechanism']
sif_funding = data['SIF Funding Required']
#Area of research
titles = data['Project Title']
strategy = data['Strategy Theme']
research = data['Research Areas']
technology = data['Technology Areas']
sector = data['Lead Sector']
secondary_sectors = data['Other Related Sectors']

#Determine the time difference between the start and end dates
start_dt = pd.to_datetime(start_date, format="%d/%m/%Y", errors='coerce')
end_dt = pd.to_datetime(end_date, format="%d/%m/%Y", errors='coerce')
time_difference = end_dt - start_dt
durations = time_difference.dt.days

#For the projects involved in multiple sectors, make sure they are included in each sector list
sector_types = sector.unique()
sector_types = sector_types[:4]
sector_types_idx = [sector[sector.str.contains(st, na=False)].index.tolist() for st in sector_types]

#Do the same for owners as well
owner_types = owners.unique()
owner_types = [ot for ot in owner_types if pd.notna(ot)]
owner_types_idx = [owners[owners.str.contains(ot, na=False)].index.tolist() for ot in owner_types]

#Do the same for strategy themes as well
strategy_types = strategy.unique()
strategy_types = [st for st in strategy_types if pd.notna(st)]
strategy_types_idx = [strategy[strategy.str.contains(st, na=False)].index.tolist() for st in strategy_types]

#Do the same for technology as well
technology_types = ['Active Network Management','Asset Management', 'Biomethane', 'Carbon Emission Reduction Technologies', 'Commercial', 'Comms and IT',\
                    'Community Schemes', 'Condition Monitoring', 'Conductors', 'Control Systems', 'Cyber Security', 'Demand Response', 'Demand Side Management',\
                    'Digital Network', 'Distributed Generation', 'Electric Vehicles', 'Electricity Transmission Networks', 'Energy Storage', 'Energy Storage and Demand Response',\
                    'Environmental', 'Fault Current', 'Fault Level', 'Fault Management', 'Gas Distribution Networks', 'Gas Transmission Networks', 'Gas Vehicles',\
                    'Green Gas', 'HVDC', 'Harmonics', 'Health and Safety', 'Heat Pumps', 'High Voltage Technology', 'Hydrogen', 'LV & 11kV Networks', 'Low Carbon Generation',\
                    'Maintenance & Inspections', 'Measurement', 'Meshed Networks', 'Modelling', 'Network Automation', 'Network Monitoring', 'Offshore Transmission',\
                    'Overhead Lines', 'Photovoltaics', 'Poverty', 'Pre-Heat', 'Protection', 'Resilience', 'Stakeholder Engagement', 'Storage', 'Substation Monitoring',\
                    'Substations', 'System Security', 'Transformers', 'Voltage Control']
technology_types = [tt for tt in technology_types if pd.notna(tt)]
technology_types_idx = [technology[technology.str.contains(tt, na=False)].index.tolist() for tt in technology_types]

#Do the same for research as well
research_types = ['ED - Customer and stakeholder focus', 'ED - Network improvements and system operability', 'ED - New technologies and commercial evolution',\
                  'ED - Safety, health and environment', 'ED - Transition to low carbon future', 'ET - Customer and stakeholder focus', 'ET - Network improvements and system operability',\
                  'ET - New technologies and commercial evolution', 'ET - Transition to low carbon future', 'GD - Environment and low carbon', 'GD - Future of gas', 'GD - Mains Replacement',\
                  'GD - Reliability and maintenance', 'GD - Repair', 'GD - Safety and emergency', 'GD - Security', 'GT - Environment and low carbon', 'GT - Future of gas', 'GT - Mains Replacement',\
                  'GT - Reliability and maintenance', 'GT - Repair', 'GT - Safety and emergency', 'Others']
research_types = [rt for rt in research_types if pd.notna(rt)]
research_types_idx = [research[research.str.contains(rt, na=False)].index.tolist() for rt in research_types]

#Do the same for funding mechanism as well
funding_mechanism_types = funding_mechanism.unique()
funding_mechanism_types = [ft for ft in funding_mechanism_types if pd.notna(ft)]
funding_mechanism_types_idx = [funding_mechanism[funding_mechanism.str.contains(ft, na=False)].index.tolist() for ft in funding_mechanism_types]

#Investigate four strategy themes of interest
#These can be identified in an array below
want_strategy_types_idx = [0, 3, 5, 7]
interest_strategy_types = [strategy_types[i] for i in want_strategy_types_idx]
interest_strategy_types_idx = [strategy[strategy.str.contains(ist, na=False)].index.tolist() for ist in interest_strategy_types]

#Plot of total project budgets vs interested strategy themes
total_interest_strategy_budget = np.zeros(len(interest_strategy_types))
for i in range(len(interest_strategy_types)):
  for j in range(len(interest_strategy_types_idx[i])):
    total_interest_strategy_budget[i] += budget[interest_strategy_types_idx[i][j]]
bts_total_interest_strategy_budget_idx = np.argsort(total_interest_strategy_budget)[::-1]
bts_total_interest_strategy_budget = total_interest_strategy_budget[bts_total_interest_strategy_budget_idx]
bts_interest_strategy_types = np.array(interest_strategy_types)[bts_total_interest_strategy_budget_idx]

TOTAL_interest_strategy_budget = np.sum(total_interest_strategy_budget)

fig = px.bar(x=bts_interest_strategy_types, y=bts_total_interest_strategy_budget, labels={'x':'Strategy Theme', 'y':'Total Funding (£)'})
fig.update_traces(name=f'Total Budget (£{TOTAL_interest_strategy_budget:,.2f})', showlegend=True)
fig.update_layout(legend=dict(yanchor='top', y=0.99, xanchor='right', x=0.99))
st.write(fig)

#Determine the number of projects of each technology has received funding for each strategy theme
tech_4_int_strat = []
for i in range(len(interest_strategy_types)):
  filtered_tech = technology[interest_strategy_types_idx[i]].dropna()
  filtered_tech = filtered_tech.str.split(', ').explode().str.strip()
  tech_4_int_strat.append(filtered_tech)

tech_4_int_strat_type = []
for i in range(len(interest_strategy_types)):
  counts = tech_4_int_strat[i].value_counts()
  counts = counts.reindex(technology_types, fill_value=0)
  tech_4_int_strat_type.append(counts)

bts_tech_4_int_strat_type = []
bts_technology_types = []
for i in range(len(interest_strategy_types)):
  counts = tech_4_int_strat_type[i].sort_values(ascending=False)
  non_zero_counts = counts[counts > 0]
  bts_technology_types.append(non_zero_counts.index)
  bts_tech_4_int_strat_type.append(non_zero_counts)

fig = go.Figure()
fig.add_trace(go.Bar(x=bts_technology_types[0], y=bts_tech_4_int_strat_type[0].values, name=f'{interest_strategy_types[0]}'))
for i in range(1, len(interest_strategy_types)):
  fig.add_trace(go.Bar(x=bts_technology_types[i], y=bts_tech_4_int_strat_type[i].values, name=f'{interest_strategy_types[i]}', visible=False))

buttons = []
buttons.append(dict(label=f'{interest_strategy_types[0]}', method='update', args=[{'visible': [True] + [False]*(len(interest_strategy_types) - 1)}, {'title':{'text': f'Cumulative Number of Projects for {interest_strategy_types[0]}'}}]))
for i in range(1, len(interest_strategy_types)):
  visible = [False] * (len(interest_strategy_types))
  visible[i] = True
  buttons.append(dict(label=f'{interest_strategy_types[i]}', method='update', args=[{'visible': visible}, {'title':{'text': f'Cumulative Number of Projects for {interest_strategy_types[i]}'}}]))

fig.update_layout(updatemenus=[dict(buttons=buttons, direction='down', showactive=True, x=0, xanchor='left', y=1.1, yanchor='top')],
                  xaxis_title='Technology', yaxis_title='Number of Projects', title='Cumulative Number of Projects', hovermode='x unified')
fig.update_layout(width=1400, height=600)
fig.update_xaxes(tickmode='linear', tickangle=20, tickfont=dict(size=8))
st.write(fig)

#Create a similar plot where dates on x-axis, tech on y-axis, and marker size corresponds to number of projects at date
tech_4_int_strat = []
tech_4_int_strat_start_dt = []
tech_4_int_strat_count = []
tech_4_int_strat_present = []
for i in range(len(interest_strategy_types)):
  current_int_strat_idx = interest_strategy_types_idx[i]
  current_int_strat_tech = technology[current_int_strat_idx].dropna()
  current_int_strat_tech = current_int_strat_tech.str.split(', ').explode().str.strip()
  current_int_strat_tech = current_int_strat_tech[current_int_strat_tech.isin(technology_types)]
  current_owner_start_dt = start_dt.loc[current_int_strat_tech.index]
  df = pd.DataFrame({'technology': current_int_strat_tech.values, 'start_dt': current_owner_start_dt.values})
  df = (df.groupby(['start_dt', 'technology']).size().reset_index(name='count'))
  df = df.sort_values(by='start_dt')
  tech_4_int_strat.append(df['technology'])
  tech_4_int_strat_start_dt.append(df['start_dt'])
  tech_4_int_strat_count.append(df['count'])
  tech_4_int_strat_present.append(df['technology'].unique())

colours = (px.colors.qualitative.Plotly + px.colors.qualitative.D3 + px.colors.qualitative.Set3)
technology_colours = {tech: colours[i % len(colours)] for i, tech in enumerate(technology_types)}

fig = go.Figure()
fig.add_trace(go.Scatter(x=tech_4_int_strat_start_dt[0], y=tech_4_int_strat[0], mode='markers', marker=dict(size=tech_4_int_strat_count[0]*6+5, color=[technology_colours[tech] for tech in tech_4_int_strat[0]]),\
                         customdata=tech_4_int_strat_count[0], hovertemplate=('Date: %{x}<br>' 'Technology: %{y}<br>' 'Projects Funded: %{customdata}' '<extra></extra>'), name=f'{interest_strategy_types[0]}'))
for i in range(len(interest_strategy_types)-1):
  fig.add_trace(go.Scatter(x=tech_4_int_strat_start_dt[i+1], y=tech_4_int_strat[i+1], mode='markers', marker=dict(size=tech_4_int_strat_count[i+1]*6+5, color=[technology_colours[tech] for tech in tech_4_int_strat[i+1]]),\
                           customdata=tech_4_int_strat_count[i+1], hovertemplate=('Date: %{x}<br>' 'Technology: %{y}<br>' 'Projects Funded: %{customdata}' '<extra></extra>'), name=f'{interest_strategy_types[i+1]}', visible=False))

buttons = []
buttons.append(dict(label=f'{interest_strategy_types[0]}', method='update', args=[{'visible': [True] + [False]*(len(interest_strategy_types) - 1)},\
                                                                      {'title': {'text':f'Technology Area funded by date ({interest_strategy_types[0]})'}}]))
for i in range(1, len(interest_strategy_types)):
  visible = [False] * (len(interest_strategy_types))
  visible[i] = True
  buttons.append(dict(label=f'{interest_strategy_types[i]}', method='update', args=[{'visible': visible},\
                                                                        {'title': {'text': f'Technology Area funded by date ({interest_strategy_types[i]})'},\
                                                                         'yaxis': {'categoryorder': 'array', 'categoryarray': tech_4_int_strat_present[i]}}]))

fig.update_layout(updatemenus=[dict(buttons=buttons, direction='down', showactive=True, x=0, xanchor='left', y=1.04, yanchor='top')],\
                  xaxis_title='Date (DD-MM-YY)', yaxis_title='Technology Area', title=f'Technology Area funded by date ({interest_strategy_types[0]})', hovermode='closest',\
                  yaxis=dict(categoryorder='array', categoryarray=tech_4_int_strat_present[0]))
fig.update_layout(width=1400, height=1200)
st.write(fig)