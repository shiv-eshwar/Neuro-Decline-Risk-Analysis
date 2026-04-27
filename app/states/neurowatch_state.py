import reflex as rx
from typing import TypedDict, Optional
from datetime import datetime, timedelta
import random
import uuid


class TypingMetrics(TypedDict):
    speed_wpm: float
    keystroke_interval_variance_ms: float
    error_rate_percent: float
    backspace_frequency: float
    key_hold_duration_ms: float


class ReactionMetrics(TypedDict):
    mean_reaction_time_ms: float
    reaction_time_variance_ms: float
    miss_rate_percent: float
    anticipation_errors: int


class MemoryMetrics(TypedDict):
    recall_accuracy_percent: float
    recall_latency_ms: float
    pattern_recognition_score: float
    sequence_memory_score: float
    false_positive_rate_percent: float


class VoiceMetrics(TypedDict):
    speech_rate_wpm: float
    pause_frequency: float
    mean_pause_duration_ms: float
    pitch_variation_coefficient: float
    articulation_score: float


class SessionData(TypedDict):
    session_id: str
    session_number: int
    timestamp: str
    typing: TypingMetrics
    reaction: ReactionMetrics
    memory: MemoryMetrics
    voice: VoiceMetrics


class DomainScore(TypedDict):
    name: str
    score: int
    trend: str
    flags: int
    flag_list: list[str]
    key_observation: str
    risk_color: str


class AnalysisResult(TypedDict):
    session_id: str
    risk_score: int
    risk_level: str
    domain_scores: dict[str, DomainScore]
    personalized_summary: str
    positive_indicators: list[str]
    areas_to_watch: list[str]
    lifestyle_recommendations: list[str]
    alerts: list[str]


class UserProfile(TypedDict):
    name: str
    age: int
    caregiver_contact: str
    avatar_url: str


def generate_mock_session(session_number: int, is_baseline: bool) -> SessionData:
    deg = 0 if is_baseline else (session_number - 7) * 0.05
    if deg < 0:
        deg = 0
    return {
        "session_id": str(session_number),
        "session_number": session_number,
        "timestamp": (
            datetime.now() - timedelta(days=(12 - session_number) * 7)
        ).strftime("%Y-%m-%d"),
        "typing": {
            "speed_wpm": max(20.0, 45.0 * (1 - deg * 0.8)),
            "keystroke_interval_variance_ms": 45.0 * (1 + deg * 1.5),
            "error_rate_percent": 2.5 * (1 + deg),
            "backspace_frequency": 1.2 * (1 + deg),
            "key_hold_duration_ms": 110.0 * (1 + deg * 0.5),
        },
        "reaction": {
            "mean_reaction_time_ms": 280.0 * (1 + deg * 1.2),
            "reaction_time_variance_ms": 30.0 * (1 + deg * 2.0),
            "miss_rate_percent": 1.0 * (1 + deg),
            "anticipation_errors": int(1 + deg * 4),
        },
        "memory": {
            "recall_accuracy_percent": max(40.0, 95.0 * (1 - deg * 1.5)),
            "recall_latency_ms": 1200.0 * (1 + deg),
            "pattern_recognition_score": max(30.0, 90.0 * (1 - deg)),
            "sequence_memory_score": max(20.0, 85.0 * (1 - deg * 1.2)),
            "false_positive_rate_percent": 5.0 * (1 + deg * 2.0),
        },
        "voice": {
            "speech_rate_wpm": max(80.0, 130.0 * (1 - deg * 0.5)),
            "pause_frequency": 4.0 * (1 + deg),
            "mean_pause_duration_ms": 400.0 * (1 + deg * 1.5),
            "pitch_variation_coefficient": max(0.1, 0.45 * (1 - deg)),
            "articulation_score": max(50.0, 92.0 * (1 - deg * 0.3)),
        },
    }


