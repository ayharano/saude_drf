from datetime import UTC, date, datetime

import factory
from django.urls import reverse
from rest_framework.test import APITestCase

from api.models import HealthCareWorker
from api.tests.models.factories import HealthCareWorkerFactory


INITIAL_HCW_COUNT = 3


CONTENT_TYPE = 'content-type'
APPLICATION_JSON = 'application/json'


class HealthCareWorkersViewSetTestCase(APITestCase):
    def setUp(self):
        self.existing_hcw = HealthCareWorkerFactory.create_batch(INITIAL_HCW_COUNT)

    def test_create_health_care_worker(self):
        # Adapted from
        # https://factoryboy.readthedocs.io/en/stable/recipes.html#converting-a-factory-s-output-to-a-dict
        # Generated input data using a factory
        health_care_worker_as_dict = factory.build(dict, FACTORY_CLASS=HealthCareWorkerFactory)
        request_data = {
            'nome_legal': health_care_worker_as_dict['legal_name'],
            'nome_social': health_care_worker_as_dict['preferred_name'],
            'pronomes': health_care_worker_as_dict['pronouns'],
            'data_de_nascimento': health_care_worker_as_dict['date_of_birth'].isoformat(),
            'especializacao': health_care_worker_as_dict['specialization'],
        }

        url = reverse("api:health-care-workers-list")
        response = self.client.post(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)

        instance = HealthCareWorker.objects.filter(
            legal_name=health_care_worker_as_dict['legal_name'],
            preferred_name=health_care_worker_as_dict['preferred_name'],
            pronouns=health_care_worker_as_dict['pronouns'],
            date_of_birth=health_care_worker_as_dict['date_of_birth'],
            specialization=health_care_worker_as_dict['specialization'],
        ).order_by('-created').first()
        expected_response_data = request_data | {'uuid': str(instance.uuid)}

        self.assertEqual(response_data, expected_response_data)

    def test_list_health_care_workers(self):
        url = reverse("api:health-care-workers-list")
        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(list(response_data), ['data'])
        self.assertEqual(len(response_data['data']), len(self.existing_hcw))

    def test_detail_health_care_worker(self):
        chosen_instance = self.existing_hcw[INITIAL_HCW_COUNT-1]
        expected_response_data = {
            'uuid': str(chosen_instance.uuid),
            'nome_legal': chosen_instance.legal_name,
            'nome_social': chosen_instance.preferred_name,
            'pronomes': chosen_instance.pronouns,
            'data_de_nascimento': chosen_instance.date_of_birth.isoformat(),
            'especializacao': chosen_instance.specialization,
        }

        url = reverse("api:health-care-workers-detail", args=[chosen_instance.uuid])
        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_fail_detail_health_care_worker_for_non_existing_instance(self):
        non_existing_instance_uuid = '01234567-89ab-cdef-0123-456789abcdef'
        expected_response_data = {'detail': 'Not found.'}

        url = reverse("api:health-care-workers-detail", args=[non_existing_instance_uuid])
        response = self.client.get(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_full_update_health_care_worker(self):
        chosen_instance = self.existing_hcw[0]
        id_ = chosen_instance.id
        uuid_ = chosen_instance.uuid
        created = chosen_instance.created
        last_modified = chosen_instance.modified
        request_data = {
            'nome_legal': "John Ercel Fryer",
            'nome_social': "Henry Anonymous",
            'pronomes': "He/Him",
            'data_de_nascimento': "1937-11-07",
            'especializacao': "Psychiatrist",
        }
        expected_response_data = request_data | {'uuid': str(uuid_)}

        url = reverse("api:health-care-workers-detail", args=[str(uuid_)])
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
        self.assertEqual(chosen_instance.legal_name, "John Ercel Fryer")
        self.assertEqual(chosen_instance.preferred_name, "Henry Anonymous")
        self.assertEqual(chosen_instance.pronouns, "He/Him")
        self.assertEqual(chosen_instance.date_of_birth, date(year=1937, month=11, day=7))
        self.assertEqual(chosen_instance.specialization, "Psychiatrist")

    def test_fail_full_update_health_care_worker_for_non_existing_instance(self):
        non_existing_instance_uuid = '01234567-89ab-cdef-0123-456789abcdef'
        request_data = {
            'nome_legal': "John Ercel Fryer",
            'nome_social': "Henry Anonymous",
            'pronomes': "He/Him",
            'data_de_nascimento': "1937-11-07",
            'especializacao': "Psychiatrist",
        }
        expected_response_data = {'detail': 'Not found.'}

        url = reverse("api:health-care-workers-detail", args=[non_existing_instance_uuid])
        response = self.client.put(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_partial_update_health_care_worker(self):
        chosen_instance = self.existing_hcw[0]
        id_ = chosen_instance.id
        uuid_ = chosen_instance.uuid
        created = chosen_instance.created
        last_modified = chosen_instance.modified
        request_data = {
            'nome_social': 'Jane Doe',
            'pronomes': 'They/Them',
        }
        expected_response_data = {
            'uuid': str(chosen_instance.uuid),
            'nome_legal': chosen_instance.legal_name,
            'nome_social': 'Jane Doe',
            'pronomes': 'They/Them',
            'data_de_nascimento': chosen_instance.date_of_birth.isoformat(),
            'especializacao': chosen_instance.specialization,
        }

        url = reverse("api:health-care-workers-detail", args=[chosen_instance.uuid])
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
        self.assertEqual(chosen_instance.preferred_name, 'Jane Doe')
        self.assertEqual(chosen_instance.pronouns, 'They/Them')

    def test_fail_partial_update_health_care_worker_for_non_existing_instance(self):
        non_existing_instance_uuid = '01234567-89ab-cdef-0123-456789abcdef'
        request_data = {
            'nome_social': 'Jane Doe',
            'pronomes': 'They/Them',
        }
        expected_response_data = {'detail': 'Not found.'}

        url = reverse("api:health-care-workers-detail", args=[non_existing_instance_uuid])
        response = self.client.patch(url, request_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)

    def test_delete_update_health_care_worker(self):
        chosen_instance = self.existing_hcw[1]
        expected_response_data = b''

        url = reverse("api:health-care-workers-detail", args=[chosen_instance.uuid])
        before = datetime.now(UTC)
        response = self.client.delete(url, format='json')
        response_data = response.content

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response_data, expected_response_data)

        with self.assertRaisesRegex(
            HealthCareWorker.DoesNotExist,
            'HealthCareWorker matching query does not exist',
        ):
            chosen_instance.refresh_from_db()

    def test_fail_delete_health_care_worker_for_non_existing_instance(self):
        non_existing_instance_uuid = '01234567-89ab-cdef-0123-456789abcdef'
        expected_response_data = {'detail': 'Not found.'}

        url = reverse("api:health-care-workers-detail", args=[non_existing_instance_uuid])
        response = self.client.delete(url, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers[CONTENT_TYPE], APPLICATION_JSON)
        self.assertEqual(response_data, expected_response_data)
