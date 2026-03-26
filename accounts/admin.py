from django.contrib import admin
from .models import Student, Room, Complaint, Fee


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'room')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'capacity', 'available_beds')


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('student', 'issue', 'status')
    list_filter = ('status',)


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status')
    list_filter = ('status',)