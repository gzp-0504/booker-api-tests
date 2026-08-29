import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://httpbin.org")

# httpbin.org 的端点（它不支持真正的 booking API，我们用 /post 模拟）
BOOKING_ENDPOINT = f"{BASE_URL}/post"
AUTH_ENDPOINT = f"{BASE_URL}/post"