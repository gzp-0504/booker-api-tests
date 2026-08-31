import requests
import allure

BASE_URL = "https://restful-booker.herokuapp.com"

@allure.feature("Health Check")
class TestSample:

    @allure.story("API 可达性测试")
    def test_ping(self):
        """测试 booking 服务的 ping 接口是否返回 201"""
        response = requests.get(f"{BASE_URL}/ping")
        assert response.status_code == 201