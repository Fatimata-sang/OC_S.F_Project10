from django.shortcuts import render

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import User, Project, Issue, Comment
from api.permissions import (
    IsAuthorOrReadOnly,
    IsProjectAuthor,
    IsProjectContributor,
    UserPermission,
)
from api.serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserDetailSerializer,

    ProjectCreateSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,

    ContributorCreateSerializer,
    ContributorListSerializer,
    ContributorDetailSerializer,

    IssueCreateSerializer,
    IssueListSerializer,
    IssueDetailSerializer,

    CommentCreateSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
)


# ---------------------------------------------------------
#  UTILISATEURS
# ---------------------------------------------------------

class RegisterView(generics.CreateAPIView):
    """
    Vue permettant l'inscription d'un nouvel utilisateur.
    """
    serializer_class = UserCreateSerializer
    permission_classes = []


class UserViewSet(ModelViewSet):
    """
    Vue permettant de consulter ou modifier un utilisateur.
    L'utilisateur ne peut modifier que son propre compte.
    """
    permission_classes = [IsAuthenticated, UserPermission]

    def get_serializer_class(self):
        """
        Retourne le serializer approprié selon l'action.
        """
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'list':
            return UserListSerializer
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserDetailSerializer  # par défaut

    def get_queryset(self):
        """
        Retourne la liste ordonnée des utilisateurs.
        """
        return User.objects.all().order_by("date_joined")


# ---------------------------------------------------------
#  PROJETS
# ---------------------------------------------------------

class ProjectViewSet(ModelViewSet):
    """
    Vue permettant de créer, consulter, modifier ou supprimer un projet.
    Seul l'auteur peut modifier ou supprimer.
    """
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    _project = None  # Pour éviter les requêtes répétées

    @property
    def project(self):
        """
        Retourne la liste des projets accessibles à l'utilisateur (en tant que contributeur).
        Valeur mise en cache pour éviter les requêtes multiples.
        """
        if self._project is None:
            self._project = Project.objects.filter(contributors=self.request.user)
        return self._project

    def get_serializer_class(self):
        """
        Choisit automatiquement le serializer selon l'action.
        """
        if self.action == 'create':
            return ProjectCreateSerializer
        if self.action == 'list':
            return ProjectListSerializer
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectCreateSerializer

    def get_queryset(self):
        """
        Retourne la liste des projets ordonnée par date de création.
        """
        return self.project.order_by("created_time")

    def perform_create(self, serializer):
        """
        Lors de la création, l'utilisateur connecté devient :
        - auteur du projet
        - contributeur initial du projet
        """
        serializer.save(author=self.request.user, contributors=[self.request.user])

    def destroy(self, request, *args, **kwargs):
        """
        Suppression d’un projet.
        """
        super().destroy(request, *args, **kwargs)
        return Response({"status": "Projet supprimé avec succès."}, status=204)


# ---------------------------------------------------------
#  CONTRIBUTEURS
# ---------------------------------------------------------

class ContributorViewSet(ModelViewSet):
    """
    Vue permettant d'ajouter, consulter et retirer les contributeurs d’un projet.
    Seul l'auteur du projet peut ajouter/des retirer des contributeurs.
    """
    permission_classes = [IsProjectAuthor]
    _project = None

    @property
    def project(self):
        """
        Retourne le projet concerné, mis en cache.
        """
        if self._project is None:
            self._project = get_object_or_404(
                Project.objects.prefetch_related("contributors"),
                pk=self.kwargs["project_pk"],
            )
        return self._project

    def get_queryset(self):
        """
        Retourne les contributeurs du projet, triés par date d'inscription.
        """
        return self.project.contributors.all().order_by("date_joined")

    def get_serializer_class(self):
        """
        Choisit automatiquement le serializer selon l’action.
        """
        if self.action == 'create':
            return ContributorCreateSerializer
        if self.action == 'list':
            return ContributorListSerializer
        if self.action == 'retrieve':
            return ContributorDetailSerializer
        return ContributorCreateSerializer

    def perform_create(self, serializer):
        """
        Ajoute un contributeur au projet.
        """
        self.project.contributors.add(serializer.validated_data["user"])

    def create(self, request, *args, **kwargs):
        """
        Retourne un message personnalisé après création.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"status": "Contributeur ajouté avec succès."}, status=201)

    def perform_destroy(self, instance):
        """
        Retire un contributeur du projet.
        """
        self.project.contributors.remove(instance)

    def destroy(self, request, *args, **kwargs):
        """
        Retourne un message personnalisé après suppression.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"status": "Contributeur retiré avec succès."}, status=204)

class IssueViewSet(ModelViewSet):
    """
    Vue permettant de créer, consulter, modifier et supprimer des issues.
    - Accessible uniquement aux contributeurs du projet.
    - Modifiable uniquement par l’auteur.
    """
    permission_classes = [IsAuthorOrReadOnly, IsProjectContributor]

    _issue = None

    @property
    def issue(self):
        """
        Retourne les issues du projet (mise en cache).
        """
        if self._issue is None:
            self._issue = Issue.objects.filter(project_id=self.kwargs["project_pk"])
        return self._issue

    def get_queryset(self):
        return self.issue.order_by("created_time")

    def get_serializer_class(self):
        if self.action == 'create':
            return IssueCreateSerializer
        if self.action == 'list':
            return IssueListSerializer
        if self.action == 'retrieve':
            return IssueDetailSerializer
        return IssueCreateSerializer

    def perform_create(self, serializer):
        """
        Lors de la création :
        - auteur = utilisateur connecté
        - assignee = valeur fournie ou auteur par défaut
        - project = projet correspondant
        """
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])
        assignee = serializer.validated_data.get("assignee", self.request.user)

        serializer.save(
            author=self.request.user,
            assignee=assignee,
            project=project
        )

    def destroy(self, request, *args, **kwargs):
        """
        Suppression d’une issue.
        """
        super().destroy(request, *args, **kwargs)
        return Response({"status": "Issue supprimée avec succès."}, status=204)

class CommentViewSet(ModelViewSet):
    """
    Vue permettant de créer, consulter, modifier et supprimer des commentaires.
    - Accessible uniquement aux contributeurs du projet.
    - Modifiable uniquement par l’auteur.
    """
    permission_classes = [IsAuthorOrReadOnly, IsProjectContributor]

    _comment = None

    @property
    def comment(self):
        """
        Retourne les commentaires liés à l’issue (mise en cache).
        """
        if self._comment is None:
            self._comment = Comment.objects.filter(issue_id=self.kwargs["issue_pk"])
        return self._comment

    def get_queryset(self):
        return self.comment.order_by("created_time")

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action == 'list':
            return CommentListSerializer
        if self.action == 'retrieve':
            return CommentDetailSerializer
        return CommentCreateSerializer

    def perform_create(self, serializer):
        """
        Lors de la création :
        - auteur = utilisateur connecté
        - issue = récupération via URL
        - issue_url = URL construite automatiquement
        """
        project_pk = self.kwargs["project_pk"]
        issue_pk = self.kwargs["issue_pk"]

        issue = get_object_or_404(Issue, id=issue_pk)
        issue_url = f"{settings.BASE_URL}/api/projects/{project_pk}/issues/{issue_pk}/"

        serializer.save(
            author=self.request.user,
            issue=issue,
            issue_url=issue_url
        )

    def destroy(self, request, *args, **kwargs):
        """
        Suppression d’un commentaire.
        """
        super().destroy(request, *args, **kwargs)
        return Response({"status": "Commentaire supprimé avec succès."}, status=204)
