import reflex as rx
from app.states.neurowatch_state import NeuroWatchState
from app.states.auth_state import AuthState
from app.components.sidebar import sidebar
from app.components.dashboard_cards import risk_gauge, domain_card
from app.components.charts import trend_chart
from app.components.session_table import session_table
from app.pages.session_detail import session_detail_page
from app.components.new_session_modal import new_session_modal
from app.pages.assessment import assessment_page
from app.pages.activity import activity_page
from app.pages.assistant import assistant_page
from app.pages.profile import profile_page
from app.pages.auth import login_page, signup_page


def layout(content: rx.Component, title: str) -> rx.Component:
    return rx.el.main(
        sidebar(),
        rx.el.div(
            rx.el.header(
                rx.el.h1(title, class_name="text-2xl font-bold text-gray-900"),
                rx.el.div(
                    rx.el.button(
                        rx.icon("plus", class_name="h-4 w-4 mr-2"),
                        "New Session",
                        on_click=rx.redirect("/assessment"),
                        class_name="bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded-xl flex items-center text-sm font-semibold transition-all shadow-sm shadow-teal-100",
                    ),
                    class_name="flex items-center gap-4",
                ),
                class_name="flex justify-between items-center mb-8 sticky top-0 bg-slate-50/80 backdrop-blur-md py-4 z-10",
            ),
            content,
            new_session_modal(),
            class_name="flex-1 ml-64 p-8 bg-slate-50 min-h-screen",
        ),
        class_name="font-['Inter'] flex",
    )


def index() -> rx.Component:
    content = rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("flame", class_name="h-4 w-4 text-orange-500"),
                rx.el.span(
                    f"{NeuroWatchState.current_streak}-Day Streak! Next assessment due: {NeuroWatchState.next_assessment_due}.",
                    class_name="text-sm font-semibold text-teal-800",
                ),
                class_name="flex items-center gap-2 bg-teal-50 px-4 py-2 rounded-xl mb-6 w-full border border-teal-100 shadow-sm",
            ),
            rx.el.div(
                risk_gauge(), trend_chart(), class_name="grid grid-cols-3 gap-6 mb-6"
            ),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.foreach(NeuroWatchState.domain_scores_list, domain_card),
            class_name="grid grid-cols-4 gap-6 mb-6",
        ),
        session_table(),
        class_name="flex flex-col",
    )
    return layout(content, "Dashboard Overview")


def sessions_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search by date or ID...",
                            on_change=NeuroWatchState.set_search_query.debounce(500),
                            class_name="pl-10 pr-4 py-2 w-64 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all",
                        ),
                        class_name="relative",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("All Risk Levels", value="All"),
                            rx.el.option("Low", value="Low"),
                            rx.el.option("Moderate", value="Moderate"),
                            rx.el.option("Elevated", value="Elevated"),
                            rx.el.option("High", value="High"),
                            on_change=NeuroWatchState.set_filter_risk_level,
                            class_name="appearance-none bg-white border border-gray-200 rounded-xl px-4 py-2 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                    class_name="flex gap-4 items-center",
                ),
                rx.el.button(
                    rx.icon("download", class_name="h-4 w-4 mr-2"),
                    "Export CSV",
                    on_click=NeuroWatchState.export_sessions_csv,
                    class_name="flex items-center px-4 py-2 bg-white border border-gray-200 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-colors shadow-sm",
                ),
                class_name="flex justify-between items-center mb-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Session #",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "Date",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "Risk Level",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "Score",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "Flagged Domain",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.th("", class_name="py-3 px-4"),
                        ),
                        class_name="border-b border-gray-100",
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            NeuroWatchState.filtered_sessions,
                            lambda row: rx.el.tr(
                                rx.el.td(
                                    f"#{row['num']}",
                                    class_name="py-4 px-4 text-sm font-medium text-gray-900",
                                ),
                                rx.el.td(
                                    row["date"],
                                    class_name="py-4 px-4 text-sm text-gray-600",
                                ),
                                rx.el.td(
                                    rx.el.span(
                                        row["level"],
                                        class_name=rx.match(
                                            row["level"],
                                            (
                                                "Low",
                                                "px-2 py-1 rounded-full text-xs font-semibold bg-green-50 text-green-600",
                                            ),
                                            (
                                                "Moderate",
                                                "px-2 py-1 rounded-full text-xs font-semibold bg-yellow-50 text-yellow-600",
                                            ),
                                            (
                                                "Elevated",
                                                "px-2 py-1 rounded-full text-xs font-semibold bg-orange-50 text-orange-600",
                                            ),
                                            "px-2 py-1 rounded-full text-xs font-semibold bg-red-50 text-red-600",
                                        ),
                                    ),
                                    class_name="py-4 px-4",
                                ),
                                rx.el.td(
                                    row["score"].to_string(),
                                    class_name="py-4 px-4 text-sm font-bold text-gray-900",
                                ),
                                rx.el.td(
                                    row["signal"],
                                    class_name="py-4 px-4 text-sm text-gray-600",
                                ),
                                rx.el.td(
                                    rx.el.button(
                                        rx.icon("eye", class_name="h-4 w-4 mr-2"),
                                        "View",
                                        on_click=lambda: NeuroWatchState.view_session(
                                            row["id"].to_string()
                                        ),
                                        class_name="flex items-center text-xs font-bold text-teal-600 hover:text-teal-700",
                                    ),
                                    class_name="py-4 px-4 text-right",
                                ),
                                class_name="border-b border-gray-50 hover:bg-slate-50 transition-colors",
                            ),
                        )
                    ),
                    class_name="w-full table-auto",
                ),
                class_name="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden",
            ),
            class_name="flex flex-col",
        ),
        "Clinical Data Management",
    )


