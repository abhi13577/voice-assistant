from fastapi import FastAPI
from app.schemas.request import VoiceRequest
from app.schemas.response import VoiceResponse
from app.schemas.action import ActionRequest, ActionResponse

from app.services.intent_engine import intent_engine
from app.services.response_builder import response_builder
from app.services.action_engine import action_engine
from app.services.llm_fallback import llm_fallback

from app.core.logging_config import configure_logging

import time
import json
import re

logger = configure_logging()

app = FastAPI(title="Voice Support Engine")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/voice/turn", response_model=VoiceResponse)
async def voice_turn(request: VoiceRequest):

    start_time = time.time()

    # -------- STEP 1: Deterministic Intent Classification --------
    intent, confidence = intent_engine.classify(request.transcript)

    CONFIDENCE_THRESHOLD = 0.65
    llm_slots = {}

    # -------- STEP 2: LLM Fallback (Only if Low Confidence) --------
    if confidence < CONFIDENCE_THRESHOLD:
        try:
            llm_raw = llm_fallback.classify_and_extract(request.transcript)

            # -------- SAFE JSON EXTRACTION --------
            json_match = re.search(r"\{.*\}", llm_raw, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON found in LLM response")

            llm_data = json.loads(json_match.group())

            llm_intent = llm_data.get("intent")
            llm_slots = llm_data.get("slots", {}) or {}

            allowed_intents = [
                "check_run_status",
                "list_projects",
                "list_runs",
                "greeting"
            ]

            if llm_intent in allowed_intents:
                intent = llm_intent
                confidence = 0.90  # Controlled confidence after LLM
            else:
                raise ValueError("Invalid intent returned by LLM")

        except Exception as e:
            latency = round(time.time() - start_time, 3)
            logger.info(f"Escalated (LLM failed) | Latency={latency}s | Error={str(e)}")

            return VoiceResponse(
                intent="unknown",
                escalate=True,
                reply_text="I'm escalating this to L2 support.",
                suggested_actions=[],
                context_used=[],
                confidence=round(confidence, 3)
            )

    # -------- STEP 3: Logging --------
    logger.info(
        f"TRANSCRIPT='{request.transcript}' | "
        f"INTENT={intent} | "
        f"CONFIDENCE={round(confidence,3)}"
    )

    # -------- STEP 4: Build Deterministic Response --------
    reply, context_used, suggestions = await response_builder.build(
        intent,
        request.user_id,
        request.project_id,
        request.transcript,
        llm_slots
    )

    latency = round(time.time() - start_time, 3)
    logger.info(f"Response built | Latency={latency}s")

    return VoiceResponse(
        intent=intent,
        escalate=False,
        reply_text=reply,
        suggested_actions=suggestions,
        context_used=context_used,
        confidence=round(confidence, 3)
    )


@app.post("/voice/action", response_model=ActionResponse)
async def execute_action(request: ActionRequest):

    logger.info(
        f"ACTION_REQUEST | "
        f"TYPE={request.action_type} | "
        f"PARAMS={request.params}"
    )

    user_id = 1001  # demo user

    result = await action_engine.execute(
        request.action_type,
        request.params,
        user_id
    )

    logger.info(
        f"ACTION_RESULT | "
        f"SUCCESS={result['success']} | "
        f"MESSAGE={result['message']}"
    )

    return result