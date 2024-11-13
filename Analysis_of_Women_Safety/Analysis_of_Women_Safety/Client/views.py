from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from Client.forms import Userregister_Form
from Client.models import Userregister_Model, TweetModel, Feedback_Model
#machine learning libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import itertools
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.linear_model import PassiveAggressiveClassifier
import os

import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from django.db.models import Q
import datetime
import csv
def user_login(request):
	if request.method == "POST":
		name = request.POST.get('name')
		password = request.POST.get('password')
		try:
			object_id_list = ['negative']
			enter = Userregister_Model.objects.get(name=name,password=password)
			request.session['name']=enter.id
			bad=enter.bad
			print('welcomeeeeeeeeeeee')
			print(bad)
			if(bad=='positive'):
				print('positiveeeeeeeeee')
				return redirect('user_mydetails')
			elif(bad==''):
				print('positiveeeeeeeeeenulllllllllllll')
				return redirect('user_mydetails')
			elif(bad=='nutral'):
				print('positiveeeeeeeeeenulllllllllllll')
				return redirect('user_mydetails')
			else:
				print('hiiiiiiiiiiii1q1111111111')
				return render(request, 'client/user_login.html')
				#return redirect('user_mydetails')
		except:
			pass
	return render(request, 'client/user_login.html')

def user_register(request):
	if request.method == "POST":
		forms = Userregister_Form(request.POST)
		if forms.is_valid():
			forms.save()
			messages.success(request, 'You have been successfully registered')
			return redirect('user_login')
	else:
		forms = Userregister_Form()
	return render(request, 'client/user_register.html',{'form':forms})

def user_mydetails(request):
	name = request.session['name']
	ted = Userregister_Model.objects.get(id=name)
	return render(request, 'client/user_mydetails.html',{'object':ted})

def user_updatedetails(request):
	name = request.session['name']
	obj = Userregister_Model.objects.get(id=name)
	if request.method == "POST":
		UserName = request.POST.get('name', '')
		Email = request.POST.get('email', '')
		Password = request.POST.get('password', '')
		Phone_Number = request.POST.get('phoneno', '')
		Address = request.POST.get('address', '')
		Dob = request.POST.get('dob', '')
		country = request.POST.get('country', '')
		state = request.POST.get('state', '')
		city = request.POST.get('city', '')

		obj = get_object_or_404(Userregister_Model, id=name)
		obj.name = UserName
		obj.email = Email
		obj.password = Password
		obj.phoneno = Phone_Number
		obj.address = Address
		obj.dob = Dob
		obj.country = country
		obj.state = state
		obj.city = city
		obj.save(update_fields=["name", "email", "password", "phoneno", "address","dob","country","state","city"])
		return redirect('user_mydetails')


	return render(request, 'client/user_updatedetails.html',{'form':obj})

def tweet(request):
	name = request.session['name']
	userObj = Userregister_Model.objects.get(id=name)
	result = ''
	pos = []
	neg = []
	oth = []
	se = 'se'
	if request.method == "POST":
		images = request.POST.get('images')
		twt = request.POST.get('tweet')
		age = request.POST.get('age')
		transport = request.POST.get('transport')

		if '#' in twt:
			startingpoint = twt.find('#')
			a = twt[startingpoint:]
			endingPoint = a.find(' ')
			title = a[0:endingPoint]
			result = title[1:]
		# return redirect('tweetpage')

		for f in twt.split():
			if f in (
			'good', 'nice', 'beteer', 'miss', 'missed', 'new', 'best', 'excellent', 'safe','nice', 'work','better', 'happy', 'won',
			'win', 'awesome', 'love', 'positive', 'greate',):
				pos.append(f)
			elif f in (
			'worst', 'not','unsafe','isnt','harresment', 'jealous', 'suspended', 'nothing', 'pain', 'cant', 'waste', 'poor', 'error', 'imporve',
			'bad', 'sucked', 'sad', 'naked', 'worry', 'cheating',):
				neg.append(f)
			else:
				oth.append(f)
		if len(pos) > len(neg):
			se = 'positive'
			with open('E:/women updatedgraph/Dataset/women.csv','a', newline='') as fd:
				fieldnames = ['target','city','text','age','transport']
				writer = csv.DictWriter(fd, fieldnames=fieldnames)
				writer.writerow({'target':0, 'city':result,'text':twt,'age':age,'transport':transport})
		elif len(neg) > len(pos):
			se = 'negative'
			with open('E:/women updatedgraph/Dataset/women.csv','a', newline='') as fd:
				fieldnames = ['target','city','text','age','transport']
				writer = csv.DictWriter(fd, fieldnames=fieldnames)
				writer.writerow({'target':1, 'city':result,'text':twt,'age':age,'transport':transport})			   
		else:
			se = 'nutral'
		if se=='negative':
			name=request.session['name']
			enter = Userregister_Model.objects.filter(id=name).update(bad=se)
		TweetModel.objects.create(userId=userObj, tweet=twt, topics=result, sentiment=se,images=images,age=age,transport=transport,time= datetime.datetime.now() )
	obj = TweetModel.objects.all()

	return render(request,'client/tweet.html',{'list_objects': obj,'result':result,'se':se})

