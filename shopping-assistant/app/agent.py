# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from pydantic import BaseModel, Field

import os

# Simulated in-memory store for single-use discount codes
DISCOUNT_CODES = {"WELCOME50": {"used": False}, "SUMMER20": {"used": False}}

# Simulated in-memory store for user loyalty points
USER_POINTS = {}


class AwardPointsRequest(BaseModel):
    user_id: str = Field(..., description="The ID of the registered user.")
    points: int = Field(
        ...,
        gt=0,
        le=10000,
        description="The number of points to award (must be between 1 and 10000).",
    )


def redeem_discount_code(user_id: str, code: str) -> str:
    """Redeems a single-use discount code for a registered user.

    Args:
        user_id: The ID of the registered user.
        code: The discount code to redeem (e.g., WELCOME50).

    Returns:
        A string indicating the success or failure of the redemption.
    """
    code_upper = code.upper()
    if code_upper not in DISCOUNT_CODES:
        return f"Error: Discount code '{code}' is invalid."

    if DISCOUNT_CODES[code_upper]["used"]:
        return f"Error: Discount code '{code}' has already been redeemed."

    DISCOUNT_CODES[code_upper]["used"] = True
    return f"Success: Discount code '{code}' has been redeemed for user {user_id}."


def award_loyalty_points(request: AwardPointsRequest) -> str:
    """Awards loyalty points to a user's account.

    Args:
        request: The AwardPointsRequest containing user_id and points.

    Returns:
        A string indicating the success of the point award.
    """
    user_id = request.user_id
    points = request.points

    if user_id not in USER_POINTS:
        USER_POINTS[user_id] = 0

    USER_POINTS[user_id] += points
    return f"Success: {points} loyalty points have been awarded to user {user_id}. Total balance: {USER_POINTS[user_id]}."


root_agent = Agent(
    name="shopping_assistant",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are an AI shopping assistant for a retail store. You can help users redeem single-use discount codes and award loyalty points.",
    tools=[redeem_discount_code, award_loyalty_points],
)

app = App(
    root_agent=root_agent,
    name="app",
)
