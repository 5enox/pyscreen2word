from tkinter import *
from PIL import ImageTk, Image
import pyscreenshot as ImageGrab


class OverlayWindow:
    def __init__(self, screenshot):
        self.screenshot = screenshot
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0  # Initial selection coordinates
        self.dragging = False

        # Create a new window for editing
        self.window = Toplevel()
        self.window.title("Edit Screenshot")

        # Display the screenshot
        self.img = ImageTk.PhotoImage(image=screenshot)
        self.image_label = Label(self.window, image=self.img)
        self.image_label.pack()

        # Overlay canvas for highlighting selection
        self.overlay = Canvas(
            self.window, width=screenshot.width, height=screenshot.height)
        self.overlay.pack()

        # Bind events for selection
        self.overlay.bind("<Button-1>", self.start_selection)
        self.overlay.bind("<B1-Motion>", self.update_selection)
        self.overlay.bind("<ButtonRelease-1>", self.end_selection)

        # Button to confirm and display cropped image in new window
        crop_button = Button(self.window, text="Crop", command=self.crop_image)
        crop_button.pack()

        # Run the window event loop
        self.window.mainloop()

    def start_selection(self, event):
        self.x1, self.y1 = event.x, event.y
        self.dragging = True

    def update_selection(self, event):
        if self.dragging:
            self.x2, self.y2 = event.x, event.y
            self.draw_selection()

    def end_selection(self, event):
        self.dragging = False

    def draw_selection(self):
        # Clear previous selection
        self.overlay.delete("selection")

        # Choose darkening or red lines for selection
        # Option 1: Darken the rest of the image
        mask = Image.new('RGBA', self.screenshot.size,
                         (0, 0, 0, 128))  # Semi-transparent black
        mask.paste(self.screenshot, (0, 0), mask=Image.fromarray(np.ones((self.screenshot.size), dtype=np.uint8)
                   * 255 - np.array(self.overlay.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="", outline=""))))
        self.img = ImageTk.PhotoImage(image=mask)
        self.image_label.config(image=self.img)
        self.image_label.image = self.img  # Keep reference

        # Option 2: Draw red lines around selection
        self.overlay.create_rectangle(
            self.x1, self.y1, self.x2, self.y2, outline="red", width=2)

    def crop_image(self):
        # Crop the image based on selection coordinates
        cropped_img = self.screenshot.crop(
            (self.x1, self.y1, self.x2, self.y2))

        # Display cropped image in a new window
        new_window = Toplevel()
        new_window.title("Cropped Image")
        cropped_photo = ImageTk.PhotoImage(image=cropped_img)
        image_label = Label(new_window, image=cropped_photo)
        image_label.pack()
        new_window.mainloop()

        # Close the editing window
        self.window.destroy()


def show_screenshot():
    """
    Takes a screenshot, hides the main window, and opens the overlay window for editing.
    """

    root.withdraw()
    screenshot = ImageGrab.grab()
    OverlayWindow(screenshot)
    root.deiconify()


root = Tk()
root.title("Screenshot Viewer")

button = Button(root, text="Take Screenshot", command=show_screenshot)
button.pack()

root.mainloop()
