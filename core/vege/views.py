from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .seed import generate_reportCard

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.

@login_required(login_url="/login_page/")
def recipes(request):
    if request.method == "POST":
        data = request.POST
        recipeName = data.get("recipeName")
        recipeDescription = data.get("recipeDescription")
        recipeImage = request.FILES.get("recipeImage")
        Recipe.objects.create(
            recipeName=recipeName,
            recipeDescription=recipeDescription,
            recipeImage=recipeImage
        )
        return redirect("/recipes/")

    querySet = Recipe.objects.all()

    if request.GET.get("search"):
        querySet = querySet.filter(recipeName__icontains=request.GET.get("search"))

    context = {"recipes": querySet}
    return render(request, "recipe.html", context)


def updateRecipe(request, id):
    querySet = Recipe.objects.get(id=id)
    if request.method == "POST":
        data = request.POST
        recipeName = data.get("recipeName")
        recipeDescription = data.get("recipeDescription")
        recipeImage = request.FILES.get("recipeImage")

        querySet.recipeName = recipeName
        querySet.recipeDescription = recipeDescription
        if recipeImage:
            querySet.recipeImage = recipeImage

        querySet.save()
        return redirect("/recipes/")

    context = {"recipe": querySet}
    return render(request, "updateRecipe.html", context)


def deleteRecipe(request, id):
    querySet = Recipe.objects.get(id=id)
    querySet.delete()
    return redirect("/recipes/")


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, "Username already exists..!")
            return redirect("/register/")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully...")
        login(request, user)
        return redirect("/recipes/")

    return render(request, "register.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username..!")
            return redirect("/login_page/")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            messages.error(request, "Invalid credentials..!")
            return redirect("/login_page/")
        else:
            login(request, user)
            return redirect("/recipes/")

    return render(request, "login_page.html")


def logout_page(request):
    logout(request)
    return redirect("/recipes/")


def get_students(request):
    querySet = Student.objects.all()
    paginator = Paginator(querySet, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.GET.get("student_search"):
        search = request.GET.get("student_search")
        page_obj = querySet.filter(
            Q(student_name__icontains=search) |
            Q(department__department__icontains=search) |
            Q(student_email__icontains=search)
        )
    return render(request, "student/student.html", {"querySet": page_obj})


def student_marks(request, student_id):
    generate_reportCard()
    querySet = StudentSubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks = querySet.aggregate(total_marks=Sum("marks"))

    currentRank = -1
    ranks = Student.objects.annotate(marks=Sum("studentmarks__marks")).order_by("-marks", "-student_age")
    i = 1
    for rank in ranks:
        if student_id == rank.student_id.student_id:
            currentRank = i
            break
        i = i + 1
    return render(request, "student/student_marks.html",
                  {"querySet": querySet, "total_marks": total_marks, "currentRank": currentRank})
