import requests
import unittest
import json

BASE_URL = "http://127.0.0.1:8000"

# Тестирование API с добавлением данных и последующим их удалением

class TestAPI(unittest.TestCase):

    def assertStatus(self, response, expected_code):
        """ Функция обработки сообщения об ошибке, приведение к читаемому формату вывода """
        self.assertEqual(
            response.status_code,
            expected_code,
            f"Ожидался статус {expected_code}, но получен {response.status_code}. "
            f"Ответ: {json.dumps(response.json(), ensure_ascii=False)}"
        )

    def test_get_questions_list(self):
        """Получение всех вопросов"""
        response = requests.get(f"{BASE_URL}/questions/")
        self.assertEqual(response.status_code, 200)

    def test_create_question(self):
        """Создание нового вопроса"""
        data = {
            "text": "Test message"
        }
        response = requests.post(f"{BASE_URL}/questions/", json = data)
        self.assertStatus(response, 200)
        q_id = response.json()["question"]["id"]
        requests.delete(f"{BASE_URL}/questions/{q_id}")

    def test_get_question(self):
        """Получение вопроса и ответов на него"""
        question_id = 29
        response = requests.get(f"{BASE_URL}/questions/{question_id}")
        self.assertStatus(response, 200)

    def test_get_wrong_question(self):
        """Получение вопроса, которого не существует"""
        question_id = 999
        response = requests.get(f"{BASE_URL}/questions/{question_id}")
        self.assertStatus(response, 404)

    def test_delete_question(self):
        """Удаление вопроса"""
        data = {
            "text": "Test message"
        }
        create_response = requests.post(f"{BASE_URL}/questions/", json = data)
        self.assertStatus(create_response, 200)
        id = create_response.json()["question"]["id"]
        response = requests.delete(f"{BASE_URL}/questions/{id}")
        self.assertStatus(response, 200)

    def test_delete_wrong_question(self):
        """Удаление вопроса"""
        id = 999
        response = requests.delete(f"{BASE_URL}/questions/{id}")
        self.assertStatus(response, 404)

    def test_get_answer(self):
        """Получение корректного ответа"""
        question_data = {
            "text": "Test message"
        }
        create_question = requests.post(f"{BASE_URL}/questions/", json = question_data)
        self.assertStatus(create_question, 200)
        q_id = create_question.json()["question"]["id"]
        answer_data = {
            "text": "Test Message",
            "user_id": "testid"
        }
        create_answer = requests.post(f"{BASE_URL}/questions/{q_id}/answers/", json = answer_data)
        self.assertStatus(create_answer, 200)
        a_id = create_answer.json()["answer"]["id"]
        response = requests.get(f"{BASE_URL}/answers/{a_id}")
        self.assertStatus(response, 200)

        requests.delete(f"{BASE_URL}/answers/{a_id}")
        requests.delete(f"{BASE_URL}/questions/{q_id}")

    def test_get_wrong_answer(self):
        """Получение ответа с неверным ID"""
        a_id = 999
        response = requests.get(f"{BASE_URL}/answers/{a_id}")
        self.assertStatus(response, 404)

    def test_delete_answer(self):
        """Удаление ответа"""
        question_data = {
            "text": "Test message"
        }
        create_question = requests.post(f"{BASE_URL}/questions/", json = question_data)
        self.assertStatus(create_question, 200)
        q_id = create_question.json()["question"]["id"]
        answer_data = {
            "text": "Test Message",
            "user_id": "testid"
        }
        create_answer = requests.post(f"{BASE_URL}/questions/{q_id}/answers/", json = answer_data)
        self.assertStatus(create_answer, 200)
        a_id = create_answer.json()["answer"]["id"]
        response = requests.delete(f"{BASE_URL}/answers/{a_id}")
        self.assertStatus(response, 200)
        requests.delete(f"{BASE_URL}/answers/{a_id}")
        requests.delete(f"{BASE_URL}/questions/{q_id}")

    def test_delete_wrong_answer(self):
        """Удаление несуществующего ответа"""
        a_id = 999
        response = requests.delete(f"{BASE_URL}/answers/{a_id}")
        self.assertStatus(response, 404)

    def test_create_answer(self):
        """Добавление ответа"""
        question_data = {
            "text": "Test message"
        }
        create_question = requests.post(f"{BASE_URL}/questions/", json = question_data)
        self.assertStatus(create_question, 200)
        q_id = create_question.json()["question"]["id"]
        answer_data = {
            "text": "Test Message",
            "user_id": "testid"
        }
        create_answer = requests.post(f"{BASE_URL}/questions/{q_id}/answers/", json = answer_data)
        self.assertStatus(create_answer, 200)

        a_id = create_answer.json()["answer"]["id"]
        requests.delete(f"{BASE_URL}/answers/{a_id}")
        requests.delete(f"{BASE_URL}/questions/{q_id}")

    def test_create_second_answer_by_user(self):
        """Добавление ответа"""
        question_data = {
            "text": "Test message"
        }
        create_question = requests.post(f"{BASE_URL}/questions/", json = question_data)
        self.assertStatus(create_question, 200)
        q_id = create_question.json()["question"]["id"]
        answer_data = {
            "text": "Test Message",
            "user_id": "testid"
        }
        create_answer = requests.post(f"{BASE_URL}/questions/{q_id}/answers/", json = answer_data)
        self.assertStatus(create_answer, 200)
        a_id = create_answer.json()["answer"]["id"]
        create_second_answer = requests.post(f"{BASE_URL}/questions/{q_id}/answers/", json = answer_data)
        self.assertStatus(create_second_answer, 400)


        requests.delete(f"{BASE_URL}/answers/{a_id}")
        requests.delete(f"{BASE_URL}/questions/{q_id}")


if __name__ == "__main__":
    unittest.main()