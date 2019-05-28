from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from rest_framework.compat import MinLengthValidator


class User(AbstractBaseUser):
    pass


class Student(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    student_number = models.CharField(max_length=9, validators=[MinLengthValidator(9)])


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class EducationalRepresentative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=128)


ExamStateChoice = [
    ('exam_waited', 'Waiting for exam'),
    ('edu_waited', 'Waiting for Edu. Rep.'),
    ('prof_waited', 'Waiting for prof.'),
    ('verified', 'Verified')

]


class Exam(models.Model):
    date = models.DateField()
    start_at = models.TimeField()
    end_at = models.TimeField()
    room_number = models.IntegerField()
    state = models.CharField(choices=ExamStateChoice, max_length=25)

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
    state = models.CharField(choices=ExamListItemChoices, max_length=32)

    def unset_state(self):
        self.state = 'unspecified'
        self.save()

    def set_absent(self):
        self.state = 'absent'
        self.save()

    def set_present(self):
        self.state = 'present'
        self.save()
