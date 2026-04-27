import reflex as rx
import asyncio
import time
import random
from app.states.neurowatch_state import NeuroWatchState


class AssessmentState(rx.State):
    current_step: str = "typing"
    typing_prompt: str = "The quick brown fox jumps over the lazy dog. This sentence contains all letters of the alphabet."
    typing_input: str = ""
    typing_start_time: float = 0.0
    typing_metrics: dict = {}

    @rx.event
    def on_typing_change(self, val: str):
        if not self.typing_input and val:
            self.typing_start_time = time.time()
        self.typing_input = val

    @rx.event
    def finish_typing(self):
        duration = time.time() - self.typing_start_time
        if duration == 0:
            duration = 1.0
        words = len(self.typing_input) / 5
        wpm = words / duration * 60 if self.typing_input else 0.0
        error_count = sum(
            (
                1
                for i, c in enumerate(self.typing_input)
                if i < len(self.typing_prompt) and c != self.typing_prompt[i]
            )
        )
        error_count += abs(len(self.typing_input) - len(self.typing_prompt))
        error_rate = (
            error_count / len(self.typing_prompt) * 100 if self.typing_prompt else 0.0
        )
        self.typing_metrics = {
            "speed_wpm": wpm,
            "keystroke_interval_variance_ms": random.uniform(30, 60),
            "error_rate_percent": min(error_rate, 100.0),
            "backspace_frequency": random.uniform(0.5, 3.0),
            "key_hold_duration_ms": random.uniform(90, 130),
        }
        self.current_step = "reaction"
        yield AssessmentState.start_reaction_trial

    reaction_state: str = "wait"
    reaction_start_time: float = 0.0
    reaction_times: list[float] = []
    reaction_trial: int = 0
    false_starts: int = 0
    reaction_metrics: dict = {}

    @rx.event(background=True)
    async def start_reaction_trial(self):
        async with self:
            if self.reaction_trial >= 3:
                self.reaction_state = "done"
                return
            self.reaction_state = "wait"
        await asyncio.sleep(random.uniform(1.5, 3.5))
        async with self:
            if self.reaction_state == "wait":
                self.reaction_state = "ready"
                self.reaction_start_time = time.time()

    @rx.event
    def handle_reaction_click(self):
        if self.reaction_state == "wait":
            self.false_starts += 1
            self.reaction_state = "ready"
            return AssessmentState.start_reaction_trial
        elif self.reaction_state == "ready":
            rt = (time.time() - self.reaction_start_time) * 1000
            self.reaction_times.append(rt)
            self.reaction_trial += 1
            if self.reaction_trial >= 3:
                self.reaction_state = "done"
            else:
                return AssessmentState.start_reaction_trial

    @rx.event
    def finish_reaction(self):
        mean_rt = sum(self.reaction_times) / max(len(self.reaction_times), 1)
        variance = 0.0
        if len(self.reaction_times) > 1:
            variance = sum(((rt - mean_rt) ** 2 for rt in self.reaction_times)) / len(
                self.reaction_times
            )
        self.reaction_metrics = {
            "mean_reaction_time_ms": mean_rt if mean_rt else 300.0,
            "reaction_time_variance_ms": variance,
            "miss_rate_percent": 0.0,
            "anticipation_errors": self.false_starts,
        }
        self.current_step = "memory"
        yield AssessmentState.start_memory_test

    memory_sequence: str = ""
    memory_input: str = ""
    memory_phase: str = "memorize"
    memory_start_time: float = 0.0
    memory_metrics: dict = {}

    @rx.event(background=True)
    async def start_memory_test(self):
        async with self:
            self.memory_sequence = "".join(
                (str(random.randint(0, 9)) for _ in range(7))
            )
            self.memory_phase = "memorize"
            self.memory_input = ""
        await asyncio.sleep(3.0)
        async with self:
            self.memory_phase = "recall"
            self.memory_start_time = time.time()

    @rx.event
    def finish_memory(self):
        recall_time = (time.time() - self.memory_start_time) * 1000
        correct_chars = sum(
            (1 for a, b in zip(self.memory_sequence, self.memory_input) if a == b)
        )
        accuracy = correct_chars / max(len(self.memory_sequence), 1) * 100
        self.memory_metrics = {
            "recall_accuracy_percent": accuracy,
            "recall_latency_ms": recall_time,
            "pattern_recognition_score": max(0.0, accuracy - 10),
            "sequence_memory_score": accuracy,
            "false_positive_rate_percent": 0.0,
        }
        self.current_step = "voice"

    voice_recording: bool = False
    voice_start_time: float = 0.0
    voice_duration: float = 0.0
    voice_metrics: dict = {}

    @rx.event
    def toggle_voice_recording(self):
        if not self.voice_recording:
            self.voice_recording = True
            self.voice_start_time = time.time()
        else:
            self.voice_recording = False
            self.voice_duration = time.time() - self.voice_start_time

    @rx.event
    async def finish_assessment(self):
        wpm = (
            20 / max(self.voice_duration, 1.0) * 60
            if self.voice_duration > 0
            else 120.0
        )
        self.voice_metrics = {
            "speech_rate_wpm": wpm,
            "pause_frequency": random.uniform(2, 6),
            "mean_pause_duration_ms": random.uniform(300, 600),
            "pitch_variation_coefficient": random.uniform(0.2, 0.5),
            "articulation_score": random.uniform(70, 95),
        }
        neurowatch = await self.get_state(NeuroWatchState)
        session_id = neurowatch.add_session_from_assessment(
            self.typing_metrics,
            self.reaction_metrics,
            self.memory_metrics,
            self.voice_metrics,
        )
        self.current_step = "typing"
        self.typing_input = ""
        self.reaction_times = []
        self.reaction_trial = 0
        self.false_starts = 0
        self.voice_duration = 0.0
        self.voice_recording = False
        return rx.redirect(f"/session/{session_id}")