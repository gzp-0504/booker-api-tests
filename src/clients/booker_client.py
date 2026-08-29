import requests
from src.config import AUTH_ENDPOINT, BOOKING_ENDPOINT, BASE_URL


class BookerClient:
    def __init__(self):
        self.session = requests.Session()
        self.token = None

    def login(self, username="admin", password="password123"):
        """模拟登录，httpbin 会原样返回我们发的数据"""
        resp = self.session.post(
            AUTH_ENDPOINT,
            json={"username": username, "password": password},
            timeout=10
        )
        resp.raise_for_status()
        # httpbin 返回的 body 里有个 json 字段，包含我们发的内容
        body = resp.json()
        # 模拟生成一个 token
        self.token = "fake-token-123"
        return self.token

    def create_booking(self, booking_data):
        """创建预订，httpbin 会回显我们发的 JSON"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        resp = self.session.post(
            BOOKING_ENDPOINT,
            json=booking_data,
            headers=headers,
            timeout=10
        )
        return resp

    def get_booking(self, booking_id):
        """查询预订"""
        resp = self.session.get(
            f"{BASE_URL}/get",
            params={"id": booking_id},
            timeout=10
        )
        return resp

    def update_booking(self, booking_id, booking_data):
        """更新预订"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        resp = self.session.put(
            f"{BASE_URL}/put",
            json=booking_data,
            headers=headers,
            timeout=10
        )
        return resp

    def delete_booking(self, booking_id):
        """删除预订"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        resp = self.session.delete(
            f"{BASE_URL}/delete",
            headers=headers,
            timeout=10
        )
        return resp