from huscy.project_archivenotes.filters import ArchiveNoteFilter
from huscy.project_archivenotes.models import ArchiveNote


def get_archive_notes(project=None):
    qs = ArchiveNote.objects.order_by('project__id', 'created_at')
    filters = dict(project=project and project.pk)
    return ArchiveNoteFilter(filters, queryset=qs).qs
