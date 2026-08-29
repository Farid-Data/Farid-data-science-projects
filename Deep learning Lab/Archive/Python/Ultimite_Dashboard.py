# Import required libraries
import dash  # Dash framework for building web-based dashboards
from dash import html, dcc, Input, Output  # Dash components: html for HTML elements, dcc for interactive components, Input/Output for callbacks
import pandas as pd  # Pandas for data manipulation and analysis
import plotly.express as px  # Plotly Express for creating interactive charts easily

# Load the dataset from the specified file path
# The encoding and dtype parameters handle special characters and ensure diversion-related columns are strings
try:
    df = pd.read_csv(
        r"D:\Data science\Source code\airline_data.csv",  # Path to your airline dataset
        encoding="ISO-8859-1",  # Encoding to handle special characters in the CSV
        dtype={"Div1Airport": str, "Div1TailNum": str, "Div2Airport": str, "Div2TailNum": str}  # Ensure diversion columns are strings
    )
except FileNotFoundError:
    # If the file path is incorrect, print an error and exit to prevent crashes
    print("Error: Dataset file not found. Please check the file path.")
    exit()

# Initialize the Dash application
# dash.Dash creates a Flask-based web server for the dashboard
# __name__ tells Dash the name of the current module, used to locate resources
app = dash.Dash(__name__)

# Set the title of the web page (appears in the browser tab)
# This is cosmetic, helping users identify the dashboard in their browser
app.title = "✈️ Flight Delay Dashboard"

# Clean and preprocess the dataset
# Drop rows with missing values in critical columns to ensure reliable data for analysis
df = df.dropna(subset=['Year', 'Month', 'Reporting_Airline', 'DepDelay'])

# Convert columns to appropriate data types for consistency and to avoid errors in calculations
df['Year'] = df['Year'].astype(int)  # Ensure Year is an integer for filtering
df['Month'] = df['Month'].astype(int)  # Ensure Month is an integer for grouping
df['DepDelay'] = df['DepDelay'].astype(float)  # Ensure DepDelay is a float for numerical operations
if 'ArrDelay' in df.columns:
    df['ArrDelay'] = df['ArrDelay'].astype(float)  # Convert ArrDelay to float if the column exists

# Prepare data for the dropdown and input validation
# Create a list of unique airlines for the dropdown, sorted for user-friendliness
airlines = [{'label': airline, 'value': airline} for airline in sorted(df['Reporting_Airline'].unique())]

# Get the minimum and maximum years in the dataset to set valid input ranges
min_year, max_year = df['Year'].min(), df['Year'].max()

# Define the dashboard layout
# app.layout specifies the structure of the web page using HTML and Dash components
app.layout = html.Div([
    # Main title of the dashboard, displayed at the top of the page
    html.H1("✈️ Flight Delay Dashboard😎😎", style={
        'textAlign': 'left',  # Center the title
        'color': '#2c3e50',  # Dark blue color for a professional look
        'fontFamily': 'Times New roman',  # Clean, readable font
        'marginBottom': '20px'  # Space below the title
    }),

    # Container for input controls (year input and airline dropdown)
    html.Div([
        # Label for the year input, guiding the user
        html.Label("Select Year", style={'fontSize': 18, 'marginRight': '10px'}),

        # Input field for selecting a year, with validation and styling
        dcc.Input(
            id='input-year',  # Unique ID for callback reference
            type='number',  # Restrict input to numbers
            value=2010,  # Default year (can be any year in your dataset)
            min=min_year,  # Minimum year from dataset
            max=max_year,  # Maximum year from dataset
            step=1,  # Increment by 1 (whole years)
            debounce=True,  # Update only after user stops typing
            style={'fontSize': '18px', 'width': '100px', 'marginRight': '20px'}  # Styling for size and spacing
        ),

        # Label for the airline dropdown
        html.Label("Select Airline", style={'fontSize': 18, 'marginRight': '10px'}),

        # Dropdown for selecting an airline
        dcc.Dropdown(
            id='airline-dropdown',  # Unique ID for callback reference
            options=airlines,  # List of airlines from the dataset
            value=airlines[0]['value'],  # Default to the first airline
            style={'width': '200px', 'fontSize': '16px'}  # Styling for width and font size
        )
    ], style={
        'textAlign': 'center',  # Center the input controls
        'marginBottom': '30px',  # Space below the controls
        'display': 'flex',  # Use flexbox for horizontal alignment
        'justifyContent': 'center',  # Center items horizontally
        'alignItems': 'center'  # Align items vertically
    }),

    # Graph for departure delays (line plot)
    dcc.Graph(id='dep-delay-plot', style={'width': '80%', 'margin': '0 auto'}),

    # Graph for arrival delays (bar chart, if ArrDelay exists)
    dcc.Graph(id='arr-delay-plot', style={'width': '80%', 'margin': '0 auto'}),

    # Table for summary statistics
    html.Table(id='stats-table', style={
        'width': '50%',  # Table width for readability
        'margin': '20px auto',  # Center with spacing
        'border': '1px solid #ddd',  # Light border for table
        'borderCollapse': 'collapse',  # Clean table borders
        'fontFamily': 'Arial'  # Consistent font
    })
])

