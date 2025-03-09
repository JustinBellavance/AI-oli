import os
import pandas as pd
import plotly.graph_objects as go
import json

# Read CSV data
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
    agg["carbs_pct"]   = agg["carbohydrates (g)"] / agg["total_macros"] * 100
    agg["fat_pct"]     = agg["fat (g)"] / agg["total_macros"] * 100
    
    agg["time_only"] = pd.to_datetime(agg["timestamp"]).dt.strftime('%H:%M')  # Format it to 'HH:MM' for hours and minutes

    agg["timestamp"] = agg["timestamp"].astype(str)
    


    # Create a horizontal stacked bar chart using Plotly Graph Objects
    fig = go.Figure()

    # Add traces for protein, carbohydrates, and fat
    fig.add_trace(go.Bar(
        y=agg["time_only"].tolist(),
        x=agg["protein_pct"].tolist(),
        name="Protein",
        orientation='h'
    ))
    fig.add_trace(go.Bar(
        y=agg["time_only"].tolist(),
        x=agg["carbs_pct"].tolist(),
        name="Carbohydrates",
        orientation='h'
    ))
    fig.add_trace(go.Bar(
        y=agg["time_only"].tolist(),
        x=agg["fat_pct"].tolist(),
        name="Fat",
        orientation='h'
    ))

    # Add annotations for total calories in white text at the center of each bar
    annotations = []
    for _, row in agg.iterrows():
        annotations.append(dict(
            x=50,  # Center of the bar (0-100%)
            y=row["time_only"],
            text=f'{row["calories (kcal)"]} kcal',
            font=dict(color='white', size=8),
            showarrow=False,
            xanchor='center',
            yanchor='middle'
        ))
        

    fig.update_layout(
        dragmode=False,
        barmode='stack',
        annotations=annotations,
        font=dict(size=12),
        xaxis=dict(
            tickformat='%x%', 
            showticklabels=True
        ),
        yaxis=dict(
            autorange='reversed',
            type='category',
            categoryorder='array',
            categoryarray=agg["time_only"].tolist()  # Use the formatted time-only timestamps for y-axis
        ),
        xaxis_title="",  # Remove x-axis title
        yaxis_title="",  # Remove y-axis title
        showlegend=False,  # Remove legend
        plot_bgcolor='rgba(0,0,0,0)',  # Remove plot background
        paper_bgcolor='rgba(0,0,0,0)'   # Remove paper background
    )

    config = {
        'displayModeBar': False
    }

    # Ensure the output directory exists
    output_dir = "data/figures"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "horizontal_bar_chart.html")

    # # Save the figure to a file
    # fig.write_html(output_file, config=config)

    fig_json = fig.to_dict()
    fig_json['config'] = config 
    
    return fig_json
    