def perform_analysis(session: SessionData, baselines: dict) -> AnalysisResult:
    b_typ = baselines.get("typing", session["typing"])
    b_rea = baselines.get("reaction", session["reaction"])
    b_mem = baselines.get("memory", session["memory"])
    b_voc = baselines.get("voice", session["voice"])
    t = session["typing"]
    r = session["reaction"]
    m = session["memory"]
    v = session["voice"]
    t_flags = []
    if t["speed_wpm"] < b_typ["speed_wpm"] * 0.85:
        t_flags.append("Motor speed decline detected")
    if (
        t["keystroke_interval_variance_ms"]
        > b_typ["keystroke_interval_variance_ms"] * 1.25
    ):
        t_flags.append("Rhythmic disruption in typing")
    if t["error_rate_percent"] > b_typ["error_rate_percent"] * 1.25:
        t_flags.append("Increased error frequency")
    r_flags = []
    if r["mean_reaction_time_ms"] > b_rea["mean_reaction_time_ms"] * 1.15:
        r_flags.append("Processing speed reduction")
    if r["reaction_time_variance_ms"] > b_rea["reaction_time_variance_ms"] * 1.3:
        r_flags.append("Inconsistent reaction times")
    m_flags = []
    if m["recall_accuracy_percent"] < b_mem["recall_accuracy_percent"] * 0.85:
        m_flags.append("Memory recall degradation")
    if m["sequence_memory_score"] < b_mem["sequence_memory_score"] * 0.85:
        m_flags.append("Sequence memory decline")
    v_flags = []
    if v["speech_rate_wpm"] < b_voc["speech_rate_wpm"] * 0.85:
        v_flags.append("Speech rate reduction")
    if v["mean_pause_duration_ms"] > b_voc["mean_pause_duration_ms"] * 1.25:
        v_flags.append("Increased speech hesitancy")
    if v["pitch_variation_coefficient"] < b_voc["pitch_variation_coefficient"] * 0.85:
        v_flags.append("Reduced vocal prosody")

    def calc_domain_score(flags) -> int:
        if not flags:
            return 0
        pts = len(flags) * 20
        if len(flags) > 1:
            pts = int(pts * 1.3)
        return min(100, pts)

    t_score = calc_domain_score(t_flags)
    r_score = calc_domain_score(r_flags)
    m_score = calc_domain_score(m_flags)
    v_score = calc_domain_score(v_flags)
    overall_score = int(t_score * 0.25 + r_score * 0.25 + m_score * 0.3 + v_score * 0.2)
    if max([t_score, r_score, m_score, v_score]) > 50:
        overall_score = max(overall_score, 45)
    if max([t_score, r_score, m_score, v_score]) > 70:
        overall_score = max(overall_score, 65)
    overall_score = min(100, overall_score)
    if overall_score <= 25:
        level = "Low"
    elif overall_score <= 50:
        level = "Moderate"
    elif overall_score <= 70:
        level = "Elevated"
    else:
        level = "High"

    def get_color(s):
        if s <= 25:
            return "#22c55e"
        if s <= 50:
            return "#eab308"
        if s <= 70:
            return "#f97316"
        return "#ef4444"

    return {
        "session_id": session["session_id"],
        "risk_score": overall_score,
        "risk_level": level,
        "domain_scores": {
            "Typing": {
                "name": "Typing",
                "score": t_score,
                "trend": "stable" if t_score < 30 else "declining",
                "flags": len(t_flags),
                "flag_list": t_flags,
                "key_observation": "Consistent rhythm."
                if not t_flags
                else "Motor speed issues detected.",
                "risk_color": get_color(t_score),
            },
            "Reaction": {
                "name": "Reaction",
                "score": r_score,
                "trend": "stable" if r_score < 30 else "declining",
                "flags": len(r_flags),
                "flag_list": r_flags,
                "key_observation": "Quick processing."
                if not r_flags
                else "Processing delayed.",
                "risk_color": get_color(r_score),
            },
            "Memory": {
                "name": "Memory",
                "score": m_score,
                "trend": "stable" if m_score < 30 else "declining",
                "flags": len(m_flags),
                "flag_list": m_flags,
                "key_observation": "Strong recall."
                if not m_flags
                else "Recall metrics lower than baseline.",
                "risk_color": get_color(m_score),
            },
            "Voice": {
                "name": "Voice",
                "score": v_score,
                "trend": "stable" if v_score < 30 else "declining",
                "flags": len(v_flags),
                "flag_list": v_flags,
                "key_observation": "Clear prosody."
                if not v_flags
                else "Hesitancy in speech patterns.",
                "risk_color": get_color(v_score),
            },
        },
        "personalized_summary": f"Session #{session['session_number']} indicates a {level.lower()} risk profile. "
        + (
            "Significant declines noted in memory."
            if m_score > 50
            else "Baseline remains relatively stable."
        ),
        "positive_indicators": ["Completed full assessment"],
        "areas_to_watch": [
            f for dom in [t_flags, r_flags, m_flags, v_flags] for f in dom
        ][:3],
        "lifestyle_recommendations": ["Ensure 8hrs of sleep", "Stay hydrated"],
        "alerts": ["Caregiver alerted to elevated risk"] if overall_score > 50 else [],
    }


