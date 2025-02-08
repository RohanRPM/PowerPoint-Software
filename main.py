import tkinter as tk
from tkinter import ttk
from ai_helper import AISummarizer
from tkinter import filedialog
from PIL import Image, ImageTk


class PresentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Presentation Tool")
        # Initialize slides: for a simple start, each slide is a dict with a title and content.
        self.slides = [
            {"title": "Welcome Slide", "content": "Welcome to the presentation!"}
        ]
        self.current_slide = 0

        # Create a Canvas to display slide content.
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Create a Text widget for editing slide content.
        self.text_editor = tk.Text(root, height=10)
        self.text_editor.pack(fill=tk.X)
        self.text_editor.bind("<KeyRelease>", self.update_slide_content)

        # Create control buttons.
        self.prev_btn = ttk.Button(root, text="Previous", command=self.prev_slide)
        self.prev_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_btn = ttk.Button(root, text="Next", command=self.next_slide)
        self.next_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        # Save and Load buttons (added later in file handling).
        self.save_btn = ttk.Button(root, text="Save", command=self.save_presentation)
        self.save_btn.pack(side=tk.BOTTOM, pady=5)
        self.load_btn = ttk.Button(root, text="Load", command=self.load_presentation)
        self.load_btn.pack(side=tk.BOTTOM, pady=5)
        
        self.image_btn = ttk.Button(root, text="Add Image", command=self.add_image)
        self.image_btn.pack(side=tk.BOTTOM, pady=5)


        # (Optional) AI Summarization button.
        self.ai_btn = ttk.Button(root, text="AI Summarize", command=self.ai_summarize)
        self.ai_btn.pack(side=tk.BOTTOM, pady=5)
        self.summarizer = AISummarizer()
        # Display the first slide.
        self.display_slide()


    def display_slide(self):
        self.canvas.delete("all")
        slide = self.slides[self.current_slide]
        self.canvas.create_text(400, 50, text=slide["title"], font=("Arial", 24))
        self.canvas.create_text(
            400, 300, text=slide["content"], font=("Arial", 16), width=700
        )
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert(tk.END, slide["content"])

        # Display images if any.
        if "images" in slide:
            x_pos = 150
            for photo in slide["images"]:
                self.canvas.create_image(x_pos, 500, image=photo)
                x_pos += 250

    def update_slide_content(self, event):
        # Update current slide's content based on text editor.
        self.slides[self.current_slide]["content"] = self.text_editor.get(
            "1.0", tk.END
        ).strip()

    def next_slide(self):
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            self.display_slide()

    def prev_slide(self):
        if self.current_slide > 0:
            self.current_slide -= 1
            self.display_slide()

    # File Handling methods (see Step 5).
    def save_presentation(self):
        import json

        with open("presentation.json", "w") as f:
            json.dump(self.slides, f)
        print("Presentation saved.")
    def add_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            img = Image.open(file_path)
            img = img.resize((200, 200))  # Adjust as needed
            photo = ImageTk.PhotoImage(img)
            # Save image in slide data; ensure the 'images' list exists.
            self.slides[self.current_slide].setdefault("images", []).append(photo)
            self.display_slide()
    def load_presentation(self):
        import json

        try:
            with open("presentation.json", "r") as f:
                self.slides = json.load(f)
            self.current_slide = 0
            self.display_slide()
            print("Presentation loaded.")
        except Exception as e:
            print("Error loading presentation:", e)

    # Placeholder for AI summarization (see Step 6).
    def ai_summarize(self):
        # Retrieve current text.
        current_text = self.text_editor.get("1.0", tk.END).strip()
        if current_text:
            summary = self.summarizer.summarize(current_text, max_length=50)
            # Update text editor and slide content with the summary.
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert(tk.END, summary)
            self.slides[self.current_slide]["content"] = summary
            self.display_slide()


if __name__ == "__main__":
    root = tk.Tk()
    app = PresentationApp(root)
    root.mainloop()
