from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from core.fields import WeekDayField


class TimeSlot(models.Model):
    weekday = models.IntegerField()


class ClassFormation(models.Model):
    starts_at = models.TimeField()
    ends_at = models.TimeField()
    weekday = WeekDayField()
    room_number = models.IntegerField()


class User(AbstractBaseUser):
    pass


class Student(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)


class Professor(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)


class EducationalRepresentative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=128)
    professor = models.ForeignKey('core.Professor', on_delete=models.CASCADE)


ExamStateChoice = [
    ('exam_waited', 'Waiting for exam'),
    ('edu_waited', 'Waiting for Edu. Rep.'),
    ('prof_waited', 'Waiting for prof.'),
    ('verified', 'Verified')

]


class Exam(models.Model):
    date = models.DateField()
    course = models.OneToOneField('core.Course', on_delete=models.CASCADE)
    formation = models.OneToOneField('core.ClassFormation', on_delete=models.CASCADE)
    state = models.CharField(choices=ExamStateChoice, max_length=25, default=ExamStateChoice[0][0])

    def verify_from_professor(self):
        if self.state != 'prof_waited':
            raise
        self.state = 'verified'
        self.save()

    def verify_from_edu_rep(self):
        if self.state != 'edu_waited':
            raise
        self.state = 'prof_waited'
        self.save()


ExamListItemChoices = [
    ('unspecified', 'Unspecified'),
    ('absent', 'Absent'),
    ('present', 'Present'),
    ('allaf', 'Allaf'),
    ('divert', 'Divert'),
]


class ExamListItem(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='items')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    chair_number = models.PositiveIntegerField()
    state = models.CharField(choices=ExamListItemChoices, max_length=32,
                             default=ExamListItemChoices[0][0])

    def unset_state(self):
        self.state = 'unspecified'
        self.save()

    def set_absent(self):
        self.state = 'absent'
        self.save()

    def set_present(self):
        self.state = 'present'
        self.save()