def tweetview(request):
	obj = TweetModel.objects.all()

	return render(request,'client/tweetview.html',{'list_objects':obj})


def feedback(request):
	if request.method == "POST":
		name=request.POST.get('name')
		mobilenumber=request.POST.get('mobilenumber')
		feedback=request.POST.get('feedback')
		Feedback_Model.objects.create(name=name,mobilenumber=mobilenumber,feedback=feedback,)
		return redirect('feedback')

	return render(request,'client/feedback.html')
def redirPredInput(request):
	return render(request,'client/predinput.html')
def redPredInput2(request):
	return render(request,'client/predinput2.html')
def accuracy2(request):
	if request.method == 'POST':
		if request.method == 'POST':
			headline= request.POST.get('name')
			print(headline)
			input=[headline]
			df1 = pd.read_excel('E:/women updatedgraph/Dataset/Static Dataset.xlsx')
			y = df1.target=df1.target.astype(str)
			X = df1.text=df1.text.astype(str)	#df = pd.read_csv('E:/Earth Quake/data.xlsx')
	
			#train_test separation
			X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2)
			#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
			#Ans_test=headline
			#Ans_test=['Kenya parliament passes controversial election law amendment']
			#Applying tfidf to the data set
			tfidf_vect = TfidfVectorizer(stop_words = 'english')
			tfidf_train = tfidf_vect.fit_transform(X_train)
			tfidf_test = tfidf_vect.transform(X_test)
			tfidf_test1= tfidf_vect.transform(input)
			tfidf_df = pd.DataFrame(tfidf_train.A, columns=tfidf_vect.get_feature_names())
			#Applying Passive Aggressive classifier
			linear_clf = PassiveAggressiveClassifier()
			linear_clf.fit(tfidf_train, y_train)
			pred = linear_clf.predict(tfidf_test)
			pred1 = linear_clf.predict(tfidf_test1)
			city=''
			if pred1=='0':
				city='safe'
			else:
				city='unsafe'


			
			
			e = {'g':city}
			return render(request,'client/displaypredinput.html',e)
	return render(request,'client/displaypredinput.html',e)			
def accuracy(request):
	if request.method == 'POST':
		if request.method == 'POST':
			headline= request.POST.get('name')
			print(headline)
			input=[headline]
			df1 = pd.read_csv('E:/women updatedgraph/Dataset/women.csv')
			y = df1.target=df1.target.astype(str)
			X = df1.text=df1.text.astype(str)	#df = pd.read_csv('E:/Earth Quake/data.xlsx')
	
			#train_test separation
			X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2)
			#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
			#Ans_test=headline
			#Ans_test=['Kenya parliament passes controversial election law amendment']
			#Applying tfidf to the data set
			tfidf_vect = TfidfVectorizer(stop_words = 'english')
			tfidf_train = tfidf_vect.fit_transform(X_train)
			tfidf_test = tfidf_vect.transform(X_test)
			tfidf_test1= tfidf_vect.transform(input)
			tfidf_df = pd.DataFrame(tfidf_train.A, columns=tfidf_vect.get_feature_names())
			#Applying Passive Aggressive classifier
			linear_clf = PassiveAggressiveClassifier()
			linear_clf.fit(tfidf_train, y_train)
			pred = linear_clf.predict(tfidf_test)
			pred1 = linear_clf.predict(tfidf_test1)
			city=''
			if pred1=='0':
				city='safe'
			else:
				city='unsafe'


			
			
			e = {'g':city}
			return render(request,'client/displaypredinput.html',e)
	return render(request,'client/displaypredinput.html',e)		