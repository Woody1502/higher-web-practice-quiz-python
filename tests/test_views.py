import pytest
from http import HTTPStatus
from django.urls import reverse


@pytest.mark.django_db
class TestCategoryAPI:
    def test_create_and_get_category(self, client, category_create_get_url) -> None:
        """Тест создания и получения категории"""

        response = client.post(
            category_create_get_url,
            {'title': 'History'},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.CREATED

        response = client.get(category_create_get_url)
        assert response.status_code == HTTPStatus.OK
        assert response.json()[0]['title'] == 'History'

    def test_list_put_delete_category(self, client, category_create_get_url) -> None:
        """Тест получения списка, редактирования и удаления категории"""

        response = client.post(
            category_create_get_url,
            {'title': 'History'},
            content_type='application/json'
        )
        category_id = response.json()['id']
        list_put_delete_url = reverse('category-detail', kwargs={'pk': category_id})
        response = client.get(
            list_put_delete_url,
        )
        assert response.status_code == HTTPStatus.OK

        response = client.put(list_put_delete_url,
                              {'title': 'Cars'},
                                content_type='application/json')
        assert response.status_code == HTTPStatus.OK
        assert response.json()['title'] == 'Cars'

        response = client.delete(list_put_delete_url)
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_create_invalid_data_category(self, client, category_create_get_url) -> None:
        """Тест с неправильныйми данными (дублирование) категории"""

        response = client.post(
            category_create_get_url,
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

        response = client.post(
            category_create_get_url,
            {'title': 'History'},
            content_type='application/json'
        )
        response = client.post(
            category_create_get_url,
            {'title': 'History'},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_title_len_category(self, client, category_create_get_url) -> None:
        """Тест с неправильными данными(длина поля title) категории"""

        response = client.post(
            category_create_get_url,
            {'title': 'History'*1000},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_not_found(self, client) -> None:
        """Тест с неверным id"""

        list_put_delete_url = reverse('category-detail', kwargs={'pk': 1})

        response = client.get(list_put_delete_url)

        assert response.status_code == HTTPStatus.NOT_FOUND

        response = client.put(list_put_delete_url,
                              {'title': 'Cars'},
                                content_type='application/json')
        assert response.status_code == HTTPStatus.NOT_FOUND

        response = client.delete(list_put_delete_url,
                              {'title': 'Cars'},
                                content_type='application/json')
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
class TestQuizAPI:
    def test_create_and_get_quiz(self, client, quiz_create_get_url) -> None:
        """Тест создания и получения квиза"""

        response = client.post(
            quiz_create_get_url,
            {'title': 'Football',
             'description': 'football description'},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.CREATED

        response = client.post(
            quiz_create_get_url,
            {'title': 'Baseball'},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.CREATED
        response = client.get(quiz_create_get_url)
        assert response.status_code == HTTPStatus.OK
        assert response.json()[0]['title'] == 'Baseball'

    def test_list_put_delete_quiz(self, client, quiz_create_get_url) -> None:
        """Тест получения списка, редактирования и удаления квиза"""

        response = client.post(
            quiz_create_get_url,
            {'title': 'Football'},
            content_type='application/json'
        )
        quiz_id = response.json()['id']
        list_put_delete_url = reverse('quiz-detail', kwargs={'pk': quiz_id})
        response = client.get(
            list_put_delete_url,
        )
        assert response.status_code == HTTPStatus.OK

        response = client.put(list_put_delete_url,
                              {'title': 'Cars'},
                                content_type='application/json')
        assert response.status_code == HTTPStatus.OK
        assert response.json()['title'] == 'Cars'

        response = client.delete(list_put_delete_url)
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_create_invalid_data_quiz(self, client, quiz_create_get_url) -> None:
        """Тест с неправильныйми данными (дублирование) квиза"""

        response = client.post(
            quiz_create_get_url,
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

        response = client.post(
            quiz_create_get_url,
            {'title': 'Football'},
            content_type='application/json'
        )
        response = client.post(
            quiz_create_get_url,
            {'title': 'Football'},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_title_desc_len_quiz(self, client, quiz_create_get_url) -> None:
        """Тест с неправильными данными(длина полей title и description) категории"""

        response = client.post(
            quiz_create_get_url,
            {'title': 'History'*1000},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

        response = client.post(
            quiz_create_get_url,
            {'title': 'Maths',
             'description': 'qwerty123'*31415},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
    
    def test_not_found(self, client) -> None:
        """Тест с неверным id"""
        
        list_put_delete_url = reverse('quiz-detail', kwargs={'pk': 1})

        response = client.get(list_put_delete_url)

        assert response.status_code == HTTPStatus.NOT_FOUND

        response = client.put(list_put_delete_url,
                              {'title': 'History of country',
                               'description': 'description'},
                                content_type='application/json')
        assert response.status_code == HTTPStatus.NOT_FOUND

        response = client.delete(list_put_delete_url,
                              {'title': 'Cars'},
                                content_type='application/json')
        assert response.status_code == HTTPStatus.NOT_FOUND

        quiz_random_url = reverse('quiz-random-question', kwargs={'id': 100})

        response = client.get(quiz_random_url)

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
class TestQuestionAPI:
    def test_create_and_get_question(self,
                                     client,
                                     question_response,
                                     question_create_get_url,) -> None:
        """Тест создания и получения вопроса"""
        
        assert question_response.status_code == HTTPStatus.CREATED

        response = client.get(question_create_get_url)
        assert response.status_code == HTTPStatus.OK

    def test_list_put_delete_question(self,
                                     client,
                                     question_response,) -> None:
        """Тест получения списка, редактирования и удаления вопроса"""

        assert question_response.status_code == HTTPStatus.CREATED
        question_id = question_response.json()['id']
        quiz_id = question_response.json()['quiz_id']
        category_id = question_response.json()['category_id']
        list_put_delete_url = reverse('question-detail', kwargs={'pk': question_id})
        response = client.put(list_put_delete_url,
                            {'quiz_id': quiz_id,
                            'category_id': category_id,
                            'text': 'text2',
                            'description': 'description2',
                            'options': ["1", "2", "3"],
                            'correct_answer': "2",
                            'explanation': 'explanation2',
                            'difficulty': 'easy'
                            },
                                content_type='application/json')
        assert response.status_code == HTTPStatus.OK
        assert response.json()['text'] == 'text2'

        response = client.delete(list_put_delete_url)
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_check_answer_endpoint(self,
                                     client,
                                     question_response) -> None:
        """Тест проверки ответа на вопрос"""
        
        question_id = question_response.json()['id']
        
        check_url = reverse('question-check-answer', kwargs={'id': question_id})
        response = client.post(
            check_url,
            {'answer': '1'},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get('answer') == True
        
        response = client.post(
            check_url,
            {'answer': '3'},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json().get('answer') == False

    def test_search_questions_by_text(self,
                                     client,
                                     category_create_get_url,
                                     quiz_create_get_url) -> None:
        """Тест поиска вопросов по тексту"""
        response = client.post(
            quiz_create_get_url,
            {'title': 'Search Test Quiz'},
            content_type='application/json'
        )
        quiz_id = response.json()['id']
        
        response = client.post(
            category_create_get_url,
            {'title': 'Search Category'},
            content_type='application/json'
        )
        category_id = response.json()['id']
    
        url = reverse('question-list')

        response = client.post(
            url,
            {
            'quiz_id': quiz_id,
            'category_id': category_id,
            'text': 'текст',
            'description': 'описание',
            'options': ['1', '2', '3'],
            'correct_answer': '2',
            'explanation': 'объяснение',
            'difficulty': 'easy'
        },
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.CREATED
        
        search_url = reverse('question-by-text', kwargs={'text': 'екст'})
        response = client.get(search_url)
        assert response.status_code == HTTPStatus.OK
        results = response.json()
        assert len(results) >= 1
        assert 'екст' in results[0]['text']

    def test_search_quiz_by_title(self, client, quiz_create_get_url) -> None:
        """Тест поиска квизов по названию"""
        response = client.post(
            quiz_create_get_url,
            {'title': 'Search Test Quiz'},
            content_type='application/json'
        )
        
        search_url = reverse('quiz-by-title', kwargs={'title': 'Search'})
        response = client.get(search_url)
        assert response.status_code == HTTPStatus.OK
        results = response.json()
        assert len(results) >= 1
        assert 'Search' in results[0]['title']

    def test_question_with_minimal_options(self, client):
        """Тест: вопрос с минимальным количеством вариантов """
        response = client.post(
            reverse('quiz-list'),
            {'title': 'Search Test Quiz'},
            content_type='application/json'
        )
        quiz_id = response.json()['id']
        
        response = client.post(
            reverse('category-list'),
            {'title': 'Search Category'},
            content_type='application/json'
        )
        category_id = response.json()['id']
    
        url = reverse('question-list')

        response = client.post(
            url,
            {
            'quiz_id': quiz_id,
            'category_id': category_id,
            'text': 'текст',
            'description': 'описание',
            'options': ['1'],
            'correct_answer': '1',
            'explanation': 'объяснение',
            'difficulty': 'easy'
        },
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_question_difficulty_validation(self, client):
        """Тест значения поля difficulty"""
        response = client.post(
            reverse('quiz-list'),
            {'title': 'Search Test Quiz'},
            content_type='application/json'
        )
        quiz_id = response.json()['id']
        
        response = client.post(
            reverse('category-list'),
            {'title': 'Search Category'},
            content_type='application/json'
        )
        category_id = response.json()['id']
    
        url = reverse('question-list')

        response = client.post(
            url,
            {
            'quiz_id': quiz_id,
            'category_id': category_id,
            'text': 'текст',
            'description': 'описание',
            'options': ['1', '2'],
            'correct_answer': '1',
            'explanation': 'объяснение',
            'difficulty': 'not easy'
        },
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_not_found(self, client,
                       category_create_get_url,
                       quiz_create_get_url,
                       question_create_get_url) -> None:
        """Тест с неверным id"""

        response = client.post(
            quiz_create_get_url,
            {'title': 'History of country',
             'description': 'description'},
            content_type='application/json'
        )
        quiz_id = response.json()['id']
        response = client.post(
                category_create_get_url,
                {'title': 'History',
                'description': 'description'},
                content_type='application/json'
            )
        category_id = response.json()['id']
        response = client.post(
                question_create_get_url,
                {'quiz_id': quiz_id,
                'category_id': category_id,
                'text': 'text',
                'description': 'description',
                'options': ["1", "2"],
                'correct_answer': "1",
                'explanation': 'explanation',
                'difficulty': 'easy'
                },
                content_type='application/json')
    
        list_put_delete_url = reverse('question-detail', kwargs={'pk': 100})

        response = client.get(list_put_delete_url)

        assert response.status_code == HTTPStatus.NOT_FOUND

        response = client.put(list_put_delete_url,
                               {'quiz_id': quiz_id,
                               'category_id': category_id,
                               'text': 'text',
                               'description': 'description',
                               'options': ["1", "2"],
                               'correct_answer': "2",
                               'explanation': 'explanation',
                               'difficulty': 'easy'
                            },
                                content_type='application/json')
        assert response.status_code == HTTPStatus.NOT_FOUND

        response = client.delete(list_put_delete_url,
                                content_type='application/json')
        assert response.status_code == HTTPStatus.NOT_FOUND