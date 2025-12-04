from rest_framework.permissions import BasePermission
from SoftDesk.api.models import Contributor


class IsAuthor(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `author_user_id` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author_user_id == request.user


class IsContributor(BasePermission):
    """
    Permission a utiliser pour les objets Project
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.contributors.all()


class CustomIsProjectAuthorOrContrib(BasePermission):
    """
    Permission instanciable afin de lui communiquer l'objet Project
    Renvoie True si l'utilisateur auth est auteur ou contributeur
    """

    def __call__(self):
        return self

    def __init__(self, project):
        self.project = project

    def has_permission(self, request, view):
        is_author = request.user == self.project.author_user_id
        print('is project author : ', is_author)
        is_contributor = Contributor.objects.filter(user_id=request.user,
                                                    project_id=self.project).exists()
        print('is project contributor : ', is_contributor)

        return is_author or is_contributor
