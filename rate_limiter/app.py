import time

class RateLimiter:
    def __init__(self, max_requests_per_second):
        self.max_requests_per_second = max_requests_per_second
        self.request_counts = {}

    def _get_current_time(self):
        return time.time()

    def allow_request(self, user_id):
        current_time = self._get_current_time()
        
        if user_id not in self.request_counts:
            self.request_counts[user_id] = []

        self.request_counts[user_id] = [timestamp for timestamp in self.request_counts[user_id] if current_time - timestamp < 1]
        
        if len(self.request_counts[user_id]) < self.max_requests_per_second:

            self.request_counts[user_id].append(current_time)
            return True  
        else:
            return False  

# Example 
rate_limiter = RateLimiter(max_requests_per_second=5)

user_id = "user123"

print("Max rate limit:", rate_limiter.max_requests_per_second, "requests per second")
# Simulate 10 requests for the user
for _ in range(10):
    if rate_limiter.allow_request(user_id):
        print(f"Request allowed for {user_id}")
    else:
        print(f"Rate limit exceeded for {user_id}")
    time.sleep(0.1)  
