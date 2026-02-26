from shiny import App, render, ui, reactive
import plotly.express as px
from shinywidgets import render_plotly, output_widget
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "data", "raw", "ncr_ride_bookings.csv")

# Read CSV
uber = pd.read_csv(csv_path)
uber["Date"] = pd.to_datetime(uber["Date"]).dt.date
uber.columns = uber.columns.str.replace(' ', '_')

# ---------------- UI ----------------
app_ui = ui.page_fluid(

    ui.tags.style("""
        .shiny-value-box .card-body {
            padding: 0.5rem;
            font-size: 1em;
            line-height: 1.1;
        }
        .shiny-value-box .card-title {
            font-size: 0.65em;
            margin-bottom: 0.2rem;
        }
        .shiny-columns {
            gap: 0.5rem;
        }
    """),

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

            # Value boxes
            [
                ui.layout_columns(
                    ui.value_box("Total Bookings", ui.output_text("total_bookings")),
                    ui.value_box("Total Revenue", ui.output_text("total_revenue")),
                    ui.value_box("Canceled Bookings", ui.output_text("canceled_bookings")),
                    col_widths=[4, 4, 4],
                )
            ],

            # Pie chart
            [
                output_widget("pie_chart")
            ],

            col_widths=[6, 6],
        ),

        ui.output_ui("vehicle_select_ui"),

        ui.layout_columns(
            ui.card(
                ui.card_header("Average Customer Rating by Vehicle Type"),
                output_widget("rating_barplot"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Total Booking Value Over Time"),
                output_widget("line_chart"),
                full_screen=True,
            ),
            col_widths=[6, 6],
        ),
    ),
)

# ---------------- SERVER ----------------
def server(input, output, session):

    # Date filter
    @reactive.calc
    def filtered_data():
        idx = uber.Date.between(
            left=input.slider()[0],
            right=input.slider()[1],
            inclusive="both",
        )
        return uber[idx]

    # Vehicle filter logic (clean reusable filter)
    def apply_vehicle_filter(df):
        selected = input.vehicle_type()
        if selected and "All" not in selected:
            df = df[df.Vehicle_Type.isin(selected)]
        return df

    # Value boxes
    @render.text
    def total_bookings():
        return f"{apply_vehicle_filter(filtered_data()).shape[0]}"

    @render.text
    def total_revenue():
        bill = apply_vehicle_filter(filtered_data()).Booking_Value.sum()
        return f"${bill:.2f}"

    @render.text
    def canceled_bookings():
        df = apply_vehicle_filter(filtered_data())
        count = df[df.Cancelled_Rides_by_Driver == 1].shape[0]
        count += df[df.Cancelled_Rides_by_Customer == 1].shape[0]
        return f"{count}"

    # Dropdown (Selectize) with "All"
    @output
    @render.ui
    def vehicle_select_ui():
        df = filtered_data()
        vehicle_choices = sorted(df["Vehicle_Type"].unique().tolist())
        vehicle_choices = ["All"] + vehicle_choices

        return ui.input_selectize(
            id="vehicle_type",
            label="Select Vehicle Type",
            choices=vehicle_choices,
            selected="All",
            multiple=True,
            options={"placeholder": "Choose vehicle type(s)"},
        )

    # Bar plot
    @render_plotly
    def rating_barplot():
        df = apply_vehicle_filter(filtered_data())
        avg_rating = df.groupby("Vehicle_Type")[""].mean().reset_index()

        fig = px.bar(
            avg_rating,
            x="Vehicle_Type",
            y="Driver_Ratings",
            text="Driver_Ratings",
            title="Average Driver Rating by Vehicle Type",
            labels={
                "Driver_Rating": "Avg Driver Rating",
                "Vehicle_Type": "Vehicle Type",
            },
        )

        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(yaxis_range=[0, 5])
        return fig

    # Line chart
    @render_plotly
    def line_chart():
        df = apply_vehicle_filter(filtered_data())
        df_agg = df.groupby("Date")["Booking_Value"].sum().reset_index()

        fig = px.line(
            df_agg,
            x="Date",
            y="Booking_Value",
            title="Total Booking Value Over Time",
            labels={
                "Booking_Value": "Total Booking Value",
                "Date": "Date",
            },
        )

        fig.update_layout(xaxis_title="Date", yaxis_title="Total Booking Value")
        return fig

    # Pie chart
    @render_plotly
    def pie_chart():
        df = apply_vehicle_filter(filtered_data())
        revenue_by_vehicle_type = (
            df.groupby("Vehicle_Type")["Booking_Value"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            revenue_by_vehicle_type,
            names="Vehicle_Type",
            values="Booking_Value",
            title="Revenue by Vehicle Type",
        )

        return fig


# Create app
app = App(app_ui, server)