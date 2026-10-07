import streamlit as st
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

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

#Look to include all of this in a separate page on the website
#Investigate the differences between total budget and SIF funding
useful_sif_funding, useful_budget, useful_start_dt, useful_tech, useful_sector, useful_owners, useful_funding_mechanism = [], [], [], [], [], [], []
for i in range(len(sif_funding)):
  if pd.notna(sif_funding[i]):
    useful_sif_funding.append(sif_funding[i])
    useful_budget.append(budget[i])
    useful_start_dt.append(start_dt[i])
    useful_tech.append(technology[i])
    useful_sector.append(sector[i])
    useful_owners.append(owners[i])
    useful_funding_mechanism.append(funding_mechanism[i])
useful_sif_funding = pd.Series(useful_sif_funding)
useful_budget = pd.Series(useful_budget)
useful_start_dt = pd.Series(useful_start_dt)
useful_tech = pd.Series(useful_tech)
useful_sector = pd.Series(useful_sector)
useful_owners = pd.Series(useful_owners)
useful_funding_mechanism = pd.Series(useful_funding_mechanism)

useful_sector_types = useful_sector.unique()
useful_sector_types = useful_sector_types[:4]
useful_sector_types_idx = [useful_sector[useful_sector.str.contains(uts, na=False)].index.tolist() for uts in useful_sector_types]

useful_owner_types = useful_owners.unique()
useful_owner_types = [uto for uto in useful_owner_types if pd.notna(uto)]
useful_owner_types_idx = [useful_owners[useful_owners.str.contains(uto, na=False)].index.tolist() for uto in useful_owner_types]

useful_tech_types_idx = [useful_tech[useful_tech.str.contains(tt, na=False)].index.tolist() for tt in technology_types]
useful_tech_types_idx_full, useful_tech_types = [], []
for i in range(len(useful_tech_types_idx)):
  if len(useful_tech_types_idx[i]) > 0:
    useful_tech_types_idx_full.append(useful_tech_types_idx[i])
    useful_tech_types.append(technology_types[i])
useful_tech_types_count = [len(utfi) for utfi in useful_tech_types_idx_full]

#Create a plot to compare how the budget compares to funding received
st.subheader("Give plot a title")
lin_data = np.linspace(0, 4.5e7, 2)
fig = go.Figure()
fig.add_trace(go.Scatter(x=lin_data, y=lin_data, fill='tozerox', fillcolor='black', mode='lines', line=dict(color='blue', width=3),showlegend=False))
fig.add_trace(go.Scatter(x=useful_budget, y=useful_sif_funding, mode='markers', showlegend=False))
fig.update_xaxes(range=[0, 4.5e7])
fig.update_yaxes(range=[0, 4.5e7])
fig.update_layout(height=600, width=1200, xaxis_title='Total Funding (£)', yaxis_title='SIF Funding Required (£)')
st.write(fig)

#Determine dates when projects received funding, looking at the cumulative number to receive across time
st.subheader("Give plot a title")
useful_start_dt_sort_idx = np.argsort(useful_start_dt)
useful_start_dt_sort = useful_start_dt[useful_start_dt_sort_idx]
total_cumul = [np.sum(useful_start_dt_sort <= date) for date in useful_start_dt_sort]
fig = go.Figure()
fig.add_trace(go.Scatter(x=useful_start_dt_sort, y=total_cumul, mode='markers+lines', showlegend=False))
fig.update_layout(height=600, width=1200, xaxis_title='Date (DD-MM-YY)', yaxis_title='Number of Projects')
st.write(fig)

#Determine what technologies have received investment from this innovation fund
st.subheader("Give plot a title")
bts_useful_tech_types_idx = np.argsort(useful_tech_types_count)[::-1]
bts_useful_tech_types = np.array(useful_tech_types)[bts_useful_tech_types_idx]
bts_useful_tech_types_count = np.array(useful_tech_types_count)[bts_useful_tech_types_idx]
fig = go.Figure()
fig.add_trace(go.Bar(x=bts_useful_tech_types, y=bts_useful_tech_types_count, showlegend=False))
fig.update_xaxes(tickmode='linear', tickangle=30, tickfont=dict(size=8))
fig.update_layout(height=600, width=1200, xaxis_title='Technology', yaxis_title='Number of Projects')
st.write(fig)

#Compare the difference in budget and funding across technologies
st.subheader("Give plot a title")
total_useful_tech_budget = np.zeros(len(useful_tech_types))
total_useful_tech_sif_funding = np.zeros(len(useful_tech_types))
for i in range(len(useful_tech_types)):
  for idx in useful_tech_types_idx_full[i]:
    total_useful_tech_budget[i] += useful_budget[idx]
    total_useful_tech_sif_funding[i] += useful_sif_funding[idx]

TOTAL_useful_tech_budget = np.sum(total_useful_tech_budget)
TOTAL_useful_tech_sif_funding = np.sum(total_useful_tech_sif_funding)

bts_total_useful_tech_budget_idx = np.argsort(total_useful_tech_budget)[::-1]
bts_total_useful_tech_budget = total_useful_tech_budget[bts_total_useful_tech_budget_idx]
bts_useful_tech_types_4_budget = np.array(useful_tech_types)[bts_total_useful_tech_budget_idx]
bts_useful_tech_sif_funding = np.array(total_useful_tech_sif_funding)[bts_total_useful_tech_budget_idx]

fig = make_subplots(rows=3, cols=1, subplot_titles=('Bar Chart', 'Scatter Diagram', 'Differences'))
fig.add_trace(go.Bar(x=bts_useful_tech_types_4_budget, y=bts_total_useful_tech_budget, name=f'Total Budget (£{TOTAL_useful_tech_budget:,.2f})', showlegend=True), row=1, col=1)
fig.add_trace(go.Bar(x=bts_useful_tech_types_4_budget, y=bts_useful_tech_sif_funding, name=f'Total SIF Funding (£{TOTAL_useful_tech_sif_funding:,.2f})', showlegend=True), row=1, col=1)
fig.add_trace(go.Scatter(x=bts_useful_tech_types_4_budget, y=bts_total_useful_tech_budget, mode='markers+lines', showlegend=False), row=2, col=1)
fig.add_trace(go.Scatter(x=bts_useful_tech_types_4_budget, y=bts_useful_tech_sif_funding, mode='markers+lines', showlegend=False), row=2, col=1)
fig.add_trace(go.Scatter(x=bts_useful_tech_types_4_budget, y=bts_total_useful_tech_budget - bts_useful_tech_sif_funding, mode='markers', name='Difference (£)', showlegend=False), row=3, col=1)
fig.update_xaxes(tickmode='linear', tickangle=30, tickfont=dict(size=8))
fig.update_xaxes(title_text='Technology')
fig.update_yaxes(title_text='Total Funding (£)')
fig.update_layout(height=1500, width=1400, legend=dict(yanchor='top', y=0.99, xanchor='right', x=0.99))
st.write(fig)