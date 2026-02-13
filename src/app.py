from shiny import App, render, ui, reactive
import plotly.express as px
from ridgeplot import ridgeplot
# import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget
import pandas as pd

uber = pd.read_csv(r"..\data\raw\ncr_ride_bookings.csv")
uber["Date"] = pd.to_datetime(uber["Date"]).dt.date
uber.columns = uber.columns.str.replace(' ', '_')


# UI
app_ui = ui.page_fluid(
    ui.tags.style("body { font-size: 0.6em; }"),
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
            # ui.input_checkbox_group(
            #     id="checkbox_group",
            #     label="Food service",
            #     choices={
            #         "Lunch": "Lunch",
            #         "Dinner": "Dinner",
            #     },
            #     selected=[
            #         "Lunch",
            #         "Dinner",
            #     ],
            # ),
            ui.input_action_button("action_button", "Reset filter"),
            open="desktop",
        ),
   
        ui.layout_columns(
            ui.value_box("Total Bookings", ui.output_text("total_bookings")),
            ui.value_box("Total Revenue", ui.output_text("total_revenue")),
            ui.value_box("Canceled Bookings", ui.output_text("canceled_bookings")),
            # ui.value_box("Successful Bookings", ui.output_text("successful_bookings")),

            fill=False,
        ),
        output_widget("pie_chart"),
        ui.layout_columns(
            ui.card(
                ui.card_header("Average Customer Rating by Vehicle Type"),
                output_widget("rating_barplot"),  # new output widget for the bar chart
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Total Bookings Value per Month"),
                output_widget("scatterplot"),
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

    # @render.data_frame
    # def uber_data():
    #     df = filtered_data().copy()
    #     df["tip_pct"] = df.tip / df.total_bill
    #     summary = df.groupby("day").agg(
    #         count=("tip", "size"),
    #         avg_bill=("total_bill", "mean"),
    #         avg_tip=("tip", "mean"),
    #         avg_tip_pct=("tip_pct", "mean"),
    #     ).round(2).reset_index()
    #     return summary
    
    @render_plotly
    def rating_barplot():
        # Group by Vehicle_Type and calculate average Customer_Rating
        avg_rating = filtered_data().groupby("Vehicle_Type")["Customer_Rating"].mean().reset_index()

        # Create bar plot
        fig = px.bar(
            avg_rating,
            x="Vehicle_Type",
            y="Customer_Rating",
            text="Customer_Rating",
            title="Average Customer Rating by Vehicle Type",
            labels={"Customer_Rating": "Avg Customer Rating", "Vehicle_Type": "Vehicle Type"},
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(yaxis_range=[0, 5])  # assuming rating is out of 5
        return fig

    @render_plotly
    def scatterplot():
        return px.scatter(filtered_data(), x="Date", y="Booking_Value", trendline="lowess")

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
