from django.db import models
import uuid
# Create your models here.
class Question(models.Model):
	question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	question_title = models.CharField(max_length=100)
	question_text = models.CharField(max_length=200,null=False)
	question_type = models.CharField(max_length=50,null=False,default='one')
	create_time = models.DateTimeField()

class Option(models.Model):
	question_id = models.ForeignKey(to="Question", to_field="question_id", on_delete=models.CASCADE)
	question_index = models.IntegerField(default=0)
	option_val =  models.CharField(max_length=100,null=False, default="")
	create_time = models.DateTimeField()
	correctness = models.BooleanField(null=False)
	longtext = models.TextField(help_text="这个是longtext", default="")
