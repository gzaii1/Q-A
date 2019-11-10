from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Question, Option

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Question
		fields = ['question_id', 'question_title', 'question_text', 'question_type', 'create_time']

class OptionSerializer(serializers.ModelSerializer):
	# publish = serializers.HyperlinkedIdentityField(
	# 	view_name='option',  # publish具体对象对应的url别名
	# 	lookup_field='question_id',  # 该字段在表中的字段名
	# 	)
	class Meta:
		model = Option
		fields = ['question_id', 'question_index', 'option_val' ,'create_time', 'correctness']
