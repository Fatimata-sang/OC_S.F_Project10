from rest_framework import serializers
from api.models import User, Project, Issue, Comment


# ---------------------------------------------------------
#  UTILISATEURS
# ---------------------------------------------------------

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour créer un nouvel utilisateur.
    """

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'password', 'age',
            'contact_consent', 'data_share_consent'
        ]

    def validate_age(self, value):
        """
        Validation du champ 'age'.
        L'utilisateur doit avoir au minimum 16 ans.
        """
        if value < 16:
            raise serializers.ValidationError("L’âge doit être supérieur ou égal à 16 ans.")
        return value

    def create(self, validated_data):
        """
        Création d'un nouvel utilisateur avec mot de passe chiffré.
        """
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            age=validated_data["age"],
            contact_consent=validated_data["contact_consent"],
            data_share_consent=validated_data["data_share_consent"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Mise à jour d’un utilisateur avec chiffrement du mot de passe.
        """
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer pour afficher une liste d’utilisateurs.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='api:user-detail'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'url']


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer pour afficher les détails d’un utilisateur.
    """

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'age',
            'contact_consent', 'data_share_consent',
            'is_superuser', 'date_joined'
        ]
        read_only_fields = ['id', 'username', 'password', 'date_joined', 'is_superuser']


# ---------------------------------------------------------
#  PROJETS
# ---------------------------------------------------------

class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour créer un projet.
    """

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type']

    def validate(self, attrs):
        """
        Vérifie qu’un projet identique (nom + type)
        n’existe pas déjà pour cet utilisateur.
        """
        project_queryset = self.context["view"].project
        name = attrs.get("name")
        type_ = attrs.get("type")

        if project_queryset.filter(name=name, type=type_).exists():
            raise serializers.ValidationError(
                "Un projet avec ce nom et ce type existe déjà."
            )

        return attrs


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer listant les projets de l'utilisateur.
    """
    url = serializers.HyperlinkedIdentityField(view_name='api:project-detail')

    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'author', 'contributors', 'url']


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillant un projet.
    """

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'type', 'description',
            'author', 'contributors', 'created_time'
        ]


# ---------------------------------------------------------
#  CONTRIBUTEURS
# ---------------------------------------------------------

class ContributorCreateSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour ajouter un contributeur à un projet.
    """

    # ID du user à ajouter, utilisé uniquement en écriture
    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'user']

    def validate_user(self, value):
        """
        Vérifie que :
        - l'utilisateur existe,
        - il n'est pas superuser,
        - il n'est pas déjà contributeur du projet.
        """
        project = self.context["view"].project
        user = User.objects.filter(pk=value).first()

        if user is None:
            raise serializers.ValidationError("Cet utilisateur n'existe pas.")

        if user.is_superuser:
            raise serializers.ValidationError(
                "Un superutilisateur ne peut pas être ajouté comme contributeur."
            )

        if project.contributors.filter(pk=value).exists():
            raise serializers.ValidationError(
                "Cet utilisateur est déjà contributeur de ce projet."
            )

        return user


class ContributorListSerializer(serializers.ModelSerializer):
    """
    Serializer listant les contributeurs d’un projet.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='api:user-detail',
        format='html',
        lookup_field='pk'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'url']


class ContributorDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillant un contributeur.
    """

    class Meta:
        model = User
        fields = [
            'id', 'username', 'age',
            'contact_consent', 'data_share_consent'
        ]


# ---------------------------------------------------------
#  ISSUES
# ---------------------------------------------------------

class IssueCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour créer ou modifier une issue.
    """

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'tag', 'state', 'priority', 'assignee']

    def validate(self, attrs):
        """
        Vérifie qu'une issue identique (nom + tag + state + priority)
        n'existe pas déjà dans le projet.
        """
        name = attrs.get("name")
        tag = attrs.get("tag")
        state = attrs.get("state")
        priority = attrs.get("priority")

        queryset = self.context["view"].issue

        if name:
            queryset = queryset.filter(name=name)
        if tag:
            queryset = queryset.filter(tag=tag)
        if state:
            queryset = queryset.filter(state=state)
        if priority:
            queryset = queryset.filter(priority=priority)

        if queryset.exists():
            raise serializers.ValidationError("Cette issue existe déjà.")

        return attrs


class IssueListSerializer(serializers.ModelSerializer):
    """
    Serializer listant les issues.
    """

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'tag', 'state', 'priority', 'author']


class IssueDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillant une issue.
    """

    class Meta:
        model = Issue
        fields = [
            'id', 'name', 'description', 'tag', 'state',
            'priority', 'created_time', 'author', 'assignee', 'project'
        ]


# ---------------------------------------------------------
#  COMMENTAIRES
# ---------------------------------------------------------

class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour créer un commentaire.
    """

    class Meta:
        model = Comment
        fields = ['id', 'name', 'description']

    def validate_name(self, value):
        """
        Vérifie qu’un commentaire portant le même nom n’existe pas déjà.
        """
        if self.context["view"].comment.filter(name=value).exists():
            raise serializers.ValidationError(
                "Un commentaire portant ce nom existe déjà."
            )

        return value


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer listant les commentaires d’une issue.
    """

    class Meta:
        model = Comment
        fields = ['id', 'name', 'description', 'author']


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillant un commentaire.
    """

    class Meta:
        model = Comment
        fields = [
            'id', 'name', 'description',
            'created_time', 'author', 'issue', 'issue_url'
        ]
