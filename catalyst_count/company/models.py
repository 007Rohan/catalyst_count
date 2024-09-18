from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    domain = models.URLField()
    linkedn_url = models.URLField()
    year_founded = models.CharField(max_length=10,null=True,blank=True)
    industry = models.CharField(max_length=200)
    country_name = models.CharField(max_length=150) 
    state_name = models.CharField(max_length=150)
    city_name = models.CharField(max_length=150)
    current_employee_count = models.BigIntegerField()
    total_employee_count = models.BigIntegerField()
    size_range = models.CharField(max_length=20)

    def __str__(self):
        return self.name
