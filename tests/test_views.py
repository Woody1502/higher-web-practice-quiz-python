import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestCategoryAPI:
    def test_create_and_get_category(self, client) -> None:
        """Тест создания и получения категории"""

        create_get_url = reverse('category-list')
        response = client.post(
            create_get_url,
            {'title': 'History'},
            content_type='application/json'
        )
        assert response.status_code == 201

        response = client.get(create_get_url)
        assert response.status_code == 200
        assert response.json()[0]['title'] == 'History'

    def test_list_put_delete_category(self, client) -> None:
        """Тест получения списка, редактирования и удаления категории"""

        create_get_url = reverse('category-list')
        response = client.post(
            create_get_url,
            {'title': 'History'},
            content_type='application/json'
        )
        category_id = response.json()['id']
        list_put_delete_url = reverse('category-detail', kwargs={'pk': category_id})
        response = client.get(
            list_put_delete_url,
        )
        assert response.status_code == 200

        response = client.put(list_put_delete_url,
                              {'title': 'Cars'},
                                content_type='application/json')
        assert response.status_code == 200
        assert response.json()['title'] == 'Cars'

        response = client.delete(list_put_delete_url)
        assert response.status_code == 204

    def test_create_invalid_data_category(self, client) -> None:
        """Тест с неправильныйми данными (дублирование) категории"""

        create_get_url = reverse('category-list')
        response = client.post(
            create_get_url,
            content_type='application/json'
        )
        assert response.status_code == 400

        response = client.post(
            create_get_url,
            {'title': 'History'},
            content_type='application/json'
        )
        response = client.post(
            create_get_url,
            {'title': 'History'},
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_title_len_category(self, client) -> None:
        """Тест с неправильными данными(длина поля title) категории"""

        create_get_url = reverse('category-list')
        response = client.post(
            create_get_url,
            {'title': 'History'*1000},
            content_type='application/json'
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestQuizAPI:
    def test_create_and_get_quiz(self, client) -> None:
        """Тест создания и получения квиза"""

        create_get_url = reverse('quiz-list')
        response = client.post(
            create_get_url,
            {'title': 'Football',
             'description': 'football description'},
            content_type='application/json'
        )
        assert response.status_code == 201

        response = client.post(
            create_get_url,
            {'title': 'Baseball'},
            content_type='application/json'
        )
        assert response.status_code == 201
        response = client.get(create_get_url)
        assert response.status_code == 200
        assert response.json()[0]['title'] == 'Baseball'

    def test_list_put_delete_quiz(self, client) -> None:
        """Тест получения списка, редактирования и удаления квиза"""

        create_get_url = reverse('quiz-list')
        response = client.post(
            create_get_url,
            {'title': 'Football'},
            content_type='application/json'
        )
        quiz_id = response.json()['id']
        list_put_delete_url = reverse('quiz-detail', kwargs={'pk': quiz_id})
        response = client.get(
            list_put_delete_url,
        )
        assert response.status_code == 200

        response = client.put(list_put_delete_url,
                              {'title': 'Cars'},
                                content_type='application/json')
        assert response.status_code == 200
        assert response.json()['title'] == 'Cars'

        response = client.delete(list_put_delete_url)
        assert response.status_code == 204

    def test_create_invalid_data_quiz(self, client) -> None:
        """Тест с неправильныйми данными (дублирование) квиза"""

        create_get_url = reverse('quiz-list')
        response = client.post(
            create_get_url,
            content_type='application/json'
        )
        assert response.status_code == 400

        response = client.post(
            create_get_url,
            {'title': 'Football'},
            content_type='application/json'
        )
        response = client.post(
            create_get_url,
            {'title': 'Football'},
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_title_desc_len_quiz(self, client) -> None:
        """Тест с неправильными данными(длина полей title и description) категории"""

        create_get_url = reverse('quiz-list')
        response = client.post(
            create_get_url,
            {'title': 'History'*1000},
            content_type='application/json'
        )
        assert response.status_code == 400

        response = client.post(
            create_get_url,
            {'title': 'Maths',
             'description': 'qwerty123'*31415},
            content_type='application/json'
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestQuestionAPI:
    def test_create_and_get_question(self, client) -> None:
        """Тест создания и получения вопроса"""
        
        create_get_url = reverse('quiz-list')
        response = client.post(
            create_get_url,
            {'title': 'History of country',
             'description': 'description'},
            content_type='application/json'
        )
        quiz_id = response.json()['id']
        create_get_url = reverse('category-list')
        response = client.post(
            create_get_url,
            {'title': 'History',
             'description': 'description'},
            content_type='application/json'
        )
        category_id = response.json()['id']
        create_get_url = reverse('question-list')
        response = client.post(
            create_get_url,
            {'quiz_id': quiz_id,
             'category_id': category_id,
             'text': 'text',
             'description': 'description',
             'options': ["1", "2"],
             'correct_answer': "1",
             'explanation': 'explanation',
             'difficulty': 'easy'
             },
            content_type='application/json'
        )
        assert response.status_code == 201

        response = client.get(create_get_url)
        assert response.status_code == 200

    def test_list_put_delete_question(self, client) -> None:
        """Тест получения списка, редактирования и удаления вопроса"""

        create_get_url = reverse('quiz-list')
        response = client.post(
            create_get_url,
            {'title': 'History of country',
             'description': 'description'},
            content_type='application/json'
        )

        quiz_id = response.json()['id']

        create_get_url = reverse('category-list')
        response = client.post(
            create_get_url,
            {'title': 'History',
             'description': 'description'},
            content_type='application/json'
        )

        category_id = response.json()['id']

        create_get_url = reverse('question-list')
        response = client.post(
            create_get_url,
            {'quiz_id': quiz_id,
             'category_id': category_id,
             'text': 'text',
             'description': 'description',
             'options': ["1", "2"],
             'correct_answer': "1",
             'explanation': 'explanation',
             'difficulty': 'easy'
             },
            content_type='application/json'
        )
        assert response.status_code == 201
        question_id = response.json()['id']
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
        assert response.status_code == 200
        assert response.json()['text'] == 'text2'

        response = client.delete(list_put_delete_url)
        assert response.status_code == 204

    def test_check_answer_endpoint(self, client) -> None:
        """Тест проверки ответа на вопрос"""
        
        response = client.post(
            reverse('quiz-list'),
            {'title': 'Test Quiz'},
            content_type='application/json'
        )
        quiz_id = response.json()['id']
        
        response = client.post(
            reverse('category-list'),
            {'title': 'Test Category'},
            content_type='application/json'
        )
        category_id = response.json()['id']
        
        response= client.post(
            reverse('question-list'),
            {
                'quiz_id': quiz_id,
                'category_id': category_id,
                'text': 'text',
                'description': 'description',
                'options': ['1', '2', '3', '4'],
                'correct_answer': '2',
                'explanation': 'explanation',
                'difficulty': 'medium'
            },
            content_type='application/json'
        )
        question_id = response.json()['id']
        
        check_url = reverse('question-check-answer', kwargs={'id': question_id})
        response = client.post(
            check_url,
            {'answer': '2'},
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json().get('answer') == True
        
        response = client.post(
            check_url,
            {'answer': '3'},
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json().get('answer') == False

    def test_search_questions_by_text(self, client) -> None:
        """Тест поиска вопросов по тексту"""
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
            'options': ['1', '2', '3'],
            'correct_answer': '2',
            'explanation': 'объяснение',
            'difficulty': 'easy'
        },
            content_type='application/json'
        )
        assert response.status_code == 201
        
        search_url = reverse('question-by-text', kwargs={'text': 'екст'})
        response = client.get(search_url)
        assert response.status_code == 200
        results = response.json()
        assert len(results) >= 1
        assert 'екст' in results[0]['text']

    def test_search_quiz_by_title(self, client) -> None:
        """Тест поиска квизов по названию"""
        response = client.post(
            reverse('quiz-list'),
            {'title': 'Search Test Quiz'},
            content_type='application/json'
        )
        
        search_url = reverse('quiz-by-title', kwargs={'title': 'Search'})
        response = client.get(search_url)
        assert response.status_code == 200
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
        assert response.status_code == 400

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
        assert response.status_code == 400