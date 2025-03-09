import os
import pandas as pd
import plotly.graph_objects as go
import json

def create_figure(df):
    # Group data by timestamp and sum up calories and macronutrients
    agg = df.groupby("timestamp").agg({
        "calories (kcal)": "sum",
        "protein (g)": "sum",
        "carbohydrates (g)": "sum",
        "fat (g)": "sum"
    }).reset_index()

    # Compute total grams of macronutrients for percentage calculation
    agg["total_macros"] = agg["protein (g)"] + agg["carbohydrates (g)"] + agg["fat (g)"]

    # Optionally, remove any rows with zero total_macros to avoid empty bars
    agg = agg[agg["total_macros"] > 0]

    # Calculate percentage for each macronutrient so that they sum to 100%
    agg["protein_pct"] = agg["protein (g)"] / agg["total_macros"] * 100
    agg["carbs_pct"] = agg["carbohydrates (g)"] / agg["total_macros"] * 100
    agg["fat_pct"] = agg["fat (g)"] / agg["total_macros"] * 100

    # Format the timestamp to show just the date and time for the x-axis
    agg["time_only"] = pd.to_datetime(agg["timestamp"]).dt.strftime('%H:%M')  # Format it to 'HH:MM' for hours and minutes
    agg["timestamp"] = agg["timestamp"].astype(str)

    # Create a vertical stacked bar chart using Plotly Graph Objects
    fig = go.Figure()

    # Add traces for protein, carbohydrates, and fat
    fig.add_trace(go.Bar(
        x=agg["timestamp"].tolist(),
        y=agg["protein_pct"].tolist(),
        name="Protein",
        marker=dict(color='#C9B488')
    ))
    fig.add_trace(go.Bar(
        x=agg["timestamp"].tolist(),
        y=agg["carbs_pct"].tolist(),
        name="Carbohydrates",
        marker=dict(color='#CFA486')
    ))
    fig.add_trace(go.Bar(
        x=agg["timestamp"].tolist(),
        y=agg["fat_pct"].tolist(),
        name="Fat",
        marker=dict(color='#C18076')
    ))

    # Add annotations for total calories in white text at the center of the macronutrient with the highest percentage
    annotations = []
    for _, row in agg.iterrows():
        max_pct = max(row["protein_pct"], row["carbs_pct"], row["fat_pct"])
        if max_pct == row["protein_pct"]:
            y_position = row["protein_pct"] / 2
        elif max_pct == row["carbs_pct"]:
            y_position = row["protein_pct"] + row["carbs_pct"] / 2
        else:
            y_position = row["protein_pct"] + row["carbs_pct"] + row["fat_pct"] / 2

        annotations.append(dict(
            x=row["timestamp"],  # Position at the timestamp on the x-axis
            y=y_position,  # Position in the middle of the macronutrient with the highest percentage
            text=f'{row["calories (kcal)"]} kcal',
            font=dict(color='white', size=20),  # Increase font size to 12
            showarrow=False,
            xanchor='center',
            yanchor='middle'
        ))

    # Update layout with necessary configurations
    fig.update_layout(
        barmode='stack',
        annotations=annotations,
        font=dict(size=14),  # Increase font size to 14
        xaxis=dict(
            title=dict(text="", font=dict(size=16)),  # Remove x-axis title
            showticklabels=True,
            type = 'category',
            categoryorder = 'array',
            categoryarray = agg["timestamp"].tolist()
        ),
        yaxis=dict(
            title=dict(text="", font=dict(size=16)),  # Remove y-axis title
            showticklabels=False,  # Remove y-axis labels
        ),
        showlegend=True,  # Show the legend
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=1.02,
            xanchor="center",  # Center the legend horizontally
            x=0.5,  # Center the legend horizontally
            font=dict(size=10)  # Reduce font size of the legend text to 10
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Remove plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Remove paper background
        margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins to center the plot
    )

    config = {
        'displayModeBar': False
    }

    # Ensure the output directory exists
    output_dir = "data/figures"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "vertical_bar_chart.html")

    # Save the figure to a file (optional)
    # fig.write_html(output_file, config=config)

    fig_json = fig.to_dict()
    fig_json['config'] = config 
    
    return fig_json
