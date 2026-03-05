from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from users.models import User

class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'author', 'created_time']

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role', 'date_joined']

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
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'project', 'author', 'created_time', 'assignee'
        ]

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'uuid', 'issue', 'author', 'content', 'created_time']