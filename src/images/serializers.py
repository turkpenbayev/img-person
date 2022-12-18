from logging import getLogger

from rest_framework import serializers

from images.models import Person, Images


logger = getLogger('django')


class ListImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('id', 'file',)
        read_only_fields = fields


class CreateImagesSerializer(serializers.ModelSerializer):
    people = serializers.ListField(child=serializers.CharField(max_length=128))

    class Meta:
        model = Images
        fields = ('id', 'file', 'date', 'location', 'description', 'people')
        read_only_fields = ('id',)

    def create(self, validated_data):
        people = validated_data.pop('people')
        people = list(set(people))
        instance = super().create(validated_data)
        people_obj = []
        for person_name in people:
            person, _ = Person.objects.get_or_create(name=person_name.lower())
            people_obj.append(person.pk)

        logger.info(f'adding person names to image')
        instance.people.add(*people_obj)

        return instance


class RetrieveImagesSerializer(serializers.ModelSerializer):
    people = serializers.SerializerMethodField()

    class Meta:
        model = Images
        fields = ('id', 'file', 'date', 'location', 'description', 'people')
        read_only_fields = fields

    def get_people(self, instance):
        return [item.name for item in instance.people.all()]


class ListPersonNameSerializer(serializers.Serializer):
    names = serializers.ListField(child=serializers.CharField(max_length=128))
