from PyQt5.QtCore import QObject, pyqtSignal
import traceback

class FetchWorker(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, fetch_function, view):
        super().__init__()
        self.fetch_function = fetch_function
        self.view = view
        self._is_running = True

    def run(self):
        self._is_running = True
        try:
            self.fetch_function(self.view, self.stop_requested, self.progress.emit)
        except Exception as e:
            self.progress.emit(f"Error: {e}")
            traceback.print_exc()
        finally:
            if self._is_running:
                self.finished.emit()
            else:
                self.stopped.emit()

    def stop(self):
        self._is_running = False

    def stop_requested(self):
        return not self._is_running
