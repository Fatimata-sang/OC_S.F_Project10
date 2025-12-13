from django.urls import include, path
from rest_framework_nested import routers as nested_routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import (
    RegisterView,
    UserViewSet,
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet
)

app_name = "api"

# We use rest_framework_nested allowing nested urls.
# https://github.com/alanjds/drf-nested-routers
# Examples:
# domains_router = routers.NestedSimpleRouter(router, r'domains', lookup='domain')
# domains_router.register(r'nameservers', NameserverViewSet, basename='domain-nameservers').
# 'basename' is optional. Needed only if the same viewset is registered more than once.

# DefaultRouter for the API Root
default_router = nested_routers.DefaultRouter()

# To generate:/users/ and /users/{pk}/
default_router.register(r'users', UserViewSet, basename="user")

# To generate:/projects/ and /projects/{pk}/
default_router.register(r'projects', ProjectViewSet, basename="project")

# projects router - for 2nd level of nesting
project_router = nested_routers.NestedSimpleRouter(default_router, r"projects", lookup="project")

# To generate:api/projects/{pk}/contributors/ and api/projects/{pk}/contributors/{pk}/
project_router.register(r"contributors", ContributorViewSet, basename="project-contributor")

# To generate:api/projects/{pk}/issues/ and api/projects/{pk}/issues/{pk}/
project_router.register(r"issues", IssueViewSet, basename="project-issue")

# comments router - for 3rd level of nesting
comment_router = nested_routers.NestedSimpleRouter(project_router, r"issues", lookup="issue")

# To generate:api/projects/{pk}/issues/{pk}/comments/ and api/projects/{pk}/issues/{pk}/comments/{pk}/
comment_router.register(r"comments", CommentViewSet, basename="issue-comment")


# Wire up our API using automatic URL routing.
# Additionally, we include login and signup URLs for the browsable API.
urlpatterns = [
    path('', include(default_router.urls)),
    path('', include(project_router.urls)),
    path('', include(comment_router.urls)),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
