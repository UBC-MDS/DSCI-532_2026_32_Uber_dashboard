from shiny import App, render, ui, reactive
import plotly.express as px
from shinywidgets import render_plotly, output_widget
import pandas as pd
import os

# ---------------- DATA ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "data", "raw", "ncr_ride_bookings.csv")

uber = pd.read_csv(csv_path)
uber.columns = uber.columns.str.replace(' ', '_')
uber["Date"] = pd.to_datetime(uber["Date"]).dt.date
uber['Issue_Reason'] = (uber['Reason_for_cancelling_by_Customer']
                        .fillna(uber['Driver_Cancellation_Reason'])
                        .fillna(uber['Incomplete_Rides_Reason'])
                        .fillna('')
                        )

# ---------------- UI ----------------
app_ui = ui.page_fillable(                              
    ui.tags.link(
        rel="stylesheet",
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ),

    # ---------- Styling ----------
    ui.tags.style("""
        html, body { height: 100%; overflow: hidden; }   /* no scroll */

        .shiny-value-box {
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.08);
            transition: transform 0.2s ease;
        }
        .shiny-value-box:hover { transform: translateY(-4px); }

        .shiny-value-box .card-body {
            font-size: 32px;
            font-weight: 700;
            text-align: center;
        }
        .shiny-value-box .card-title {
            font-size: 14px;
            font-weight: 500;
            opacity: 0.85;
            text-align: center;
        }
        .gradient-box {
            background: linear-gradient(135deg, #4F46E5, #3B82F6);
            color: white;
        }
        .card-header { font-size: 12px; padding: 6px 10px; }
        .card { margin-bottom: 0 !important; }
    """),

    # ---------- Title ----------
    ui.div(
        "Uber Data Visualization Dashboard",
        style="""
            font-size: 20px;
            font-weight: 800;
            color: black;
            text-align: center;
            padding: 6px 0;
            text-shadow: 1px 2px 6px rgba(0,0,0,0.15);
        """
    ),

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
            width=220,                           
        ),

        # ---------------- MAIN CONTENT ----------------
        ui.div(
            ui.layout_columns(
                # ----- Row 1: Value Boxes + Pie -----
                ui.layout_columns(
                    ui.value_box(
                        "Total Bookings",
                        ui.output_text("total_bookings"),
                        showcase=ui.HTML('<i class="fa-solid fa-car fa-lg"></i>'),
                        theme="total-bookings-box",
                        height="260px",
                    ),
                    ui.value_box(
                        "Total Revenue",
                        ui.output_text("total_revenue"),
                        showcase=ui.HTML('<i class="fa-solid fa-dollar-sign fa-lg"></i>'),
                        theme="gradient-box",
                        height="260px",
                    ),
                    ui.value_box(
                        "Canceled Bookings",
                        ui.output_text("canceled_bookings"),
                        showcase=ui.HTML('<i class="fa-solid fa-handshake-slash fa-lg"></i>'),
                        theme="gradient-box",
                        height="260px",
                    ),
                    col_widths=[3, 5, 4],
                    style="height: 260px; gap:4px;",
                    
                ),
                ui.div(
                    output_widget("pie_chart"),
                    style="height: 260px;",
                ),
                col_widths=[6, 6],
                style="height: 260px; gap:4px;",
            ),
            style="flex: 0 0 45%; min-height: 0;",
        ),

        # ----- Row 2: Three Charts -----
        ui.div(
            ui.layout_columns(
                ui.card(
                    ui.card_header("Avg Driver Rating by Vehicle Type"),
                    output_widget("rating_dotplot"),
                    fill=True,
                    full_screen=False,
                ),
                ui.card(
                    ui.card_header("Total Booking Value Over Time"),
                    output_widget("line_chart"),
                    fill=True,
                ),
                ui.card(
                    ui.card_header("Booking Status Breakdown"),
                    output_widget("sunburst_chart"),
                    fill=True,
                ),
                col_widths=[4, 4, 4],
                fill=True,
                style="height: 100%; gap:4px;",
            ),
            style="flex: 0 0 55%; min-height: 0;",
        ),

        fillable=True,
        style="display:flex; flex-direction:column; gap:6px;",
    ),
)

