import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")

# Initialize Gemini API
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    raise ValueError("API key not found! Please check your .env file.")

class PresentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Presentation Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize Gemini API
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Title Label
        self.title_label = tk.Label(root, text="Dynamic Presentation Tool", font=("Arial", 20, "bold"), bg="#00509E", fg="white", padx=20, pady=10)
        self.title_label.pack(fill=tk.X)
        
        # Slide Canvas
        self.canvas_frame = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)
        self.canvas_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=450, bg="white", highlightthickness=0)
        self.canvas.pack()
        
        # Text Editor for Slide Content
        self.text_editor = scrolledtext.ScrolledText(root, height=5, wrap=tk.WORD, font=("Arial", 12))
        self.text_editor.pack(fill=tk.X, padx=10, pady=5)
        self.text_editor.bind("<KeyRelease>", self.update_slide_content)
        
        # Control Buttons Frame
        self.control_frame = ttk.Frame(root)
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Navigation Buttons
        nav_buttons = [
            ("First", self.first_slide),
            ("Previous", self.prev_slide),
            ("Next", self.next_slide),
            ("Last", self.last_slide)
        ]
        for txt, cmd in nav_buttons:
            ttk.Button(self.control_frame, text=txt, command=cmd).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Slide Management Buttons
        ttk.Button(self.control_frame, text="Add Slide", command=self.add_slide).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.control_frame, text="Delete Slide", command=self.delete_slide).pack(side=tk.LEFT, padx=5)
        
        # Save & Load Buttons
        ttk.Button(self.control_frame, text="Save", command=self.save_presentation).pack(side=tk.RIGHT, padx=5)
        ttk.Button(self.control_frame, text="Load", command=self.load_presentation).pack(side=tk.RIGHT, padx=5)
        
        # Image Upload Button
        ttk.Button(self.control_frame, text="Add Image", command=self.add_image).pack(side=tk.RIGHT, padx=5)
        
        # Summarize Button
        ttk.Button(self.control_frame, text="Summarize", command=self.summarize_content).pack(side=tk.RIGHT, padx=5)
        
        # Initialize slides
        self.slides = [{"title": "Welcome Slide", "content": "Welcome to the presentation!", "images": []}]
        self.current_slide = 0
        
        # Display first slide
        self.display_slide()
        
        # Keyboard shortcuts
        self.root.bind("<Left>", lambda event: self.prev_slide())
        self.root.bind("<Right>", lambda event: self.next_slide())
    
    def display_slide(self):
        self.canvas.delete("all")
        slide = self.slides[self.current_slide]
        
        self.canvas.create_text(400, 50, text=slide["title"], font=("Arial", 24, "bold"), fill="darkblue")
        self.canvas.create_text(400, 200, text=slide["content"], font=("Arial", 16), width=700, fill="black")
        
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert(tk.END, slide["content"])
        
        x_pos = 200
        for img_data in slide.get("images", []):
            if "photo" in img_data:
                self.canvas.create_image(x_pos, 350, image=img_data["photo"])
                x_pos += 250
    
    def update_slide_content(self, event):
        self.slides[self.current_slide]["content"] = self.text_editor.get("1.0", tk.END).strip()
    
    def next_slide(self):
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            self.display_slide()
    
    def prev_slide(self):
        if self.current_slide > 0:
            self.current_slide -= 1
            self.display_slide()
    
    def first_slide(self):
        self.current_slide = 0
        self.display_slide()
    
    def last_slide(self):
        self.current_slide = len(self.slides) - 1
        self.display_slide()
    
    def add_slide(self):
        self.slides.append({"title": f"Slide {len(self.slides) + 1}", "content": "", "images": []})
        self.current_slide = len(self.slides) - 1
        self.display_slide()
    
    def delete_slide(self):
        if len(self.slides) > 1:
            del self.slides[self.current_slide]
            self.current_slide = max(0, self.current_slide - 1)
            self.display_slide()
        else:
            messagebox.showwarning("Warning", "You cannot delete the only slide!")
    
    def save_presentation(self):
        slides_copy = [{"title": s["title"], "content": s["content"], "images": [img["path"] for img in s.get("images", [])]} for s in self.slides]
        with open("presentation.json", "w") as f:
            json.dump(slides_copy, f, indent=4)
        messagebox.showinfo("Success", "Presentation saved successfully!")
    
    def load_presentation(self):
        try:
            with open("presentation.json", "r") as f:
                self.slides = json.load(f)
            for slide in self.slides:
                slide["images"] = [{"path": img, "photo": ImageTk.PhotoImage(Image.open(img).resize((200, 200)))} for img in slide.get("images", [])]
            self.current_slide = 0
            self.display_slide()
            messagebox.showinfo("Success", "Presentation loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading presentation: {e}")
    
    def add_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img = Image.open(file_path).resize((200, 200))
            photo = ImageTk.PhotoImage(img)
            self.slides[self.current_slide].setdefault("images", []).append({"path": file_path, "photo": photo})
            self.display_slide()
    
    def summarize_content(self):
        content = self.text_editor.get("1.0", tk.END).strip()
        if content:
            try:
                response = self.model.generate_content(f"Summarize the following text for a presentation slide: {content}")
                summary = response.text
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert(tk.END, summary)
                self.slides[self.current_slide]["content"] = summary
                self.display_slide()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to summarize content: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter some content to summarize.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PresentationApp(root)
    root.mainloop()