from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from .models import Document, SharedAccess
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and password required")
            return render(request, 'login.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, 'login.html')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    owned_docs = Document.objects.filter(owner=request.user)
    shared_docs = Document.objects.filter(shares__shared_with=request.user)
    return render(request, 'dashboard.html', {
        'owned_docs': owned_docs,
        'shared_docs': shared_docs,
    })


@login_required
def create_document(request):
    doc = Document.objects.create(title="Untitled Document", owner=request.user)
    return redirect('edit_document', doc_id=doc.id)


import json

@login_required
def edit_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)

    is_owner = doc.owner == request.user
    is_shared = SharedAccess.objects.filter(document=doc, shared_with=request.user).exists()
    if not (is_owner or is_shared):
        messages.error(request, "You don't have access to this document.")
        return redirect('dashboard')

    if request.method == 'POST':
        if not is_owner:
            return JsonResponse({'status': 'error', 'message': 'Only owner can edit'}, status=403)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        doc.title = data.get('title', doc.title)
        doc.content = data.get('content', doc.content)
        doc.save()
        return JsonResponse({'status': 'success'})

    all_users = User.objects.exclude(id=request.user.id)
    shared_with = SharedAccess.objects.filter(document=doc).values_list('shared_with__username', flat=True)

    return render(request, 'editor.html', {
        'document': doc,
        'is_owner': is_owner,
        'all_users': all_users,
        'shared_with': list(shared_with),
    })


@login_required
def share_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id, owner=request.user)  # only owner can share
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            target_user = User.objects.get(username=username)
            SharedAccess.objects.get_or_create(document=doc, shared_with=target_user)
            messages.success(request, f"Shared with {username}")
        except User.DoesNotExist:
            messages.error(request, "User not found")
    return redirect('edit_document', doc_id=doc.id)


@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        allowed_extensions = ('.txt', '.md')

        if not uploaded_file.name.endswith(allowed_extensions):
            messages.error(request, "Only .txt and .md files are supported.")
            return redirect('dashboard')

        content = uploaded_file.read().decode('utf-8', errors='ignore')
        doc = Document.objects.create(
            title=uploaded_file.name,
            content=content.replace('\n', '<br>'),  # basic conversion
            owner=request.user
        )
        return redirect('edit_document', doc_id=doc.id)

    return redirect('dashboard')
