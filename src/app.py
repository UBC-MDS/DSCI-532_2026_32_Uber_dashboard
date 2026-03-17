from shiny import App, render, ui, reactive
import plotly.express as px
from shinywidgets import render_plotly, output_widget
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
import querychat
from chatlas import ChatGithub
import ibis
import plotly.graph_objects as go
from data_wrangling import data_wrangling


# ---------------- DATA ----------------

BASE_DIR = Path(__file__).parent
csv_path = BASE_DIR.parent / "data" / "raw" / "ncr_ride_bookings.csv"
csv_path.parent.mkdir(parents=True, exist_ok=True)
parquet_path = BASE_DIR.parent / "data" / "processed" / "ncr_ride_bookings.parquet"
clean_parquet_path = BASE_DIR.parent / "data" / "processed" / "ncr_ride_bookings_clean.parquet"

# Load raw parquet or CSV
if os.path.exists(parquet_path):
    uber = pd.read_parquet(parquet_path)
else:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    uber = pd.read_csv(csv_path)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    uber.to_parquet(parquet_path, engine="pyarrow", index=False)

# Clean and transform
data_wrangling(uber)

# Save clean parquet AFTER renaming, then load into ibis
if not os.path.exists(clean_parquet_path):
    uber.to_parquet(clean_parquet_path, engine="pyarrow", index=False)
con = ibis.duckdb.connect()
uber_table = con.read_parquet(clean_parquet_path)

