from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import Project


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission objet :
    Autorise uniquement l'auteur à modifier ou supprimer l'objet.
    La lecture est accessible à tous.
    """

    message = "Vous devez être l'auteur pour modifier ou supprimer cet objet."

    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour GET / HEAD / OPTIONS
        if request.method in SAFE_METHODS:
            return True

        # Modification réservée à l'auteur
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    """
    Permission vue :
    Autorise uniquement l'auteur d’un projet
    à gérer ses contributeurs.
    """

    message = "Seul l'auteur du projet peut ajouter ou retirer des contributeurs."

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_id)

        return request.user == project.author


class IsProjectContributor(BasePermission):
    """
    Permission vue :
    Autorise uniquement les contributeurs du projet.
    """

    message = "Vous devez être contributeur de ce projet pour accéder à cette ressource."

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_id)

        return request.user in project.contributors.all()


class UserPermission(BasePermission):
    """
    Permission objet :
    Un utilisateur ne peut consulter ou modifier que son propre compte.
    """

    message = "Vous ne pouvez consulter ou modifier que votre propre compte."

    def has_object_permission(self, request, view, obj):
        return view.action in ["retrieve", "update", "partial_update"] and obj == request.user
