from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings


from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.context_processors import csrf
from django.template import RequestContext

from blog.models import Entry, UserProfile, Comment
from blog.forms import CommentForm, UserForm, EntryForm, SearchForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            credentials = register_form.cleaned_data
            user = User.objects.create(username=credentials['username'])
            user.set_password(credentials['password1'])
            user.save()
            user_name = credentials['username']
            pass_word = credentials['password1']
            new_user = auth.authenticate(username=user_name, password=pass_word)
            if new_user is not None and user.is_active:
                auth.login(request, new_user)
                return HttpResponseRedirect("/home/")
    else:
        register_form = UserCreationForm()
    return render_to_response("register.html", 
        					  {'register_form': register_form},
        					   context_instance = RequestContext(request))

def index(request):
    return render_to_response(
    	'index.html',
    	context_instance = RequestContext(request)
    )
    
def login(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/home/")
        else:
            message = "Invalid Credentials. Please check you credentials"
    return render_to_response("login.html", {'message': message}, 
                              context_instance = RequestContext(request))

    
@login_required
def home(request):
    search_form = SearchForm()
    entries = Entry.objects.filter(creator=request.session.get('_auth_user_id'))
    user_profiles = []
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            term = search_form.cleaned_data['search_term']
            user_profiles = User.objects.filter(first_name__icontains=term)
    return render_to_response(
    	'home.html',
    	{ 'entries': entries, 'search_form': search_form,
    	  'user_profiles': user_profiles},
    	context_instance = RequestContext(request)
    )
 
@login_required
def profile(request):
    try:
        profile = UserProfile.objects.filter(user=request.user.id)
    except:
        profile = []
    profile_correct = profile[0] if profile else []
    if request.method == "POST":
        profile_form = UserForm(request.POST, request.FILES)
        if profile_form.is_valid():
            user_cred = profile_form.cleaned_data
            user = User.objects.get(pk=request.user.id)
            user.first_name = user_cred['firstname']
            user.last_name = user_cred['lastname']
            user.username = user_cred['username']
            user.email = user_cred['email']
            user.save()
            try:
                uploadpic = request.FILES['photo']
            except:
                uploadpic = None
            pform, created = UserProfile.objects.get_or_create(user=user)
            if created:
                pform.country = user_cred["country"]
            if uploadpic:
                pform.photo.save(uploadpic.name, uploadpic)
            pform.save()
            return HttpResponseRedirect("/home/profile/")
    else:
        p_country_final = profile_correct.country if profile_correct else ''
        p_photo_final = profile_correct.photo if profile_correct else ''
        data = {"username": request.user.username,
                "firstname": request.user.first_name,
                "lastname": request.user.last_name,
                "email": request.user.email,
                "country": p_country_final }
        profile_form = UserForm(initial=data)
    return render_to_response(
        'profile.html',
        { 'profile_form': profile_form,
          'photo': p_photo_final,
          'profile': profile_correct},
         context_instance = RequestContext(request)
    )
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")
   
def detail(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    comments = entry.comment_set.all()
    if request.method == "POST":
        entry_list = Entry.objects.filter(id=entry_id)
        entry = entry_list[0]
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            values = comment_form.cleaned_data
            created = values['created']
            author = values['author']
            body = values['body']
            comment = Comment.objects.create(created=created, author=author,
                                       body=body, post=entry)
            comment.save()
            return HttpResponseRedirect("/home/detail/" + str(entry.id) + "/")
    else:
        comment_form = CommentForm()
    return render_to_response(
    	'detail.html',
    	{ 'entry': entry, 'comment_form':comment_form, "comments":comments},
    	 context_instance = RequestContext(request)
    )
    
def add_entry(request):
    if request.method == "POST":
        entry_form = EntryForm(request.POST)
        if entry_form.is_valid():
            entry_form.save()
            return HttpResponseRedirect("/home/")        
    else:
        entry_form = EntryForm()
    return render_to_response(
    	'entry.html',
    	{'entry_form':entry_form },
    	 context_instance = RequestContext(request))
