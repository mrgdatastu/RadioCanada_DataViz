import pandas as pd
import numpy as np
import plotly.express as px

def generate_sunburst(data):

    # Create an empty dictionary to store the users for each action
    action_users = {}

    # Load the dataset
    df = data.copy() #pd.read_csv('f:/RC-poly_donnees_simulees.csv')

    # Select the columns of interest
    dataset = df[['identifiant_visite', 'simulated_detailed_event', 'visit_page_num']]

    # Iterate over the dataset
    for index, row in dataset.iterrows():
        user = row['identifiant_visite']
        action = row['simulated_detailed_event']
        level = row['visit_page_num']
        #print(level)
        # Skip empty actions
        if pd.isnull(action):
            continue
        
        # Check if the action is already in the dictionary
        if action in action_users:
            action_users[action].append((user, level))
        else:
            action_users[action] = [(user, level)]
    #action_users.values()
    # Find the maximum length of the user lists
    max_length = 7 #max(len(users) for users in action_users.values()) #= 334
    #max_length
    # Pad shorter user lists with NaN values
    for users in action_users.values():
        #print(users)
        users.extend([(np.nan, np.nan)] * (max_length - len(users)))
    #users
    # action_users
    action_users_sorted = sorted(action_users)
    df.visit_page_num


    # df5 = action_users.sorted(['Action_autre','Action_creation_compte','Page_Info','Page_Mordu','Page_OHdio','Page_accueil_Info','Page_accueil_Mordu','Page_accueil_OHdio','Video_Info','Video_Mordu'], axis=1)
    # df5
    #df['visit_page_num']

    # Create a pivot table
    pivot_table = df.pivot_table(index='identifiant_visite', columns='simulated_detailed_event', values='visit_page_num', aggfunc='first', fill_value=0)
    pivot_table = pivot_table.reindex(sorted(pivot_table.columns), axis=1)

    # Replace non-zero values with column headers
    pivot_table = pivot_table.apply(lambda x: np.where(x != 0, x.name, 'None'))
    pivot_table['Actions_Done'] = pivot_table.apply(lambda row: row[row != 'None'].count(), axis=1)
    pivot_table = pivot_table.merge(df[['identifiant_visite', 'visit_page_num']], on='identifiant_visite')


    pivot_table
    fig = px.sunburst(pivot_table, path=['Action_autre','Action_creation_compte','Page_Info','Page_Mordu','Page_OHdio','Page_accueil_Info','Page_accueil_Mordu','Page_accueil_OHdio','Video_Info','Video_Mordu'], values='visit_page_num', color='visit_page_num', branchvalues='total')

    # # Show the plot
    return fig