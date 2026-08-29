import dash
from dash import html, Input, dcc, Output, callback
import pandas as pd
import plotly.express as px


try:
    df = pd.read_csv(r"D:\Data science\Source code\airline_data.csv",
                                    encoding ="ISO-8859-1",
                                    dtype = {"Div1Airport": str,
                                             "Div1TailNum": str,
                                             "Div2Airport": str,
                                             "Div2TailNum": str})
except FileNotFoundError:
    print("Error: Dataset file not found. Please check the file path.")
    exit()

# this initializes the Dash application
app = dash.Dash(__name__)
app.title = "Airline Delay Board"

df = df.dropna(subset=["Year","Month","Reporting_Airline","DepDelay"]) # this line drop rows that contain nan values
df["Year"] = df["Year"].astype(int)
df["Month"] = df["Month"].astype(int)
df["DepDelay"] = df["DepDelay"].astype(float)
if "ArrDelay" in df.columns:
    df["ArrDelay"] = df["ArrDelay"].astype(float) # convert df["ArrDelay"] If exists


airlines = [{"label":airlines,"value":airlines} for airlines in sorted(df["Reporting_Airline"].unique())]
min_year, max_year = df["Year"].min(), df["Year"].max()

app.layout = html.Div([
     html.H1("Airlines Delay😎", style={
         "textAlign": "center",
         "color": "#2c3e50",
         "fontFamily": "Arial",
         "marginBottom":"20px"

     }),
    html.Div([

        html.Label("select year❤️❤",
                   style={"fontSize":18,"marginRight":"10px"}),
        dcc.Input(
            id="input-Year",
            type="number",
            value = 2010,
            min= min_year,
            max=max_year,
            step=1,
            debounce=True,
            style= {"fontSize":"18px",
                    "width": "100px",
                    "marginRight":"20px"}
        ),
        html.Label("Select airline", style={"fontSize": 18, "marginRight":"10px"}),

        dcc.Dropdown(id='airline-dropdown',
                     options=airlines,
                     value=airlines[0]["value"],
                     style={'width': '200px', 'fontSize': '16px'})

    ],style={"textAlign": "center",
             "marginBottom":"30px",
             "display":"flex",
             'justifyContent':"center",
             "alignItems":"center"}),
    # this Graph is for departure arrival ==> Line chart
    dcc.Graph(id='dep-delay-plot', style={'width': '80%', 'margin': '0 auto'}),
    # This Graph is for arrival delays ==> Bar chart
    dcc.Graph(id='arr-delay-plot', style={'width': '80%', 'margin': '0 auto'}),

    html.Table(id="stats-table", style={
        "width":"60%",
        "marginLeft":"400px",
        "fontFamily":"Arial",
        "border":"1px solid #ddd",
        "borderCollapse":"collapse",

    })
])

@app.callback(
        [Output('dep-delay-plot',"figure"),
               Output('arr-delay-plot',"figure"),
               Output("stats-table","children")],
              [Input("input-Year","value"),
               Input("airline-dropdown","value")])

def update_dashboard(year,airline):

    if not year or not airline:
        # Returns an empty plot and error
        return(px.line(title="Invalid input please retry"),
               px.line(title="Invalid input please retry"),
               [html.Tr([html.Td("Please select a valid year and airline.")])]
               )
    #convert year to  integer year
    year = int(year)

    if (year < min_year) or (year > max_year):
        # Check if the year is within the dataset's range
        return(px.line(title="Invalid input"),
               px.line(title="Invalid input"),
               [html.Tr([html.Td(f"Year must be between {min_year} and {max_year}")])])

    #filtered the data set for the selected year and airline

    filtered_df = df[(df["Year"] == year) & (df['Reporting_Airline'] == airline)]
    if filtered_df.empty:
        return(px.line(title="No Data available"),
               px.line(title="No Data available"),
               [html.Tr([html.Td(f"No data for {airline} in {year}")])])

    monthly_delays = filtered_df .groupby("Month")[['DepDelay', 'ArrDelay']].mean().reset_index()

    dep_fig = px.line(monthly_delays,
                      x = "Month",
                      y = "DepDelay",
                      title = f"Average Departure Delay for{airline} in {year}",
                      labels = {"Month":"Month","DepDelay":'Average Departure Delay (minutes)'},
                      markers=True)

    dep_fig.update_layout(
        xaxis= dict(
            tickmode="array",
            tickvals = list(range(1,13,1)),
            ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis_title = "Avg Dep Delay (min)",
        title_x = 0.5,
        template = "plotly_white"
    )

    arr_fig = px.line(title="Arrival Delay Data Not Available")
    if "ArrDelay" in filtered_df.columns:
        arr_fig = px.bar(monthly_delays,
                         x="Month",
                         y='ArrDelay',
                         labels={"Month":"Month",
                                "ArrDelay":"Average Arrival Delay (minutes)"},
                         title=f'Average Arrival Delay for {airline} in {year}'
                         )

        arr_fig.update_layout(
            xaxis = dict(tickmode="array",
                         tickvals =list(range(1,13,1)),
                         ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
            yaxis_title = "Avg Arr Delay (min)",
            title_x  =0.5,
            template = "plotly_white",
        )
        # Create a summary with key statistics
        stats = {"Metric" : ['Avg Dep Delay', 'Max Dep Delay', 'Min Dep Delay', 'Total Flights'],
         "Value" : [
              round(filtered_df["DepDelay"].mean(), 2),
              round(filtered_df["DepDelay"].max(),  2),
              round(filtered_df["DepDelay"].min(),  2),
              len(filtered_df)
          ]

         }

        if "ArrDelay" in filtered_df.columns:
            stats["Metric"].extend(['Avg Arr Delay', 'Max Arr Delay', 'Min Arr Delay'])
            stats["Value"].extend([
                round(filtered_df["ArrDelay"].mean(), 2),
                round(filtered_df["ArrDelay"].max(), 2),
                round(filtered_df["ArrDelay"].min(), 2)
            ])

        #convert stats to a DataFrame for Table Rendering
        stats_df = pd.DataFrame(stats)

        table = [html.Tr([html.Th(col , style= {"border":"1px solid #ddd","padding":"8px","backgroundColor":'#f2f2f2'}) for col in stats_df.columns])]  + [
                 html.Tr([html.Td(stats_df.iloc[i][col], style={'border': '1px solid #ddd', 'padding': '8px'}) for col in stats_df.columns ])
            for i in range(len(stats_df))
        ]

        return dep_fig, arr_fig, table

if __name__ =="__main__":
    app.run_server(debug=True)