from django_filters import rest_framework as filters

from huscy.project_archivenotes import models


class ArchiveNoteFilter(filters.FilterSet):
    class Meta:
        model = models.ArchiveNote
        fields = (
            'project',
        )
