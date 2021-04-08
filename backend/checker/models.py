from django.db import models

class SymptomsModel(models.Model):
    ID = models.IntegerField(primary_key=True, editable=False, unique=True)
    Name = models.CharField(max_length=200)

class IssuesDetail(models.Model):
    Issue_Id                = models.IntegerField(primary_key=True, unique=True)
    DescriptionShort        = models.TextField()
    MedicalCondition        = models.TextField()
    Name                    = models.CharField(max_length=200)
    ProfName                = models.CharField(max_length=200)
    TreatmentDescription    = models.TextField()





