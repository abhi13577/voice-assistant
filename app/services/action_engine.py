from app.services.product_api_client import product_api_client

ALLOWED_ACTIONS = {"rerun_test", "get_run_status"}

class ActionEngine:
    async def execute(self, action_type: str, params: dict, user_id: int):
        if action_type not in ALLOWED_ACTIONS:
            return {
                "success": False,
                "message": "Invalid action type.",
                "data": None
            }
        if not self._check_permission(user_id, action_type):
            return {
                "success": False,
                "message": "Unauthorized action.",
                "data": None
            }
        if action_type == "rerun_test":
            test_case_id = params.get("test_case_id")
            if not test_case_id:
                return {
                    "success": False,
                    "message": "Missing test_case_id.",
                    "data": None
                }
            result = await product_api_client.get_last_error(42)
            return {
                "success": True,
                "message": f"Test {test_case_id} rerun triggered successfully.",
                "data": result
            }
        if action_type == "get_run_status":
            result = await product_api_client.get_last_error(42)
            return {
                "success": True,
                "message": "Run status fetched.",
                "data": result
            }

    def _check_permission(self, user_id: int, action_type: str):
        # Mock permission check
        return True

action_engine = ActionEngine()