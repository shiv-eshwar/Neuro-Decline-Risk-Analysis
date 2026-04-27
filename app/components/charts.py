import reflex as rx
from app.states.neurowatch_state import NeuroWatchState


def trend_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Risk Score Progression",
                class_name="text-lg font-semibold text-gray-900",
            ),
            rx.el.p(
                "3-month trend across all domains", class_name="text-sm text-gray-500"
            ),
            class_name="mb-6",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", vertical=False, stroke="#f1f5f9"
            ),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "white",
                    "borderRadius": "12px",
                    "border": "1px solid #e2e8f0",
                    "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
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
            rx.recharts.reference_line(
                rx.recharts.label(
                    value="Moderate",
                    position="insideBottomRight",
                    custom_attrs={"fontSize": "10px", "fill": "#eab308"},
                ),
                y=25,
                stroke="#eab308",
                stroke_dasharray="5 5",
            ),
            rx.recharts.reference_line(
                rx.recharts.label(
                    value="Elevated",
                    position="insideBottomRight",
                    custom_attrs={"fontSize": "10px", "fill": "#f97316"},
                ),
                y=50,
                stroke="#f97316",
                stroke_dasharray="5 5",
            ),
            rx.recharts.reference_line(
                rx.recharts.label(
                    value="High",
                    position="insideBottomRight",
                    custom_attrs={"fontSize": "10px", "fill": "#ef4444"},
                ),
                y=75,
                stroke="#ef4444",
                stroke_dasharray="5 5",
            ),
            rx.recharts.area(
                data_key="score",
                stroke="#0d9488",
                fill="#0d9488",
                fill_opacity=0.1,
                stroke_width=3,
                type_="monotone",
            ),
            data=NeuroWatchState.chart_data,
            width="100%",
            height=300,
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm col-span-2",
    )