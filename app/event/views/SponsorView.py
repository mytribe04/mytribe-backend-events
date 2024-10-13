from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.sponsor import Sponsor
from ..serializers.sponsor_serializer import SponsorSerializer


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
