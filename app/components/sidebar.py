import reflex as rx
from app.states.neurowatch_state import NeuroWatchState


def nav_item(label: str, icon: str) -> rx.Component:
    is_active = NeuroWatchState.active_page == label
    return rx.el.button(
        rx.icon(
            icon,
            class_name=rx.cond(
                is_active, "h-5 w-5 text-teal-600", "h-5 w-5 text-gray-400"
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                is_active, "font-semibold text-teal-600", "font-medium text-gray-600"
            ),
        ),
        on_click=lambda: NeuroWatchState.set_active_page(label),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 w-full p-3 rounded-xl bg-teal-50 transition-all duration-200",
            "flex items-center gap-3 w-full p-3 rounded-xl hover:bg-gray-50 transition-all duration-200",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("brain", class_name="h-6 w-6 text-white"),
                    class_name="bg-teal-600 p-2 rounded-lg",
                ),
                rx.el.span(
                    "NeuroWatch",
                    class_name="text-xl font-bold text-gray-900 tracking-tight",
                ),
                class_name="flex items-center gap-3 px-2 mb-10",
            ),
            rx.el.nav(
                nav_item("Dashboard", "layout-dashboard"),
                nav_item("Sessions", "list"),
                nav_item("Trends", "trending-up"),
                nav_item("Alerts", "bell"),
                nav_item("Settings", "settings"),
                class_name="flex flex-col gap-2",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=NeuroWatchState.user_profile["avatar_url"],
                    class_name="h-10 w-10 rounded-full bg-slate-100",
                ),
                rx.el.div(
                    rx.el.p(
                        NeuroWatchState.user_profile["name"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        "Age: " + NeuroWatchState.user_profile["age"].to_string(),
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3 p-3 rounded-xl bg-gray-50 border border-gray-100",
            ),
            class_name="mt-auto pt-6 border-t border-gray-100",
        ),
        class_name="fixed left-0 top-0 bottom-0 w-64 bg-white border-r border-gray-200 p-6 flex flex-col z-20",
    )