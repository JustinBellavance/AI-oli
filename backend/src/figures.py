import os
import pandas as pd
from plotly import graph_objs as go

# Read CSV data (adjust the path/filename as needed)
df = pd.read_csv("data/data.csv")

# Group data by timestamp and sum up calories and macronutrients
agg = df.groupby("timestamp").agg({
    "calories (kcal)": "sum",
    "protein (g)": "sum",
    "carbohydrates (g)": "sum",
    "fat (g)": "sum"
}).reset_index()

# Compute total grams of macronutrients for percentage calculation
agg["total_macros"] = agg["protein (g)"] + agg["carbohydrates (g)"] + agg["fat (g)"]

# Calculate the percentage for each macronutrient (so they sum to 100%)
agg["protein_pct"] = agg["protein (g)"] / agg["total_macros"] * 100
agg["carbs_pct"]   = agg["carbohydrates (g)"] / agg["total_macros"] * 100
agg["fat_pct"]     = agg["fat (g)"] / agg["total_macros"] * 100

# Create the horizontal stacked bar chart using Plotly Graph Objects
fig = go.Figure()

# Add protein trace
fig.add_trace(go.Bar(
    y=agg["timestamp"],
    x=agg["protein_pct"],
    name="Protein",
    orientation='h'
))

# Add carbohydrates trace
fig.add_trace(go.Bar(
    y=agg["timestamp"],
    x=agg["carbs_pct"],
    name="Carbohydrates",
    orientation='h'
))

# Add fat trace
fig.add_trace(go.Bar(
    y=agg["timestamp"],
    x=agg["fat_pct"],
    name="Fat",
    orientation='h'
))

# Add annotations: total calories in white text in the center of each bar
annotations = []
for index, row in agg.iterrows():
    annotations.append(dict(
        x=50,  # middle of 0-100%
        y=row["timestamp"],
        text=f'{row["calories (kcal)"]} kcal',
        font=dict(color='white'),
        showarrow=False,
        xanchor='center',
        yanchor='middle'
    ))

# Update layout with stacking and annotations
fig.update_layout(
    barmode='stack',
    xaxis_title="Percentage (%)",
    yaxis_title="Timestamp",
    title="Macronutrient Composition by Timestamp (100% Stacked Horizontal Bar Chart)",
    annotations=annotations
)

# Ensure the output directory exists
output_dir = "data/figures"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "horizontal_bar_chart.png")

fig.write_html(output_file)

# Optionally, also show the figure
fig.show()
