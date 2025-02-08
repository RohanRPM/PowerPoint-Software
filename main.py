import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import json


class PresentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Presentation Tool")
        self.root.geometry("1000x700")
        
        # Initialize slides
        self.slides = [
            {"title": "Welcome Slide", "content": "Welcome to the presentation!", "images": []}
        ]
        self.current_slide = 0

        # Create a Canvas to display slide content
        self.canvas = tk.Canvas(root, width=800, height=500, bg="white", highlightthickness=2)
        self.canvas.pack(pady=10)

        # Create a Text widget for editing slide content
        self.text_editor = tk.Text(root, height=5, wrap=tk.WORD, font=("Arial", 12))
        self.text_editor.pack(fill=tk.X, padx=10, pady=5)
        self.text_editor.bind("<KeyRelease>", self.update_slide_content)

        # Control Buttons Frame
        self.control_frame = ttk.Frame(root)
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Navigation Buttons
        ttk.Button(self.control_frame, text="First", command=self.first_slide).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.control_frame, text="Previous", command=self.prev_slide).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.control_frame, text="Next", command=self.next_slide).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.control_frame, text="Last", command=self.last_slide).pack(side=tk.LEFT, padx=5)

        # Slide Management Buttons
        ttk.Button(self.control_frame, text="Add Slide", command=self.add_slide).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.control_frame, text="Delete Slide", command=self.delete_slide).pack(side=tk.LEFT, padx=5)

        # Save & Load Buttons
        ttk.Button(self.control_frame, text="Save", command=self.save_presentation).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.control_frame, text="Load", command=self.load_presentation).pack(side=tk.LEFT, padx=5)

        # Image Upload Button
        ttk.Button(self.control_frame, text="Add Image", command=self.add_image).pack(side=tk.LEFT, padx=5)

        # Display first slide
        self.display_slide()

    def display_slide(self):
        """ Displays the current slide on the canvas """
        self.canvas.delete("all")
        slide = self.slides[self.current_slide]
        
        # Title
        self.canvas.create_text(400, 50, text=slide["title"], font=("Arial", 24, "bold"), fill="darkblue")

        # Content
        self.canvas.create_text(400, 250, text=slide["content"], font=("Arial", 16), width=700, fill="black")

        # Update text editor
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert(tk.END, slide["content"])

        # Display Images
        x_pos = 150
        if "images" in slide:
            for img_data in slide["images"]:
                if "photo" in img_data:
                    self.canvas.create_image(x_pos, 400, image=img_data["photo"])
                    x_pos += 250

    def update_slide_content(self, event):
        """ Updates the slide content in real-time when editing """
        self.slides[self.current_slide]["content"] = self.text_editor.get("1.0", tk.END).strip()

    def next_slide(self):
        """ Navigates to the next slide """
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            self.display_slide()

    def prev_slide(self):
        """ Navigates to the previous slide """
        if self.current_slide > 0:
            self.current_slide -= 1
            self.display_slide()

    def first_slide(self):
        """ Jumps to the first slide """
        self.current_slide = 0
        self.display_slide()

    def last_slide(self):
        """ Jumps to the last slide """
        self.current_slide = len(self.slides) - 1
        self.display_slide()

    def add_slide(self):
        """ Adds a new slide """
        self.slides.append({"title": f"Slide {len(self.slides) + 1}", "content": "", "images": []})
        self.current_slide = len(self.slides) - 1
        self.display_slide()

    def delete_slide(self):
        """ Deletes the current slide (if more than one exists) """
        if len(self.slides) > 1:
            del self.slides[self.current_slide]
            self.current_slide = max(0, self.current_slide - 1)
            self.display_slide()
        else:
            messagebox.showwarning("Warning", "You cannot delete the only slide!")

    def save_presentation(self):
        """ Saves the presentation to a JSON file """
        slides_copy = []

        for slide in self.slides:
            slide_copy = slide.copy()
            slide_copy["images"] = [img["path"] for img in slide.get("images", [])]  # Save only image paths
            slides_copy.append(slide_copy)

        with open("presentation.json", "w") as f:
            json.dump(slides_copy, f, indent=4)

        messagebox.showinfo("Success", "Presentation saved successfully!")

    def load_presentation(self):
        """ Loads a saved presentation from a JSON file """
        try:
            with open("presentation.json", "r") as f:
                self.slides = json.load(f)

            # Reload images from file paths
            for slide in self.slides:
                slide["images"] = [
                    {"path": img_path, "photo": ImageTk.PhotoImage(Image.open(img_path).resize((200, 200)))}
                    for img_path in slide.get("images", [])
                ]

            self.current_slide = 0
            self.display_slide()
            messagebox.showinfo("Success", "Presentation loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading presentation: {e}")

    def add_image(self):
        """ Adds an image to the current slide """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img = Image.open(file_path).resize((200, 200))
            photo = ImageTk.PhotoImage(img)

            # Store path and PhotoImage object
            self.slides[self.current_slide].setdefault("images", []).append({"path": file_path, "photo": photo})

            self.display_slide()


if __name__ == "__main__":
    root = tk.Tk()
    app = PresentationApp(root)
    root.mainloop()
