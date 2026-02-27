from app.services.product_api_client import product_api_client
from app.services.slot_resolver import SlotResolver


class ResponseBuilder:

    async def build(
        self,
        intent: str,
        user_id: int,
        project_id: int,
        transcript: str,
        llm_slots: dict = None
    ):

        projects = product_api_client.get_projects(user_id)
        templates = product_api_client.get_tts_templates()

        # -------- SLOT RESOLUTION --------
        if llm_slots:
            slots = llm_slots
        else:
            slot_resolver = SlotResolver(projects)
            slots = slot_resolver.resolve(transcript)

        # -------- SYSTEM INTENT --------
        if intent == "greeting":
            return (
                "Hello. I can help you check your run status or list your projects.",
                [],
                []
            )

        # -------- CHECK RUN STATUS --------
        if intent == "check_run_status":

            if slots.get("project"):
                run = product_api_client.get_last_run_by_project(
                    user_id,
                    slots["project"]
                )
            else:
                run = product_api_client.get_last_run(user_id)

            if not run:
                reply = templates["run_not_found"]
                return reply, ["run_status"], []

            project_name = next(
                p["name"] for p in projects if p["id"] == run["project_id"]
            )

            # All tests passed
            if run["failed_tests"] == 0:
                reply = templates["check_run_status_all_passed"].format(
                    project_name=project_name,
                    total_tests=run["total_tests"]
                )
            else:
                reply = templates["check_run_status_success"].format(
                    project_name=project_name,
                    passed_tests=run["passed_tests"],
                    failed_tests=run["failed_tests"],
                    status=run["status"]
                )

            return reply, ["run_status"], []

        # -------- LIST PROJECTS --------
        if intent == "list_projects":
            names = [p["name"] for p in projects]

            reply = templates["list_projects"].format(
                count=len(names),
                project_names=", ".join(names)
            )

            return reply, ["projects"], []

        # -------- LIST RUNS --------
        if intent == "list_runs":
            runs = product_api_client.get_runs(user_id)

            reply = f"You have {len(runs)} test runs."
            return reply, ["runs"], []

        # -------- FALLBACK --------
        return (
            "I didn’t understand that. You can ask about your last run or list your projects.",
            [],
            []
        )


response_builder = ResponseBuilder()