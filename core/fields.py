from django.core.validators import MaxValueValidator
from django.db import models


class WeekDayField(models.PositiveSmallIntegerField):
    default_validators = [MaxValueValidator(6)]
