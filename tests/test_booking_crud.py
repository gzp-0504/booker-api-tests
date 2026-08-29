import allure
import pytest
import requests


# ========== 数据驱动：多组测试数据 ==========

booking_test_data = [
    pytest.param(
        {"firstname": "Jim", "lastname": "Brown", "totalprice": 111, "depositpaid": True,
         "bookingdates": {"checkin": "2023-01-01", "checkout": "2023-01-05"}, "additionalneeds": "Breakfast"},
        id="正常数据-Jim"
    ),
    pytest.param(
        {"firstname": "张三", "lastname": "李四", "totalprice": 999, "depositpaid": False,
         "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"}, "additionalneeds": "Late Checkout"},
        id="正常数据-中文名"
    ),
    pytest.param(
        {"firstname": "A", "lastname": "B", "totalprice": 0, "depositpaid": True,
         "bookingdates": {"checkin": "2023-12-01", "checkout": "2023-12-02"}, "additionalneeds": ""},
        id="边界数据-最小值"
    ),
]


@allure.feature("预订管理")
@allure.story("创建预订")
@allure.title("创建预订 - {booking_data[firstname]} {booking_data[lastname]}")
@pytest.mark.smoke
@pytest.mark.booking
@pytest.mark.parametrize("booking_data", booking_test_data)
def test_create_booking(client, booking_data):
    """发送创建请求 → httpbin 回显数据 → 断言返回 200 且字段一致"""
    with allure.step("发送POST请求创建booking"):
        resp = client.create_booking(booking_data)
        allure.attach(str(booking_data), name="请求体", attachment_type=allure.attachment_type.JSON)
        allure.attach(resp.text, name="响应体", attachment_type=allure.attachment_type.JSON)

    with allure.step("校验响应状态码为200"):
        assert resp.status_code == 200

    with allure.step("校验返回的firstname与请求一致"):
        body = resp.json()
        assert body["json"]["firstname"] == booking_data["firstname"]


@allure.feature("预订管理")
@allure.story("查询预订")
@pytest.mark.smoke
@pytest.mark.booking
def test_get_booking(client):
    """查询请求 → 断言返回 200"""
    booking_id = 1
    get_resp = client.get_booking(booking_id)
    assert get_resp.status_code == 200


@allure.feature("预订管理")
@allure.story("更新预订")
@allure.title("更新预订 - 修改姓名和价格")
@pytest.mark.regression
@pytest.mark.booking
def test_update_booking(client, sample_booking):
    """更新请求 → 断言返回 200"""
    booking_id = 1
    updated = sample_booking.copy()
    updated["firstname"] = "James"
    updated["totalprice"] = 999

    with allure.step("发送PUT请求更新booking"):
        update_resp = client.update_booking(booking_id, updated)
        allure.attach(str(updated), name="更新数据", attachment_type=allure.attachment_type.JSON)

    assert update_resp.status_code == 200


@allure.feature("预订管理")
@allure.story("删除预订")
@allure.title("删除预订 - 校验返回200")
@pytest.mark.regression
@pytest.mark.booking
def test_delete_booking(client):
    """删除请求 → 断言返回 200"""
    booking_id = 1
    delete_resp = client.delete_booking(booking_id)
    assert delete_resp.status_code == 200


@allure.feature("预订管理")
@allure.story("异常场景")
@allure.title("不传token创建预订")
@pytest.mark.regression
def test_create_booking_without_auth(sample_booking):
    """不传 token 创建 → 仍然能发请求（httpbin 不校验鉴权）"""
    resp = requests.post(
        "https://httpbin.org/post",
        json=sample_booking,
        timeout=10
    )
    assert resp.status_code == 200