def trends_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Domain Comparison", class_name="text-lg font-semibold"),
                    rx.el.p(
                        "Multi-domain performance tracking",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="mb-6",
                ),
                rx.recharts.line_chart(
                    rx.recharts.cartesian_grid(
                        stroke_dasharray="3 3", vertical=False, stroke="#f1f5f9"
                    ),
                    rx.recharts.graphing_tooltip(
                        content_style={
                            "backgroundColor": "white",
                            "borderRadius": "12px",
                            "border": "1px solid #e2e8f0",
                        }
                    ),
                    rx.recharts.x_axis(
                        data_key="date",
                        axis_line=False,
                        tick_line=False,
                        custom_attrs={"fontSize": "12px", "fill": "#94a3b8"},
                    ),
                    rx.recharts.y_axis(
                        domain=[0, 100],
                        axis_line=False,
                        tick_line=False,
                        custom_attrs={"fontSize": "12px", "fill": "#94a3b8"},
                    ),
                    rx.recharts.line(
                        data_key="typing",
                        stroke="#3b82f6",
                        stroke_width=2,
                        dot=False,
                        name="Typing",
                    ),
                    rx.recharts.line(
                        data_key="reaction",
                        stroke="#a855f7",
                        stroke_width=2,
                        dot=False,
                        name="Reaction",
                    ),
                    rx.recharts.line(
                        data_key="memory",
                        stroke="#f97316",
                        stroke_width=2,
                        dot=False,
                        name="Memory",
                    ),
                    rx.recharts.line(
                        data_key="voice",
                        stroke="#0d9488",
                        stroke_width=2,
                        dot=False,
                        name="Voice",
                    ),
                    data=NeuroWatchState.trend_chart_data,
                    width="100%",
                    height=400,
                ),
                class_name="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Strongest Signal Indicator",
                        class_name="text-lg font-semibold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        NeuroWatchState.strongest_signal_insight,
                        class_name="text-gray-600",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.icon("brain", class_name="h-8 w-8 text-orange-500"),
                    class_name="p-4 bg-orange-50 rounded-2xl",
                ),
                class_name="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm flex items-center justify-between",
            ),
            class_name="flex flex-col",
        ),
        "Advanced Trends & Analytics",
    )


