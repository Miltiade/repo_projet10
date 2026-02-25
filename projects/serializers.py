from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from users.models import User

class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Project
        fields = '__all__'

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )
    status = serializers.ChoiceField(choices=Issue.STATUS_CHOICES, default='todo')
    priority = serializers.ChoiceField(choices=Issue.PRIORITY_CHOICES, default='medium')

    class Meta:
        model = Issue
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'