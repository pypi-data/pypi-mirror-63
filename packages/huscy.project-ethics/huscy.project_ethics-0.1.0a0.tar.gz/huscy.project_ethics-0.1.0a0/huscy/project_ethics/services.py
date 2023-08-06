from huscy.project_ethics.filters import EthicFilter
from huscy.project_ethics.models import Ethic, EthicBoard, EthicFile


def create_ethic_file(ethic, filehandle, filetype, creator):
    filename = filehandle.name.split('/')[-1]

    return EthicFile.objects.create(
        ethic=ethic,
        filehandle=filehandle,
        filename=filename,
        filetype=filetype,
        uploaded_by=creator.get_full_name(),
    )


def get_ethic_files():
    return EthicFile.objects.all()


def get_ethics(project=None):
    qs = Ethic.objects.order_by('pk')
    filters = dict(project=project and project.pk)
    return EthicFilter(filters, queryset=qs).qs


def get_ethic_boards():
    return EthicBoard.objects.all()