# ---------------- QUERYCHAT SETUP ----------------
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
        ui.nav_panel("Home",
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
                    background: var(--bs-body-bg);
                    color: var(--bs-body-color);
                }

                .dashboard-title {
                    font-size: 16px;
                    font-weight: 800;
                }

                .dashboard-header {
                    display: flex;
                    flex-direction: row;
                    padding: 2px 8px;
                }

                .theme-toggle-wrap {
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    margin-left: 25px;
                }

                .theme-label {
                    font-size: 12px;
                    color: var(--bs-body-color);
                }

                #root, .bslib-page-fillable, .container-fluid {
                    height:100vh !important;
                    width:100vw !important;
                    overflow:hidden !important;
                }

                nav[data-tab="AI-Powered"] .sidebar,
                [data-nav-panel="AI-Powered"] .sidebar,
                .page-sidebar[data-current-nav="AI-Powered"] .sidebar {
                    overflow: visible !important;
                    height: 100% !important;
                }

                .chat-container, .chat-messages, .messages-container,
                [class*="chat"], [class*="message"], .querychat-container,
                div[class*="chat"][style*="height"], div[style*="overflow"] {
                    max-height: 95vh !important;
                    overflow-y: auto !important;
                    overflow-x: hidden !important;
                    scrollbar-width: thin !important;
                }

                .nav-panel:not([data-tab="AI-Powered"]) .sidebar,
                .layout-sidebar:not(.page-sidebar) .sidebar {
                    overflow: hidden !important;
                }

                .js-plotly-plot, .plot-container, .svg-container,
                .ai-main-content, .main, .layout-main {
                    height:100% !important;
                    overflow:hidden !important;
                }

                * { box-sizing:border-box; }

                .kpi-card {
                    border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.08);
                    padding:0px;
                    text-align:center;
                    background: var(--bs-body-bg);
                    color: var(--bs-body-color);
                    border: 1px solid var(--bs-border-color);
                }

                .kpi-row {
                    display:flex; justify-content:center; align-items:center;
                    gap:4px; font-size:12px; font-weight:600;
                }

                .kpi-icon { font-size:16px; }
                .kpi-value { font-size:18px; font-weight:700; }

                .card {
                    border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.08);
                    background: var(--bs-body-bg);
                    color: var(--bs-body-color);
                    border: 1px solid var(--bs-border-color);
                    padding:0; margin:0; overflow:hidden;
                }

                .card-header {
                    font-size:12px; font-weight:600; padding:4px 6px;
                }
            """),

            ui.div(
                ui.div("Uber Data Visualization Dashboard", class_="dashboard-title"),
                ui.div(
                    ui.span("Theme", class_="theme-label"),
                    ui.input_dark_mode(id="theme_mode"),
                    class_="theme-toggle-wrap",
                ),
                class_="dashboard-header"
            ),

            # ---------------- SIDEBAR + MAIN ----------------
            ui.layout_sidebar(
                ui.sidebar(
                    ui.div(
                        ui.input_slider(
                            "slider",
                            "Date range",
                            min=uber.Date.min(),
                            max=uber.Date.max(),
                            value=[uber.Date.min(), uber.Date.max()],
                            time_format="%Y-%m-%d",
                            timezone="UTC"
                        ),
                        style="margin-left:10px; margin-right:10px;"
                    ),
                    ui.input_selectize(
                        "vehicle_type",
                        "Vehicle Type",
                        choices=sorted(uber["Vehicle_Type"].unique()),
                        selected=[],
                        multiple=True,
                        options={"placeholder": " select vehicle types..."}
                    ),
                    ui.input_action_button("action_button", "Reset Filters"),
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
                                    ui.div(ui.output_text("vehicle_suffix_bookings"), style="font-size:11px;font-weight:500;text-align:center;min-height:16px;"),
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
                                    ui.div(ui.output_text("vehicle_suffix_revenue"), style="font-size:11px;font-weight:500;text-align:center;min-height:16px;"),
                                    ui.div(ui.output_text("total_revenue"), class_="kpi-value")
                                ]),
                                class_="kpi-card"
                            ),
                            ui.card(
                                ui.div([
                                    ui.div([
                                        ui.HTML('<i class="fa-solid fa-handshake-slash kpi-icon"></i>'),
                                        ui.div("Cancelled Bookings")
                                    ], class_="kpi-row"),
                                    ui.div(ui.output_text("vehicle_suffix_cancelled"), style="font-size:11px;font-weight:500;text-align:center;min-height:16px;"),
                                    ui.div(ui.output_text("canceled_bookings"), class_="kpi-value")
                                ]),
                                class_="kpi-card"
                            ),
                            col_widths=[4, 4, 4],
                            style="gap:4px;margin-bottom:4px;"
                        ),
                        ui.card(
                            ui.card_header(ui.output_text("sunburst_title")),
                            output_widget("sunburst_chart"),
                            style="height:600px;padding:0;margin:0;"
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
                            ui.card_header(ui.output_text("line_chart_title")),
                            output_widget("line_chart"),
                            style="height:205px;margin-bottom:4px;padding:0;"
                        ),
                        ui.card(
                            ui.card_header("Average Driver Rating by Vehicle Type"),
                            output_widget("rating_bar"),
                            style="height:195px;margin-bottom:4px;padding:0;"
                        )
                    ),
                    col_widths=[6, 6],
                    style="gap:4px;"
                )
            )
        ),

        ui.nav_panel("AI-Powered",
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
    title="Uber AI-Powered"
)

# ---------------- SERVER ----------------
def server(input, output, session):
    qc_vals = qc.server()

    # Single filtered_data() using ibis for date + vehicle type filtering
    @reactive.calc
    def filtered_data():
        expr = filtered_by_date(uber_table)

        selected = input.vehicle_type()
        if selected and "All" not in selected:
            expr = expr.filter(expr.Vehicle_Type.isin(selected))

        df = expr.execute()
        df.columns = df.columns.str.replace(" ", "_", regex=False)
        df["Issue_Reason"] = (
            df.get("Reason_for_cancelling_by_Customer", pd.Series(dtype=str))
            .fillna(df.get("Driver_Cancellation_Reason", pd.Series(dtype=str)))
            .fillna(df.get("Incomplete_Rides_Reason", pd.Series(dtype=str)))
            .fillna('')
        )
        return df

    def filtered_by_date(table):
        expr = table.mutate(Date=table.Date.cast('timestamp'))

        date_min, date_max = input.slider()
        date_min = pd.Timestamp(date_min)
        date_max = pd.Timestamp(date_max)

        expr = expr.filter(expr.Date.between(date_min, date_max))
        return expr

    @reactive.calc
    def filtered_data_date_only():
        expr = filtered_by_date(uber_table)
        return expr.execute()

    @reactive.Effect
    def reset_filters():
        if input.action_button() > 0:
            ui.update_slider("slider", value=[uber.Date.min(), uber.Date.max()])
            ui.update_selectize("vehicle_type", selected=[])

    @reactive.calc
    def vehicle_label():
        selected = list(input.vehicle_type())
        if len(selected) == 1:
            return f": {selected[0]}"
        elif len(selected) > 1:
            return f": {', '.join(selected)}"
        return ""

    @render.text
    def line_chart_title():
        return f"Total Booking Value Over Time ( 7-Day Moving Average ){vehicle_label()}"

    @render.text
    def sunburst_title():
        return f"Booking Status Breakdown{vehicle_label()}"

    @render.text
    def vehicle_suffix_bookings():
        selected = list(input.vehicle_type())
        return selected[0] if len(selected) == 1 else ', '.join(selected) if selected else ""

    @render.text
    def vehicle_suffix_revenue():
        selected = list(input.vehicle_type())
        return selected[0] if len(selected) == 1 else ', '.join(selected) if selected else ""

    @render.text
    def vehicle_suffix_cancelled():
        selected = list(input.vehicle_type())
        return selected[0] if len(selected) == 1 else ', '.join(selected) if selected else ""

    def plot_theme():
        mode = input.theme_mode()
        is_dark = mode in ("dark", True)
        if is_dark:
            return {
                "text": "#e9ecef",
                "grid": "#495057",
                "axis": "#ced4da",
            }
        return {
            "text": "#212529",
            "grid": "#dee2e6",
            "axis": "#495057",
        }

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

        booking_status_issue_short = {
            "Incomplete": "InComp",
            "No Driver Found": "NoDrv",
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

        booking_status["Booking_Status_Short"] = booking_status["Booking_Status"].map(
            booking_status_issue_short).fillna(booking_status["Booking_Status"])

        booking_status["Issue_Reason"] = booking_status["Issue_Reason"].fillna("No Issue")
        booking_status["Issue_Reason"] = booking_status["Issue_Reason"].replace("", "Not Given")
        booking_status["Issue_Reason"] = booking_status["Issue_Reason"].map(
            booking_status_issue_short).fillna(booking_status["Issue_Reason"])

        booking_status["Booking_Status_Short"] = booking_status["Booking_Status_Short"].astype(str)
        booking_status["Issue_Reason"] = booking_status["Issue_Reason"].astype(str)

        fig = px.sunburst(
            booking_status,
            path=["Booking_Status_Short", "Issue_Reason"],
            values="counts",
            color_discrete_sequence=px.colors.qualitative.Set1,
        )
        fig.update_traces(
            domain=dict(x=[0.15, 0.99], y=[0.15, 0.98])
        )

        codebook_text = "<br>".join([f"{v} = {k}" for k, v in booking_status_issue_short.items()])

        t = plot_theme()
        fig.update_layout(
            margin=dict(l=1, r=1, t=1, b=8),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            annotations=[
                dict(
                    text=f"<b>Codebook:</b><br>{codebook_text}",
                    xref="paper",
                    yref="paper",
                    x=0,
                    y=0,
                    showarrow=False,
                    align="left",
                    xanchor="left",
                    yanchor="bottom",
                    font=dict(size=10, color=t["text"]),
                )
            ],
        )
        return fig

    @render_plotly
    def rating_bar():
        df = filtered_data_date_only()
        avg = df.groupby("Vehicle_Type")["Driver_Ratings"].mean().reset_index()

        min_val = avg["Driver_Ratings"].min()
        max_val = avg["Driver_Ratings"].max() + 0.005
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

        t = plot_theme()
        fig.update_layout(
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=5, r=5, t=25, b=5),
            xaxis_title="",
            yaxis_title="Average Rating",
            font=dict(color=t["text"]),
            xaxis=dict(
                tickfont=dict(color=t["axis"]),
                title_font=dict(color=t["axis"]),
                gridcolor=t["grid"],
            ),
            yaxis=dict(
                tickfont=dict(color=t["axis"]),
                title_font=dict(color=t["axis"]),
                gridcolor=t["grid"],
                range=y_range
            )
        )

        fig_widget = go.FigureWidget(fig)

        def on_bar_click(trace, points, state):
            if points.point_inds:
                vehicle = trace.x[points.point_inds[0]]
                current = list(input.vehicle_type())
                if len(current) == 1 and vehicle in current:
                    ui.update_selectize("vehicle_type", selected=[])
                else:
                    ui.update_selectize("vehicle_type", selected=[vehicle])

        for trace in fig_widget.data:
            trace.on_click(on_bar_click)

        return fig_widget

    @render_plotly
    def line_chart():
        df = filtered_data()
        df_agg = df.groupby("Date")["Booking_Value"].sum().reset_index()

        window_size = 7
        df_agg['Booking_Value_MA'] = df_agg['Booking_Value'].rolling(
            window=window_size, min_periods=1, center=True
        ).mean()

        fig = px.line(
            df_agg,
            x="Date",
            y="Booking_Value_MA",
            labels={"Booking_Value_MA": "Booking Value"},
        )

        t = plot_theme()
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="",
            yaxis_title="Booking Val.",
            margin=dict(l=5, r=5, t=45, b=15),
            font=dict(color=t["text"]),
            xaxis=dict(
                tickfont=dict(color=t["axis"]),
                title_font=dict(color=t["axis"]),
                gridcolor=t["grid"],
            ),
            yaxis=dict(
                tickfont=dict(color=t["axis"]),
                title_font=dict(color=t["axis"]),
                gridcolor=t["grid"],
            ),
        )
        return fig

    @render_plotly
    def pie_chart():
        df = filtered_data_date_only()
        if df.empty:
            return go.Figure(go.Pie(labels=["No data available"], values=[1]))

        revenue = df.groupby("Vehicle_Type")["Booking_Value"].sum().reset_index()
        total = revenue["Booking_Value"].sum()
        threshold = 0.15

        text_pos = ["outside" if v / total < threshold else "inside" for v in revenue["Booking_Value"]]
        pull_vals = [0.02 if v / total < threshold else 0 for v in revenue["Booking_Value"]]

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

        t = plot_theme()
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=1),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=t["text"]),
        )

        fig_widget = go.FigureWidget(fig)

        def on_pie_click(trace, points, state):
            if points.point_inds:
                vehicle = trace.labels[points.point_inds[0]]
                current = list(input.vehicle_type())
                if len(current) == 1 and vehicle in current:
                    ui.update_selectize("vehicle_type", selected=[])
                else:
                    ui.update_selectize("vehicle_type", selected=[vehicle])

        fig_widget.data[0].on_click(on_pie_click)
        return fig_widget

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
        t = plot_theme()
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=t["text"]),
            xaxis=dict(
                tickfont=dict(color=t["axis"]),
                title_font=dict(color=t["axis"]),
                gridcolor=t["grid"],
            ),
            yaxis=dict(
                tickfont=dict(color=t["axis"]),
                title_font=dict(color=t["axis"]),
                gridcolor=t["grid"],
            ),
        )
        return fig

    @render_plotly
    def qc_line_chart():
        df = qc_vals.df()
        if df.empty:
            return px.line(title="No data available")

        df_agg = df.groupby("Date")["Booking_Value"].sum().reset_index()

        fig = px.line(df_agg, x="Date", y="Booking_Value")
        t = plot_theme()
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=1, r=1, t=1, b=1),
            font=dict(color=t["text"]),
            xaxis=dict(
                tickfont=dict(color=t["axis"]),
                title_font=dict(color=t["axis"]),
                gridcolor=t["grid"],
            ),
            yaxis=dict(
                tickfont=dict(color=t["axis"]),
                title_font=dict(color=t["axis"]),
                gridcolor=t["grid"],
            ),
        )
        return fig

    @render.download(filename="uber_filtered_data.csv")
    def download_data():
        df = qc_vals.df()
        if df.empty:
            yield pd.DataFrame().to_csv(index=False)
        else:
            yield df.to_csv(index=False)

    @render.text
    def title():
        return qc_vals.title() or "Uber Rides dataset"


# ---------------- APP ----------------
app = App(app_ui, server)