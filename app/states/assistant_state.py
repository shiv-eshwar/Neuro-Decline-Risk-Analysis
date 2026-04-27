import reflex as rx
import asyncio
import logging
from app.states.neurowatch_state import NeuroWatchState


class AssistantState(rx.State):
    messages: list[dict[str, str]] = [
        {
            "role": "bot",
            "content": "Hello Eleanor. I'm NeuroBot. How can I assist you with your cognitive data today?",
        }
    ]
    chat_input: str = ""
    is_thinking: bool = False

    @rx.event
    def set_chat_input(self, value: str):
        self.chat_input = value

    @rx.event(background=True)
    async def handle_submit(self):
        if not self.chat_input.strip():
            return
        user_msg = self.chat_input.strip()
        async with self:
            self.messages.append({"role": "user", "content": user_msg})
            self.chat_input = ""
            self.is_thinking = True
            yield
        import asyncio

        await asyncio.sleep(1.2)
        async with self:
            nw_state = await self.get_state(NeuroWatchState)
            msg_lower = user_msg.lower()
            if "memory" in msg_lower:
                response = f"I've analyzed your recent memory tests. {await nw_state.get_var_value(NeuroWatchState.strongest_signal_insight)} It might be helpful to review your sequence recall scores in the Trends tab."
            elif "typing" in msg_lower:
                response = "Your typing dynamics appear relatively stable compared to your baseline. I noticed minor rhythm fluctuations during the last session, but nothing that triggers a clinical alert yet."
            elif "risk" in msg_lower or "score" in msg_lower:
                risk_level = await nw_state.get_var_value(
                    NeuroWatchState.current_risk_level
                )
                risk_score = await nw_state.get_var_value(
                    NeuroWatchState.current_risk_score
                )
                response = f"Your current profile is at a '{risk_level}' risk level with an overall score of {risk_score}/100. This is based on the composite analysis of all four neurological domains."
            else:
                response = "I'm here to help monitor your neurological health. You can ask me about your memory trends, typing speed, or your overall risk score for more context."
            self.messages.append({"role": "bot", "content": response})
            self.is_thinking = False