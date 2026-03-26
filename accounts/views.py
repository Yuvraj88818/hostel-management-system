from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Complaint, Student, Room, Fee


# ------------------ HOME ------------------

def home(request):
    return render(request, 'home.html')


# ------------------ COMPLAINT ------------------

@login_required
def add_complaint(request):
    if request.method == 'POST':
        issue = request.POST['issue']
        description = request.POST['description']

        Complaint.objects.create(
            student=request.user.student,
            issue=issue,
            description=description
        )

        return redirect('view_complaints')

    return render(request, 'add_complaint.html')


@login_required
def view_complaints(request):
    complaints = Complaint.objects.filter(student=request.user.student)
    return render(request, 'view_complaints.html', {'complaints': complaints})


# ------------------ DASHBOARD ------------------

@login_required
def dashboard(request):
    total = Complaint.objects.filter(student=request.user.student).count()
    pending = Complaint.objects.filter(student=request.user.student, status='Pending').count()
    resolved = Complaint.objects.filter(student=request.user.student, status='Resolved').count()

    context = {
        'total': total,
        'pending': pending,
        'resolved': resolved,
    }

    return render(request, 'dashboard.html', context)


# ------------------ FEE ------------------

@login_required
def fee_status(request):
    fees = Fee.objects.filter(student=request.user.student)
    return render(request, 'fee.html', {'fees': fees})


# ------------------ REGISTRATION ------------------

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        room_id = request.POST['room']

        room = Room.objects.get(id=room_id)

        if room.available_beds <= 0:
            return render(request, 'register.html', {
                'rooms': Room.objects.all(),
                'error': 'Room is full ❌'
            })

        user = User.objects.create_user(username=username, password=password)

        Student.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            room=room
        )

        room.available_beds -= 1
        room.save()

        return redirect('login')

    rooms = Room.objects.all()
    return render(request, 'register.html', {'rooms': rooms})