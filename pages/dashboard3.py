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