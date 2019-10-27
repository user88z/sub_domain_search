from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Input_data(models.Model):
    main_domain = models.TextField()
    depth = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(3),
            MinValueValidator(1)
        ])