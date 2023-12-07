import uuid
from datetime import UTC, datetime

import factory
from django.test import TestCase

from api.serializers import HealthCareWorkerSerializer
from api.serializers.health_care_worker import MODEL_TO_SERIALIZER, SERIALIZER_TO_MODEL
from api.tests.models.factories import HealthCareWorkerFactory


class HealthCareWorkerSerializerTestCase(TestCase):
    def test_health_care_worker_can_be_created_using_serializer_data(self):
        # Adapted from
        # https://factoryboy.readthedocs.io/en/stable/recipes.html#converting-a-factory-s-output-to-a-dict
        # Generated input data using a factory
        health_care_worker_as_dict = factory.build(dict, FACTORY_CLASS=HealthCareWorkerFactory)

        # Cleaning up serializer data and also filtering fields for validation
        model_fields_to_validate = []
        serializer_data = {}
        for model_field, serializer_field in MODEL_TO_SERIALIZER.items():
            missing_model_field = model_field not in health_care_worker_as_dict
            # As we are using a write serializer, we must remove any read-only fields
            read_only_field = serializer_field in HealthCareWorkerSerializer.Meta.read_only_fields

            if missing_model_field or read_only_field:
                continue

            serializer_data[serializer_field] = health_care_worker_as_dict[model_field]
            model_fields_to_validate.append(model_field)

        serializer = HealthCareWorkerSerializer(data=serializer_data, write_only=True)
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.instance)

        before = datetime.now(UTC)

        health_care_worker = serializer.save()

        self.assertIsInstance(health_care_worker.id, int)
        self.assertGreater(health_care_worker.id, 0)
        self.assertIsInstance(health_care_worker.uuid, uuid.UUID)
        self.assertGreater(health_care_worker.created, before)
        self.assertGreaterEqual(health_care_worker.modified, health_care_worker.created)

        for model_field in model_fields_to_validate:
            self.assertEqual(
                getattr(health_care_worker, model_field),
                health_care_worker_as_dict[model_field],
            )

    def test_health_care_worker_can_be_created_using_serializer_data_with_a_blank_preferred_name(self):
        # Adapted from
        # https://factoryboy.readthedocs.io/en/stable/recipes.html#converting-a-factory-s-output-to-a-dict
        # Generated input data using a factory
        health_care_worker_as_dict = factory.build(dict, FACTORY_CLASS=HealthCareWorkerFactory)
        health_care_worker_as_dict['preferred_name'] = ''

        # Cleaning up serializer data and also filtering fields for validation
        model_fields_to_validate = []
        serializer_data = {}
        for model_field, serializer_field in MODEL_TO_SERIALIZER.items():
            missing_model_field = model_field not in health_care_worker_as_dict
            # As we are using a write serializer, we must remove any read-only fields
            read_only_field = serializer_field in HealthCareWorkerSerializer.Meta.read_only_fields

            if missing_model_field or read_only_field:
                continue

            serializer_data[serializer_field] = health_care_worker_as_dict[model_field]
            model_fields_to_validate.append(model_field)

        serializer = HealthCareWorkerSerializer(data=serializer_data, write_only=True)
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.instance)

        before = datetime.now(UTC)

        health_care_worker = serializer.save()

        self.assertIsInstance(health_care_worker.id, int)
        self.assertGreater(health_care_worker.id, 0)
        self.assertIsInstance(health_care_worker.uuid, uuid.UUID)
        self.assertGreater(health_care_worker.created, before)
        self.assertGreaterEqual(health_care_worker.modified, health_care_worker.created)

        for model_field in model_fields_to_validate:
            self.assertEqual(
                getattr(health_care_worker, model_field),
                health_care_worker_as_dict[model_field],
            )

    def test_health_care_worker_can_be_retrieved_using_serializer(self):
        health_care_worker = HealthCareWorkerFactory()

        serializer = HealthCareWorkerSerializer(health_care_worker)

        manual_check = set({'date_of_birth', 'uuid'})

        # Map model fields into serializer for field validation
        for model_field, serializer_field in MODEL_TO_SERIALIZER.items():
            if model_field in manual_check:
                continue

            self.assertEqual(
                getattr(health_care_worker, model_field),
                serializer.data[serializer_field]
            )

        self.assertEqual(
            health_care_worker.date_of_birth.isoformat(),
            serializer.data['data_de_nascimento'],
        )
        self.assertEqual(
            health_care_worker.uuid,
            uuid.UUID(serializer.data['uuid']),
        )
