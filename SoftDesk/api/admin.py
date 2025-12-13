from django.contrib import admin
from api.models import User, Project, Issue, Comment


admin.site.register(User)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)