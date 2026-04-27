import reflex as rx
from app.components.sidebar import sidebar
from app.states.neurowatch_state import NeuroWatchState


def profile_section(title: str, icon: str, content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-teal-600 mr-2"),
            rx.el.h3(title, class_name="text-lg font-bold text-gray-900"),
            class_name="flex items-center mb-6 pb-2 border-b border-gray-100",
        ),
        content,
        class_name="bg-white p-8 rounded-3xl border border-gray-200 shadow-sm",
    )


def profile_page() -> rx.Component:
    return rx.el.main(
        sidebar(),
        rx.el.div(
            rx.el.header(
                rx.el.h1(
                    "Comprehensive Medical Profile",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Protected Health Information • Clinician Access Only",
                    class_name="text-xs font-bold text-red-500 uppercase tracking-widest mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    profile_section(
                        "Core Patient Information",
                        "user",
                        rx.el.div(
                            rx.el.div(
                                rx.image(
                                    src=NeuroWatchState.user_profile["avatar_url"],
                                    class_name="size-24 rounded-3xl bg-slate-50",
                                ),
                                rx.el.div(
                                    rx.el.h2(
                                        NeuroWatchState.user_profile["name"],
                                        class_name="text-2xl font-bold text-gray-900",
                                    ),
                                    rx.el.p(
                                        "Patient ID: NW-88219-EV",
                                        class_name="text-sm text-gray-500 font-medium",
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            f"Age: {NeuroWatchState.user_profile['age']}",
                                            class_name="px-2 py-1 bg-slate-100 rounded text-xs font-bold text-gray-600",
                                        ),
                                        rx.el.span(
                                            "D.O.B: 1958-04-12",
                                            class_name="px-2 py-1 bg-slate-100 rounded text-xs font-bold text-gray-600",
                                        ),
                                        class_name="flex gap-2 mt-2",
                                    ),
                                    class_name="flex-1",
                                ),
                                class_name="flex gap-6 items-center",
                            ),
                            class_name="space-y-4",
                        ),
                    ),
                    profile_section(
                        "Medications List",
                        "pill",
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p(
                                        "Donepezil",
                                        class_name="font-bold text-gray-900",
                                    ),
                                    rx.el.p(
                                        "5mg • Daily • Evening",
                                        class_name="text-sm text-gray-500",
                                    ),
                                    class_name="p-4 bg-teal-50/50 rounded-2xl border border-teal-100",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Memantine",
                                        class_name="font-bold text-gray-900",
                                    ),
                                    rx.el.p(
                                        "10mg • Daily • Morning",
                                        class_name="text-sm text-gray-500",
                                    ),
                                    class_name="p-4 bg-teal-50/50 rounded-2xl border border-teal-100",
                                ),
                                class_name="grid grid-cols-2 gap-4",
                            )
                        ),
                    ),
                    class_name="space-y-6",
                ),
                rx.el.div(
                    profile_section(
                        "Clinical Notes",
                        "clipboard-list",
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Diagnosis History",
                                    class_name="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2",
                                ),
                                rx.el.p(
                                    "Diagnosed with Mild Cognitive Impairment (MCI) on 2025-11-04 following neuropsychological assessment. Amnestic subtype confirmed via Rey Auditory Verbal Learning Test (RAVLT).",
                                    class_name="text-sm text-gray-700 leading-relaxed",
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Baseline Status",
                                    class_name="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2",
                                ),
                                rx.el.p(
                                    "Baseline established on 2026-03-15 after 7 initialization sessions. Stable rhythmic patterns identified in typing. Memory variance +/- 15% from mean.",
                                    class_name="text-sm text-gray-700 leading-relaxed",
                                ),
                            ),
                        ),
                    ),
                    profile_section(
                        "Care Team",
                        "users",
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p(
                                        "Dr. Sarah Chen, MD",
                                        class_name="font-bold text-gray-900",
                                    ),
                                    rx.el.p(
                                        "Primary Neurologist",
                                        class_name="text-xs text-teal-600 font-bold uppercase",
                                    ),
                                    class_name="p-4 border border-gray-100 rounded-2xl",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        NeuroWatchState.user_profile[
                                            "caregiver_contact"
                                        ],
                                        class_name="font-bold text-gray-900",
                                    ),
                                    rx.el.p(
                                        "Family Caregiver / SON",
                                        class_name="text-xs text-gray-500 font-bold uppercase",
                                    ),
                                    class_name="p-4 border border-gray-100 rounded-2xl",
                                ),
                                class_name="space-y-3",
                            )
                        ),
                    ),
                    class_name="space-y-6",
                ),
                class_name="grid grid-cols-2 gap-6",
            ),
            class_name="flex-1 ml-64 p-8 bg-slate-50 min-h-screen",
        ),
        class_name="font-['Inter'] flex",
    )