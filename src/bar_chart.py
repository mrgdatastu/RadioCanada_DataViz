import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_clickable_bar_chart(data):
    #data = pd.read_csv("f:/RC1000-1.csv")

    filtered_data = data.dropna(subset=['referrer', 'simulated_subject'])

    page_counts = filtered_data.groupby(['referrer', 'simulated_subject']).size().reset_index(name='visit_count')

    page_counts = page_counts[~page_counts['simulated_subject'].isna()]

    colors = ['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921']

    fig = px.bar(page_counts, x='referrer', y='visit_count', color='simulated_subject',
                 color_discrete_sequence=colors, barmode='group')

    fig.update_layout(
        xaxis_title='Referrer',
        yaxis_title='Visit Count',
        title='Pages Visited in Referrer Column (Excluding NaN)',
        showlegend=True,
        legend_title='Simulated Subject'
    )

    fig.update_yaxes(type='log')

    clicked_charts = []

    def update_colors(clicked_subject):
        # Update the colors based on the clicked subject
        fig.data[0].marker.color = [colors[i] if subject == clicked_subject else 'lightgray' for i, subject in enumerate(page_counts['simulated_subject'])]

    fig.update_traces(marker=dict(line=dict(width=0)))

    def on_click(trace, points, state):
        if points.point_inds:
            clicked_subject = page_counts.loc[points.point_inds[0], 'simulated_subject']
            if clicked_subject not in clicked_charts:
                clicked_charts.append(clicked_subject)
            else:
                clicked_charts.remove(clicked_subject)
            update_colors(clicked_subject)

    fig.data[0].on_click(on_click)

    # Add clickable feature to your code
    scatter = fig.data[0]
    scatter.marker.color = colors

    def update_point(trace, points, selector):
        c = list(scatter.marker.color)
        for i in points.point_inds:
            c[i] = '#bae2be'
        with fig.batch_update():
            scatter.marker.color = c

    scatter.on_click(update_point)

    fig.show()