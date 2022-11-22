
import base64
from collections import OrderedDict
from datetime import datetime
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from freezegun import freeze_time
from helpdesk.models import CustomField, Queue, Ticket
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.exceptions import ErrorDetail
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN
)
from rest_framework.test import APITestCase


class TicketTest(APITestCase):
    due_date = datetime(2022, 4, 10, 15, 6)

    @classmethod
    def setUpTestData(cls):
        cls.queue = Queue.objects.create(
            title='Test Queue',
            slug='test-queue',
        )

    def test_create_api_ticket_not_authenticated_user(self):
        response = self.client.post('/api/tickets/')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_api_ticket_authenticated_non_staff_user(self):
        non_staff_user = User.objects.create_user(username='test')
        self.client.force_authenticate(non_staff_user)
        response = self.client.post('/api/tickets/')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_api_ticket_no_data(self):
        staff_user = User.objects.create_user(username='test', is_staff=True)
        self.client.force_authenticate(staff_user)
        response = self.client.post('/api/tickets/')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'queue': [ErrorDetail(string='This field is required.', code='required')],
            'title': [ErrorDetail(string='This field is required.', code='required')]
        })
        self.assertFalse(Ticket.objects.exists())

    def test_create_api_ticket_wrong_date_format(self):
        staff_user = User.objects.create_user(username='test', is_staff=True)
        self.client.force_authenticate(staff_user)
        response = self.client.post('/api/tickets/', {
            'queue': self.queue.id,
            'title': 'Test title',
            'due_date': 'monday, 1st of may 2022'
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'due_date': [ErrorDetail(string='Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', code='invalid')]
        })
        self.assertFalse(Ticket.objects.exists())

    def test_create_api_ticket_authenticated_staff_user(self):
        staff_user = User.objects.create_user(username='test', is_staff=True)
        self.client.force_authenticate(staff_user)
        response = self.client.post('/api/tickets/', {
            'queue': self.queue.id,
            'title': 'Test title',
            'description': 'Test description\nMulti lines',
            'submitter_email': 'test@mail.com',
            'priority': 4
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        created_ticket = Ticket.objects.get()
        self.assertEqual(created_ticket.title, 'Test title')
        self.assertEqual(created_ticket.description,
                         'Test description\nMulti lines')
        self.assertEqual(created_ticket.submitter_email, 'test@mail.com')
        self.assertEqual(created_ticket.priority, 4)
        self.assertEqual(created_ticket.followup_set.count(), 1)

    def test_create_api_ticket_with_basic_auth(self):
        username = 'admin'
        password = 'admin'
        User.objects.create_user(
            username=username, password=password, is_staff=True)

        test_user = User.objects.create_user(username='test')
        merge_ticket = Ticket.objects.create(
            queue=self.queue, title='merge ticket')

        # Generate base64 credentials string
        credentials = f"{username}:{password}"
        base64_credentials = base64.b64encode(credentials.encode(
            HTTP_HEADER_ENCODING)).decode(HTTP_HEADER_ENCODING)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Basic {base64_credentials}")
        response = self.client.post(
            '/api/tickets/',
            {
                'queue': self.queue.id,
                'title': 'Title',
                'description': 'Description',
                'resolution': 'Resolution',
                'assigned_to': test_user.id,
                'submitter_email': 'test@mail.com',
                'status': Ticket.RESOLVED_STATUS,
                'priority': 1,
                'on_hold': True,
                'due_date': self.due_date,
                'merged_to': merge_ticket.id
            }
        )

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        created_ticket = Ticket.objects.last()
        self.assertEqual(created_ticket.title, 'Title')
        self.assertEqual(created_ticket.description, 'Description')
        # resolution can not be set on creation
        self.assertIsNone(created_ticket.resolution)
        self.assertEqual(created_ticket.assigned_to, test_user)
        self.assertEqual(created_ticket.submitter_email, 'test@mail.com')
        self.assertEqual(created_ticket.priority, 1)
        # on_hold is False on creation
        self.assertFalse(created_ticket.on_hold)
        # status is always open on creation
        self.assertEqual(created_ticket.status, Ticket.OPEN_STATUS)
        self.assertEqual(created_ticket.due_date, self.due_date)
        # merged_to can not be set on creation
        self.assertIsNone(created_ticket.merged_to)

    def test_edit_api_ticket(self):
        staff_user = User.objects.create_user(username='admin', is_staff=True)
        test_ticket = Ticket.objects.create(
            queue=self.queue, title='Test ticket')

        test_user = User.objects.create_user(username='test')
        merge_ticket = Ticket.objects.create(
            queue=self.queue, title='merge ticket')

        self.client.force_authenticate(staff_user)
        response = self.client.put(
            '/api/tickets/%d/' % test_ticket.id,
            {
                'queue': self.queue.id,
                'title': 'Title',
                'description': 'Description',
                'resolution': 'Resolution',
                'assigned_to': test_user.id,
                'submitter_email': 'test@mail.com',
                'status': Ticket.RESOLVED_STATUS,
                'priority': 1,
                'on_hold': True,
                'due_date': self.due_date,
                'merged_to': merge_ticket.id
            }
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        test_ticket.refresh_from_db()
        self.assertEqual(test_ticket.title, 'Title')
        self.assertEqual(test_ticket.description, 'Description')
        self.assertEqual(test_ticket.resolution, 'Resolution')
        self.assertEqual(test_ticket.assigned_to, test_user)
        self.assertEqual(test_ticket.submitter_email, 'test@mail.com')
        self.assertEqual(test_ticket.priority, 1)
        self.assertTrue(test_ticket.on_hold)
        self.assertEqual(test_ticket.status, Ticket.RESOLVED_STATUS)
        self.assertEqual(test_ticket.due_date, self.due_date)
        self.assertEqual(test_ticket.merged_to, merge_ticket)

    def test_partial_edit_api_ticket(self):
        staff_user = User.objects.create_user(username='admin', is_staff=True)
        test_ticket = Ticket.objects.create(
            queue=self.queue, title='Test ticket')

        self.client.force_authenticate(staff_user)
        response = self.client.patch(
            '/api/tickets/%d/' % test_ticket.id,
            {
                'description': 'New description',
            }
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        test_ticket.refresh_from_db()
        self.assertEqual(test_ticket.description, 'New description')

    def test_delete_api_ticket(self):
        staff_user = User.objects.create_user(username='admin', is_staff=True)
        test_ticket = Ticket.objects.create(
            queue=self.queue, title='Test ticket')
        self.client.force_authenticate(staff_user)
        response = self.client.delete('/api/tickets/%d/' % test_ticket.id)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(Ticket.objects.exists())

    @freeze_time('2022-06-30 23:09:44')
    def test_create_api_ticket_with_custom_fields(self):
        # Create custom fields
        for field_type, field_display in CustomField.DATA_TYPE_CHOICES:
            extra_data = {}
            if field_type in ('varchar', 'text'):
                extra_data['max_length'] = 10
            if field_type == 'integer':
                # Set one field as required to test error if not provided
                extra_data['required'] = True
            if field_type == 'decimal':
                extra_data['max_length'] = 7
                extra_data['decimal_places'] = 3
            if field_type == 'list':
                extra_data['list_values'] = '''Green
                Blue
                Red
                Yellow'''
            CustomField.objects.create(
                name=field_type, label=field_display, data_type=field_type, **extra_data)

        staff_user = User.objects.create_user(username='test', is_staff=True)
        self.client.force_authenticate(staff_user)

        # Test creation without providing required field
        response = self.client.post('/api/tickets/', {
            'queue': self.queue.id,
            'title': 'Test title',
            'description': 'Test description\nMulti lines',
            'submitter_email': 'test@mail.com',
            'priority': 4
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'custom_integer': [ErrorDetail(
            string='This field is required.', code='required')]})

        # Test creation with custom field values
        response = self.client.post('/api/tickets/', {
            'queue': self.queue.id,
            'title': 'Test title',
            'description': 'Test description\nMulti lines',
            'submitter_email': 'test@mail.com',
            'priority': 4,
            'custom_varchar': 'test',
            'custom_text': 'multi\nline',
            'custom_integer': '1',
            'custom_decimal': '42.987',
            'custom_list': 'Red',
            'custom_boolean': True,
            'custom_date': '2022-4-11',
            'custom_time': '23:59:59',
            'custom_datetime': '2022-4-10 18:27',
            'custom_email': 'email@test.com',
            'custom_url': 'http://django-helpdesk.readthedocs.org/',
            'custom_ipaddress': '127.0.0.1',
            'custom_slug': 'test-slug',
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        # Check all fields with data returned from the response
        self.assertEqual(response.data, {
            'id': 1,
            'queue': 1,
            'title': 'Test title',
            'description': 'Test description\nMulti lines',
            'resolution': None,
            'submitter_email': 'test@mail.com',
            'assigned_to': None,
            'status': 1,
            'on_hold': False,
            'priority': 4,
            'due_date': None,
            'merged_to': None,
            'followup_set': [OrderedDict([
                ('id', 1),
                ('ticket', 1),
                ('date', '2022-06-30T23:09:44'),
                ('title', 'Ticket Opened'),
                ('comment', 'Test description\nMulti lines'),
                ('public', True),
                ('user', 1),
                ('new_status', None),
                ('message_id', None),
                ('time_spent', None),
                ('followupattachment_set', [])
            ])],
            'custom_varchar': 'test',
            'custom_text': 'multi\nline',
            'custom_integer': 1,
            'custom_decimal': '42.987',
            'custom_list': 'Red',
            'custom_boolean': True,
            'custom_date': '2022-04-11',
            'custom_time': '23:59:59',
            'custom_datetime': '2022-04-10T18:27',
            'custom_email': 'email@test.com',
            'custom_url': 'http://django-helpdesk.readthedocs.org/',
            'custom_ipaddress': '127.0.0.1',
            'custom_slug': 'test-slug'
        })

    def test_create_api_ticket_with_attachment(self):
        staff_user = User.objects.create_user(username='test', is_staff=True)
        self.client.force_authenticate(staff_user)
        test_file = SimpleUploadedFile(
            'file.jpg', b'file_content', content_type='image/jpg')
        response = self.client.post('/api/tickets/', {
            'queue': self.queue.id,
            'title': 'Test title',
            'description': 'Test description\nMulti lines',
            'submitter_email': 'test@mail.com',
            'priority': 4,
            'attachment': test_file
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        created_ticket = Ticket.objects.get()
        self.assertEqual(created_ticket.title, 'Test title')
        self.assertEqual(created_ticket.description,
                         'Test description\nMulti lines')
        self.assertEqual(created_ticket.submitter_email, 'test@mail.com')
        self.assertEqual(created_ticket.priority, 4)
        self.assertEqual(created_ticket.followup_set.count(), 1)
        self.assertEqual(created_ticket.followup_set.get(
        ).followupattachment_set.count(), 1)
        attachment = created_ticket.followup_set.get().followupattachment_set.get()
        self.assertEqual(
            attachment.file.name,
            f'helpdesk/attachments/test-queue-1-{created_ticket.secret_key}/1/file.jpg'
        )

    def test_create_follow_up_with_attachments(self):
        staff_user = User.objects.create_user(username='test', is_staff=True)
        self.client.force_authenticate(staff_user)
        ticket = Ticket.objects.create(queue=self.queue, title='Test')
        test_file_1 = SimpleUploadedFile(
            'file.jpg', b'file_content', content_type='image/jpg')
        test_file_2 = SimpleUploadedFile(
            'doc.pdf', b'Doc content', content_type='application/pdf')

        response = self.client.post('/api/followups/', {
            'ticket': ticket.id,
            'title': 'Test',
            'comment': 'Test answer\nMulti lines',
            'attachments': [
                test_file_1,
                test_file_2
            ]
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        created_followup = ticket.followup_set.last()
        self.assertEqual(created_followup.title, 'Test')
        self.assertEqual(created_followup.comment, 'Test answer\nMulti lines')
        self.assertEqual(created_followup.followupattachment_set.count(), 2)
        self.assertEqual(
            created_followup.followupattachment_set.first().filename, 'doc.pdf')
        self.assertEqual(
            created_followup.followupattachment_set.first().mime_type, 'application/pdf')
        self.assertEqual(
            created_followup.followupattachment_set.last().filename, 'file.jpg')
        self.assertEqual(
            created_followup.followupattachment_set.last().mime_type, 'image/jpg')
