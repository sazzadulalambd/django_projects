from django.db import models

# Create your models here.
POSITION_TYPE = (
    ("ProjectManager", "Project Manager"),
    ("TeamLead", "Team Lead"),
    ("Devoper", "Devoper"),
    ("Tester", "Tester"),
)


class Team(models.Model):
    name = models.CharField(max_length=25)
    position = models.CharField(max_length=20, choices=POSITION_TYPE)
    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=520)
    assign = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="teams")
    completed = models.BooleanField(default = False)
    pending = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title