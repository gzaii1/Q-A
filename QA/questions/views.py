from django.shortcuts import render
from . models import Question,Option
from questions.serializers import QuestionSerializer, OptionSerializer
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
		questions = QuestionSerializer(Question.objects.all().order_by('create_time'), many=True ).data
		for one in questions:
			# 返回类型为OrdededDict, 键值对形式存储数据,
			optionSet = OptionViewSet()
			option_list = optionSet.getOptionById(one['question_id'])
			one['option_list'] = option_list
			one['right_answer'] = ["%s"%item['question_index'] for item in filter(lambda n:n['correctness']==True, option_list)]
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
		req = json.loads(request.body.decode())
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
		req = json.loads(request.body.decode())
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
		req = json.loads(request.body.decode())
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
		data = Option.objects.filter(question_id = id).order_by('question_index')
		serializer = OptionSerializer(data,many=True)
		return serializer.data
	# 获取正确答案
	def getRightAnswer(self, id):
		data = Option.objects.filter(question_id = id)
		serializer = OptionSerializer(data,many=True)

		return serializer.data

	# 增加单条option
	# 参数: question_id, question_index, option_val, create_time, correctness
	# url: /options/addOptionById/
	@action(methods=['post'],detail=False)
	def addOptionById(self, request):
		responseObj = json.loads(request.body.decode())
		q = Question()
		q.question_id = responseObj['question_id']
		obj = {
			'question_id':q,
			'question_index' : responseObj['question_index'],
			'option_val' : responseObj['option_val'],
			'create_time' : responseObj['create_time'],
			'correctness' : responseObj['correctness'],
			'longtext' : responseObj['longtext'],
		}

		questionWithThisOption = OptionSerializer(Option.objects.filter(option_val=obj['option_val']),many=True).data
		if not obj['option_val']:
			res = {
				'success':False,
				'data':'',
				'message':'所填内容不能为空',
			}
			return Response(res)
		# elif responseObj['question_type']=='short':
		# 	Option.objects.create(**obj)
		# 	res = {
		# 		'success':False,
		# 		'data':'',
		# 		'message':'短文'
		# 	}
		# 	return Response(res)
		elif q.question_id in ['%s'%item['question_id'] for item  in questionWithThisOption]:
			res = {
				'success':False,
				'data':'',
				'message':'不能录入已存在的选项'
			}
			return Response(res)
		Option.objects.create(**obj)
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
		responseObj = json.loads(request.body.decode())
		serializer = Option.objects.filter(question_id=responseObj['question_id'])
		serializer.filter(question_index=responseObj['question_index']).delete()
		# 删除后重新排序idx
		idx = 0
		for item in serializer.all().order_by('question_index'):
			item.question_index = idx
			item.save()
			idx = idx + 1
		res = {
			'success':True,
			'data':'',
			'message':'删除成功',
		}
		return Response(res)

	# 更新单条option (目前只有单选题的功能, 其他功能还未补充, 此外, 检查是否为空和是否为重复的机制需要单独封装)  仅修改选项
	# 参数:
	# question_id
	# question_type
	# option_val
	# correctness
	# question_index
	# url:/option/updateOneOption/
	@action(methods=['post'],detail=False)
	def updateOneOption(self, request):
		responseObj = json.loads(request.body.decode())
		question_id = responseObj['question_id']
		option_val = responseObj['option_val']
		# 如果为单选
		if responseObj['question_type'] =='single':
			# 判断修改的题目是否重复
			#questionWithThisOption = OptionSerializer(Option.objects.filter(option_val=option_val),many=True).data
			# if not option_val:
			# 	res = {
			# 		'success':False,
			# 		'data':'',
			# 		'message':'所填内容不能为空',
			# 	}
			# 	return Response(res)
			# elif question_id in ['%s'%item['question_id'] for item in questionWithThisOption]:
			# 	res = {
			# 		'success':False,
			# 		'data':'',
			# 		'message':'不能录入已存在的选项'
			# 	}
			# 	return Response(res)
			Option.objects.filter(question_id=responseObj['question_id']).update(correctness=False)
			Option.objects.filter(question_id=responseObj['question_id']).filter(question_index=responseObj['question_index']).update(correctness=True, option_val=responseObj['option_val'])

			res = {
				'success':True,
				'data':'',
				'message':'已修改答案'
			}
			return Response(res)
		elif responseObj['question_type'] =='multi':
			Option.objects.filter(question_id=responseObj['question_id']).filter(question_index=responseObj['question_index']).update(correctness=responseObj['correctness'])
			res = {
				'success':True,
				'data':'',
				'message':'已修改答案'
			}
			return Response(res)
		res = {
				'success':True,
				'data':'',
				'message':'test'
			}
		return Response(res)
	# 重新录入表单
	# 参数:question_id, options {question_index option_val correctness question_id create_time}
	# url:/option/updateOptionsById/
	@action(methods=['post'],detail=False)
	def updateOptionsById(self, request):
		responseObj = json.loads(request.body.decode())
		# 删除该问题下的所有选项 (待改进)
		serializer = Option.objects.filter(question_id=responseObj['question_id']).delete()
		# 序列化dumps
		[self.addOption(item) for item in responseObj['options']]
		res = {
			'success':True,
			'data':'',
			'message':'测试'
		}
		return Response(res)
	# 添加单个option
	def addOption(self, item):
		question = Question()
		question.question_id = item['question_id']
		option = Option()
		option.question_id = question
		option.question_index = item['question_index']
		option.option_val = item['option_val']
		option.create_time = item['create_time']
		option.correctness = item['correctness']
		option.save()
