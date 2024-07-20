from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from ..models.organiser import Organiser
from ..serializers.organiserSerializer import OrganiserSerializer


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
