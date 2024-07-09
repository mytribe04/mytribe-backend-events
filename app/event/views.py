from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Event, Organiser, Sponsor
from .serializers import EventSerializer, OrganiserSerializer, SponsorSerializer


# Create your views here.


@api_view(['GET','POST'])
def event_list(request):

    if request.method == 'GET':
        event = Event.objects.all()
        serializer = EventSerializer(event, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, event_id):
    try :
        event = Event.objects.get(pk= event_id)
    except Event.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET' :
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def organiser_list(request):

    if request.method == 'GET':
        organisers = Organiser.objects.all()
        serializer = OrganiserSerializer(organisers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def organiser_detail(request, pk):

    try:
        organiser = Organiser.objects.get(pk=pk)
    except Organiser.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrganiserSerializer(organiser)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def sponsor_list(request):

    if request.method == 'GET':
        sponsor = Sponsor.objects.all()
        serializer = SponsorSerializer(sponsor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def sponsor_detail(request, pk):

    try:
        sponsor = Sponsor.objects.get(pk=pk)
    except Sponsor.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SponsorSerializer(sponsor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
