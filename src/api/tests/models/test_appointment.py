import uuid
from datetime import UTC, date, datetime, timedelta

from django.db.utils import IntegrityError
from django.test import TestCase

from api.models import Appointment, HealthCareWorker


class AppointmentTestCase(TestCase):
    def test_appointment_can_be_created(self):
        # From https://en.wikipedia.org/wiki/Louise_Pearce
        health_care_worker = HealthCareWorker.objects.create(
            legal_name="Louise Pearce",
            preferred_name="",
            pronouns="She/Her",
            date_of_birth=date(year=1885, month=3, day=5),
            specialization="Pathologist",
        )

        before = datetime.now(UTC)
        tomorrow = before.date() + timedelta(days=1)

        appointment = Appointment.objects.create(
            health_care_worker=health_care_worker,
            date=tomorrow,
            info="Test appointment",
        )

        self.assertIsInstance(appointment.id, int)
        self.assertGreater(appointment.id, 0)
        self.assertIsInstance(appointment.uuid, uuid.UUID)
        self.assertGreater(appointment.created, before)
        self.assertGreaterEqual(appointment.modified, appointment.created)
        self.assertEqual(appointment.health_care_worker, health_care_worker)
        self.assertEqual(appointment.health_care_worker_id, health_care_worker.id)
        self.assertEqual(appointment.date, tomorrow)
        self.assertEqual(appointment.info, "Test appointment")

    def test_appointment_date_and_health_care_worker_must_be_unique(self):
        # From https://en.wikipedia.org/wiki/Sara_Josephine_Baker
        health_care_worker = HealthCareWorker.objects.create(
            legal_name="Sara Josephine Baker",
            preferred_name="",
            pronouns="She/Her",
            date_of_birth=date(year=1873, month=11, day=15),
            specialization="Public Health",
        )

        appointment_date = date(year=2123, month=4, day=20)

        first_appointment = Appointment.objects.create(
            health_care_worker=health_care_worker,
            date=appointment_date,
            info="First appointment",
        )

        with self.assertRaisesRegex(
            IntegrityError,
            'duplicate key value violates unique constraint "unique_appointment_date_health_care_worker"',
        ):
            Appointment.objects.create(
                health_care_worker=health_care_worker,
                date=appointment_date,
                info="Conflicting appointment",
            )

    def test_appointment_date_must_be_in_the_future(self):
        # From https://en.wikipedia.org/wiki/Sara_Josephine_Baker
        health_care_worker = HealthCareWorker.objects.create(
            legal_name="Sara Josephine Baker",
            preferred_name="",
            pronouns="She/Her",
            date_of_birth=date(year=1873, month=11, day=15),
            specialization="Public Health",
        )

        with self.assertRaisesRegex(
            IntegrityError,
            'new row for relation "api_appointment" violates check constraint "appointment_date_must_be_in_the_future"',
        ):
            Appointment.objects.create(
                health_care_worker=health_care_worker,
                date=date(year=1900, month=9, day=1),
                info="Appointment must be in the future",
            )
