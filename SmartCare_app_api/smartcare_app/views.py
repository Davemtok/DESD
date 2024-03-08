import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Task
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect


def tasks(request):
    """
    Return a JSON response with all tasks
    """
    # Query all tasks
    tasks_queryset = Task.objects.all()
    # Serialize the queryset to JSON
    tasks_json = serializers.serialize("json", tasks_queryset, fields=(
        "title", "description", "completed", "created_at"))
    return HttpResponse(tasks_json, content_type="application/json")


@ csrf_protect
@ csrf_exempt
def create_task(request):
    """
    Create a new task and returns a JSON response with the new task
    """
    # Get the title from the POST request
    title = request.POST["title"]
    # Get the description from the POST request
    description = request.POST["description"]
    # Create a new task
    task = Task(title=title, description=description)
    # Save the task to the database
    task.save()
    # Return a JSON response with the new task
    return JsonResponse({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at,
    })


@ csrf_protect
@ csrf_exempt
def update_task(request, pk):
    """
    Update a task and returns a JSON response with the updated task
    """
    task = Task.objects.get(pk=pk)
    if request.POST.get("title"):
        task.title = request.POST["title"]
    if request.POST.get("description"):
        task.description = request.POST["description"]
    if request.POST.get("completed"):
        task.completed = json.loads(request.POST["completed"].lower())
    task.save()
    return JsonResponse({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at,
    })


def delete_task(request, pk):
    """
    Delete a task and returns a JSON response with the status
    """
    task = Task.objects.get(pk=pk)
    task.delete()
    return JsonResponse({"status": "Successfully deleted task."})
