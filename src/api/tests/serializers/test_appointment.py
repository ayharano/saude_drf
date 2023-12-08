import uuid
from datetime import UTC, datetime

import factory
from django.db.utils import IntegrityError
from django.test import TestCase

from api.constants import (
    APPOINTMENT_DATE_ERROR_MESSAGE,
    UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_ERROR_MESSAGE,
)
from api.serializers import AppointmentSerializer
from api.serializers.appointment import MODEL_TO_SERIALIZER, SERIALIZER_TO_MODEL
from api.tests.models.factories import AppointmentFactory, HealthCareWorkerFactory


class AppointmentSerializerTestCase(TestCase):
    def setUp(self):
        self.health_care_worker = HealthCareWorkerFactory()

    def test_appointment_can_be_created_using_serializer_data(self):
        # Adapted from
        # https://factoryboy.readthedocs.io/en/stable/recipes.html#converting-a-factory-s-output-to-a-dict
        # Generated input data using a factory
        appointment_as_dict = factory.build(
            dict,
            FACTORY_CLASS=AppointmentFactory,
            health_care_worker=self.health_care_worker,
        )

        # Cleaning up serializer data and also filtering fields for validation
        model_fields_to_validate = []
        serializer_data = {}
        for model_field, serializer_field in MODEL_TO_SERIALIZER.items():
            missing_model_field = model_field not in appointment_as_dict
            # As we are using a write serializer, we must remove any read-only fields
            read_only_field = serializer_field in AppointmentSerializer.Meta.read_only_fields

            if missing_model_field or read_only_field:
                continue

            serializer_data[serializer_field] = appointment_as_dict[model_field]
            model_fields_to_validate.append(model_field)

        # Custom handling fields
        serializer_data['profissional_uuid'] = str(self.health_care_worker.uuid)

        serializer = AppointmentSerializer(data=serializer_data, write_only=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIsNone(serializer.instance)

        before = datetime.now(UTC)

        appointment = serializer.save()

        self.assertIsInstance(appointment.id, int)
        self.assertGreater(appointment.id, 0)
        self.assertIsInstance(appointment.uuid, uuid.UUID)
        self.assertGreater(appointment.created, before)
        self.assertGreaterEqual(appointment.modified, appointment.created)

        for model_field in model_fields_to_validate:
            self.assertEqual(
                getattr(appointment, model_field),
                appointment_as_dict[model_field],
            )

        self.assertEqual(
            appointment.health_care_worker.uuid,
            uuid.UUID(serializer.data['profissional_uuid']),
        )

    def test_appointment_cannot_be_created_for_existing_date_and_health_care_worker_combinatation(self):
        appointment = AppointmentFactory(health_care_worker=self.health_care_worker)

        serializer = AppointmentSerializer(appointment)

        # Adapted from
        # https://factoryboy.readthedocs.io/en/stable/recipes.html#converting-a-factory-s-output-to-a-dict
        # Generated input data using a factory
        duplicate_appointment_as_dict = factory.build(
            dict,
            FACTORY_CLASS=AppointmentFactory,
            health_care_worker=self.health_care_worker,
            date=appointment.date,
        )

        # Cleaning up serializer data and also filtering fields for validation
        model_fields_to_validate = []
        serializer_data = {}
        for model_field, serializer_field in MODEL_TO_SERIALIZER.items():
            missing_model_field = model_field not in duplicate_appointment_as_dict
            # As we are using a write serializer, we must remove any read-only fields
            read_only_field = serializer_field in AppointmentSerializer.Meta.read_only_fields

            if missing_model_field or read_only_field:
                continue

            serializer_data[serializer_field] = duplicate_appointment_as_dict[model_field]
            model_fields_to_validate.append(model_field)

        # Custom handling fields
        serializer_data['profissional_uuid'] = str(self.health_care_worker.uuid)

        serializer = AppointmentSerializer(data=serializer_data, write_only=True)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(len(serializer.errors['non_field_errors']), 1)
        self.assertEqual(
            str(serializer.errors['non_field_errors'][0]),
            UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_ERROR_MESSAGE,
        )

    def test_appointment_cannot_be_created_for_today(self):
        # Adapted from
        # https://factoryboy.readthedocs.io/en/stable/recipes.html#converting-a-factory-s-output-to-a-dict
        # Generated input data using a factory
        appointment_as_dict = factory.build(
            dict,
            FACTORY_CLASS=AppointmentFactory,
            health_care_worker=self.health_care_worker,
        )

        # Cleaning up serializer data and also filtering fields for validation
        model_fields_to_validate = []
        serializer_data = {}
        for model_field, serializer_field in MODEL_TO_SERIALIZER.items():
            missing_model_field = model_field not in appointment_as_dict
            # As we are using a write serializer, we must remove any read-only fields
            read_only_field = serializer_field in AppointmentSerializer.Meta.read_only_fields

            if missing_model_field or read_only_field:
                continue

            serializer_data[serializer_field] = appointment_as_dict[model_field]
            model_fields_to_validate.append(model_field)

        # Custom handling fields
        serializer_data['profissional_uuid'] = str(self.health_care_worker.uuid)

        # Past date
        serializer_data['data'] = '2010-11-12'

        serializer = AppointmentSerializer(data=serializer_data, write_only=True)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertIn('data', serializer.errors)
        self.assertEqual(len(serializer.errors['data']), 1)
        self.assertEqual(
            str(serializer.errors['data'][0]),
            APPOINTMENT_DATE_ERROR_MESSAGE,
        )

    def test_appointment_can_be_retrieved_using_serializer(self):
        appointment = AppointmentFactory(health_care_worker=self.health_care_worker)

        serializer = AppointmentSerializer(appointment)

        manual_check = set({'date', 'uuid'})

        # Map model fields into serializer for field validation
        for model_field, serializer_field in MODEL_TO_SERIALIZER.items():
            if model_field in manual_check:
                continue

            self.assertEqual(
                getattr(appointment, model_field),
                serializer.data[serializer_field]
            )

        self.assertEqual(
            appointment.date.isoformat(),
            serializer.data['data'],
        )
        self.assertEqual(
            appointment.health_care_worker.uuid,
            uuid.UUID(serializer.data['profissional_uuid']),
        )
        self.assertEqual(
            appointment.uuid,
            uuid.UUID(serializer.data['uuid']),
        )
