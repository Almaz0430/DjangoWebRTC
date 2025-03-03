from django.contrib import admin
from .models import Room, RoomMember

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'host__username')
    readonly_fields = ('id', 'created_at')

@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'joined_at', 'is_connected')
    list_filter = ('is_connected', 'joined_at')
    search_fields = ('user__username', 'room__name') 