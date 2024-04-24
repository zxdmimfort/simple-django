from workers.utils import menu


def get_worker_context(request):
    return {"mainmenu": menu}
