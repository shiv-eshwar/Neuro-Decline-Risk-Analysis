import reflex as rx
from app.states.neurowatch_state import NeuroWatchState


def session_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Recent Session History",
                class_name="text-lg font-semibold text-gray-900",
            ),
            rx.el.button(
                "View All",
                class_name="text-sm text-teal-600 font-medium hover:underline",
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
                            "Overall Score",
                            class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.th(
                            "Strongest Signal",
                            class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase",
                        ),
                        rx.el.th("", class_name="py-3 px-4"),
                    ),
                    class_name="border-b border-gray-100",
                ),
                rx.el.tbody(
                    rx.foreach(
                        NeuroWatchState.table_data,
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
                                    rx.icon("chevron-right", class_name="h-4 w-4"),
                                    on_click=lambda: NeuroWatchState.view_session(
                                        row["id"].to_string()
                                    ),
                                    class_name="text-gray-400 hover:text-teal-600 transition-colors",
                                ),
                                class_name="py-4 px-4 text-right",
                            ),
                            on_click=lambda: NeuroWatchState.view_session(
                                row["id"].to_string()
                            ),
                            class_name="border-b border-gray-50 hover:bg-slate-50 transition-colors cursor-pointer",
                        ),
                    )
                ),
                class_name="w-full table-auto",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
    )