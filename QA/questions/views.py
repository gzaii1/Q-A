from django.shortcuts import render
from . models import Question,Option
from questions.serializers import QuestionSerializer,OptionSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import json, uuid ,datetime

# Create your views here.


'''
		"问题"操作视图
'''
class QuestionViewSet(viewsets.ModelViewSet):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer
	# lookup_field = 'question_id'

	# 获取全部Question 以及其下的Option
	# 参数:(无)
	# url: /question/getAllQuestion/
	@action(methods=['get'],detail=False)
	def getAllQuestion(self, request):
		questions = QuestionSerializer(Question.objects.all().order_by('-question_id'), many=True ).data
		for one in questions:
			# 返回类型为OrdededDict, 键值对形式存储数据,
			optionSet = OptionViewSet()
			one['option_list'] = optionSet.getOptionById(one['question_id'])
		res = {
			'success':True,
			'data':questions
		}
		return Response(res)

	# 新建问题
	# 参数: question_title, question_text, question_type
	# url: /question/createQuestion/
	@action(methods=['post'],detail=False)
	def createQuestion(self, request):
		req = json.loads(request.body)
		localtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		question_id = uuid.uuid4()
		newOne = {
			'question_id':question_id,
			'question_title':req['question_title'],
			'question_text': req['question_text'],
			'question_type': req['question_type'],
			'create_time':localtime
		}
		Question.objects.create(**newOne)
		res = {
			'success':True,
			'data':question_id,
			'message':'添加成功'
		}
		return Response(res)

	# 更新问题
	# 参数:question_id, question_title, question_type
	# url: /question/updateQuestion/
	@action(methods=['post'],detail=False)
	def updateQuestion(self, request):
		req = json.loads(request.body)
		question = Question.objects.get(question_id=req['question_id'])
		question.question_title = req['question_title']
		question.question_text = req['question_text']
		question.question_type = req['question_type']
		question.save()
		res = {
			'success':True,
			'data':question.question_id,
			'message':'更新成功'
		}
		return Response(res)

	# 删除问题
	# 参数:question_id
	# url: /question/deleteQuestionById/
	@action(methods=['post'],detail=False)
	def deleteQuestionById(self, request):
		req = json.loads(request.body)
		question = Question.objects.filter(question_id=req['question_id']).delete()
		res = {
			'success':True,
			'data':'',
			'message':'删除成功',
		}
		return Response(res)


'''
		"选项"操作视图
'''
class OptionViewSet(viewsets.ModelViewSet):
	queryset = Option.objects.all()
	serializer_class = OptionSerializer
	lookup_field = 'question_id'

	def getAll(self, request):
		data = Option.objects.all().order_by('-question_id')
		serializer = OptionSerializer(data)
		res = {
			'success':True,
			'data':serializer.data,
		}
		return Response(res)

	# 获取全部option
	@action(methods=['get'],detail=False)
	def getAllOption(self, request):
		data = Option.objects.all().order_by('-question_id')
		res = {
			'success':True,
			'data':OptionSerializer(data,many=True,context={'request': request}).data
		}
		return Response(res)
		
	# 获取单个question下的option(根据id)
	def getOptionById(self, id):
		data = Option.objects.filter(question_id = id).order_by('-question_index')
		serializer = OptionSerializer(data,many=True)
		res = {
			'success':True,
			'data':serializer.data,
			'message':'',
		}
		return serializer.data

	# 增加单条option
	# 参数: question_id, question_index, option_val, create_time, correctness
	# url: /options/addOptionById/
	@action(methods=['post'],detail=False)
	def addOptionById(self, request):
		responseObj = json.loads(request.body)
		q = Question()
		q.question_id = responseObj['question_id']
		responseObj['question_id'] = q
		question_index = responseObj['question_index']
		option_val = responseObj['option_val']
		create_time = responseObj['create_time']
		correctness = responseObj['correctness']
		Option.objects.create(**responseObj)
		
		res = {
			'success':True,
			'data':'',
			'message':'添加成功',
		}
		return Response(res)


	# 删除单条option
	# 参数:question_id, question_index
	# url:/options/deleteOptionById/
	@action(methods=['post'],detail=False)
	def deleteOptionById(self, request):
		responseObj = json.loads(request.body)
		Option.objects.filter(question_id=responseObj['question_id']).filter(question_index=responseObj['question_index']).delete()
		res = {
			'success':True,
			'data':'',
			'message':'添加成功',
		}
		return Response(res)