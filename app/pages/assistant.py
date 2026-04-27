import reflex as rx
from app.components.sidebar import sidebar
from app.states.assistant_state import AssistantState


def message_bubble(msg: dict[str, str]) -> rx.Component:
    is_bot = msg["role"] == "bot"
    return rx.el.div(
        rx.el.div(
            rx.cond(
                is_bot,
                rx.el.div(
                    rx.icon("bot", class_name="h-4 w-4 text-teal-600"),
                    class_name="p-1.5 bg-teal-100 rounded-lg mr-2 shrink-0",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.p(msg["content"], class_name="text-sm leading-relaxed"),
                class_name=rx.cond(
                    is_bot,
                    "bg-teal-50 text-teal-900 rounded-2xl rounded-tl-none p-4 border border-teal-100",
                    "bg-teal-600 text-white rounded-2xl rounded-tr-none p-4 shadow-sm",
                ),
            ),
            class_name=rx.cond(
                is_bot,
                "flex items-start max-w-[80%]",
                "flex items-start max-w-[80%] flex-row-reverse",
            ),
        ),
        class_name=rx.cond(is_bot, "flex justify-start mb-4", "flex justify-end mb-4"),
    )


def suggestion_chip(text: str) -> rx.Component:
    return rx.el.button(
        text,
        on_click=lambda: AssistantState.set_chat_input(text),
        class_name="px-4 py-1.5 bg-white border border-gray-200 rounded-full text-xs font-semibold text-gray-600 hover:bg-teal-50 hover:border-teal-200 transition-all",
    )


def assistant_page() -> rx.Component:
    return rx.el.main(
        sidebar(),
        rx.el.div(
            rx.el.header(
                rx.el.h1(
                    "NeuroBot Assistant", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.span(
                    "Clinical AI Companion",
                    class_name="text-xs font-bold text-teal-600 uppercase tracking-widest px-2 py-1 bg-teal-50 rounded-md ml-4",
                ),
                class_name="flex items-center mb-8 sticky top-0 bg-slate-50/80 backdrop-blur-md py-4 z-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.foreach(AssistantState.messages, message_bubble),
                        rx.cond(
                            AssistantState.is_thinking,
                            rx.el.div(
                                rx.el.div(
                                    class_name="size-2 bg-teal-400 rounded-full animate-bounce"
                                ),
                                rx.el.div(
                                    class_name="size-2 bg-teal-400 rounded-full animate-bounce [animation-delay:0.2s]"
                                ),
                                rx.el.div(
                                    class_name="size-2 bg-teal-400 rounded-full animate-bounce [animation-delay:0.4s]"
                                ),
                                class_name="flex gap-1 p-4 bg-teal-50 rounded-2xl w-fit ml-8 border border-teal-100",
                            ),
                            rx.fragment(),
                        ),
                        class_name="flex-1 overflow-y-auto p-6 flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.div(
                            suggestion_chip("Is my memory declining?"),
                            suggestion_chip("Summarize my last typing test"),
                            suggestion_chip("How is my overall score?"),
                            class_name="flex gap-2 p-4 border-t border-gray-100 flex-wrap",
                        ),
                        rx.el.div(
                            rx.el.input(
                                placeholder="Ask NeuroBot about your data...",
                                on_change=AssistantState.set_chat_input,
                                on_key_down=lambda e: rx.cond(
                                    e == "Enter",
                                    rx.cond(
                                        AssistantState.chat_input,
                                        rx.cond(
                                            AssistantState.is_thinking,
                                            rx.noop(),
                                            AssistantState.handle_submit,
                                        ),
                                        rx.noop(),
                                    ),
                                    rx.noop(),
                                ),
                                class_name="flex-1 bg-gray-50 border-none focus:ring-0 p-4 text-sm",
                                default_value=AssistantState.chat_input,
                            ),
                            rx.el.button(
                                rx.icon("send", class_name="h-4 w-4"),
                                on_click=AssistantState.handle_submit,
                                disabled=AssistantState.is_thinking,
                                class_name="p-4 text-teal-600 hover:text-teal-700 disabled:opacity-30",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="bg-white border-t border-gray-100",
                    ),
                    class_name="bg-white rounded-3xl border border-gray-200 shadow-sm overflow-hidden flex flex-col h-[calc(100vh-200px)]",
                ),
                class_name="max-w-4xl mx-auto",
            ),
            class_name="flex-1 ml-64 p-8 bg-slate-50 min-h-screen",
        ),
        class_name="font-['Inter'] flex",
    )