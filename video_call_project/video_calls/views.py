from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Room, RoomMember
import uuid

@login_required
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        room = Room.objects.create(
            name=room_name,
            host=request.user
        )
        RoomMember.objects.create(
            room=room,
            user=request.user
        )
        return redirect('video_calls:join_room', room_id=room.id)
    return render(request, 'video_calls/create_room.html')

@login_required
def join_room(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_active=True)
    
    # Create or get room member
    member, created = RoomMember.objects.get_or_create(
        room=room,
        user=request.user,
        defaults={'is_connected': True}
    )
    
    if not created:
        member.is_connected = True
        member.save()
    
    context = {
        'room': room,
        'is_host': room.host == request.user,
        'room_members': room.room_members.filter(is_connected=True)
    }
    return render(request, 'video_calls/room.html', context)

@login_required
def leave_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    member = get_object_or_404(RoomMember, room=room, user=request.user)
    member.is_connected = False
    member.save()
    
    # If host leaves, close the room
    if room.host == request.user:
        room.is_active = False
        room.save()
    
    return redirect('video_calls:room_list')

@login_required
def room_list(request):
    active_rooms = Room.objects.filter(is_active=True)
    context = {
        'rooms': active_rooms,
        'hosted_rooms': request.user.hosted_rooms.filter(is_active=True)
    }
    return render(request, 'video_calls/room_list.html', context) 