import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def generate_bar_chart(data):
    filtered_data = data.dropna(subset=['referrer', 'simulated_subject'])

    page_counts = filtered_data.groupby(['referrer', 'simulated_subject']).size().reset_index(name='visit_count')

    page_counts = page_counts[~page_counts['simulated_subject'].isna()]

    colors = ['rgb(247,251,255)', 'rgb(222,235,247)', 'rgb(198,219,239)', 'rgb(158,202,225)', 'rgb(107,174,214)', 'rgb(66,146,198)', 'rgb(33,113,181)', 'rgb(8,81,156)', 'rgb(8,48,107)']

    fig = px.bar(page_counts, x='referrer', y='visit_count', color='simulated_subject',
                 color_discrete_sequence=colors, barmode='group')

    fig.update_layout(
        plot_bgcolor='#f2f2f2',
        paper_bgcolor='#f2f2f2',
        xaxis=dict(
            showgrid=True,
            gridcolor='gray',
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='gray',
        ),
        xaxis_title='Reference',
        yaxis_title='Visit Count',
        title={
            'text': 'Page visited based on reference sources and sections',
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.95
        },
        showlegend=True,
        legend_title='Sections'
    )

    clicked_charts = []

    def update_colors(clicked_subject):
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

    scatter = fig.data[0]
    scatter.marker.color = colors

    def update_point(trace, points, selector):
        c = list(scatter.marker.color)
        for i in points.point_inds:
            c[i] = '#bae2be'
        with fig.batch_update():
            scatter.marker.color = c

    scatter.on_click(update_point)

    return fig