# Define the callback to make the dashboard interactive
# This function updates the graphs and table based on user inputs (year and airline)
@app.callback(
    [Output('dep-delay-plot', 'figure'),  # Output: departure delay plot
     Output('arr-delay-plot', 'figure'),  # Output: arrival delay plot
     Output('stats-table', 'children')],  # Output: table content
    [Input('input-year', 'value'),  # Input: year from input field
     Input('airline-dropdown', 'value')]  # Input: airline from dropdown
)
def update_dashboard(year, airline):
    # Validate inputs to prevent errors
    if not year or not airline:
        # Return empty plots and an error message if inputs are missing
        return (px.line(title="Invalid input"),
                px.line(title="Invalid input"),
                [html.Tr([html.Td("Please select a valid year and airline.")])])
    
    # Convert year to integer for filtering
    year = int(year)
    # Check if the year is within the dataset’s range
    if year < min_year or year > max_year:
        return (px.line(title="Year out of range"),
                px.line(title="Year out of range"),
                [html.Tr([html.Td(f"Year must be between {min_year} and {max_year}.")])])

    # Filter the dataset for the selected year and airline
    filtered_df = df[(df['Year'] == year) & (df['Reporting_Airline'] == airline)]

    # Check if filtered data is empty
    if filtered_df.empty:
        return (px.line(title="No data available"),
                px.line(title="No data available"),
                [html.Tr([html.Td(f"No data for {airline} in {year}.")])])

    # Aggregate average departure and arrival delays by month
    monthly_delays = filtered_df.groupby('Month')[['DepDelay', 'ArrDelay']].mean().reset_index()

    # Create a line plot for average departure delays
    dep_fig = px.line(
        monthly_delays,
        x='Month',  # X-axis: months (1–12)
        y='DepDelay',  # Y-axis: average departure delay
        title=f'Average Departure Delay for {airline} in {year}',  # Dynamic title
        labels={'Month': 'Month', 'DepDelay': 'Average Departure Delay (minutes)'},  # Axis labels
        markers=True  # Show markers on the line for clarity
    )
    dep_fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),  # Custom month names
        yaxis_title="Avg Dep Delay (min)",  # Y-axis label
        title_x=0.5,  # Center the title
        template='plotly_white'  # Clean white background
    )

    # Create a bar chart for average arrival delays (if ArrDelay exists)
    arr_fig = px.line(title="Arrival Delay Data Not Available")  # Default if ArrDelay is missing
    if 'ArrDelay' in filtered_df.columns:
        arr_fig = px.bar(
            monthly_delays,
            x='Month',  # X-axis: months
            y='ArrDelay',  # Y-axis: average arrival delay
            title=f'Average Arrival Delay for {airline} in {year}',  # Dynamic title
            labels={'Month': 'Month', 'ArrDelay': 'Average Arrival Delay (minutes)'}  # Axis labels
        )
        arr_fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            ),  # Custom month names
            yaxis_title="Avg Arr Delay (min)",  # Y-axis label
            title_x=0.5,  # Center the title
            template='plotly_white'  # Clean white background
        )

    # Create a summary table with key statistics
    stats = {
        'Metric': ['Avg Dep Delay', 'Max Dep Delay', 'Min Dep Delay', 'Total Flights'],
        'Value': [
            round(filtered_df['DepDelay'].mean(), 2),  # Average departure delay
            round(filtered_df['DepDelay'].max(), 2),  # Maximum departure delay
            round(filtered_df['DepDelay'].min(), 2),  # Minimum departure delay
            len(filtered_df)  # Number of flights
        ]
    }
    if 'ArrDelay' in filtered_df.columns:
        # Add arrival delay stats if the column exists
        stats['Metric'].extend(['Avg Arr Delay', 'Max Arr Delay', 'Min Arr Delay'])
        stats['Value'].extend([
            round(filtered_df['ArrDelay'].mean(), 2),
            round(filtered_df['ArrDelay'].max(), 2),
            round(filtered_df['ArrDelay'].min(), 2)
        ])

    # Convert stats to a DataFrame for table rendering
    stats_df = pd.DataFrame(stats)
    # Create HTML table rows with headers and data
    table = [
        html.Tr([html.Th(col, style={'border': '1px solid #ddd', 'padding': '8px', 'backgroundColor': '#f2f2f2'}) for col in stats_df.columns])] + [
        html.Tr([html.Td(stats_df.iloc[i][col], style={'border': '1px solid #ddd', 'padding': '8px'}) for col in stats_df.columns])
        for i in range(len(stats_df))
    ]

    # Return the updated figures and table
    return dep_fig, arr_fig, table

# Run the Dash app
# debug=True enables live reloading and error messages in the browser
if __name__ == '__main__':
    app.run_server(debug=True)