"""
LCMAP Time Series and Analysis Plotting Tool
"""
import sys
import lcmap_tap
from lcmap_tap.logger import log, exc_handler
from PyQt5.QtWidgets import QApplication
from lcmap_tap.Controls.controls import MainControls

try:
    from pip._internal.operations import freeze
except ImportError:
    from pip.operations import freeze

sys.excepthook = exc_handler


def main():
    """
    TAP main entry point
    Setup working directory and execute Qt main window
    """
    lcmap_tap.mkdirs(lcmap_tap.home())
    log.debug("*** System Information ***")
    log.debug("Platform: %s", sys.platform)
    log.debug("Python: %s", str(sys.version).replace("\n", ""))
    log.debug("Pip: %s", ", ".join(freeze.freeze()))
    log.info("Working directory is: %s", lcmap_tap.home())
    log.info("Running lcmap-tap version %s", lcmap_tap.version())

    # Create a QApplication object, necessary to manage the GUI control flow and settings
    app = QApplication(sys.argv)

    # session_id = "session_{}".format(MainControls.get_time())

    control_window = MainControls()

    if control_window:
        # Enter the main event loop
        # begin event handling for application widgets until exit() is called

        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
