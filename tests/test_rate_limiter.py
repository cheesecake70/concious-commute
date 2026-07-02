import pytest
import time
from fastapi import Request, HTTPException
from backend.security.rate_limiter import RateLimiter

class MockRequest:
    def __init__(self, host):
        self.client = type('Client', (object,), {'host': host})()

def test_rate_limiter_basic():
    limiter = RateLimiter(requests_limit=2, window_seconds=1)
    req = MockRequest("127.0.0.1")
    
    # First request
    limiter.check_rate_limit(req)
    # Second request
    limiter.check_rate_limit(req)
    
    # Third request within window should fail
    with pytest.raises(HTTPException) as exc_info:
        limiter.check_rate_limit(req)
    assert exc_info.value.status_code == 429

def test_rate_limiter_expiry():
    limiter = RateLimiter(requests_limit=1, window_seconds=1)
    req = MockRequest("127.0.0.2")
    
    limiter.check_rate_limit(req)
    
    # Wait for window to expire
    time.sleep(1.1)
    
    # Request should succeed again
    limiter.check_rate_limit(req)

def test_rate_limiter_memory_leak_pruning():
    limiter = RateLimiter(requests_limit=5, window_seconds=1)
    req1 = MockRequest("127.0.0.3")
    req2 = MockRequest("127.0.0.4")
    
    limiter.check_rate_limit(req1)
    assert "127.0.0.3" in limiter.history
    
    time.sleep(1.1)
    
    # Running check_rate_limit on a different IP should trigger list cleanup of 127.0.0.3
    # And pop it from history because it has no active timestamps
    limiter.check_rate_limit(req2)
    assert "127.0.0.3" not in limiter.history
