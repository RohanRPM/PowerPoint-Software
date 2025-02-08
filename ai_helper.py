from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers.onnx import export
from pathlib import Path
import torch

class AISummarizer:
    def __init__(self):
        self.model_name = "sshleifer/distilbart-cnn-12-6"  # A small summarization model
        self.setup_onnx()

    def setup_onnx(self):
        onnx_path = Path("model.onnx")
        if not onnx_path.exists():
            self.export_model_to_onnx(onnx_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def export_model_to_onnx(self, path):
        # Load the PyTorch model and tokenizer
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Define example inputs for export
        dummy_input = tokenizer("Hello, this is a test.", return_tensors="pt")
        
        # Export the model to ONNX
        export(
            preprocessor=tokenizer,  # Correct argument name
            model=model,
            output=path,
            opset=12, 
            tokenizer=tokenizer,  # Keep tokenizer for compatibility
            feature="seq2seq-lm",  # Specify model type
            dynamic_axes={"input_ids": {0: "batch_size"}, "attention_mask": {0: "batch_size"}}, 
            example_inputs=(dummy_input["input_ids"], dummy_input["attention_mask"])  # Example inputs
        )
        print("Exported model to ONNX.")

    def summarize(self, text, max_length=50):
        # Tokenize input text
        inputs = self.tokenizer([text], return_tensors="np", max_length=1024, truncation=True)
        outputs = self.session.run(None, dict(inputs))
        # Decode the summary
        summary = self.tokenizer.decode(outputs[0][0], skip_special_tokens=True)
        return summary
