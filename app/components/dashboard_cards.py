import reflex as rx
from app.states.neurowatch_state import NeuroWatchState, DomainScore


def risk_gauge() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        NeuroWatchState.current_risk_score.to_string(),
                        class_name="text-5xl font-bold",
                    ),
                    rx.el.span("/ 100", class_name="text-gray-400 text-lg ml-1"),
                    class_name="absolute inset-0 flex items-center justify-center flex-row",
                ),
                rx.el.svg(
                    rx.el.circle(
                        cx="60",
                        cy="60",
                        r="54",
                        class_name="stroke-gray-100 fill-none stroke-[8px]",
                    ),
                    rx.el.circle(
                        cx="60",
                        cy="60",
                        r="54",
                        class_name="fill-none stroke-[8px] transition-all duration-1000",
                        style={
                            "stroke": NeuroWatchState.current_risk_color,
                            "strokeDasharray": "339",
                            "strokeDashoffset": (
                                339 * (1 - NeuroWatchState.current_risk_score / 100)
                            ).to_string(),
                            "strokeLinecap": "round",
                            "transform": "rotate(-90deg)",
                            "transformOrigin": "center",
                        },
                    ),
                    view_box="0 0 120 120",
                    class_name="w-48 h-48",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.h2(
                    NeuroWatchState.current_risk_level,
                    class_name="text-2xl font-bold text-gray-900 mt-4",
                ),
                rx.el.p(
                    "Last assessed: Today, 10:45 AM", class_name="text-sm text-gray-500"
                ),
                class_name="text-center",
            ),
            class_name="flex flex-col items-center p-8 bg-white rounded-2xl border border-gray-200 shadow-sm",
        ),
        class_name="col-span-1",
    )


def domain_card(domain: DomainScore) -> rx.Component:
    icon_map = {
        "Typing": "keyboard",
        "Reaction": "zap",
        "Memory": "brain",
        "Voice": "mic",
    }
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    rx.match(
                        domain["name"],
                        ("Typing", "keyboard"),
                        ("Reaction", "zap"),
                        ("Memory", "brain"),
                        "mic",
                    ),
                    class_name="h-5 w-5",
                ),
                class_name="p-2 rounded-lg bg-slate-50 text-gray-600",
            ),
            rx.el.div(
                rx.el.span(
                    domain["flags"].to_string() + " Flags",
                    class_name=rx.cond(
                        domain["flags"] > 0,
                        "text-xs font-semibold px-2 py-0.5 rounded-full bg-red-50 text-red-600",
                        "text-xs font-medium px-2 py-0.5 rounded-full bg-green-50 text-green-600",
                    ),
                ),
                class_name="ml-auto",
            ),
            class_name="flex items-center gap-3 mb-4",
        ),
        rx.el.p(domain["name"], class_name="text-sm font-medium text-gray-500"),
        rx.el.div(
            rx.el.span(
                domain["score"].to_string(),
                class_name="text-3xl font-bold text-gray-900",
            ),
            rx.icon(
                rx.match(
                    domain["trend"],
                    ("declining", "arrow-down-right"),
                    ("improving", "arrow-up-right"),
                    "arrow-right",
                ),
                class_name=rx.cond(
                    domain["trend"] == "declining",
                    "h-5 w-5 text-red-500",
                    rx.cond(
                        domain["trend"] == "improving",
                        "h-5 w-5 text-green-500",
                        "h-5 w-5 text-gray-400",
                    ),
                ),
            ),
            class_name="flex items-center gap-2 mt-1",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm border-l-4",
        style={"borderLeftColor": domain["risk_color"]},
    )