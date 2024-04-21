from django.contrib import admin
from catalog.models import Collection, Container


class ContainerAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'url_type')
    search_fields = ('title', 'container__name')


admin.site.register(Container, ContainerAdmin)
admin.site.register(Collection)

