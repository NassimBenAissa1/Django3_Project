from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here.

def is_Esprit_Email(value):
    """
    Tests if an email ends with @esprit.tn
    Args:
        value (any): model or form attribut value
    Returns:
        Boolean: if required constraints are met
    """

    if not str(value).endswith('@esprit.tn'):
        raise ValidationError(
            'Your email must be @esprit.tn', params={'value': value})
    return value

class User(models.Model):
    first_name = models.CharField(verbose_name="Prénom", max_length=30)
    last_name = models.CharField(verbose_name="Nom", max_length=30)
    email = models.EmailField(verbose_name="Email", 
        null=False,
        validators=[
            is_Esprit_Email
        ]
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(User):
    pass


class Coach(User):
    pass


class Project(models.Model):
    project_name = models.CharField(
        verbose_name="Titre du projet", max_length=50)
    project_duration = models.IntegerField(
        verbose_name="Durée Estimée", default=0)
    time_allocated = models.IntegerField(verbose_name="Temps Alloué",validators=[
            MinValueValidator(1, 'The minimum time allowed is 1 hour'),
            MaxValueValidator(10, 'The maximum time allowed is 10 hours')
        ])
    needs = models.TextField(verbose_name="Besoins", max_length=250)
    description = models.TextField(max_length=250)

    isValid = models.BooleanField(default=False)
    
    creator = models.OneToOneField(
        to = Student, 
        on_delete = models.CASCADE, 
        related_name = "project_owner"
    )
    
    supervisor = models.ForeignKey(
        to=Coach,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="project_coach"
    )
    
    members = models.ManyToManyField(
        to = Student,
        blank = True,
        related_name = 'Les_Membres',
        through = 'MembershipInProject',
    )
    
    def __str__(self):
        return self.project_name
    
    
class MembershipInProject (models.Model):
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
    )
    
    student = models.ForeignKey(
        Student,
        on_delete = models.CASCADE,
    )
    
    time_allocated_by_member = models.IntegerField(
        'Temps alloué par le membre',
    )
    
    def __str__(self):
        return f"Member: {self.student.last_name} {self.student.first_name} in {self.project.project_name}"

    
    class Meta:
        unique_together = ("project", "student")