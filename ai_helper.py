from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import onnxruntime as ort
from transformers.onnx import export as onnx_export
from pathlib import Path

class AISummarizer:
    def __init__(self):
        self.model_name = "sshleifer/distilbart-cnn-12-6"  # A small summarization model
        self.setup_onnx()

    def setup_onnx(self):
        onnx_path = Path("model.onnx")
        if not onnx_path.exists():
            self.export_model_to_onnx(onnx_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.session = ort.InferenceSession(str(onnx_path))  # Ensure path is string

    def export_model_to_onnx(self, path):
        # Load the PyTorch model
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Corrected ONNX export function call
        onnx_export(preprocessor=tokenizer, model=model, output=path, opset=12)

        print("Exported model to ONNX.")

    def summarize(self, text, max_length=50):
        # Tokenize input text.
        inputs = self.tokenizer([text], return_tensors="np", max_length=1024, truncation=True)
        outputs = self.session.run(None, dict(inputs))
        # Decode the summary. (This is a simplified example.)
        summary = self.tokenizer.decode(outputs[0][0], skip_special_tokens=True)
        return summary
