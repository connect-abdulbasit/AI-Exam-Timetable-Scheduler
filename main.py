import sys
import os
import types

# Project root is this folder (contains gui/, core/, models/). Code uses the package name
# "exam_scheduler" in relative imports (..core, ..models), but the directory is not literally
# named exam_scheduler — register it so imports resolve.
ROOT = os.path.dirname(os.path.abspath(__file__))
_pkg = types.ModuleType("exam_scheduler")
_pkg.__path__ = [ROOT]
sys.modules["exam_scheduler"] = _pkg

from exam_scheduler.gui.main_window import AppWindow
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