INITIAL_SESSIONS = [generate_mock_session(i, i <= 7) for i in range(1, 13)]
INITIAL_BASELINES = {
    "typing": INITIAL_SESSIONS[6]["typing"],
    "reaction": INITIAL_SESSIONS[6]["reaction"],
    "memory": INITIAL_SESSIONS[6]["memory"],
    "voice": INITIAL_SESSIONS[6]["voice"],
}
INITIAL_ANALYSIS = [perform_analysis(s, INITIAL_BASELINES) for s in INITIAL_SESSIONS]


class NeuroWatchState(rx.State):
    active_page: str = "Dashboard"
    user_profile: UserProfile = {
        "name": "Eleanor Vance",
        "age": 68,
        "caregiver_contact": "Dr. Aris (Son), +1-555-0192",
        "avatar_url": "https://api.dicebear.com/9.x/notionists/svg?seed=Eleanor",
    }
    selected_session_id: str = "12"
    search_query: str = ""
    filter_risk_level: str = "All"
    baselines: dict = INITIAL_BASELINES
    sessions: list[SessionData] = INITIAL_SESSIONS
    analysis_results: list[AnalysisResult] = INITIAL_ANALYSIS
    show_new_session_modal: bool = False
    is_simulating: bool = False

    @rx.var
    def current_session(self) -> AnalysisResult:
        if not self.analysis_results:
            return INITIAL_ANALYSIS[-1]
        return self.analysis_results[-1]

    @rx.var
    def selected_analysis(self) -> AnalysisResult:
        for a in self.analysis_results:
            if a["session_id"] == self.selected_session_id:
                return a
        return self.current_session

    @rx.var
    def selected_session_data(self) -> SessionData:
        for s in self.sessions:
            if s["session_id"] == self.selected_session_id:
                return s
        return self.sessions[-1]

    @rx.var
    def current_risk_score(self) -> int:
        return self.current_session["risk_score"]

    @rx.var
    def current_risk_color(self) -> str:
        score = self.current_risk_score
        if score <= 25:
            return "#22c55e"
        elif score <= 50:
            return "#eab308"
        elif score <= 70:
            return "#f97316"
        else:
            return "#ef4444"

    @rx.var
    def current_risk_level(self) -> str:
        return self.current_session["risk_level"]

    @rx.var
    def domain_scores_list(self) -> list[DomainScore]:
        return [
            self.current_session["domain_scores"]["Typing"],
            self.current_session["domain_scores"]["Reaction"],
            self.current_session["domain_scores"]["Memory"],
            self.current_session["domain_scores"]["Voice"],
        ]

    @rx.var
    def chart_data(self) -> list[dict[str, str | int]]:
        return [
            {"date": s["timestamp"], "score": self.analysis_results[i]["risk_score"]}
            for i, s in enumerate(self.sessions)
        ]

    @rx.var
    def table_data(self) -> list[dict[str, str | int]]:
        return [
            {
                "id": s["session_id"],
                "num": s["session_number"],
                "date": s["timestamp"],
                "score": self.analysis_results[i]["risk_score"],
                "level": self.analysis_results[i]["risk_level"],
                "signal": "Memory"
                if self.analysis_results[i]["domain_scores"]["Memory"]["flags"] > 0
                else "None",
            }
            for i, s in enumerate(self.sessions)
        ]

    @rx.var
    def filtered_sessions(self) -> list[dict[str, str | int]]:
        data = self.table_data[::-1]
        if self.search_query:
            query = self.search_query.lower()
            data = [
                row
                for row in data
                if query in str(row["id"]).lower() or query in str(row["date"]).lower()
            ]
        if self.filter_risk_level != "All":
            data = [row for row in data if row["level"] == self.filter_risk_level]
        return data

    @rx.var
    def trend_chart_data(self) -> list[dict[str, str | int]]:
        return [
            {
                "date": s["timestamp"],
                "typing": self.analysis_results[i]["domain_scores"]["Typing"]["score"],
                "reaction": self.analysis_results[i]["domain_scores"]["Reaction"][
                    "score"
                ],
                "memory": self.analysis_results[i]["domain_scores"]["Memory"]["score"],
                "voice": self.analysis_results[i]["domain_scores"]["Voice"]["score"],
            }
            for i, s in enumerate(self.sessions)
        ]

    @rx.var
    def alert_history(self) -> list[dict[str, str]]:
        history = []
        for i, res in enumerate(self.analysis_results):
            if res["risk_score"] > 50:
                history.append(
                    {
                        "date": self.sessions[i]["timestamp"],
                        "level": res["risk_level"],
                        "message": res["personalized_summary"],
                        "status": "Acknowledged"
                        if i < len(self.analysis_results) - 1
                        else "Sent",
                    }
                )
        return history[::-1]

    @rx.var
    def total_sessions(self) -> int:
        return len(self.sessions)

    @rx.var
    def current_streak(self) -> int:
        return 7

    @rx.var
    def completion_rate(self) -> str:
        return "92%"

    @rx.var
    def next_assessment_due(self) -> str:
        return "Tomorrow"

    @rx.var
    def activity_heatmap(self) -> list[dict[str, str | int]]:
        data: list[dict[str, str | int]] = []
        today = datetime.now()
        session_dates = {s["timestamp"] for s in self.sessions}
        for i in range(83, -1, -1):
            d = today - timedelta(days=i)
            ds = d.strftime("%Y-%m-%d")
            intensity = 0
            if ds in session_dates:
                intensity = random.randint(2, 4)
            else:
                intensity = random.choice([0, 0, 0, 1])
            data.append({"date": ds, "intensity": intensity})
        return data

    @rx.var
    def strongest_signal_insight(self) -> str:
        scores = [
            res["domain_scores"]["Memory"]["score"]
            for res in self.analysis_results[-4:]
        ]
        avg_decline = sum(scores) / len(scores)
        return f"Memory scores have shown a consistent {avg_decline:.0f}% average risk elevation over the last 4 sessions."

    @rx.event
    def set_active_page(self, page: str):
        self.active_page = page
        return rx.redirect(f"/{(page.lower() if page != 'Dashboard' else '')}")

    @rx.event
    def view_session(self, session_id: str):
        self.selected_session_id = session_id
        return rx.redirect(f"/session/{session_id}")

    @rx.event
    def export_sessions_csv(self):
        import io
        import csv

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            ["Session ID", "Date", "Risk Score", "Risk Level", "Strongest Signal"]
        )
        for row in self.table_data:
            writer.writerow(
                [row["num"], row["date"], row["score"], row["level"], row["signal"]]
            )
        csv_data = output.getvalue()
        return rx.download(data=csv_data, filename="neurowatch_sessions_export.csv")

    @rx.event
    def download_caregiver_report(self):
        res = self.selected_analysis
        sd = self.selected_session_data
        report = f"NEUROWATCH CLINICAL REPORT\n"
        report += f"Patient: {self.user_profile['name']}\n"
        report += f"Session ID: {res['session_id']}\n"
        report += f"Date: {sd['timestamp']}\n"
        report += f"----------------------------------\n"
        report += (
            f"Risk Profile: {res['risk_level']} (Score: {res['risk_score']}/100)\n\n"
        )
        report += f"Summary: {res['personalized_summary']}\n\n"
        report += """Domain Flags:
"""
        for d_name, d_val in res["domain_scores"].items():
            report += (
                f"- {d_name}: {d_val['flags']} flags ({d_val['key_observation']})\n"
            )
        return rx.download(
            data=report, filename=f"caregiver_report_{res['session_id']}.txt"
        )

    @rx.event
    def load_session(self):
        session_id = self.router.page.params.get("session_id", "")
        if session_id:
            self.selected_session_id = session_id

    @rx.event
    def toggle_new_session_modal(self):
        self.show_new_session_modal = not self.show_new_session_modal

    @rx.event
    async def simulate_session(self):
        self.is_simulating = True
        yield
        import asyncio

        await asyncio.sleep(1)
        new_num = len(self.sessions) + 1
        new_s = generate_mock_session(new_num, False)
        new_s["timestamp"] = datetime.now().strftime("%Y-%m-%d")
        new_a = perform_analysis(new_s, self.baselines)
        self.sessions.append(new_s)
        self.analysis_results.append(new_a)
        self.is_simulating = False
        self.show_new_session_modal = False
        self.selected_session_id = str(new_num)
        yield rx.redirect(f"/session/{new_num}")

    @rx.event
    def add_session_from_assessment(
        self,
        typing_metrics: dict,
        reaction_metrics: dict,
        memory_metrics: dict,
        voice_metrics: dict,
    ) -> str:
        new_num = len(self.sessions) + 1
        new_session: SessionData = {
            "session_id": str(new_num),
            "session_number": new_num,
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "typing": typing_metrics,
            "reaction": reaction_metrics,
            "memory": memory_metrics,
            "voice": voice_metrics,
        }
        new_analysis = perform_analysis(new_session, self.baselines)
        self.sessions.append(new_session)
        self.analysis_results.append(new_analysis)
        self.selected_session_id = str(new_num)
        return str(new_num)