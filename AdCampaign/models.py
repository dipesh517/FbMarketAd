from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

class AccountSecrets(models.Model):
  account_id = models.CharField(max_length=120)
  app_id = models.CharField(max_length=120, null = True, blank = True)
  app_secret = models.CharField(max_length=256, null = True, blank = True)
  access_token = models.CharField(max_length=256)

  def save(self, *args, **kwargs):
    if not self.pk and AccountSecrets.objects.exists():
    # if you'll not check for self.pk 
    # then error will also raised in update of exists model
      raise ValidationError('There can be only one Company Profile instance')
    
    return super(AccountSecrets, self).save(*args, **kwargs)



