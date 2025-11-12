import unittest
from unittest import mock
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

class TestAPI(unittest.TestCase):

    def setUp(self):
        patcher_get = mock.patch('requests.get')
        patcher_post = mock.patch('requests.post')
        patcher_delete = mock.patch('requests.delete')

        self.mock_get = patcher_get.start()
        self.mock_post = patcher_post.start()
        self.mock_delete = patcher_delete.start()

        self.addCleanup(patcher_get.stop)
        self.addCleanup(patcher_post.stop)
        self.addCleanup(patcher_delete.stop)

    def assertStatus(self, response, expected_code):
        self.assertEqual(
            response.status_code,
            expected_code,
            f"Ожидался статус {expected_code}, но получен {response.status_code}. "
            f"Ответ: {json.dumps(response.json(), ensure_ascii=False)}"
        )

    # GET /questions/
    def test_get_questions_list(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json.return_value = [{"id": 1, "text": "Test question"}]

        response = requests.get(f"{BASE_URL}/questions/")
        self.assertStatus(response, 200)
        self.assertEqual(response.json()[0]["id"], 1)

    # POST /questions/
    def test_create_question(self):
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.return_value = {"question": {"id": 1}}

        response = requests.post(f"{BASE_URL}/questions/", json={"text": "Test"})
        self.assertStatus(response, 200)
        self.assertEqual(response.json()["question"]["id"], 1)

    # GET /questions/{id}
    def test_get_question(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json.return_value = {"id": 1, "text": "Test question"}

        response = requests.get(f"{BASE_URL}/questions/1")
        self.assertStatus(response, 200)
        self.assertEqual(response.json()["id"], 1)

    # GET /questions/{wrong_id} -> 404
    def test_get_wrong_question(self):
        self.mock_get.return_value.status_code = 404
        self.mock_get.return_value.json.return_value = {"detail": "Not found"}

        response = requests.get(f"{BASE_URL}/questions/999")
        self.assertStatus(response, 404)

    # DELETE /questions/{id}
    def test_delete_question(self):
        self.mock_delete.return_value.status_code = 200
        self.mock_delete.return_value.json.return_value = {}

        response = requests.delete(f"{BASE_URL}/questions/1")
        self.assertStatus(response, 200)

    # DELETE /questions/{wrong_id} -> 404
    def test_delete_wrong_question(self):
        self.mock_delete.return_value.status_code = 404
        self.mock_delete.return_value.json.return_value = {"detail": "Not found"}

        response = requests.delete(f"{BASE_URL}/questions/999")
        self.assertStatus(response, 404)

    # POST /questions/{id}/answers/
    def test_create_answer(self):
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.return_value = {"answer": {"id": 1}}

        response = requests.post(f"{BASE_URL}/questions/1/answers/", json={"text": "Test", "user_id": "test"})
        self.assertStatus(response, 200)
        self.assertEqual(response.json()["answer"]["id"], 1)

    # GET /answers/{id}
    def test_get_answer(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json.return_value = {"id": 1, "text": "Test answer"}

        response = requests.get(f"{BASE_URL}/answers/1")
        self.assertStatus(response, 200)
        self.assertEqual(response.json()["id"], 1)

    # GET /answers/{wrong_id} -> 404
    def test_get_wrong_answer(self):
        self.mock_get.return_value.status_code = 404
        self.mock_get.return_value.json.return_value = {"detail": "Not found"}

        response = requests.get(f"{BASE_URL}/answers/999")
        self.assertStatus(response, 404)

    # DELETE /answers/{id}
    def test_delete_answer(self):
        self.mock_delete.return_value.status_code = 200
        self.mock_delete.return_value.json.return_value = {}

        response = requests.delete(f"{BASE_URL}/answers/1")
        self.assertStatus(response, 200)

    # DELETE /answers/{wrong_id} -> 404
    def test_delete_wrong_answer(self):
        self.mock_delete.return_value.status_code = 404
        self.mock_delete.return_value.json.return_value = {"detail": "Not found"}

        response = requests.delete(f"{BASE_URL}/answers/999")
        self.assertStatus(response, 404)

    # POST /questions/{id}/answers/ — повторная попытка добавить ответ тем же пользователем
    def test_create_second_answer_by_user(self):
        """Проверка, что пользователь не может добавить второй ответ"""

        first_response = mock.Mock()
        first_response.status_code = 200
        first_response.json.return_value = {"question": {"id": 1}}

        second_response = mock.Mock()
        second_response.status_code = 200
        second_response.json.return_value = {"answer": {"id": 10}}

        third_response = mock.Mock()
        third_response.status_code = 400
        third_response.json.return_value = {"detail": "User already answered this question"}

        self.mock_post.side_effect = [first_response, second_response, third_response]

        q_resp = requests.post(f"{BASE_URL}/questions/", json={"text": "Test"})
        self.assertStatus(q_resp, 200)
        q_id = q_resp.json()["question"]["id"]

        a_resp = requests.post(f"{BASE_URL}/questions/{q_id}/answers/", json={"text": "Hi", "user_id": "u1"})
        self.assertStatus(a_resp, 200)
        self.assertEqual(a_resp.json()["answer"]["id"], 10)

        a2_resp = requests.post(f"{BASE_URL}/questions/{q_id}/answers/", json={"text": "Again", "user_id": "u1"})
        self.assertStatus(a2_resp, 400)
        self.assertIn("User already answered", a2_resp.json()["detail"])

        self.assertEqual(self.mock_post.call_count, 3)


if __name__ == "__main__":
    unittest.main()
