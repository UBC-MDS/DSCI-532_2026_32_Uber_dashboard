from shiny import App, render, ui, reactive
import plotly.express as px
from shinywidgets import render_plotly, output_widget
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
import querychat
from chatlas import ChatGithub
import plotly.graph_objects as go


# ---------------- DATA ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "data", "raw", "ncr_ride_bookings.csv")

uber = pd.read_csv(csv_path)
uber.columns = uber.columns.str.replace(' ', '_')
uber["Date"] = pd.to_datetime(uber["Date"]).dt.date

uber['Issue_Reason'] = (
    uber['Reason_for_cancelling_by_Customer']
    .fillna(uber['Driver_Cancellation_Reason'])
    .fillna(uber['Incomplete_Rides_Reason'])
    .fillna('')
)

# ---------------- querychat setup ----------------
# Load .env from the same directory
load_dotenv(Path(__file__).parent / ".env")

qc = querychat.QueryChat(
    uber,
    "uber",
    client=ChatGithub(model="openai/gpt-4o-mini"))

# ---------------- HELPER ----------------
def shiny_human_format(num):
    num = float(num)
    if abs(num) >= 1_000_000_000:
        return f"{num/1_000_000_000:.0f}B"
    elif abs(num) >= 1_000_000:
        return f"{num/1_000_000:.0f}M"
    elif abs(num) >= 1_000:
        return f"{num/1_000:.0f}K"
    else:
        return f"{num:.0f}"

