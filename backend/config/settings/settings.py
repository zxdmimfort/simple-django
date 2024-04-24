import os


MODE = os.environ.get("MODE", "LOCAL")
if MODE == "PROD":
    from .prod import *
elif MODE == "DEV":
    from .dev import *
elif MODE == "TEST":
    from .test import *
else:
    from .local import *
