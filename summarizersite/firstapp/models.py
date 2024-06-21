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

class Login(models.Model):
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=15)
    active_inactive = models.BooleanField()

    class Meta:
        db_table = "Login"
        verbose_name_plural = "Login"

    def __str__(self):
        return self.email_id

class DocumentInfo(models.Model):
    document_title = models.CharField(max_length=500)
    document_path = models.CharField(max_length=500)
    document_type = models.CharField(max_length=100)
    document_size = models.IntegerField()

    class Meta:
        db_table = "DocumentInfo"
        verbose_name_plural = "DocumentInfo"

    def __str__(self):
        return self.document_title
    
class Feedback(models.Model):
    email_id = models.EmailField()
    rating = models.FloatField()
    comments = models.TextField()

    class Meta:
        db_table = "Feedback"
        verbose_name_plural = "Feedback"

    def __str__(self):
        return self.email_id