# ---------------- UI ----------------
app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav_panel("Original Dashboard",
            ui.tags.link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
            ),

            ui.tags.style("""
                html, body {
                    height:100vh;
                    width:100vw;
                    margin:0;
                    padding:0;
                    overflow:hidden !important;
                    background:#f8f9fb;
                }

                #root, .bslib-page-fillable, .container-fluid {
                    height:100vh !important;
                    width:100vw !important;
                    overflow:hidden !important;
                }

                nav[data-tab="AI-Powered Dashboard"] .sidebar,
                [data-nav-panel="AI-Powered Dashboard"] .sidebar,
                .page-sidebar[data-current-nav="AI-Powered Dashboard"] .sidebar {
                    overflow: visible !important;
                    height: 100% !important;
                }

                /* Querychat chat container selectors  */
                .chat-container, .chat-messages, .messages-container,
                [class*="chat"], [class*="message"], .querychat-container,
                div[class*="chat"][style*="height"], div[style*="overflow"] {
                    max-height: 95vh !important;
                    overflow-y: auto !important;
                    overflow-x: hidden !important;
                    scrollbar-width: thin !important;
                }

                /* Original dashboard sidebar */
                .nav-panel:not([data-tab="AI-Powered Dashboard"]) .sidebar,
                .layout-sidebar:not(.page-sidebar) .sidebar {
                    overflow: hidden !important;
                }

                /* Charts and main content */
                .js-plotly-plot, .plot-container, .svg-container,
                .ai-main-content, .main, .layout-main {
                    height:100% !important;
                    overflow:hidden !important;
                }

                * { box-sizing:border-box; }

                .kpi-card {
                    border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.08);
                    padding:0px; text-align:center; background:white;
                }

                .kpi-row {
                    display:flex; justify-content:center; align-items:center;
                    gap:4px; font-size:12px; font-weight:600;
                }

                .kpi-icon { font-size:16px; }
                .kpi-value { font-size:18px; font-weight:700; }

                .card {
                    border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.08);
                    background:white; padding:0; margin:0; overflow:hidden;
                }

                .card-header {
                    font-size:12px; font-weight:600; padding:4px 6px;
                }
            """),

            ui.div(
                "Uber Data Visualization Dashboard",
                style="font-size:16px;font-weight:800;text-align:center;padding:2px 0;"
            ),

            # ---------------- SIDEBAR + MAIN ----------------
            ui.layout_sidebar(
                ui.sidebar(
                    # --- Wrap slider in a div with margin-bottom to prevent scrolling ---
                    ui.div(
                        ui.input_slider(
                            "slider",
                            "Date range",
                            min=uber.Date.min(),
                            max=uber.Date.max(),
                            value=[uber.Date.min(), uber.Date.max()],
                        ),
                        style="margin-left:10px; margin-right:10px;"  # extra space for min/max labels
                    ),

                    ui.input_selectize(
                        "vehicle_type",
                        "Vehicle Type",
                        choices=["All"] + sorted(uber["Vehicle_Type"].unique()),
                        selected="All",
                        multiple=True
                    ),
                    ui.input_action_button("action_button","Reset Filters"),
                    width=230
                ),
                ui.layout_columns(
                    # ---------------- LEFT COLUMN ----------------
                    ui.div(
                        ui.layout_columns(
                            ui.card(
                                ui.div([
                                    ui.div([
                                        ui.HTML('<i class="fa-solid fa-car kpi-icon"></i>'),
                                        ui.div("Total Bookings")
                                    ], class_="kpi-row"),
                                    ui.div(ui.output_text("total_bookings"), class_="kpi-value")
                                ]),
                                class_="kpi-card"
                            ),
                            ui.card(
                                ui.div([
                                    ui.div([
                                        ui.HTML('<i class="fa-solid fa-dollar-sign kpi-icon"></i>'),
                                        ui.div("Total Revenue")
                                    ], class_="kpi-row"),
                                    ui.div(ui.output_text("total_revenue"), class_="kpi-value")
                                ]),
                                class_="kpi-card"
                            ),
                            ui.card(
                                ui.div([
                                    ui.div([
                                        ui.HTML('<i class="fa-solid fa-handshake-slash kpi-icon"></i>'),
                                        ui.div("Canceled Bookings")
                                    ], class_="kpi-row"),
                                    ui.div(ui.output_text("canceled_bookings"), class_="kpi-value")
                                ]),
                                class_="kpi-card"
                            ),
                            col_widths=[4,4,4],
                            style="gap:4px;margin-bottom:4px;"
                        ),
                        ui.card(
                            ui.card_header("Booking Status Breakdown"),
                            output_widget("sunburst_chart"),
                            style="height:597px;padding:0;margin:0;"
                        )
                    ),
                    # ---------------- RIGHT COLUMN ----------------
                    ui.div(
                        ui.card(
                            ui.card_header("Revenue Distribution by Vehicle Type"),
                            output_widget("pie_chart"),
                            style="height:275px;margin-bottom:4px;padding:0;"
                        ),
                        ui.card(
                            ui.card_header("Total Booking Value Over Time"),
                            output_widget("line_chart"),
                            style="height:205px;margin-bottom:4px;padding:0;"
                        ),
                        ui.card(
                            ui.card_header("Avg Driver Rating by Vehicle Type"),
                            output_widget("rating_bar"),
                            style="height:195px;margin-bottom:4px;padding:0;"
                        )
                    ),
                    col_widths=[6,6],
                    style="gap:4px;"
                )   
            )
        ),

        ui.nav_panel("AI-Powered Dashboard",
            ui.page_sidebar(
                qc.sidebar(),
                ui.div(
                    ui.card(
                        ui.card_header([
                            "Filtered Data",
                            ui.download_button(
                                "download_data", 
                                "📥 Download CSV", 
                                class_="btn btn-outline-primary btn-sm float-end"
                            )
                        ]),
                        ui.output_data_frame("qc_data_table"),
                        style="margin-bottom:8px;height:380px;"
                    ),
                    ui.layout_columns(
                        ui.card(
                            ui.card_header("Revenue Distribution by Vehicle Type"),
                            output_widget("qc_pie_chart"),
                            style="height:280px;padding:0;"
                        ),
                        ui.card(
                            ui.card_header("Bookings Over Time"),
                            output_widget("qc_line_chart"),
                            style="height:280px;padding:0;"
                        ),
                        col_widths=[6, 6],
                        style="gap:8px;"
                    ),
                    class_="ai-main-content" 
                ),
                fillable=True
            )
        )
    ),
    title="Uber AI-Powered Dashboard"
)

