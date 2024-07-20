from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .. import logger
from ..models.event import Event
from ..serializers.event_serializer import EventSerializer
from ..utils.exceptions import CustomException


class EventAPIView(APIView):
    def get(self, request):
        try:
            event = Event.objects.all()
            serializer = EventSerializer(event, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error("Event retrieval failed; Error: %s" % (str(e)))
            raise CustomException(
                message="Error while fetching Event",
                status=HTTP_400_BAD_REQUEST,
                log_msg=str(e),
            )

    def post(self, request):
        try:
            serializer = EventSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Event retrieval failed; Error: %s" % (str(e)))
            raise CustomException(
                message="Error while fetching Event",
                status=HTTP_400_BAD_REQUEST,
                log_msg=str(e),
            )


class EventDetailAPIView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            if not event:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Event detail retrieval failed; Error: %s" % (str(e)))
            raise CustomException(
                message="Error while fetching Event detail",
                status=HTTP_400_BAD_REQUEST,
                log_msg=str(e),
            )

    def put(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            if not event:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Event edit failed; Error: %s" % (str(e)))
            raise CustomException(
                message="Error while editing Event",
                status=HTTP_400_BAD_REQUEST,
                log_msg=str(e),
            )

    def delete(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            if not event:
                return Response(status=status.HTTP_404_NOT_FOUND)
            event.is_active = False
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error("Event Deletion error; Error: %s" % (str(e)))
            raise CustomException(
                message="Error while deleting Event",
                status=HTTP_400_BAD_REQUEST,
                log_msg=str(e),
            )
