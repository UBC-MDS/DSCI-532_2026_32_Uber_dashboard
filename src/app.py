from shiny import App, render, ui, reactive
import plotly.express as px
from shinywidgets import render_plotly, output_widget
import pandas as pd
import os

# ---------------- DATA ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "data", "raw", "ncr_ride_bookings.csv")

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
            font-size: 0.7em;
            margin-bottom: 0.2rem;
        }
        .shiny-columns {
            gap: 0.5rem;
        }
    """),

    ui.panel_title("Uber Data Visualization Dashboard"),

    ui.layout_sidebar(

        # ---------------- SIDEBAR ----------------
        ui.sidebar(
            ui.input_slider(
                id="slider",
                label="Date range",
                min=uber.Date.min(),
                max=uber.Date.max(),
                value=[uber.Date.min(), uber.Date.max()],
            ),

            ui.input_selectize(
                id="vehicle_type",
                label="Select Vehicle Type",
                choices=["All"] + sorted(uber["Vehicle_Type"].unique().tolist()),
                selected="All",
                multiple=True,
                options={"placeholder": "Choose vehicle type(s)"},
            ),

            ui.input_action_button("action_button", "Reset filter"),
            
        ),

        # ---------------- MAIN CONTENT ----------------
        ui.layout_columns(
            [
                ui.layout_columns(
                    ui.value_box("Total Bookings", ui.output_text("total_bookings")),
                    ui.value_box("Total Revenue", ui.output_text("total_revenue")),
                    ui.value_box("Canceled Bookings", ui.output_text("canceled_bookings")),
                    col_widths=[4, 4, 4],
                )
            ],
            [
                output_widget("pie_chart")
            ],
            col_widths=[6, 6],
        ),

        ui.layout_columns(
            ui.card(
                ui.card_header("Average Driver Rating by Vehicle Type"),
                output_widget("rating_dotplot"),
            
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

    # Single reactive data source (affects whole dashboard)
    @reactive.calc
    def filtered_data():
        df = uber[
            uber.Date.between(
                input.slider()[0],
                input.slider()[1],
                inclusive="both",
            )
        ]

        selected = input.vehicle_type()

        if selected and "All" not in selected:
            df = df[df.Vehicle_Type.isin(selected)]

        return df
    @reactive.calc
    def filtered_data_date_only():
        return uber[
            uber.Date.between(
                input.slider()[0],
                input.slider()[1],
                inclusive="both",
            )
        ]

    # Inside server:
    @reactive.Effect
    def reset_filters():
        # Trigger when button is clicked
        if input.action_button() > 0:  # >0 ensures it triggers only on click
            # Reset slider to full date range
            ui.update_slider("slider", value=[uber.Date.min(), uber.Date.max()])
            
            # Reset vehicle dropdown to "All"
            ui.update_selectize("vehicle_type", selected=["All"])
    # ---------------- VALUE BOXES ----------------
    @render.text
    def total_bookings():
        return f"{filtered_data().shape[0]:,}"

    @render.text
    def total_revenue():
        total = filtered_data().Booking_Value.sum()
        return f"${total:,.0f}"

    @render.text
    def canceled_bookings():
        df = filtered_data()
        count = df[df.Cancelled_Rides_by_Driver == 1].shape[0]
        count += df[df.Cancelled_Rides_by_Customer == 1].shape[0]
        return f"{count:,}"

    # ---------------- DOT PLOT ----------------
    @render_plotly
    def rating_dotplot():
        df = filtered_data()

        avg_rating = (
            df.groupby("Vehicle_Type")["Driver_Ratings"]
            .mean()
            .reset_index()
            .sort_values("Vehicle_Type", ascending=False)
        )

        fig = px.scatter(
            avg_rating,
            x="Driver_Ratings",
            y="Vehicle_Type",
            text="Driver_Ratings",
            labels={
                "Driver_Ratings": "Average Rating",
                "Vehicle_Type": "Vehicle Type",
            },
            size=[14] * len(avg_rating),
        )

        fig.update_traces(
            texttemplate="%{text:.3f}",
            textposition="middle right"
        )

        min_rating = avg_rating["Driver_Ratings"].min()
        max_rating = avg_rating["Driver_Ratings"].max()

        fig.update_layout(
            xaxis_range=[min_rating - 0.02, max_rating + 0.02],
            xaxis_title="Average Rating",
            yaxis_title="Vehicle Type",           
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(showgrid=True,       
                        gridcolor="lightgray",  
                        gridwidth=1,        
                        zeroline=False), 
            yaxis=dict(showgrid=True,
                       gridcolor="lightgray",  
                       gridwidth=1,        
                       zeroline=False),
        )

        return fig

    # ---------------- LINE CHART ----------------
    @render_plotly
    def line_chart():
        df = filtered_data()

        df_agg = df.groupby("Date")["Booking_Value"].sum().reset_index()

        fig = px.line(
            df_agg,
            x="Date",
            y="Booking_Value",
            labels={
                "Booking_Value": "Total Booking Value",
                "Date": "Date",
            },
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Total Booking Value",
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(showgrid=True,
                       gridcolor="lightgray",  
                       gridwidth=1,        
                       zeroline=False), 
            yaxis=dict(showgrid=True,
                       gridcolor="lightgray",  
                       gridwidth=1,        
                       zeroline=False),
        )

        return fig

    # ---------------- PIE CHART ----------------
    @render_plotly
    def pie_chart():
        # Only filtered by date, ignore vehicle type
        df = filtered_data_date_only()

        revenue_by_vehicle_type = (
            df.groupby("Vehicle_Type")["Booking_Value"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            revenue_by_vehicle_type,
            names="Vehicle_Type",
            values="Booking_Value",
            title="Revenue by Vehicle Type (All Vehicles)", 
            color_discrete_sequence=px.colors.qualitative.Set2  # color-blind friendly palette

        )

        return fig


# ---------------- APP ----------------
app = App(app_ui, server)