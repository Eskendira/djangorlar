from rest_framework import serializers

from apps.education.models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'is_active','owner','created_at', 'updated_at','deleted_at','lessons_count']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at', 'owner','lessons_count']

    def get_lessons_count(self, obj):
        return obj.lessons.filter(deleted_at__isnull=True).count()

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'course','indentation','order','is_published','created_at', 'updated_at','deleted_at']
        read_only_fields = ['order','created_at', 'updated_at', 'deleted_at']

        def validate_identation(self, value):
            if value is None:
                return 0    
            if value < 0 or value > 5:
                raise serializers.ValidationError("Indentation must be between 0 and 5.")
            return value

    def create(self, validated_data):
        request = self.context['request']
        course = validated_data.get('course')
        if course.owner != request.user.id:
            raise serializers.ValidationError("You do not have permission to add lessons to this course.")
        return super().create(validated_data)