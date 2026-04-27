import reflex as rx
from app.states.auth_state import AuthState


def auth_layout(content: rx.Component, title: str, subtitle: str) -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("brain", class_name="h-10 w-10 text-white"),
                    class_name="bg-teal-600 p-3 rounded-2xl mb-6 shadow-lg shadow-teal-100",
                ),
                rx.el.h1(title, class_name="text-3xl font-bold text-gray-900 mb-2"),
                rx.el.p(subtitle, class_name="text-gray-500 mb-8"),
                content,
                class_name="w-full max-w-md bg-white p-10 rounded-3xl border border-gray-100 shadow-xl flex flex-col items-center",
            ),
            class_name="min-h-screen w-screen flex items-center justify-center bg-slate-50 p-6",
        ),
        class_name="font-['Inter']",
    )


def login_page() -> rx.Component:
    return auth_layout(
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Email Address",
                    class_name="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 block",
                ),
                rx.el.input(
                    placeholder="name@example.com",
                    name="email",
                    type="email",
                    required=True,
                    class_name="w-full p-3 bg-slate-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 outline-none transition-all",
                ),
                class_name="mb-6 w-full",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 block",
                ),
                rx.el.input(
                    placeholder="••••••••",
                    name="password",
                    type="password",
                    required=True,
                    class_name="w-full p-3 bg-slate-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 outline-none transition-all",
                ),
                class_name="mb-8 w-full",
            ),
            rx.el.button(
                "Sign In",
                type="submit",
                class_name="w-full py-4 bg-teal-600 hover:bg-teal-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-teal-100 mb-6",
            ),
            rx.el.div(
                rx.el.span(
                    "Don't have an account? ", class_name="text-sm text-gray-500"
                ),
                rx.el.a(
                    "Create account",
                    href="/signup",
                    class_name="text-sm font-bold text-teal-600 hover:underline",
                ),
                class_name="text-center",
            ),
            on_submit=AuthState.login,
            class_name="w-full",
        ),
        "Welcome Back",
        "Sign in to monitor neurological health metrics",
    )


def signup_page() -> rx.Component:
    return auth_layout(
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Full Name",
                    class_name="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 block",
                ),
                rx.el.input(
                    placeholder="John Doe",
                    name="name",
                    required=True,
                    class_name="w-full p-3 bg-slate-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 outline-none transition-all",
                ),
                class_name="mb-6 w-full",
            ),
            rx.el.div(
                rx.el.label(
                    "Email Address",
                    class_name="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 block",
                ),
                rx.el.input(
                    placeholder="name@example.com",
                    name="email",
                    type="email",
                    required=True,
                    class_name="w-full p-3 bg-slate-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 outline-none transition-all",
                ),
                class_name="mb-6 w-full",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 block",
                ),
                rx.el.input(
                    placeholder="••••••••",
                    name="password",
                    type="password",
                    required=True,
                    class_name="w-full p-3 bg-slate-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 outline-none transition-all",
                ),
                class_name="mb-8 w-full",
            ),
            rx.el.button(
                "Create Account",
                type="submit",
                class_name="w-full py-4 bg-teal-600 hover:bg-teal-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-teal-100 mb-6",
            ),
            rx.el.div(
                rx.el.span(
                    "Already have an account? ", class_name="text-sm text-gray-500"
                ),
                rx.el.a(
                    "Sign in",
                    href="/login",
                    class_name="text-sm font-bold text-teal-600 hover:underline",
                ),
                class_name="text-center",
            ),
            on_submit=AuthState.signup,
            class_name="w-full",
        ),
        "Get Started",
        "Join NeuroWatch for advanced behavioral tracking",
    )