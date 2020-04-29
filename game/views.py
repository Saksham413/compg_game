from django.shortcuts import render
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from game.models import *
from game.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
# Create your views here.

'''
*if the user is logged in already, then home page is rendered
*else directed to login page
'''
@login_required
def index(request):
	if request.user.is_authenticated:
		return render(request,'index.html')
	return render(request,'index.html')

'''
directs to login page, authentication is nullified
'''
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/game/login/')

'''
Called for registering
*receives request from frontend when user tries to register
*request has the information to be registered
*if type of request=POST, saves the user details in the SQLITE3 database
*else registration page is rendered again
*
'''
def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		# print(user_form)
		profile_form = UserProfileInfoForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			# our_user = UserProfileInfo(user = user_form.save(),indicesList = "'NDVI':'(nir-r)/(nir+r)'")
			# print(our_user)
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			# our_user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			# userInfo = UserProfileInfo.objects.all()
			# print(userInfo)
			profile.save()
			registered = True
		else:
			print(user_form.errors,profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()
	return render(request,'registration.html',
						  {'user_form':user_form,
						   'profile_form':profile_form,
						   'registered':registered})
'''
Called for loggin in
*request has the username and password given in by the user
This function-
*after receiving request(POST) for login, authenticates the requesting user's 
password and username
*if successful, directed to home page
*login page rendered again in case the request is not of the type POST
'''
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		t_res={}
		t_res['username']=username
		t_res['password']=password
		# print(t_res)
		#need to return this response
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				#return HttpResponseRedirect(reverse('index'))
				#go to the map interface after this
				print('jhihih')
				return redirect('/game/home/')
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'login.html', {})

'''
stores the id of the user logging in and renders home page
'''	
@login_required
def home(request):
	id = request.user.id
	# print(request.user)
	user = UserProfileInfo.objects.get(user = request.user)
	# print('hi')
	print(user)

	return render(request,'index.html')

def login(request):
	return render(request,'login.html')

def leaderboard(request):
	curr_user = UserProfileInfo.objects.get(user_id=request.user)
	data_rcvd = json.loads( request.body.decode('utf-8') )
	curr_user.score = max(curr_user.score, int(data_rcvd['score']) )
	curr_user.save()
	print('score is', curr_user.score)
	leaderboard = UserProfileInfo.objects.order_by('-score')
	print(leaderboard)
	username = []
	score = []
	for i in range(10):
		try:
			username.append(leaderboard[i].user.username)
			score.append(leaderboard[i].score)
		except:
			pass

	curr_score = curr_user.score
	rank = 1
	for player in leaderboard:
		if curr_user == player:
			break
		if curr_score <= player.score:
			rank += 1

	resp = {'username': username, 'score': score, 'rank': rank}
	return HttpResponse(json.dumps(resp), content_type='application/json')