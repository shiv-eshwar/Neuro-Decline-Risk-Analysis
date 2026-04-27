import reflex as rx
from app.components.sidebar import sidebar
from app.states.assessment_state import AssessmentState


def step_indicator(label: str, step_id: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name=rx.cond(
                AssessmentState.current_step == step_id,
                "h-3 w-3 rounded-full bg-teal-600",
                "h-3 w-3 rounded-full bg-gray-300",
            )
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                AssessmentState.current_step == step_id,
                "text-sm font-bold text-teal-700",
                "text-sm font-medium text-gray-500",
            ),
        ),
        class_name="flex items-center gap-2",
    )


def typing_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Typing Assessment", class_name="text-2xl font-bold mb-4 text-gray-900"
        ),
        rx.el.p(
            "Please type the following text as quickly and accurately as possible:",
            class_name="mb-6 text-gray-600",
        ),
        rx.el.div(
            AssessmentState.typing_prompt,
            class_name="p-4 bg-slate-100 rounded-xl mb-6 font-medium text-gray-800 text-lg border border-gray-200",
        ),
        rx.text_area(
            on_change=AssessmentState.on_typing_change,
            placeholder="Start typing here...",
            class_name="w-full p-4 border-2 border-gray-300 rounded-xl h-40 mb-6 focus:border-teal-500 focus:ring-0 text-lg",
            default_value=AssessmentState.typing_input,
        ),
        rx.el.button(
            "Next: Reaction Test",
            on_click=AssessmentState.finish_typing,
            disabled=AssessmentState.typing_input.length() == 0,
            class_name="w-full py-3 bg-teal-600 text-white font-bold rounded-xl hover:bg-teal-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
        ),
        class_name="max-w-2xl mx-auto",
    )


def reaction_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Reaction Assessment", class_name="text-2xl font-bold mb-4 text-gray-900"
        ),
        rx.el.p(
            "Click the box as soon as it turns green. We will do 3 trials.",
            class_name="mb-6 text-gray-600",
        ),
        rx.el.div(
            rx.el.p(
                f"Trial {AssessmentState.reaction_trial + 1} of 3",
                class_name="text-sm font-bold text-gray-500 mb-2",
            ),
            rx.cond(
                AssessmentState.reaction_state == "done",
                rx.el.div(
                    rx.el.p(
                        "All trials completed!",
                        class_name="text-xl font-bold text-teal-700 mb-6",
                    ),
                    rx.el.button(
                        "Next: Memory Test",
                        on_click=AssessmentState.finish_reaction,
                        class_name="py-3 px-8 bg-teal-600 text-white font-bold rounded-xl hover:bg-teal-700 transition-colors",
                    ),
                    class_name="flex flex-col items-center justify-center h-64 bg-slate-50 rounded-2xl border-2 border-dashed border-gray-300",
                ),
                rx.el.button(
                    rx.match(
                        AssessmentState.reaction_state,
                        ("wait", "Wait for green..."),
                        ("ready", "CLICK NOW!"),
                        "...",
                    ),
                    on_click=AssessmentState.handle_reaction_click,
                    class_name=rx.match(
                        AssessmentState.reaction_state,
                        (
                            "wait",
                            "w-full h-64 rounded-2xl flex items-center justify-center text-3xl font-bold transition-colors bg-gray-200 text-gray-500",
                        ),
                        (
                            "ready",
                            "w-full h-64 rounded-2xl flex items-center justify-center text-3xl font-bold transition-colors bg-green-500 text-white shadow-xl shadow-green-200 cursor-pointer",
                        ),
                        "w-full h-64 rounded-2xl bg-gray-100",
                    ),
                ),
            ),
        ),
        class_name="max-w-2xl mx-auto",
    )


