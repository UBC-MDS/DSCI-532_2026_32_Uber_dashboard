from shiny import App, render, ui, reactive
import plotly.express as px
from ridgeplot import ridgeplot
# import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget
import pandas as pd

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# CSV is in ../data/raw/ relative to src/
csv_path = os.path.join(BASE_DIR, "..", "data", "raw", "ncr_ride_bookings.csv")

# Read CSV
uber = pd.read_csv(csv_path)
uber["Date"] = pd.to_datetime(uber["Date"]).dt.date
uber.columns = uber.columns.str.replace(' ', '_')


# UI
app_ui = ui.page_fluid(
        ui.tags.style("""
        /* Reduce padding inside value boxes */
        .shiny-value-box .card-body {
            padding: 0.5rem;
            font-size: 1em;   /* adjust number size */
            line-height: 1.1;
        }

        /* Reduce label font size */
        .shiny-value-box .card-title {
            font-size: 0.65em;
            margin-bottom: 0.2rem;
        }

        /* Reduce gap between columns */
        .shiny-columns {
            gap: 0.5rem;
        }
    """),
    ui.tags.style("body { font-size: 0.4em; }"),
    ui.panel_title("Uber Data Visualization"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                id="slider",
                label="Date range",
                min=uber.Date.min(),
                max=uber.Date.max(),
                value=[uber.Date.min(), uber.Date.max()],
            ),
            ui.input_action_button("action_button", "Reset filter"),
            open="desktop",
        ),
   
        ui.layout_columns(
            # Left column: value boxes in a horizontal row
            [
                ui.layout_columns(
                    ui.value_box("Total Bookings", ui.output_text("total_bookings"),
                                     style=" font-size: 2em;"),
                    ui.value_box("Total Revenue", ui.output_text("total_revenue"),
                                     style=" font-size: 2em;"),
                    ui.value_box("Canceled Bookings", ui.output_text("canceled_bookings"),
                                     style=" font-size: 2em;"),
                    col_widths=[4, 4, 4],  # each value box gets equal width
                )
            ],
            # Right column: Pie chart
            [
                output_widget("pie_chart")
            ],
            col_widths=[6, 6], 
        ),            
        ui.output_ui("vehicle_select_ui"),
        
        ui.layout_columns(
        ui.card(
            ui.card_header("Average Customer Rating by Vehicle Type"),
            output_widget("rating_barplot"),  # new output widget for the bar chart
            full_screen=True,
        ),
        ui.card(
            ui.card_header("Total Bookings Value Over Time"),
            output_widget("line_chart"),
            full_screen=True,
        ),
        col_widths=[6, 6],
        ),
         ),
)


# Server
def server(input, output, session):

    @reactive.calc
    def filtered_data():
        idx1 = uber.Date.between(
            left=input.slider()[0],
            right=input.slider()[1],
            inclusive="both",
        )
        # idx2 = uber.time.isin(input.checkbox_group())
        # uber_filtered = uber[idx1 & idx2]
        uber_filtered = uber[idx1]

        return uber_filtered
    
    @render.text
    def total_bookings():
        count = filtered_data().shape[0]
        return f"{count}"
     
    @render.text
    def total_revenue():
        bill = filtered_data().Booking_Value.sum()
        return f"${bill:.2f}"
    
    @render.text
    def canceled_bookings():
        count = 0
        count += filtered_data()[filtered_data().
                                 Cancelled_Rides_by_Driver == 1].shape[0]
        count += filtered_data()[filtered_data().
                                 Cancelled_Rides_by_Customer == 1].shape[0]
        return f"{count}"
    
    @output
    @render.ui
    def vehicle_select_ui():
        df = filtered_data()  # use filtered_data based on date
        vehicle_choices = df["Vehicle_Type"].unique().tolist()
        
        return ui.input_select(
            id="vehicle_type",
            label="Select Vehicle Type",
            choices=vehicle_choices,
            selected=None,  # default = all
            multiple=True,
        )

    @render_plotly
    def rating_barplot():
        df = filtered_data()
        selected_vehicles = input.vehicle_type()
        if selected_vehicles:
            df = df[df.Vehicle_Type.isin(selected_vehicles)]
        
        avg_rating = df.groupby("Vehicle_Type")["Customer_Rating"].mean().reset_index()
        fig = px.bar(avg_rating, x="Vehicle_Type", y="Customer_Rating", text="Customer_Rating",
                    title="Average Customer Rating by Vehicle Type",
                    labels={"Customer_Rating": "Avg Customer Rating", "Vehicle_Type": "Vehicle Type"})
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(yaxis_range=[0, 5])
        return fig

    @render_plotly
    def line_chart():
        df = filtered_data()
        
        # Filter by selected vehicle types
        selected_vehicles = input.vehicle_type()
        if selected_vehicles:
            df = df[df.Vehicle_Type.isin(selected_vehicles)]
        
        # Aggregate by date for line chart
        df_agg = df.groupby("Date")["Booking_Value"].sum().reset_index()
        
        # Create line chart
        fig = px.line(
            df_agg,
            x="Date",
            y="Booking_Value",
            title="Total Booking Value Over Time",
            labels={"Booking_Value": "Total Booking Value", "Date": "Date"}
        )
        
        fig.update_layout(xaxis_title="Date", yaxis_title="Total Booking Value")
        return fig

    @render_plotly
    def pie_chart():
        # Aggregate revenue by vehicle type
        revenue_by_vehicle_type = filtered_data().groupby("Vehicle_Type")["Booking_Value"].sum().reset_index()

        # Create Plotly pie chart
        fig = px.pie(
            revenue_by_vehicle_type,
            names="Vehicle_Type",
            values="Booking_Value",
            title="Revenue by Vehicle Type"
        )
        return fig

# Create app
app = App(app_ui, server)
