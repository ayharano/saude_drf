from datetime import UTC, date, datetime

import factory
from django.urls import reverse
from rest_framework.test import APITestCase

from api.constants import (
    APPOINTMENT_DATE_ERROR_MESSAGE,
    UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_ERROR_MESSAGE,
)
from api.models import Appointment
from api.tests.models.factories import AppointmentFactory, HealthCareWorkerFactory


INITIAL_APPOINTMENTS_COUNT = 3


CONTENT_TYPE = 'content-type'
APPLICATION_JSON = 'application/json'


class AppointmentsViewSetTestCase(APITestCase):
    def setUp(self):
        self.existing_appointments = AppointmentFactory.create_batch(INITIAL_APPOINTMENTS_COUNT)
        self.existing_hcw = self.existing_appointments[0].health_care_worker

    def test_create_appointment(self):
        # Adapted from
        # https://factoryboy.readthedocs.io/en/stable/recipes.html#converting-a-factory-s-output-to-a-dict
        # Generated input data using a factory
        appointment_as_dict = factory.build(dict, FACTORY_CLASS=AppointmentFactory)
        request_data = {
            'profissional_uuid': str(self.existing_hcw.uuid),
            'data': appointment_as_dict['date'].isoformat(),
            'info': appointment_as_dict['info'],
        }

        url = reverse("api:appointments-list")
        response = self.client.post(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)

        instance = Appointment.objects.filter(
            health_care_worker__uuid=request_data['profissional_uuid'],
            date=appointment_as_dict['date'],
            info=appointment_as_dict['info'],
        ).order_by('-created').first()
        expected_response_data = request_data | {'uuid': str(instance.uuid)}

        self.assertEqual(response_data, expected_response_data)

    def test_fail_create_appointment_for_existing_date_and_health_care_worker(self):
        conflicting_instance = self.existing_appointments[-1]
        request_data = {
            'profissional_uuid': str(conflicting_instance.health_care_worker.uuid),
            'data': conflicting_instance.date.isoformat(),
            'info': 'This will fail',
        }
        expected_response_data = {
            'non_field_errors': [
                UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_ERROR_MESSAGE,
            ],
        }

        url = reverse("api:appointments-list")
        response = self.client.post(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_fail_create_appointment_for_today_or_earlier(self):
        request_data = {
            'profissional_uuid': str(self.existing_hcw.uuid),
            'data': '2010-11-12',
            'info': 'This will fail',
        }
        expected_response_data = {
            'data': [
                APPOINTMENT_DATE_ERROR_MESSAGE,
            ],
        }

        url = reverse("api:appointments-list")
        response = self.client.post(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_list_appointments(self):
        url = reverse("api:appointments-list")
        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(list(response_data), ['data'])
        self.assertEqual(len(response_data['data']), len(self.existing_appointments))

    def test_list_appointments_filtered_by_profissional_uuid(self):
        new_hcw = HealthCareWorkerFactory()
        # Create 3 appointments for the new Health Care Worker
        AppointmentFactory.create_batch(3, health_care_worker=new_hcw)

        url = reverse("api:appointments-list")
        response = self.client.get(
            url,
            data={
                'profissional_uuid': str(new_hcw.uuid),
            },
            format='json',
        )
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(list(response_data), ['data'])
        self.assertEqual(len(response_data['data']), 3)
        self.assertGreater(Appointment.objects.count(), 3)

    def test_detail_appointment(self):
        chosen_instance = self.existing_appointments[INITIAL_APPOINTMENTS_COUNT-1]
        expected_response_data = {
            'uuid': str(chosen_instance.uuid),
            'profissional_uuid': str(chosen_instance.health_care_worker.uuid),
            'data': chosen_instance.date.isoformat(),
            'info': chosen_instance.info,
        }

        url = reverse("api:appointments-detail", args=[chosen_instance.uuid])
        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_fail_detail_appointment_for_non_existing_instance(self):
        non_existing_instance_uuid = '01234567-89ab-cdef-0123-456789abcdef'
        expected_response_data = {'detail': 'Not found.'}

        url = reverse("api:appointments-detail", args=[non_existing_instance_uuid])
        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_full_update_appointment(self):
        chosen_instance = self.existing_appointments[0]
        id_ = chosen_instance.id
        uuid_ = chosen_instance.uuid
        created = chosen_instance.created
        last_modified = chosen_instance.modified
        new_hcw = self.existing_appointments[-1].health_care_worker
        request_data = {
            'profissional_uuid': str(new_hcw.uuid),
            'data': "2137-11-07",
            'info': "Very far in the future",
        }
        expected_response_data = request_data | {'uuid': str(uuid_)}

        url = reverse("api:appointments-detail", args=[str(uuid_)])
        before = datetime.now(UTC)
        response = self.client.put(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

        chosen_instance.refresh_from_db()
        self.assertEqual(chosen_instance.id, id_)
        self.assertEqual(chosen_instance.uuid, uuid_)
        self.assertEqual(chosen_instance.created, created)
        self.assertGreater(before, last_modified)
        self.assertGreater(chosen_instance.modified, before)
        self.assertEqual(chosen_instance.health_care_worker, new_hcw)
        self.assertEqual(chosen_instance.date, date(year=2137, month=11, day=7))
        self.assertEqual(chosen_instance.info, "Very far in the future")

    def test_fail_full_update_appointment_for_non_existing_instance(self):
        non_existing_instance_uuid = '01234567-89ab-cdef-0123-456789abcdef'
        request_data = {
            'profissional_uuid': str(self.existing_hcw.uuid),
            'data': "2137-11-07",
            'info': "Very far in the future",
        }
        expected_response_data = {'detail': 'Not found.'}

        url = reverse("api:appointments-detail", args=[non_existing_instance_uuid])
        response = self.client.put(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_fail_full_update_appointment_for_existing_date_and_health_care_worker(self):
        chosen_instance = self.existing_appointments[0]
        id_ = chosen_instance.id
        uuid_ = chosen_instance.uuid
        last_modified = chosen_instance.modified
        conflicting_instance = self.existing_appointments[-1]
        request_data = {
            'profissional_uuid': str(conflicting_instance.health_care_worker.uuid),
            'data': conflicting_instance.date.isoformat(),
            'info': "Very far in the future",
        }
        expected_response_data = {
            'non_field_errors': [
                UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_ERROR_MESSAGE,
            ],
        }

        url = reverse("api:appointments-detail", args=[str(uuid_)])
        before = datetime.now(UTC)
        response = self.client.put(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

        chosen_instance.refresh_from_db()
        self.assertEqual(chosen_instance.id, id_)
        self.assertEqual(chosen_instance.uuid, uuid_)
        self.assertEqual(chosen_instance.modified, last_modified)

    def test_fail_full_update_appointment_for_today_or_earlier(self):
        chosen_instance = self.existing_appointments[0]
        id_ = chosen_instance.id
        uuid_ = chosen_instance.uuid
        last_modified = chosen_instance.modified
        request_data = {
            'profissional_uuid': str(chosen_instance.health_care_worker.uuid),
            'data': datetime.now(UTC).date().isoformat(),
            'info': "No appointment for today or earlier",
        }
        expected_response_data = {
            'data': [
                APPOINTMENT_DATE_ERROR_MESSAGE,
            ],
        }

        url = reverse("api:appointments-detail", args=[str(uuid_)])
        response = self.client.put(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_partial_update_appointment(self):
        chosen_instance = self.existing_appointments[0]
        id_ = chosen_instance.id
        uuid_ = chosen_instance.uuid
        created = chosen_instance.created
        last_modified = chosen_instance.modified
        request_data = {
            'data': '2101-02-03',
        }
        expected_response_data = {
            'uuid': str(chosen_instance.uuid),
            'profissional_uuid': str(chosen_instance.health_care_worker.uuid),
            'data': '2101-02-03',
            'info': chosen_instance.info,
        }

        url = reverse("api:appointments-detail", args=[chosen_instance.uuid])
        before = datetime.now(UTC)
        response = self.client.patch(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

        chosen_instance.refresh_from_db()
        self.assertEqual(chosen_instance.id, id_)
        self.assertEqual(chosen_instance.uuid, uuid_)
        self.assertEqual(chosen_instance.created, created)
        self.assertGreater(before, last_modified)
        self.assertGreater(chosen_instance.modified, before)
        self.assertEqual(chosen_instance.date.isoformat(), '2101-02-03')

    def test_fail_partial_update_appointment_for_non_existing_instance(self):
        non_existing_instance_uuid = '01234567-89ab-cdef-0123-456789abcdef'
        request_data = {
            'data': '2091-02-03',
        }
        expected_response_data = {'detail': 'Not found.'}

        url = reverse("api:appointments-detail", args=[non_existing_instance_uuid])
        response = self.client.patch(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_fail_partial_update_appointment_for_existing_date_and_health_care_worker(self):
        chosen_instance = self.existing_appointments[-1]
        id_ = chosen_instance.id
        uuid_ = chosen_instance.uuid
        last_modified = chosen_instance.modified
        conflicting_instance = self.existing_appointments[0]
        request_data = {
            'profissional_uuid': str(conflicting_instance.health_care_worker.uuid),
            'data': conflicting_instance.date.isoformat(),
        }
        expected_response_data = {
            'non_field_errors': [
                UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_ERROR_MESSAGE,
            ],
        }

        url = reverse("api:appointments-detail", args=[str(uuid_)])
        before = datetime.now(UTC)
        response = self.client.patch(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

        chosen_instance.refresh_from_db()
        self.assertEqual(chosen_instance.id, id_)
        self.assertEqual(chosen_instance.uuid, uuid_)
        self.assertEqual(chosen_instance.modified, last_modified)

    def test_fail_partial_update_appointment_for_today_or_earlier(self):
        chosen_instance = self.existing_appointments[0]
        id_ = chosen_instance.id
        uuid_ = chosen_instance.uuid
        last_modified = chosen_instance.modified
        request_data = {
            'data': datetime.now(UTC).date().isoformat(),
        }
        expected_response_data = {
            'data': [
                APPOINTMENT_DATE_ERROR_MESSAGE,
            ],
        }

        url = reverse("api:appointments-detail", args=[str(uuid_)])
        response = self.client.patch(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

        chosen_instance.refresh_from_db()
        self.assertEqual(chosen_instance.id, id_)
        self.assertEqual(chosen_instance.uuid, uuid_)
        self.assertEqual(chosen_instance.modified, last_modified)

    def test_delete_update_appointment(self):
        chosen_instance = self.existing_appointments[1]
        expected_response_data = b''

        url = reverse("api:appointments-detail", args=[chosen_instance.uuid])
        before = datetime.now(UTC)
        response = self.client.delete(url, format='json')
        response_data = response.content

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response_data, expected_response_data)

        with self.assertRaisesRegex(
            Appointment.DoesNotExist,
            'Appointment matching query does not exist',
        ):
            chosen_instance.refresh_from_db()

    def test_fail_delete_appointment_for_non_existing_instance(self):
        non_existing_instance_uuid = '01234567-89ab-cdef-0123-456789abcdef'
        expected_response_data = {'detail': 'Not found.'}

        url = reverse("api:appointments-detail", args=[non_existing_instance_uuid])
        response = self.client.delete(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)
