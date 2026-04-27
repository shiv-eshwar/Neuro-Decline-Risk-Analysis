import reflex as rx
import logging


class AuthState(rx.State):
    auth_token: str = rx.Cookie(name="auth_token", path="/", same_site="lax")

    @rx.var
    def is_authenticated(self) -> bool:
        return self.auth_token != ""

    @rx.event
    def login(self, form_data: dict[str, str]):
        """Handle login submission."""
        email = form_data.get("email", "")
        password = form_data.get("password", "")
        if email and password:
            self.auth_token = f"token_{email[:3]}_{id(self)}"
            return rx.redirect("/")
        else:
            return rx.toast(
                "Invalid credentials. Please enter email and password.", duration=3000
            )

    @rx.event
    def signup(self, form_data: dict[str, str]):
        """Handle signup submission."""
        name = form_data.get("name", "")
        email = form_data.get("email", "")
        password = form_data.get("password", "")
        if name and email and password:
            self.auth_token = f"token_{email[:3]}_{id(self)}"
            return rx.redirect("/")
        else:
            return rx.toast(
                "Please fill in all fields to create an account.", duration=3000
            )

    @rx.event
    def logout(self):
        """Clear auth token and redirect to login."""
        return [rx.remove_cookie("auth_token"), rx.redirect("/login")]

    @rx.event
    def check_auth(self):
        """Protected route guard."""
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.event
    def check_not_auth(self):
        """Guest route guard (e.g. don't show login if already logged in)."""
        if self.is_authenticated:
            return rx.redirect("/")