import reflex as rx
from app.states.neurowatch_state import NeuroWatchState


def new_session_modal() -> rx.Component:
    return rx.cond(
        NeuroWatchState.show_new_session_modal,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40",
                on_click=NeuroWatchState.toggle_new_session_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Add New Session", class_name="text-xl font-bold text-gray-900"
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-5 w-5 text-gray-500"),
                        on_click=NeuroWatchState.toggle_new_session_modal,
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.p(
                        "Enter raw metrics or simulate a session based on the current baseline trajectory.",
                        class_name="text-sm text-gray-600 mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.cond(
                                NeuroWatchState.is_simulating,
                                rx.icon(
                                    "loader", class_name="h-4 w-4 mr-2 animate-spin"
                                ),
                                rx.icon("plug_2", class_name="h-4 w-4 mr-2"),
                            ),
                            "Simulate Random Session",
                            on_click=NeuroWatchState.simulate_session,
                            disabled=NeuroWatchState.is_simulating,
                            class_name="w-full flex justify-center items-center py-3 bg-teal-50 text-teal-700 rounded-xl font-medium hover:bg-teal-100 transition-colors",
                        ),
                        class_name="space-y-4",
                    ),
                    class_name="mb-6",
                ),
                class_name="relative z-50 bg-white w-full max-w-lg rounded-2xl shadow-xl p-6 border border-gray-100",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
        ),
        rx.fragment(),
    )