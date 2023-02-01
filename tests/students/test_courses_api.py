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
    courses = course_factory(_quantity=10)
    id = courses[0].id

    # Act
    response = client.get(f'/courses/{id}/')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == courses[0].id


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
    courses = course_factory(_quantity=10)
    id = courses[0].id

    # Act
    response = client.get(f'/courses/?id={id}')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == id


@pytest.mark.django_db
def test_filter_by_name(client, course_factory):
    """
    Функция проверки фильтрации курса по его имени
    """
    # Arrange
    courses = course_factory(_quantity=10)
    name = courses[0].name

    # Act
    response = client.get(f'/courses/?name={name}')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['name'] == name


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
def test_patch_course(client, course_factory):
    """
    Функция проверки обновления курса
    """
    # Arrange
    courses = course_factory(_quantity=10)
    id = courses[0].id

    # Act
    response = client.patch(f'/courses/{id}/', data={
        'name': 'Ми-и-икроэкономика'},
        format='json')

    # Assert
    data = response.json()
    assert 1 == 1
    assert response.status_code == 200
    assert data['name'] == 'Ми-и-икроэкономика'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    """
    Функция проверки удаления курса
    """
    # Arrange
    courses = course_factory(_quantity=10)
    id = courses[0].id

    # Act
    response = client.delete(f'/courses/{id}/')

    # Assert
    assert response.status_code == 204
