from rest_framework import serializers
from api.models import User, Project, Issue, Comment


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used to create a new user.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'age', 'contact_consent',
                  'data_share_consent']

    def validate_age(self, value):
        """
        Creates custom field-level validation by adding validate_<field_name> method.
        Reference = https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
        """
        if value < 16:
            raise serializers.ValidationError("Age must be 16 or older.")
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            age=validated_data["age"],
            contact_consent=validated_data["contact_consent"],
            data_share_consent=validated_data["data_share_consent"],
        )
        # password encrypted
        user.set_password(validated_data["password"])

        # save the data in the database
        user.save()
        return user

    def update(self, instance, validated_data):
        # save new data with encrypted passwords
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer used to display all users in a list view.
    """
    # url displaying the user's detailed view.
    url = serializers.HyperlinkedIdentityField(view_name='api:user-detail')

    class Meta:
        model = User
        fields = ['id', 'username', 'url']


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer used to display a single user with more detailed info.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'age', 'contact_consent', 'data_share_consent',
                  'is_superuser', 'date_joined']
        read_only_fields = ['id', 'username', 'password', 'date_joined', 'is_superuser']


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used to create a project.
    """

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type']

    def validate(self, attrs):
        """
        Checks that the project has not already been created.
        Else, a validation error is raised.
        Reference = https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
        """
        if (
                # access project attribute from the viewset
                self.context["view"].project.filter(name=attrs["name"], type=attrs["type"]).exists()
        ):
            raise serializers.ValidationError("A project with the same name and type exists already!")
        return attrs


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer to display a list of projects.
    """
    # url displaying a project's detailed view.
    url = serializers.HyperlinkedIdentityField(view_name='api:project-detail')

    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'author', 'contributors', 'url']


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer to display the details of a given project.
    """

    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'description', 'author', 'contributors', 'created_time']


class ContributorCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used to display all contributors of a project in a list view
    """

    # We create an attribute 'user', which is write_only and given a value.
    # It will be used for field-level validations.
    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'user']

    def validate_user(self, value):
        """
        Creates custom field-level validation by adding .validate_<field_name> method.
        https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
        """
        # retrieves the first record that matches pk=value
        user = User.objects.filter(pk=value).first()

        if user is None:
            raise serializers.ValidationError("User does not exist!")

        if user.is_superuser:
            raise serializers.ValidationError("A Superuser cannot be added as contributor.")

        if self.context["view"].project.contributors.filter(pk=value).exists():
            raise serializers.ValidationError("This user is already a contributor of this project.")

        return user


class ContributorListSerializer(serializers.ModelSerializer):
    """
    Serializer used to display all contributors of a project in a list view
    """
    # url of contributor's detailed view.
    url = serializers.HyperlinkedIdentityField(view_name='api:user-detail', format='html', lookup_field='pk')

    class Meta:
        model = User
        fields = ['id', 'username', 'url']


class ContributorDetailSerializer(serializers.ModelSerializer):
    """
    Serializer used to display the details of a single project contributor.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'contact_consent', 'data_share_consent']


class IssueCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create and edit an Issue.
    """

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'tag', 'state', 'priority', 'assignee']

    #def validate(self, attrs):
        """
        Checks that the issue has not already been created.
        Else, a validation error is raised.
        """
        #if (self.context["view"].issue.filter(name=attrs.get("name"), tag=attrs.get("tag"),
         #                                     state=attrs.get("state"),
          #                                    priority=attrs.get("priority")).exists()):
        #    raise serializers.ValidationError("This issue exists already!")

       # return attrs
    def validate(self, attrs):
        """
        Checks that the issue has not already been created.
        Else, a validation error is raised.
        """
        name = attrs.get("name")
        tag = attrs.get("tag")
        state = attrs.get("state")
        priority = attrs.get("priority")

        # IMPORTANT : filtrer seulement sur les champs fournis
        query = self.context["view"].issue

        if name is not None:
            query = query.filter(name=name)
        if tag is not None:
            query = query.filter(tag=tag)
        if state is not None:
            query = query.filter(state=state)
        if priority is not None:
            query = query.filter(priority=priority)

        if query.exists():
            raise serializers.ValidationError("This issue exists already!")

        return attrs


class IssueListSerializer(serializers.ModelSerializer):
    """
    Serializer to display issues in list view.
    """

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'tag', 'state', 'priority', 'author']


class IssueDetailSerializer(serializers.ModelSerializer):
    """
    Serializer to display the details of an Issue.
    """

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'tag', 'state', 'priority', 'created_time',
                  'author', 'assignee', 'project']


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used to create a new Comment for an Issue.
    """

    class Meta:
        model = Comment
        fields = ['id', 'name', 'description']

    def validate_name(self, value):
        if self.context["view"].comment.filter(name=value).exists():
            raise serializers.ValidationError("This comment name exists already.")

        return value


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer used to display all comments of an Issue in list view.
    """

    class Meta:
        model = Comment
        fields = ['id', 'name', 'description', 'author']


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer to display the details of a comment.
    """

    class Meta:
        model = Comment
        fields = ['id', 'name', 'description', 'created_time', 'author', 'issue', 'issue_url']
