from api import SarasvatiApi
import logging

# Logging configuration
logging.basicConfig(filename='sarasvati.log', level=logging.DEBUG)

# Sarasvati Application info
version = "0.0.1 Born"
logging.info("Sarasvati " + version)

# Get one application plugin and activate it
_api_instance = SarasvatiApi()
application = _api_instance.get_application_plugin()

try:
    # Run application
    if application is None:
        raise Exception("No specified application plugin found")
    application.activate()
    application.deactivate()
except Exception as ex:
    logging.exception(ex)

    import report
    report.show(ex)

# used by py2app to find all dependencies
from plugins.app.gui import *
from plugins.app.shell import *
from plugins.commands.generic import *
from plugins.commands.shell import *
from plugins.processor.generic import *
from plugins.quick.command import *
from plugins.quick.edit import *
from plugins.storage.local import *
