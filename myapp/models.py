from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"


class Consumer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Student Name")
    email = models.EmailField(max_length=277, verbose_name="Student Email")
    image = models.ImageField(upload_to='consumer_images/', null=True, blank=True, verbose_name="Consumer Image")
    content = models.TextField(verbose_name="Consumer Content", blank=True, null=True)
    maths = models.CharField(max_length=100, verbose_name="Maths",default=0)
    PSP = models.CharField(max_length=100, verbose_name="PSP",default=0)
    Chemistry = models.CharField(max_length=100, verbose_name="Chemistry",default=0)
    MCS = models.CharField(max_length=100, verbose_name="MCS",default=0)
    Physics = models.CharField(max_length=100, verbose_name="Physics",default=0)
    adress= models.TextField(verbose_name="Adress", blank=True, null=True)
    college_department=models.CharField(max_length=100,verbose_name="College Department",default=0)
    student_semester=models.CharField(max_length=10,verbose_name="Student semester",default=0)
    def __str__(self):
        return str(self.id)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Review(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f'Review for {self.consumer.name}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"