# ---------------- SERVER ----------------
def server(input, output, session):

    @reactive.calc
    def filtered_data():
        df = uber[
            uber.Date.between(input.slider()[0], input.slider()[1], inclusive="both")
        ]
        selected = input.vehicle_type()
        if selected and "All" not in selected:
            df = df[df.Vehicle_Type.isin(selected)]
        return df

    @reactive.calc
    def filtered_data_date_only():
        return uber[
            uber.Date.between(input.slider()[0], input.slider()[1], inclusive="both")
        ]

    @reactive.Effect
    def reset_filters():
        if input.action_button() > 0:
            ui.update_slider("slider", value=[uber.Date.min(), uber.Date.max()])
            ui.update_selectize("vehicle_type", selected=["All"])

    # ---------------- VALUE BOXES ----------------
    @render.text
    def total_bookings():
        return f"{filtered_data().shape[0]:,}"

    @render.text
    def total_revenue():
        return f"{filtered_data().Booking_Value.sum():,.2f}"

    @render.text
    def canceled_bookings():
        df = filtered_data()
        count = (
            df[df.Cancelled_Rides_by_Driver == 1].shape[0]
            + df[df.Cancelled_Rides_by_Customer == 1].shape[0]
        )
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
            avg_rating, x="Driver_Ratings", y="Vehicle_Type",
            text="Driver_Ratings",
            labels={"Driver_Ratings": "Average Rating", "Vehicle_Type": "Vehicle Type"},
        )
        fig.update_traces(texttemplate="%{text:.3f}", textposition="middle right")
        min_r = avg_rating["Driver_Ratings"].min()
        max_r = avg_rating["Driver_Ratings"].max()
        fig.update_layout(
            xaxis_range=[min_r - 0.02, max_r + 0.02],
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10),        # ← tight margins
            xaxis=dict(showgrid=True, gridcolor="lightgray", zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="lightgray", zeroline=False),
        )
        return fig

    # ---------------- LINE CHART ----------------
    @render_plotly
    def line_chart():
        df = filtered_data()
        df_agg = df.groupby("Date")["Booking_Value"].sum().reset_index()
        fig = px.line(
            df_agg, x="Date", y="Booking_Value",
            labels={"Booking_Value": "Total Booking Value", "Date": "Date"},
        )
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="lightgray", zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="lightgray", zeroline=False),
        )
        return fig

    # ---------------- PIE CHART ----------------
    @render_plotly
    def pie_chart():
        df = filtered_data_date_only()
        revenue_by_vehicle_type = (
            df.groupby("Vehicle_Type")["Booking_Value"].sum().reset_index()
        )
        fig = px.pie(
            revenue_by_vehicle_type, names="Vehicle_Type", values="Booking_Value",
            color_discrete_sequence=px.colors.qualitative.Set2,
            title="Revenue Distribution by Vehicle Type" 
        )
        fig.update_traces(textinfo="percent+label", domain=dict(x=[0, 0.6]))
        fig.update_layout(
            margin=dict(l=10, r=10, t=40, b=10),  
            height=260,
            title=dict(
                x=0.5,               # center title
                xanchor="center",
                font=dict(size=14, family="Arial", color="black")
            ),
            legend=dict(
                orientation="v",
                x=0.62,
                y=0.5,
                xanchor="left",
                yanchor="middle",
            ),
        )
        return fig

    # ---------------- SUNBURST CHART ----------------
    @render_plotly
    def sunburst_chart():
        booking_status = (
            filtered_data()
            .groupby(['Booking_Status', 'Issue_Reason'])
            .agg(counts=('Issue_Reason', 'size'))
            .reset_index()
        )
        fig = px.sunburst(
            booking_status, path=["Booking_Status", "Issue_Reason"],
            values="counts",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_traces(textinfo="label+percent entry")
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        return fig


# ---------------- APP ----------------
app = App(app_ui, server)