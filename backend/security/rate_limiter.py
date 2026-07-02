from fastapi import Request, HTTPException
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_limit: int = 10, window_seconds: int = 60):
        """
        Simple IP-based Rate Limiter.
        Allows 'requests_limit' requests per 'window_seconds' per client IP.
        """
        self.limit = requests_limit
        self.window = window_seconds
        # Maps ip -> list of timestamps
        self.history = defaultdict(list)

    def check_rate_limit(self, request: Request):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        
        # Clean up expired timestamps and prune empty keys to prevent memory leaks.
        # If an IP has not made requests within the sliding window, we pop its key completely 
        # from the dictionary. This keeps the in-memory cache size strictly bounded to active 
        # clients only, preventing unbounded memory growth under high IP churn.
        for ip in list(self.history.keys()):
            self.history[ip] = [
                t for t in self.history[ip]
                if now - t < self.window
            ]
            if not self.history[ip]:
                self.history.pop(ip, None)
        
        if len(self.history[client_ip]) >= self.limit:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {self.limit} requests per {self.window} seconds."
            )
            
        self.history[client_ip].append(now)

# Create a global instance for dependency injection
limiter = RateLimiter(requests_limit=10, window_seconds=60)
