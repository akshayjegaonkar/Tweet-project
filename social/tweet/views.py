from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm , UserRegistration
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,"index.html")

def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request,"tweet_list.html",{"tweets":tweets})
@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST,request.FILES)
        if form.is_valid():
            Tweet = form.save(commit=False)
            Tweet.user = request.user
            Tweet.save()
            return redirect("tweet_list")
    else:
        form = TweetForm()
    return render(request,"tweet_form.html",{"form":form})
@login_required
def tweet_edit(request, tweet_id):
    tweet_instance = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet_instance)
        if form.is_valid():
            tweet_instance = form.save(commit=False)
            tweet_instance.user = request.user
            tweet_instance.save()
            return redirect("tweet_list")
    else:
        form = TweetForm(instance=tweet_instance)
    return render(request, "tweet_form.html", {"form": form})

@login_required
def tweet_delete(request,tweet_id):
    tweet_instance = get_object_or_404(Tweet,pk = tweet_id,user = request.user)
    if request.method == "POST":
        tweet_instance.delete()
        return redirect('tweet_list')
    return render(request,'delete_confermation.html',{'tweet':tweet_instance})

def register(request):
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request,user)
            return redirect("tweet_list")
    else:
        form = UserRegistration()
    return render(request,"registration/registration.html",{'form':form})