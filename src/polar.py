import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def generate_polar(my_df):

    keep = ['identifiant_visite', 'visit_page_num', 'visit_start_time_gmt', 'Account_Created_journey']
    my_df = my_df[keep]
    my_df = my_df[my_df['visit_page_num'] == 1]
    my_df['visit_start_time_gmt'] = pd.to_datetime(my_df['visit_start_time_gmt'])
    my_df['hour'] = my_df['visit_start_time_gmt'].dt.hour
    my_df = my_df.drop('visit_start_time_gmt', axis=1)
    hour_counts = my_df['hour'].value_counts().sort_index()
    acc_creation_ratio = my_df.groupby('hour')['Account_Created_journey'].sum().sort_index()
    hour_ratio = acc_creation_ratio / hour_counts

    theta = [360 * i / 24 for i in hour_counts.index]

    # Define the color scale using Python Plotly "Blues" color scale
    color_scale = px.colors.sequential.Blues

    # Create a polar area bar chart using go.Figure
    fig = go.Figure()

    # Create traces for the chart
    fig.add_trace(go.Barpolar(
        r=hour_counts.values,
        theta=theta,
        marker_color=hour_counts.values,  
        marker_colorscale=color_scale, 
        opacity=0.8,
        text=acc_creation_ratio.values,
        hovertemplate='Visits from %{theta}: %{r}<br> Account Creation: %{text}<extra></extra>',
        name='Visit Time'
    ))

    # Add a custom legend item for "Number of visits" as a line
    fig.add_trace(go.Scatterpolar(
        r=[0],
        theta=[0],
        mode='lines',
        line=dict(color='rgba(0,0,0,1)', width=2),
        showlegend=True,
        hoverinfo='skip',
        name='Number of visits' 
    ))

    fig.add_trace(go.Scatterpolar(
        r=[0],
        theta=[0],
        mode='markers',
        marker=dict(
            color=[acc_creation_ratio.values],
            colorscale=color_scale,
            cmax=max(acc_creation_ratio.values),
            cmin=min(acc_creation_ratio.values),
            showscale=True,
            colorbar=dict(
                title='Number of Visits',
                titleside='top',
                tickmode='array',
                tickvals=[min(acc_creation_ratio.values), max(acc_creation_ratio.values)],
                ticktext=['Min', 'Max'],
                lenmode='fraction',
                len=0.6,
                xanchor='right',
                x=1.5,
                yanchor='top',
                y=1
            )
        ),
        hoverinfo='skip',
        showlegend=False,
    ))

    # Update the layout of the chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, side="counterclockwise", ticks=''),
            angularaxis=dict(
                direction='clockwise',
                period=360,
                tickvals=[360 * i / 24 for i in range(24)],
                ticktext=['{}-{}'.format(i, (i + 1) % 24) for i in range(24)]
            ),
        ),
        showlegend=True,  # Add legend
        legend=dict(
            title='Legend',
            itemsizing='constant',
            orientation='h',  # Set the orientation to horizontal
            traceorder='reversed',
            tracegroupgap=10,
            bordercolor='rgba(0,0,0,0)',
            borderwidth=0,
            x=.85,  # Position the legend at the top right
            y=1.1,  # Position the legend above the plot
            itemclick='toggle',  # Allow toggling of the legend item
            itemdoubleclick='toggleothers',  # Allow toggling of other legend items
        ),
        coloraxis=dict(
            colorbar=dict(
                title='Color Spectrum',
                titleside='top',
                lenmode='fraction',
                len=0.6,
                xanchor='left',
                x=0.1,
                yanchor='top',
                y=1
            )
        )
    )

    # Display the chart
    return fig
