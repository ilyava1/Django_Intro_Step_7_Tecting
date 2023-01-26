import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_a_course(client, course_factory):
    """
    Функция проверки получения курса по его идентификатору
    """
    # Arrange
    course_factory(_quantity=10)

    # Act
    response = client.get('/courses/1/')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == 1


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    """
    Функция проверки получения списка курсов
    """
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get('/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for index, value in enumerate(data):
        assert value['name'] == courses[index].name


@pytest.mark.django_db
def test_filter_by_id(client, course_factory):
    """
    Функция проверки фильтрации курса по его идентификатору
    """
    # Arrange
    Course.objects.create(id=1, name='Статистика')
    Course.objects.create(id=2, name='Макроэкономика')

    # Act
    response = client.get('/courses/?id=1')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == 1


@pytest.mark.django_db
def test_filter_by_name(client, course_factory):
    """
    Функция проверки фильтрации курса по его имени
    """
    # Arrange
    Course.objects.create(id=1, name='Статистика')
    Course.objects.create(id=2, name='Макроэкономика')

    # Act
    response = client.get('/courses/?name=Макроэкономика')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['name'] == 'Макроэкономика'


@pytest.mark.django_db
def test_create_course(client):
    """
    Функция проверки создания курса
    """
    # Act
    response = client.post('/courses/', data={'name': 'Микроэкономика'},
                           format='json')

    # Assert
    data = response.json()
    assert response.status_code == 201
    assert Course.objects.count() == 1
    assert data['name'] == 'Микроэкономика'


@pytest.mark.django_db
def test_patch_course(client):
    """
    Функция проверки обновления курса
    """
    # Arrange
    Course.objects.create(id=1, name='Статистика')
    Course.objects.create(id=2, name='Микроэкономика')

    # Act
    response = client.patch('/courses/2/', data={'name': 'Ми-и-икроэкономика'
                                                 }, format='json')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == 'Ми-и-икроэкономика'


@pytest.mark.django_db
def test_delete_course(client):
    """
    Функция проверки удаления курса
    """
    # Arrange
    Course.objects.create(id=1, name='Статистика')
    Course.objects.create(id=2, name='Микроэкономика')

    # Act
    response = client.delete('/courses/2/')

    # Assert
    assert response.status_code == 204
