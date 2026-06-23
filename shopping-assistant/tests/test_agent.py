import pytest
from app.agent import redeem_discount_code, DISCOUNT_CODES

@pytest.fixture(autouse=True)
def reset_discount_codes():
    """Reset the in-memory discount codes before each test."""
    for code in DISCOUNT_CODES:
        DISCOUNT_CODES[code]["used"] = False

def test_redeem_valid_discount_code():
    """Verify that a valid discount code is successfully redeemed."""
    result = redeem_discount_code("user123", "WELCOME50")
    assert "Success" in result
    assert "user123" in result
    assert DISCOUNT_CODES["WELCOME50"]["used"] is True

def test_redeem_discount_code_case_insensitive():
    """Verify that discount codes are case-insensitive."""
    result = redeem_discount_code("user123", "summer20")
    assert "Success" in result
    assert "user123" in result
    assert DISCOUNT_CODES["SUMMER20"]["used"] is True

def test_redeem_invalid_discount_code():
    """Verify that an invalid discount code is rejected."""
    result = redeem_discount_code("user123", "INVALIDCODE")
    assert "Error" in result
    assert "invalid" in result

def test_redeem_already_used_discount_code():
    """Verify that a discount code cannot be redeemed twice (prevent replay)."""
    # First redemption should succeed
    result1 = redeem_discount_code("user123", "WELCOME50")
    assert "Success" in result1

    # Second redemption should fail
    result2 = redeem_discount_code("user456", "WELCOME50")
    assert "Error" in result2
    assert "already been redeemed" in result2

def test_identity_spoofing_vulnerability_demonstration():
    """
    Demonstrate that the tool currently lacks identity boundaries.
    Any string can be passed as a user_id, allowing spoofing.
    This serves as an outcome-based security test highlighting the need
    for strict session context validation instead of trusting inputs.
    """
    # A malicious user can pass another user's ID
    result = redeem_discount_code("admin_user", "SUMMER20")
    assert "Success" in result
    assert "admin_user" in result
    assert DISCOUNT_CODES["SUMMER20"]["used"] is True
