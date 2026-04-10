from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Complaint, Student, Room, Fee


# ------------------ HOME ------------------

def home(request):
    return render(request, 'home.html')


# ------------------ REGISTRATION ------------------

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        room_id = request.POST['room']

        # ✅ Prevent duplicate username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ")
            return redirect('register')

        # ✅ Prevent duplicate email
        if Student.objects.filter(email=email).exists():
            messages.error(request, "Email already exists ")
            return redirect('register')

        # ✅ Get room
        room = Room.objects.get(id=room_id)

        # ✅ Prevent room overflow
        if room.available_beds <= 0:
            messages.error(request, "Room is full ")
            return redirect('register')

        # ✅ Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # ✅ AUTO CREATE STUDENT
        Student.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            room=room
        )

        # ✅ Update room beds
        room.available_beds -= 1
        room.save()

        messages.success(request, "Registration successful ")
        return redirect('login')

    rooms = Room.objects.all()
    return render(request, 'register.html', {'rooms': rooms})


# ------------------ COMPLAINT ------------------

@login_required
def add_complaint(request):
    try:
        student = request.user.student
    except:
        messages.error(request, "Student profile not found ")
        return redirect('login')

    if request.method == 'POST':
        issue = request.POST['issue']
        description = request.POST['description']

        Complaint.objects.create(
            student=student,
            issue=issue,
            description=description
        )

        messages.success(request, "Complaint submitted ")
        return redirect('view_complaints')

    return render(request, 'add_complaint.html')


@login_required
def view_complaints(request):
    try:
        student = request.user.student
    except:
        return redirect('login')

    complaints = Complaint.objects.filter(student=student)
    return render(request, 'view_complaints.html', {'complaints': complaints})


# ------------------ DASHBOARD ------------------

@login_required
def dashboard(request):
    try:
        student = request.user.student
    except:
        messages.error(request, "Student profile not found ")
        return redirect('login')

    total = Complaint.objects.filter(student=student).count()
    pending = Complaint.objects.filter(student=student, status='Pending').count()
    resolved = Complaint.objects.filter(student=student, status='Resolved').count()

    context = {
        'total': total,
        'pending': pending,
        'resolved': resolved,
    }

    return render(request, 'dashboard.html', context)


# ------------------ FEE ------------------

@login_required
def fee_status(request):
    student = getattr(request.user, 'student', None)

    if not student:
        messages.error(request, "Student not found ")
        return redirect('login')

    fees = Fee.objects.filter(student=student)

    return render(request, 'fee.html', {'fees': fees})


# ------------------ RECEIPT ------------------

@login_required
def receipt(request, id):
    fee = Fee.objects.get(id=id)
    return render(request, 'receipt.html', {'fee': fee})