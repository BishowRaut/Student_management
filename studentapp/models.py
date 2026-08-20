from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=150)

    qualification = models.CharField(
        max_length=100,
        blank=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="teachers"
    )

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses"
    )

    def __str__(self):
        return self.name