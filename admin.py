from django.contrib import admin
from .models import User, Competence, UserCompetence, Quete, UserQuete

admin.site.register(User)
admin.site.register(Competence)
admin.site.register(UserCompetence)
admin.site.register(Quete)
admin.site.register(UserQuete)
