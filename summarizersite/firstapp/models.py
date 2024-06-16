from django.db import models

class Registration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)
    email_id = models.EmailField(unique=True)
    contact_no = models.IntegerField()
    birth_date = models.DateField()
    country = models.CharField(max_length=50)

    class Meta:
        db_table = "Registration"
        verbose_name_plural = "Registration"

    def __str__(self):
        return self.email_id