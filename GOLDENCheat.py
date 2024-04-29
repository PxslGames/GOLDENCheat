import tkinter as tk
import pyautogui
import pygetwindow as gw
import threading
import keyboard
import time

class AutoclickerGUI:
    def __init__(self, master):
        self.master = master
        master.title("GOLDENCheat v1.1")
        master.geometry("300x350")  # Set window size

        self.label = tk.Label(master, text="GOLDENCheat v1.1", font=("Arial", 16))
        self.label.pack()

        self.label_made_by = tk.Label(master, text="Made By Pxsl", font=("Arial", 10))
        self.label_made_by.pack()

        self.delay_label = tk.Label(master, text="Delay between clicks (ms):")
        self.delay_label.pack()

        self.delay_entry = tk.Entry(master)
        self.delay_entry.insert(0, "100")
        self.delay_entry.pack()

        self.times_label = tk.Label(master, text="Number of times to type:")
        self.times_label.pack()

        self.times_entry = tk.Entry(master)
        self.times_entry.insert(0, "1")
        self.times_entry.pack()

        self.text_label = tk.Label(master, text="Type AutoType Text Here!")
        self.text_label.pack()

        # Add a text entry for typing
        self.type_entry = tk.Entry(master)
        self.type_entry.pack()

        # Add a label for the keybind instruction
        self.keybind_label = tk.Label(master, text="Press 'TAB' to Start/Stop Autoclicker")
        self.keybind_label.pack()

        # Add a button to open the settings window
        self.settings_button = tk.Button(master, text="Settings", command=self.open_settings)
        self.settings_button.pack()

        # Add a button to start typing
        self.type_button = tk.Button(master, text="Start Typing", command=self.start_typing)
        self.type_button.pack()

        # Set the initial state of the autoclicker to stopped
        self.autoclicker_running = False

        # Add a threading event to safely stop the autoclicker
        self.stop_event = threading.Event()

        # Add a variable to keep track of whether the keybind is pressed
        self.keybind_pressed = False

        # Add an event listener for the default keybind 'TAB'
        keyboard.on_press_key('TAB', self.toggle_keybind)

    def toggle_autoclicker(self, event=None):
        if not self.autoclicker_running:
            self.start_autoclicker()
        else:
            self.stop_autoclicker()

    def start_autoclicker(self):
        delay = float(self.delay_entry.get()) / 1000.0
        times = int(self.times_entry.get())

        self.stop_event.clear()
        self.autoclicker_running = True

        def autoclicker_thread():
            while not self.stop_event.is_set():
                if self.keybind_pressed:
                    active_window = gw.getActiveWindow()
                    if active_window:
                        click_x, click_y = pyautogui.position()
                        pyautogui.click(x=click_x, y=click_y, duration=0.1)
                        time.sleep(int(delay * 1000))
                    else:
                        print("No active window found.")
                        break

            self.autoclicker_running = False

        threading.Thread(target=autoclicker_thread).start()

    def stop_autoclicker(self):
        self.stop_event.set()
        self.autoclicker_running = False

    def toggle_keybind(self, event):
        self.keybind_pressed = not self.keybind_pressed

        if self.keybind_pressed:
            print("Continue generating...")
            self.start_autoclicker()
        else:
            print("Stopped generating.")
            self.stop_autoclicker()

    def start_typing(self):
        # Get the text to type from the entry
        text_to_type = self.type_entry.get()

        # Get the number of times to type from the entry
        times = int(self.times_entry.get())

        # Call the typing function
        self.type_text(text_to_type, times)

    def type_text(self, text, times):
        for _ in range(times):
            # Type the provided text
            pyautogui.typewrite(text)

            # Press the "Enter" key
            pyautogui.press('enter')

            # Add a small delay between repetitions
            time.sleep(1)

    def open_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("200x200")

        delay_label = tk.Label(settings_window, text="Set Delay For Typing (ms):")
        delay_label.pack()

        delay_entry = tk.Entry(settings_window)
        delay_entry.insert(0, self.delay_entry.get())
        delay_entry.pack()

        times_label = tk.Label(settings_window, text="Set Number of Times For Typing:")
        times_label.pack()

        times_entry = tk.Entry(settings_window)
        times_entry.insert(0, self.times_entry.get())
        times_entry.pack()

        startdelay_label = tk.Label(settings_window, text="Set StartDelay For Typing (s):")
        startdelay_label.pack()

        startdelay_entry = tk.Entry(settings_window)
        startdelay_entry.insert(0, "5")  # Add a default value for start delay
        startdelay_entry.pack()

        save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_settings(delay_entry.get(), times_entry.get(), startdelay_entry.get(), settings_window))
        save_button.pack()

    def save_settings(self, new_delay, new_times, new_start_delay, settings_window):
        # Update the delay entry
        self.delay_entry.delete(0, tk.END)
        self.delay_entry.insert(0, new_delay)

        # Update the times entry
        self.times_entry.delete(0, tk.END)
        self.times_entry.insert(0, new_times)

        # Close the settings window
        settings_window.destroy()

    def on_closing(self):
        # Stop the autoclicker and close the window
        self.stop_autoclicker()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoclickerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Set the close button to call on_closing
    root.mainloop()
