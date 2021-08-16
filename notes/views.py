from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import *
from .serializers import *

# TEMPLATE VIEWS


@login_required
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'index.html')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "notes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "notes/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "notes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "notes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "notes/register.html")


@api_view(['GET'])
def api_overview(request):
    endpoints = {
        'API Overview': 'api/',
        'List Notes': 'api/notes/',
        'Note Update / Delete / Details': 'api/note/<id>/',
        'Note Create': 'api/create-note/',
        'Current User Info': 'api/current-user/'
    }

    return Response(endpoints)


# List items
@api_view(['GET'])
def list_notes(request):
    notes_list = Note.objects.all().order_by('-creation_date')
    serializer = NoteSerializer(notes_list, many=True)
    return Response(serializer.data)


# CRUD Actions for single instances of models
@api_view(['GET', 'POST', 'DELETE'])
def note(request, id):

    try:
        note = Note.objects.get(pk=id)
    except Note.DoesNotExist:
        return Response({
            'error': 'Note does not exist'
        })

    if request.method == 'GET':
        serializer = NoteSerializer(instance=note)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NoteSerializer(instance=note, data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    elif request.method == 'DELETE':
        note.delete()
        return Response('Note Successfully deleted.')


# Create items
@api_view(['POST'])
def create_note(request):
    serializer = NoteSerializer(data=request.data)

    if serializer.is_valid():
        # TODO: save note with user as the current user
        # serializer.save(user=request.user)
        serializer.save()

    return Response(serializer.data)
