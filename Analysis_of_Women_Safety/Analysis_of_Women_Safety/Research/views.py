from django.db.models import Count
from django.shortcuts import render, redirect
from django.db.models import F, Q

# Create your views here.
from Client.models import Userregister_Model, TweetModel, Feedback_Model


def admin_login(request):
	if request.method  == "POST":
		admin = request.POST.get('admin')
		password = request.POST.get('password')
		if admin == "admin" and password =="admin":
			return redirect('admin_viewpage')


	return render(request,'research/admin_login.html')

def admin_viewpage(request):
	obj = Userregister_Model.objects.all()
	return render(request,'research/admin_viewpage.html',{'object':obj})

def admin_viewfeedback(request):
	obj=Feedback_Model.objects.all()
	return render(request,'research/admin_viewfeedback.html',{'objects':obj})
def admin_viewtrending(request):
	topic = TweetModel.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
	return render(request,'research/admin_viewtrending.html',{'objects':topic})

def viewtreandingtopics(request,chart_type):
	dd = {}
	pos,neu,neg =0,0,0
	poss=None
	topic = TweetModel.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
	for t in topic:
		topics=t['topics']
		pos_count=TweetModel.objects.filter(topics=topics).values('sentiment').annotate(topiccount=Count('topics'))
		poss=pos_count
		for pp in pos_count:
			senti= pp['sentiment']
			if senti == 'positive':
				pos= pp['topiccount']
			elif senti == 'negative':
				neg = pp['topiccount']
			elif senti == 'nutral':
				neu = pp['topiccount']
		dd[topics]=[pos,neg,neu]
	return render(request,'research/viewtreandingtopics.html',{'object':topic,'dd':dd,'chart_type':chart_type})

'''def nuetralfeedbacktivechart(request,pk):
	print('------------------------')
	#print(pk)
	tweet = TweetModel.objects.get(id=pk)
	b=tweet.topics	  
	d1=TweetModel.objects.filter(sentiment='positive').filter(topics=b).values('topics').annotate(dcount=Count('sentiment'))
	d2=TweetModel.objects.filter(sentiment='negative').filter(topics=b).values('topics').annotate(dcount=Count('sentiment'))
	#d3=TweetModel.objects.filter(sentiment='nutral').filter(topics=b).values('topics').annotate(dcount=Count('sentiment'))
	d4=TweetModel.objects.filter(age__gte=25).filter(topics=b).values('topics').annotate(dcount=Count('sentiment'))
	d5=TweetModel.objects.filter(age__lte=25).filter(topics=b).values('topics').annotate(dcount=Count('sentiment'))
	d6=TweetModel.objects.filter(Q(transport='bus') | Q(transport='train')).filter(topics=b).values('topics').annotate(dcount=Count('sentiment'))
	d7=TweetModel.objects.filter(Q(transport='bike') | Q(transport='car')).filter(topics=b).values('topics').annotate(dcount=Count('sentiment'))
	return render(request,'research/charts3.html',{'chart_type':'bar','d1':d1,'d2':d2,'d4':d4,'d5':d5,'d6':d6,'d7':d7})
'''	
def negativefeedbacktivechart(request,chart_type):
	dd = {}
	pos, neu, neg = 0, 0, 0
	poss = None
	topic = TweetModel.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
	for t in topic:
		topics = t['topics']
		pos_count = TweetModel.objects.filter(topics=topics).values('sentiment').annotate(topiccount=Count('topics'))
		poss = pos_count
		for pp in pos_count:
			senti = pp['sentiment']
			if senti == 'positive':
				pos = pp['topiccount']
			elif senti == 'negative':
				neg = pp['topiccount']
			elif senti == 'nutral':
				neu = pp['topiccount']
		dd[topics] = [pos, neg, neu]
	return render(request,'research/negativefeedbacktivechart.html',{'object':topic,'dd':dd,'chart_type':chart_type})	 