def memory_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Memory Assessment", class_name="text-2xl font-bold mb-4 text-gray-900"
        ),
        rx.el.p(
            "Memorize the sequence, then recall it when prompted.",
            class_name="mb-6 text-gray-600",
        ),
        rx.cond(
            AssessmentState.memory_phase == "memorize",
            rx.el.div(
                rx.el.p(
                    "Memorize this sequence:",
                    class_name="text-gray-500 mb-4 font-semibold",
                ),
                rx.el.p(
                    AssessmentState.memory_sequence,
                    class_name="text-5xl font-mono font-bold tracking-widest text-teal-700",
                ),
                class_name="flex flex-col items-center justify-center h-64 bg-slate-50 rounded-2xl border border-gray-200",
            ),
            rx.el.div(
                rx.el.p(
                    "Enter the sequence:", class_name="text-gray-700 mb-4 font-semibold"
                ),
                rx.el.input(
                    on_change=AssessmentState.set_memory_input,
                    class_name="w-full text-center text-3xl font-mono tracking-widest p-4 border-2 border-gray-300 rounded-xl mb-6 focus:border-teal-500 focus:ring-0",
                    default_value=AssessmentState.memory_input,
                ),
                rx.el.button(
                    "Next: Voice Test",
                    on_click=AssessmentState.finish_memory,
                    class_name="w-full py-3 bg-teal-600 text-white font-bold rounded-xl hover:bg-teal-700 transition-colors",
                ),
                class_name="max-w-md mx-auto mt-8",
            ),
        ),
        class_name="max-w-2xl mx-auto text-center",
    )


def voice_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Voice Assessment", class_name="text-2xl font-bold mb-4 text-gray-900"
        ),
        rx.el.p(
            "Please read the following phrase aloud after pressing start:",
            class_name="mb-6 text-gray-600",
        ),
        rx.el.div(
            "I am participating in a cognitive assessment. The sun is shining brightly today.",
            class_name="p-6 bg-slate-50 rounded-xl mb-8 text-xl font-medium text-center text-gray-800 italic border-l-4 border-teal-500",
        ),
        rx.el.div(
            rx.el.button(
                rx.cond(
                    AssessmentState.voice_recording,
                    rx.icon("square", class_name="h-5 w-5 mr-2"),
                    rx.icon("mic", class_name="h-5 w-5 mr-2"),
                ),
                rx.cond(
                    AssessmentState.voice_recording, "Stop Recording", "Start Recording"
                ),
                on_click=AssessmentState.toggle_voice_recording,
                class_name=rx.cond(
                    AssessmentState.voice_recording,
                    "flex items-center justify-center py-4 px-8 bg-red-500 text-white font-bold rounded-xl hover:bg-red-600 w-full transition-all animate-pulse",
                    "flex items-center justify-center py-4 px-8 bg-slate-800 text-white font-bold rounded-xl hover:bg-slate-900 w-full transition-all",
                ),
            ),
            rx.cond(
                AssessmentState.voice_duration > 0.0,
                rx.el.button(
                    "Complete Assessment",
                    on_click=AssessmentState.finish_assessment,
                    class_name="w-full py-4 bg-teal-600 text-white font-bold rounded-xl hover:bg-teal-700 transition-colors",
                ),
                rx.fragment(),
            ),
            class_name="space-y-4 max-w-sm mx-auto",
        ),
        class_name="max-w-2xl mx-auto",
    )


def assessment_page() -> rx.Component:
    return rx.el.main(
        sidebar(),
        rx.el.div(
            rx.el.header(
                rx.el.h1(
                    "Interactive Assessment",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-5 w-5 mr-2"),
                    "Cancel",
                    on_click=rx.redirect("/"),
                    class_name="text-gray-500 hover:text-gray-700 font-medium flex items-center",
                ),
                class_name="flex justify-between items-center mb-8 sticky top-0 bg-slate-50/80 backdrop-blur-md py-4 z-10",
            ),
            rx.el.div(
                step_indicator("Typing", "typing"),
                rx.el.div(class_name="h-px w-12 bg-gray-200 mx-2 hidden sm:block"),
                step_indicator("Reaction", "reaction"),
                rx.el.div(class_name="h-px w-12 bg-gray-200 mx-2 hidden sm:block"),
                step_indicator("Memory", "memory"),
                rx.el.div(class_name="h-px w-12 bg-gray-200 mx-2 hidden sm:block"),
                step_indicator("Voice", "voice"),
                class_name="flex items-center justify-center mb-12 flex-wrap gap-4",
            ),
            rx.el.div(
                rx.match(
                    AssessmentState.current_step,
                    ("typing", typing_step()),
                    ("reaction", reaction_step()),
                    ("memory", memory_step()),
                    ("voice", voice_step()),
                    typing_step(),
                ),
                class_name="bg-white p-10 rounded-2xl border border-gray-200 shadow-sm min-h-[500px]",
            ),
            class_name="flex-1 ml-64 p-8 bg-slate-50 min-h-screen",
        ),
        class_name="font-['Inter'] flex",
    )