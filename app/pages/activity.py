import reflex as rx
from app.components.sidebar import sidebar
from app.states.neurowatch_state import NeuroWatchState


def stat_card(label: str, value: rx.Var, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-teal-600"),
            class_name="p-2 bg-teal-50 rounded-lg mb-4 w-fit",
        ),
        rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm flex-1",
    )


def heatmap_square(day: dict) -> rx.Component:
    return rx.el.div(
        title=f"{day['date']}: Level {day['intensity']}",
        class_name=rx.match(
            day["intensity"],
            (0, "size-4 rounded-sm bg-slate-100"),
            (1, "size-4 rounded-sm bg-teal-200"),
            (2, "size-4 rounded-sm bg-teal-400"),
            (3, "size-4 rounded-sm bg-teal-600"),
            (4, "size-4 rounded-sm bg-teal-800"),
            "size-4 rounded-sm bg-slate-100",
        ),
    )


def activity_page() -> rx.Component:
    return rx.el.main(
        sidebar(),
        rx.el.div(
            rx.el.header(
                rx.el.h1(
                    "Activity & Adherence",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                stat_card(
                    "Current Streak", f"{NeuroWatchState.current_streak} Days", "flame"
                ),
                stat_card(
                    "Completion Rate",
                    NeuroWatchState.completion_rate,
                    "message_circle_check",
                ),
                stat_card(
                    "Total Sessions",
                    NeuroWatchState.total_sessions.to_string(),
                    "bar-chart-3",
                ),
                class_name="flex gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Assessment Frequency (Last 12 Weeks)",
                    class_name="text-lg font-semibold mb-6",
                ),
                rx.el.div(
                    rx.foreach(NeuroWatchState.activity_heatmap, heatmap_square),
                    class_name="flex flex-wrap gap-1.5 p-6 bg-slate-50 rounded-xl border border-gray-100",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span("Less", class_name="text-xs text-gray-400"),
                        rx.el.div(class_name="size-3 rounded-sm bg-slate-100"),
                        rx.el.div(class_name="size-3 rounded-sm bg-teal-200"),
                        rx.el.div(class_name="size-3 rounded-sm bg-teal-400"),
                        rx.el.div(class_name="size-3 rounded-sm bg-teal-600"),
                        rx.el.div(class_name="size-3 rounded-sm bg-teal-800"),
                        rx.el.span("More", class_name="text-xs text-gray-400"),
                        class_name="flex items-center gap-1.5",
                    ),
                    class_name="flex justify-end mt-4",
                ),
                class_name="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm",
            ),
            class_name="flex-1 ml-64 p-8 bg-slate-50 min-h-screen",
        ),
        class_name="font-['Inter'] flex",
    )