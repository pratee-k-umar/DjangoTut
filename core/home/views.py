from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
  peoples = [
    {"name": "Prateek Kumar", "age": 19},
    {"name": "Divya Prakash", "age": 20},
    {"name": "Ayush Singh", "age": 20},
    {"name": "Akshay Arya", "age": 19},
    {"name": "Sparsh Singh", "age": 20}
  ]
  return render(request, "home/index.html", context={"peoples": peoples})

def success(request):
  return HttpResponse("This is a success page")

def contact(request):
  return render(request, "home/contact.html")

def about(request):
  return render(request, "home/about.html")