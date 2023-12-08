import uuid
from datetime import UTC, date, datetime

from django.test import TestCase

from api.models import HealthCareWorker


class HealthCareWorkerTestCase(TestCase):
    def test_health_care_worker_can_be_created(self):
        before = datetime.now(UTC)

        # From https://en.wikipedia.org/wiki/John_E._Fryer
        health_care_worker = HealthCareWorker.objects.create(
            legal_name="John Ercel Fryer",
            preferred_name="Henry Anonymous",
            pronouns="He/Him",
            date_of_birth=date(year=1937, month=11, day=7),
            specialization="Psychiatrist",
        )

        self.assertIsInstance(health_care_worker.id, int)
        self.assertGreater(health_care_worker.id, 0)
        self.assertIsInstance(health_care_worker.uuid, uuid.UUID)
        self.assertGreater(health_care_worker.created, before)
        self.assertGreaterEqual(health_care_worker.modified, health_care_worker.created)
        self.assertEqual(health_care_worker.legal_name, "John Ercel Fryer")
        self.assertEqual(health_care_worker.preferred_name, "Henry Anonymous")
        self.assertEqual(health_care_worker.pronouns, "He/Him")
        self.assertEqual(health_care_worker.date_of_birth, date(year=1937, month=11, day=7))
        self.assertEqual(health_care_worker.specialization, "Psychiatrist")