# ---------------- SERVER ----------------
def server(input, output, session):
    qc_vals = qc.server()

    @reactive.calc
    def filtered_data():
        df = uber[uber.Date.between(input.slider()[0], input.slider()[1], inclusive="both")]
        selected = input.vehicle_type()
        if selected and "All" not in selected:
            df = df[df.Vehicle_Type.isin(selected)]
        return df

    @reactive.calc
    def filtered_data_date_only():
        return uber[uber.Date.between(input.slider()[0], input.slider()[1], inclusive="both")]

    @reactive.Effect
    def reset_filters():
        if input.action_button() > 0:
            ui.update_slider("slider", value=[uber.Date.min(), uber.Date.max()])
            ui.update_selectize("vehicle_type", selected=["All"])

    # ---------------- KPI VALUES ----------------
    @render.text
    def total_bookings():
        return shiny_human_format(filtered_data().shape[0])

    @render.text
    def total_revenue():
        return shiny_human_format(filtered_data().Booking_Value.sum())

    @render.text
    def canceled_bookings():
        df = filtered_data()
        count = df[df.Cancelled_Rides_by_Driver == 1].shape[0] + df[df.Cancelled_Rides_by_Customer == 1].shape[0]
        return shiny_human_format(count)
    
    # ---------------- CHARTS ----------------
    @render_plotly
    def sunburst_chart():
        
        booking_status = (
            filtered_data()
            .groupby(["Booking_Status", "Issue_Reason"])
            .size()
            .reset_index(name="counts")
        )
            
        # Short labels mapping
        booking_status_issue_short = {
            "No Show": "NoShow",
            "Incomplete": "InComp",
            "No Driver Found": "NoDrv",
            "Other Issue": "OtherIssue",
            "AC is not working": "ACIssue",
            "Wrong Address": "WrongAddr",
            "Change of plans": "ChgPlans",
            "Vehicle Breakdown": "VehBreak",
            "Customer Demand": "CustDemand",
            "Passenger no show": "PassNoShow",
            "Cancelled by Driver": "Drv Canc",
            "Customer related issue": "CustIssue",
            "Driver asked to cancel": "DrvCanc",
            "Cancelled by Customer": "Cust Canc",
            "The customer was occupied/waiting": "CustBusy",
            "Personal & Car related issues": "PersCar",
            "Never on unmanned people in time": "NoShowTime",
            "The customer was coughing/sick": "CustSick",
            "More than permitted people in there": "OverCap",
            "Driver is not moving towards pickup location": "DrvNotMove", 
        }
        
        # Map short labels, fill unmapped with original
        booking_status["Booking_Status_Short"] = booking_status["Booking_Status"].map(
            booking_status_issue_short).fillna(booking_status["Booking_Status"])
    
        # Replace empty or NaN Issue_Reason with placeholder
        booking_status["Issue_Reason"] = booking_status["Issue_Reason"].fillna("No Issue")
        booking_status["Issue_Reason"] = booking_status["Issue_Reason"].replace("", "Not Given")
        
        booking_status["Issue_Reason"] = booking_status["Issue_Reason"].map(
            booking_status_issue_short).fillna(booking_status["Issue_Reason"])


        # Ensure both columns are strings
        booking_status["Booking_Status_Short"] = booking_status["Booking_Status_Short"].astype(str)
        booking_status["Issue_Reason"] = booking_status["Issue_Reason"].astype(str)


        # booking_status["Booking_Status_Short"] = booking_status["Booking_Status"].map(booking_status_short)
        # Create sunburst
        fig = px.sunburst(
            booking_status,
            path=["Booking_Status_Short", "Issue_Reason"],
            values="counts",
            color_discrete_sequence=px.colors.qualitative.Set1,
        )
        fig.update_traces(
          domain=dict(x=[0.15, 0.99], y=[0.15, 0.98])   # push chart to the right
            )

        # Codebook
        codebook_text = "<br>".join([f"{v} = {k}" for k, v in booking_status_issue_short.items()])

        fig.update_layout(
            margin=dict(l=1, r=1, t=1, b=8),
            plot_bgcolor="white",
            paper_bgcolor="white",
            annotations=[
                dict(
                    text=f"<b>Legend / Codebook:</b><br>{codebook_text}",
                    xref="paper",
                    yref="paper",
                    x=0,
                    y=0,
                    showarrow=False,
                    align="left",
                    xanchor="left",
                    yanchor="bottom",
                    font=dict(size=10),
                )
            ],
        )

        return fig


    @render_plotly
    def rating_bar():
        df = filtered_data()
        avg = df.groupby("Vehicle_Type")["Driver_Ratings"].mean().reset_index()

        min_val = avg["Driver_Ratings"].min()
        max_val = avg["Driver_Ratings"].max()
        padding = (max_val - min_val) * 0.05
        y_range = [min_val - padding, max_val + padding]

        fig = px.bar(
            avg,
            x="Vehicle_Type",
            y="Driver_Ratings",
            text="Driver_Ratings",
            color="Vehicle_Type",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_traces(texttemplate="%{text:.4f}", textposition="outside")

        fig.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=1,r=1,t=1,b=1),
            xaxis_title="",
            yaxis_title="Avg Rating",
            yaxis=dict(range=y_range)
        )

        return fig

    @render_plotly
    def line_chart():
        df = filtered_data()
        df_agg = df.groupby("Date")["Booking_Value"].sum().reset_index()

        fig = px.line(df_agg, x="Date", y="Booking_Value")

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=5,r=5,t=5,b=1)
        )

        return fig

    @render_plotly
    def pie_chart():
        df = filtered_data_date_only()
        if df.empty:
            # handle empty data
            return go.Figure(go.Pie(labels=["No data available"], values=[1]))

        revenue = df.groupby("Vehicle_Type")["Booking_Value"].sum().reset_index()
        total = revenue["Booking_Value"].sum()
        threshold = 0.15  # slices <5% of total are considered small

        # per-slice text positions: small slices outside, others inside
        text_pos = ["outside" if v / total < threshold else "inside" for v in revenue["Booking_Value"]]
        pull_vals = [0.02 if v / total < threshold else 0 for v in revenue["Booking_Value"]]  # slight pull for clarity

        fig = go.Figure(
            go.Pie(
                labels=revenue["Vehicle_Type"],
                values=revenue["Booking_Value"],
                textinfo="percent+label",
                textposition=text_pos,
                pull=pull_vals,
                marker=dict(colors=px.colors.qualitative.Set2)
            )
        )

        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=1),
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        return fig
    
    @render.data_frame
    def qc_data_table():
        return qc_vals.df()

    @render_plotly
    def qc_pie_chart():
        df = qc_vals.df()
        if df.empty:
            return px.pie(title="No data available")
        
        revenue = df.groupby("Vehicle_Type")["Booking_Value"].sum().reset_index()
        
        fig = px.pie(
            revenue,
            names="Vehicle_Type",
            values="Booking_Value",
            color="Vehicle_Type",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig.update_traces(textinfo="percent+label", textposition="inside")
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0,r=0,t=0,b=0),
            plot_bgcolor="white",
            paper_bgcolor="white"
        )
        return fig
    
    @render_plotly
    def qc_line_chart():
        df = qc_vals.df()
        if df.empty:
            return px.line(title="No data available")
        
        df_agg = df.groupby("Date")["Booking_Value"].sum().reset_index()
        
        fig = px.line(df_agg, x="Date", y="Booking_Value")
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=1,r=1,t=1,b=1)
        )
        return fig
    
    @render.download(filename="uber_filtered_data.csv")
    def download_data():
        df = qc_vals.df()
        if df.empty:
            yield pd.DataFrame().to_csv(index=False)
        else:
            yield df.to_csv(index=False)

    # ---------------- QUERYCHAT ----------------
    # Adapted from https://github.com/UBC-MDS/DSCI_532_vis-2_book/blob/main/code/lecture05/app-07-querychat.py
    @render.text
    def title():
        return qc_vals.title() or "Uber Rides dataset"


# ---------------- APP ----------------
app = App(app_ui, server)