def alerts_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Caregiver Notifications Active",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.button(
                        rx.el.div(
                            class_name="size-4 bg-white rounded-full transition-transform translate-x-4"
                        ),
                        class_name="w-10 h-6 bg-teal-600 rounded-full p-1 flex items-center ml-4 cursor-pointer",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.icon("phone", class_name="h-4 w-4 text-teal-600 mr-2"),
                    rx.el.span(
                        NeuroWatchState.user_profile["caregiver_contact"],
                        class_name="text-sm text-teal-700 font-medium",
                    ),
                    class_name="px-4 py-2 bg-teal-50 rounded-full flex items-center",
                ),
                class_name="flex justify-between items-center mb-8 bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Date",
                                class_name="text-left p-4 text-xs font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "Severity",
                                class_name="text-left p-4 text-xs font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "Message",
                                class_name="text-left p-4 text-xs font-semibold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="text-left p-4 text-xs font-semibold text-gray-500 uppercase",
                            ),
                        ),
                        class_name="border-b border-gray-100",
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            NeuroWatchState.alert_history,
                            lambda alert: rx.el.tr(
                                rx.el.td(
                                    alert["date"],
                                    class_name="p-4 text-sm text-gray-600",
                                ),
                                rx.el.td(
                                    rx.el.span(
                                        alert["level"],
                                        class_name=rx.match(
                                            alert["level"],
                                            (
                                                "Elevated",
                                                "px-2 py-1 rounded-full text-xs font-semibold bg-orange-50 text-orange-600",
                                            ),
                                            "px-2 py-1 rounded-full text-xs font-semibold bg-red-50 text-red-600",
                                        ),
                                    ),
                                    class_name="p-4",
                                ),
                                rx.el.td(
                                    alert["message"],
                                    class_name="p-4 text-sm text-gray-600",
                                ),
                                rx.el.td(
                                    rx.el.span(
                                        alert["status"],
                                        class_name=rx.cond(
                                            alert["status"] == "Sent",
                                            "text-blue-600",
                                            "text-gray-400",
                                        )
                                        + " text-xs font-medium",
                                    ),
                                    class_name="p-4",
                                ),
                                class_name="border-b border-gray-50",
                            ),
                        )
                    ),
                    class_name="w-full table-auto",
                ),
                class_name="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden",
            ),
            class_name="flex flex-col",
        ),
        "Caregiver Alerts & Notifications",
    )


def settings_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h3("User Profile", class_name="text-lg font-semibold mb-6"),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Full Name",
                            class_name="text-xs text-gray-500 font-bold mb-1 block",
                        ),
                        rx.el.input(
                            default_value=NeuroWatchState.user_profile["name"],
                            class_name="w-full p-2 border border-gray-200 rounded-lg text-sm",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Age",
                            class_name="text-xs text-gray-500 font-bold mb-1 block",
                        ),
                        rx.el.input(
                            default_value=NeuroWatchState.user_profile[
                                "age"
                            ].to_string(),
                            class_name="w-full p-2 border border-gray-200 rounded-lg text-sm",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Caregiver Contact",
                            class_name="text-xs text-gray-500 font-bold mb-1 block",
                        ),
                        rx.el.input(
                            default_value=NeuroWatchState.user_profile[
                                "caregiver_contact"
                            ],
                            class_name="w-full p-2 border border-gray-200 rounded-lg text-sm",
                        ),
                        class_name="mb-4",
                    ),
                    class_name="max-w-md",
                ),
                class_name="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Baseline Management", class_name="text-lg font-semibold mb-6"
                ),
                rx.el.p(
                    "Baseline established on 2026-03-15 using 7 sessions.",
                    class_name="text-sm text-gray-600 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Sessions Until Stable", class_name="text-sm text-gray-500"
                        ),
                        rx.el.span(
                            "0 (Established)",
                            class_name="text-sm font-bold text-teal-600 ml-2",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        "Recalibrate Baseline",
                        class_name="bg-teal-600 text-white px-6 py-2 rounded-xl text-sm font-semibold hover:bg-teal-700 transition-colors",
                    ),
                ),
                class_name="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm mb-8",
            ),
            rx.el.div(
                rx.el.h3("Data Quality Notes", class_name="text-lg font-semibold mb-4"),
                rx.el.div(
                    rx.icon(
                        "message_circle_check", class_name="h-4 w-4 text-green-500 mr-2"
                    ),
                    rx.el.span(
                        "System reports high quality data across all monitored domains. No significant outliers detected in recent noise filtering.",
                        class_name="text-sm text-gray-600",
                    ),
                    class_name="flex items-center p-4 bg-green-50 rounded-xl",
                ),
                class_name="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm",
            ),
            class_name="flex flex-col",
        ),
        "System Settings & Baseline Management",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=AuthState.check_auth)
app.add_page(
    session_detail_page,
    route="/session/[session_id]",
    on_load=[AuthState.check_auth, NeuroWatchState.load_session],
)
app.add_page(assessment_page, route="/assessment", on_load=AuthState.check_auth)
app.add_page(sessions_page, route="/sessions", on_load=AuthState.check_auth)
app.add_page(trends_page, route="/trends", on_load=AuthState.check_auth)
app.add_page(activity_page, route="/activity", on_load=AuthState.check_auth)
app.add_page(assistant_page, route="/assistant", on_load=AuthState.check_auth)
app.add_page(profile_page, route="/profile", on_load=AuthState.check_auth)
app.add_page(alerts_page, route="/alerts", on_load=AuthState.check_auth)
app.add_page(settings_page, route="/settings", on_load=AuthState.check_auth)
app.add_page(login_page, route="/login", on_load=AuthState.check_not_auth)
app.add_page(signup_page, route="/signup", on_load=AuthState.check_not_auth)