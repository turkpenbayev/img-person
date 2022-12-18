from logging import getLogger

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins, exceptions, parsers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from images.filters import ImagesFilter
from images.models import Images, Person
from images.serializers import ListImagesSerializer, RetrieveImagesSerializer, \
    CreateImagesSerializer, ListPersonNameSerializer


logger = getLogger('django')


class ActionSerializerViewSetMixin(object):
    """
    Utility class for get different serializer class by method.
    For example:
    method_serializer_classes = {
        ('list', ): MyModelListViewSerializer,
        ('create', 'update'): MyModelCreateUpdateSerializer
    }
    """
    serializer_classes = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = ImagesFilter

    def get_serializer_class(self):
        assert self.serializer_classes is not None, (
            'Expected viewset %s should contain serializer_classes '
            'to get right serializer class.' %
            (self.__class__.__name__,)
        )
        serializer_cls = self._get_serializer_class(
            self.serializer_classes, self.action)
        if serializer_cls is not None:
            return serializer_cls

        raise exceptions.MethodNotAllowed(self.request.method)

    def _get_serializer_class(self, classes, action):
        for actions, serializer_cls in classes.items():
            if action in actions:
                return serializer_cls
        return None


class ImagesViewSet(ActionSerializerViewSetMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_classes = {
        'retrieve': RetrieveImagesSerializer,
        'list': ListImagesSerializer,
        'create': CreateImagesSerializer
    }
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

    def get_queryset(self):
        qs = Images.objects.all()
        if self.action == 'retrieve':
            qs.prefetch_related('people')
        return qs

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM,
                              type=openapi.TYPE_FILE, required=True),
            openapi.Parameter('people', openapi.IN_FORM,
                              type=openapi.TYPE_ARRAY, items=openapi.Items(
                                  type=openapi.TYPE_STRING),
                              required=True, collection_format='multi'),
            openapi.Parameter('date', openapi.IN_FORM, type=openapi.TYPE_STRING,
                              format=openapi.FORMAT_DATETIME, required=True),
            openapi.Parameter('location', openapi.IN_FORM,
                              type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('description', openapi.IN_FORM,
                              type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            '201': RetrieveImagesSerializer,
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        data = RetrieveImagesSerializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED)


class PersonNamesViewSet(viewsets.GenericViewSet):
    serializer_class = ListPersonNameSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, required=True)
        ]
    )
    @action(methods=['GET'], detail=False)
    def names(self, request, pk=None, *args, **kwargs):
        name_query = request.query_params['name'].lower()
        names = Person.objects.filter(
            name__startswith=name_query
        ).values_list('name', flat=True)
        serializer = self.get_serializer({'names': names})
        return Response(serializer.data, status=status.HTTP_200_OK)
