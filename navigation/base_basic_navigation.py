#navigation/base_basic_navigation
import time
import psutil
import subprocess
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
import os

class BasicNavigation:
    def __init__(self):
        self.config = None
        self.pos_name = None
        self.working_directory = None
        self.executable_path = None
        self.running_program_title = None
        self.main_window_title = None
        self.backend = 'uia'

    def set_attributes(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def prepare_pos(self):
        self.set_attributes()
        print(f"Preparing {self.pos_name} for automation")
        self.cleanup()
        self.launchPOS()
        self.wait_for_pos_to_launch()


    def cleanup(self):
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if self.running_program_title in process.info['name']:
                try:
                    process_obj = psutil.Process(process.info['pid'])
                    process_obj.terminate()  # Terminate the process
                    process_obj.wait(timeout=2)
                    print("Clean-Up successful")  # Optionally wait for the process to terminate
                except psutil.NoSuchProcess:
                    pass

    def launchPOS(self):
        try:
            os.chdir(self.working_directory)
            subprocess.Popen([self.executable_path])
            print(f"Launching {self.pos_name}")
        except FileNotFoundError:
            print(f"{self.pos_name} executable not found. Please provide a valid path.")
            exit(1)

    def wait_for_pos_to_launch(self):
        timeout_duration = 60  # seconds
        start_time = time.time()
        window_found = None  # To track if the window was found
        while time.time() - start_time < timeout_duration:
            try:
                app = Application(backend="uia").connect(title_re=self.main_window_title)  # Assuming this is the correct config attribute
                window = app.window(title_re=self.main_window_title)
                if window.exists():
                    window_found = window
                    break  # Window found, exit the loop
            except ElementNotFoundError:
                pass  # Continue waiting if the window is not found yet
            except Exception as e:
                print(f"Unexpected error while trying to connect: {e}")
                break  # Exit the loop on unexpected error
            time.sleep(1)  # Wait a bit before trying again to reduce CPU usage

        if window_found is None:
            print(f"{self.pos_name} window not found within the timeout period.")
        else:
            print(f"{self.pos_name} window is ready.")


    def close_pos(self):
        raise NotImplementedError("This method should be implemented by subclasses.")








