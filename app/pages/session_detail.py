import reflex as rx
from app.states.neurowatch_state import NeuroWatchState, DomainScore


def stat_row(label: str, value: rx.Var, unit: str = "") -> rx.Component:
    return rx.el.div(
        rx.el.span(label, class_name="text-xs text-gray-500"),
        rx.el.div(
            rx.el.span(value, class_name="text-sm font-semibold text-gray-900"),
            rx.el.span(unit, class_name="text-xs text-gray-400 ml-1"),
            class_name="flex items-baseline",
        ),
        class_name="flex justify-between items-center py-2 border-b border-gray-50 last:border-0",
    )


def domain_panel(
    title: str, icon_name: str, domain_key: str, stats: list[tuple[str, rx.Var, str]]
) -> rx.Component:
    d_score = NeuroWatchState.selected_analysis["domain_scores"][domain_key]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon_name, class_name="h-5 w-5 text-gray-500 mr-2"),
                rx.el.h3(title, class_name="font-semibold text-gray-900"),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.span(
                    d_score["score"].to_string(),
                    class_name="text-lg font-bold",
                    style={"color": d_score["risk_color"]},
                ),
                rx.icon(
                    rx.cond(
                        d_score["trend"] == "declining", "trending-down", "trending-up"
                    ),
                    class_name="h-4 w-4 ml-1 text-gray-400",
                ),
                class_name="flex items-center bg-slate-50 px-3 py-1 rounded-lg",
            ),
            class_name="flex justify-between items-center mb-4 pb-4 border-b border-gray-100",
        ),
        rx.el.div(
            rx.foreach(stats, lambda s: stat_row(s[0], s[1], s[2])), class_name="mb-4"
        ),
        rx.cond(
            d_score["flags"] > 0,
            rx.el.div(
                rx.foreach(
                    d_score["flag_list"],
                    lambda f: rx.el.span(
                        f,
                        class_name="inline-block px-2 py-1 bg-red-50 text-red-600 text-xs font-medium rounded-md mr-2 mb-2",
                    ),
                ),
                class_name="mb-4",
            ),
            rx.fragment(),
        ),
        rx.el.p(d_score["key_observation"], class_name="text-sm text-gray-600 italic"),
        class_name="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm",
    )


def session_detail_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="h-4 w-4 mr-2"),
                "Back to Dashboard",
                on_click=rx.redirect("/"),
                class_name="text-sm text-gray-500 hover:text-teal-600 flex items-center mb-6 transition-colors",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        rx.cond(
                            NeuroWatchState.selected_session_data,
                            f"Session #{NeuroWatchState.selected_session_data['session_number']} — {NeuroWatchState.selected_session_data['timestamp']}",
                            "Loading Session...",
                        ),
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.el.span(
                        NeuroWatchState.selected_analysis["risk_level"],
                        class_name="px-3 py-1 rounded-full text-sm font-semibold mt-2 inline-block bg-slate-100",
                        style={
                            "color": NeuroWatchState.selected_analysis["domain_scores"][
                                "Typing"
                            ]["risk_color"]
                        },
                    ),
                    class_name="",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            NeuroWatchState.selected_analysis["risk_score"].to_string(),
                            class_name="text-3xl font-bold",
                        ),
                        rx.el.span("/100", class_name="text-gray-400 text-sm ml-1"),
                        class_name="flex items-baseline",
                    ),
                    class_name="px-6 py-4 rounded-xl border-2",
                    style={
                        "borderColor": NeuroWatchState.selected_analysis[
                            "domain_scores"
                        ]["Typing"]["risk_color"]
                    },
                ),
                class_name="flex justify-between items-start mb-6",
            ),
            rx.el.p(
                NeuroWatchState.selected_analysis["personalized_summary"],
                class_name="text-gray-600 mb-8 max-w-3xl leading-relaxed",
            ),
            rx.el.div(
                domain_panel(
                    "Typing Dynamics",
                    "keyboard",
                    "Typing",
                    [
                        (
                            "Speed",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['typing']['speed_wpm']:.1f}",
                                "0.0",
                            ),
                            "WPM",
                        ),
                        (
                            "Interval Variance",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['typing']['keystroke_interval_variance_ms']:.1f}",
                                "0.0",
                            ),
                            "ms",
                        ),
                        (
                            "Error Rate",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['typing']['error_rate_percent']:.1f}",
                                "0.0",
                            ),
                            "%",
                        ),
                    ],
                ),
                domain_panel(
                    "Reaction Time",
                    "zap",
                    "Reaction",
                    [
                        (
                            "Mean RT",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['reaction']['mean_reaction_time_ms']:.1f}",
                                "0.0",
                            ),
                            "ms",
                        ),
                        (
                            "RT Variance",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['reaction']['reaction_time_variance_ms']:.1f}",
                                "0.0",
                            ),
                            "ms",
                        ),
                        (
                            "Miss Rate",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['reaction']['miss_rate_percent']:.1f}",
                                "0.0",
                            ),
                            "%",
                        ),
                    ],
                ),
                domain_panel(
                    "Memory",
                    "brain",
                    "Memory",
                    [
                        (
                            "Recall Accuracy",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['memory']['recall_accuracy_percent']:.1f}",
                                "0.0",
                            ),
                            "%",
                        ),
                        (
                            "Sequence Memory",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['memory']['sequence_memory_score']:.1f}",
                                "0.0",
                            ),
                            "",
                        ),
                        (
                            "Recall Latency",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['memory']['recall_latency_ms']:.1f}",
                                "0.0",
                            ),
                            "ms",
                        ),
                    ],
                ),
                domain_panel(
                    "Voice Analysis",
                    "mic",
                    "Voice",
                    [
                        (
                            "Speech Rate",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['voice']['speech_rate_wpm']:.1f}",
                                "0.0",
                            ),
                            "WPM",
                        ),
                        (
                            "Pause Duration",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['voice']['mean_pause_duration_ms']:.1f}",
                                "0.0",
                            ),
                            "ms",
                        ),
                        (
                            "Articulation",
                            rx.cond(
                                NeuroWatchState.selected_session_data,
                                f"{NeuroWatchState.selected_session_data['voice']['articulation_score']:.1f}",
                                "0.0",
                            ),
                            "",
                        ),
                    ],
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
            class_name="max-w-5xl mx-auto py-8",
        ),
        class_name="min-h-screen bg-slate-50 p-8 w-full font-['Inter']",
    )