from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
import re
import datetime
import pytz

from .models import User, Message, Comment

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[A-Za-z_-]*$')

# Create your views here.
def index(request):
    if 'logged_in' not in request.session.keys():
        request.session['logged_in'] = False
        print request.session['logged_in']
        return render(request, "first_app/index.html")
    if request.session['logged_in'] == False:
        return render(request, "first_app/index.html")
        print request.session['logged_in']
    else:
        print request.session['logged_in']
        return redirect('/wall')

def login(request):
    return render(request, "first_app/login.html")

def log_out(request):
    request.session.pop('logged_in')
    return redirect('/login')

def process(request):
    if request.method == "POST":
        error = False
         # for now i am passing in the entire request object for the sake of the django messages(will fix), and i am using session to repopulate the fields,
        user = User.objects.register(request.POST, request.session, request)
        error = False
        if user:
                return redirect('/wall')
        return redirect('/')
    return redirect('/')

def submit_login(request):
    if request.method == "POST":
        error = False
        # for now i am passing in the entire request object for the sake of the django messages(will fix), and i am using session to repopulate the fields
        user = User.objects.login(request.POST, request.session, request)
        if user:
            return redirect('/wall')
        else:         
            return redirect('/login')
        return redirect('/login')

def post_message(request):
    if request.method == "POST":
        message = request.POST['message']
        user = User.objects.get(email=request.session['logged_in'])
        print user
        Message.objects.create(message = message, user= user)
        
        return redirect('/wall')
    return redirect('/')

def post_comment(request, message_id):
    if request.method == "POST":
        comment = request.POST['comment']
        user = User.objects.get(email=request.session['logged_in'])
        print user
        message = Message.objects.get(id=message_id)
        Comment.objects.create(comment = comment, user= user, message = message)
        return redirect('/wall')
    return redirect('/')

def delete_comment(request, id):
    if request.method == "POST":
        comment = Comment.objects.get(id=id)
        print comment
        if comment.user.email == request.session['logged_in']:
            comment.delete()
        else:
            messages.error(request, 'You did not write this comment! Only the author can delete or edit.')
        
        return redirect('/wall')
    return redirect('/')

def delete_message(request, id):
    if request.method == "POST":
        message = Message.objects.get(id=id)
        print message
        if message.user.email == request.session['logged_in']:
            message.delete()
        else:
            messages.error(request, 'You did not write this comment! Only the author can delete or edit.')
        return redirect('/wall')
    return redirect('/')

def success(request):
    return render(request, 'first_app/success.html')


def wall(request):
    try:
        if request.session['logged_in'] == False:
            return redirect('/')
            print request.session['logged_in']
    except:
        request.session['logged_in'] == False
    
    else:
        users = User.objects.all()
        messages = Message.objects.all()
        comments = Comment.objects.all()
        current_user = User.objects.get(email=request.session['logged_in'])


        context = {
            'all_messages': messages,
            "current_user": current_user
        }
        return render(request, 'first_app/wall.html', context)


