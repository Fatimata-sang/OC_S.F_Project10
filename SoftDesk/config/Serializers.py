from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User, Project, Issue, Comment, Contributor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email"]


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status']


class IssueListSerializer(serializers.ModelSerializer):
    author_user_id = UserListSerializer()
    assignee_user_id = UserListSerializer()
    
    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'project_id',
            'author_user_id',
            'assignee_user_id',
            'description',
            'tag',
            'priority',
            'status'
        ]


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']


class ProjectListSerializer(serializers.HyperlinkedModelSerializer):
    # Nous redéfinissons l'attribut 'issues' qui porte le même nom que dans la liste des champs à afficher
    # en lui précisant un serializer paramétré à 'many=True' car les issues sont multiples pour une catégorie
    issues = IssueSerializer(many=True)
    author_user_id = UserListSerializer()
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'issues', 'author_user_id']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description']


class CommentListSerializer(serializers.ModelSerializer):
    author_user_id = UserListSerializer()
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'issue_id',
            'author_user_id',
            'description'
        ]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id']


class ContributorListSerializer(serializers.ModelSerializer):
    user_id = UserListSerializer()
    
    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id']
