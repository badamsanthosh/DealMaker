from django.db import models


class BaseModel(models.Model):
    """
    Base Model class which will be inherited by other model classes.
    """
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "home_loans"
        abstract = True
