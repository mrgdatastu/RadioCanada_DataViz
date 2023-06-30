import pandas as pd
import plotly.express as px
import webcolors
import numpy as np

def generate_sunburst(data):
    # Fill NaN values with empty strings
    data['simulated_detailed_event'].fillna('', inplace=True)

    # Add level columns based on visit_page_num
    levels = ['level1', 'level2', 'level3', 'level4', 'level5', 'level6', 'level7']
    for i, level in enumerate(levels):
        data[level] = np.where(data['visit_page_num'] >= i + 1, data['simulated_detailed_event'], None)

    # Replace None values with "null"
    data = data.fillna("null")

    # Convert 'Account_Created_journey' column to numeric
    data['Account_Created_journey'] = pd.to_numeric(data['Account_Created_journey'], errors='coerce')

    # Filter out rows with missing or zero values in 'Account_Created_journey'
    data = data[data['Account_Created_journey'].notna() & (data['Account_Created_journey'] != 0)]

    # Calculate the total Account_Created_journey per level
    level_counts = data.groupby(levels)['Account_Created_journey'].sum().reset_index()

    # Calculate the percentage of Account_Created_journey per level
    total_journey = level_counts['Account_Created_journey'].sum()
    level_counts['Account_Created_percentage'] = (level_counts['Account_Created_journey'] / total_journey) * 100

    # Generate the sunburst chart
    fig = px.sunburst(
        level_counts,
        path=levels,
        values='Account_Created_journey',
        color='Account_Created_percentage',
        color_continuous_scale='blues',
        labels={'Account_Created_journey': 'Account Created Journey', 'Account_Created_percentage': 'Account Creation Percentage'},
    )

    # Define the hover template with custom formatting
    hover_template = '<b>Path:</b> %{id}<br>' \
                     'Account Created Journey: %{value}<br>' \
                     'Account Creation Percentage: %{customdata:.2f}%'

    # Add custom data to be displayed in the hover template
    hover_data = level_counts['Account_Created_percentage'].tolist()

    # Update the hover template and hover data
    fig.update_traces(hovertemplate=hover_template)
    fig.update_traces(customdata=hover_data)

    # Remove null values from figure data
    figure_data = fig['data'][0]
    mask = np.char.find(figure_data.ids.astype(str), "null") == -1
    figure_data.ids = figure_data.ids[mask]
    figure_data.values = figure_data.values[mask]
    figure_data.labels = figure_data.labels[mask]
    figure_data.parents = figure_data.parents[mask]

    # Update color based on path length
    max_level = level_counts[levels].apply(lambda x: pd.to_numeric(x, errors='coerce').last_valid_index(), axis=1)
    min_level = pd.to_numeric(max_level.min(), errors='coerce')
    max_level_diff = pd.to_numeric(max_level.max(), errors='coerce') - min_level
    normalized_max_level = (max_level - min_level) / max_level_diff if max_level_diff != 0 else 0

    light_colors = []
    for i, color in enumerate(px.colors.sequential.Blues):
        color_str = color if isinstance(color, str) else color[0]
        if color_str.startswith("#"):
            light_rgb = tuple(int(min(255, c + 0.6 * (255 - c))) for c in px.colors.hex_to_rgb(color_str))
        else:
            try:
                rgb_value = webcolors.name_to_rgb(color_str)
                light_rgb = tuple(int(min(255, c + 0.6 * (255 - c))) for c in rgb_value)
            except ValueError:
                # Handle invalid color names
                light_rgb = (255, 255, 255)  # Use white color as default
        light_hex = f"#{''.join(format(c, '02x') for c in light_rgb)}"  # Convert RGB to HEX color string
        light_colors.append(light_hex)

    # Convert light_colors to NumPy array for comparison
    light_colors = np.array(light_colors)

    # Update marker colors with light colors
    figure_data.marker.colors = [
        light_colors[i % len(light_colors)] if color == light_colors[i % len(light_colors)] else color
        for i, color in enumerate(figure_data.marker.colors)
    ]

    # Update the layout
    fig.update_layout(
        title={
            'text': 'Account Created Journey Sunburst Chart',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        coloraxis_colorbar=dict(
            title='Account Creation Percentage',
            len=0.5,
            yanchor='bottom',
            y=0.05,
            tickformat='.0%',
            tickvals=[i / 100 for i in range(1, 101)],
            ticktext=[f'{i}%' for i in range(1, 101)]
        )
    )

    return fig
