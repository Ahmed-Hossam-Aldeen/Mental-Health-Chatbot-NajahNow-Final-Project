from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    passwrd = models.CharField(max_length= 20)
    age = models.IntegerField()
    def _str_(self):
        return self.name

class Messege(models.Model):
    user_id = models.ForeignKey(User, on_delete= models.CASCADE)
    msg_id = models.IntegerField(primary_key=True)
    msg_ord = models.IntegerField(1)
    messege = models.CharField(max_length = 1000)
    by_user = models.BinaryField(default= 0)
    def _str_(self):
        return self.msg_id+ ' : ' +self.messege + ' : '+self.by_user