import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from tasks.models import Category, Task


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass123')


@pytest.fixture
def client_logged_in(user):
    client = Client()
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def category(user, db):
    return Category.objects.create(name='Work', color='#ff0000', created_by=user)


@pytest.mark.django_db
def test_user_registration():
    client = Client()
    response = client.post(reverse('register'), {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'Str0ngP@ss!',
        'password2': 'Str0ngP@ss!',
    })
    assert response.status_code == 302
    assert User.objects.filter(username='newuser').exists()


@pytest.mark.django_db
def test_task_create(client_logged_in, user, category):
    response = client_logged_in.post(reverse('task_create'), {
        'title': 'Test Task',
        'description': 'A test task description',
        'status': 'todo',
        'priority': 'medium',
        'category': category.pk,
    })
    assert response.status_code == 302
    assert Task.objects.filter(title='Test Task', created_by=user).exists()


@pytest.mark.django_db
def test_dashboard_requires_login():
    client = Client()
    response = client.get(reverse('dashboard'))
    assert response.status_code == 302
    assert '/accounts/login/' in response['Location']


@pytest.mark.django_db
def test_task_update(client_logged_in, user, category):
    task = Task.objects.create(title='Old Title', status='todo', priority='low', created_by=user)
    response = client_logged_in.post(reverse('task_update', args=[task.pk]), {
        'title': 'Updated Title',
        'status': 'done',
        'priority': 'high',
    })
    assert response.status_code == 302
    task.refresh_from_db()
    assert task.title == 'Updated Title'
    assert task.status == 'done'


@pytest.mark.django_db
def test_task_delete(client_logged_in, user):
    task = Task.objects.create(title='To Delete', status='todo', priority='low', created_by=user)
    task_pk = task.pk
    response = client_logged_in.post(reverse('task_delete', args=[task_pk]))
    assert response.status_code == 302
    assert not Task.objects.filter(pk=task_pk).exists()


@pytest.mark.django_db
def test_category_model_str(user, db):
    cat = Category.objects.create(name='Personal', created_by=user)
    assert str(cat) == 'Personal'


@pytest.mark.django_db
def test_task_belongs_to_user(client_logged_in, user, db):
    other_user = User.objects.create_user(username='other', password='pass123')
    task = Task.objects.create(title='Other Task', status='todo', priority='low', created_by=other_user)
    response = client_logged_in.get(reverse('task_detail', args=[task.pk]))
    assert response.status_code == 404
