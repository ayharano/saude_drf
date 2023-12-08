from datetime import UTC, datetime
from functools import partial

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from api.constants import HEALTH_PRACTITIONERS_AND_PROFESSIONALS, PRONOUNS
from api.models import Appointment, HealthCareWorker


utcnow = partial(datetime.now, UTC)


class TimestampedFactory(factory.Factory):
    created = factory.LazyFunction(utcnow)
    modified = factory.LazyAttribute(lambda obj: obj.created)


class BaseFactory(TimestampedFactory, DjangoModelFactory):
    pass


class HealthCareWorkerFactory(BaseFactory):
    class Meta:
        model = HealthCareWorker

    class Params:
        with_preferred_name = factory.Faker('pybool')
        preferred_name_ = factory.Faker('name_nonbinary')

    legal_name = factory.Faker('name')
    preferred_name = factory.Maybe(
        factory.SelfAttribute('.with_preferred_name'),
        yes_declaration=factory.SelfAttribute('.preferred_name_'),
        no_declaration='',
    )
    pronouns = factory.fuzzy.FuzzyChoice(PRONOUNS)

    date_of_birth = factory.Faker('date_of_birth', minimum_age=21)

    specialization = factory.fuzzy.FuzzyChoice(HEALTH_PRACTITIONERS_AND_PROFESSIONALS)


class AppointmentFactory(BaseFactory):
    class Meta:
        model = Appointment

    health_care_worker = factory.SubFactory(HealthCareWorkerFactory)
    date = factory.Faker('date_between', start_date='+1d', end_date='+5y')
    info = factory.Faker('sentence')
