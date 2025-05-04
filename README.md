# Blood Report Analyzer

A web-based AI-powered application to analyze blood test reports.  
It extracts key health indicators from blood reports, interprets values, and generates a structured summary report for easy understanding.

## Features

- 📸 Upload blood test report images (scanned or photographed)
- 🧬 Extract key blood parameters using AI-powered OCR and text parsing
- 📊 Generate clear, structured summaries of test results
- 📄 Download clean PDF summary reports
- 🌐 Deployed on Hugging Face Spaces (Gradio-powered)

## Demo

🚀 **Try the app live:** [Blood Report Analyzer on Hugging Face Spaces](https://huggingface.co/spaces/vijaykumar1372/blood_report_analyser)

> ⚠️ **Note:** Web scraping features (if used for reference data) may not work properly on Hugging Face Spaces due to environment limitations.  
> 🖥️ For full functionality, please run the app locally if needed.

## Tech Stack

- **Web Framework:** Gradio  
- **OCR / Text Extraction:** Google Gemini API  
- **PDF Report Generation:** Custom Python script (pdf_generator.py)  
- **Deployment:** Hugging Face Spaces (Gradio)

## Project Structure

```
├── app.py                      # Main Gradio app
├── pdf_generator.py            # Custom PDF generation script
├── extract_blood_report.py     # Text extraction and parsing logic
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Installation (Local)

```
git clone https://github.com/HR-VijayKumar/blood-report-analyzer.git
cd blood-report-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app locally
python app.py
```

## Usage

1. Upload a clear photo or scanned image of your blood test report.
2. The app will:
   - Extract text and detect key parameters (e.g., Hemoglobin, WBC count, etc.)
   - Display a structured summary of test results
   - Provide a download link for the PDF summary report
3. Download the PDF report for personal use or consultation.

## Disclaimer

This tool is intended for informational purposes only and is not a substitute for professional medical advice. Always consult a healthcare provider for diagnosis and treatment.

## Contributing

Contributions are welcome!  
Please open issues or submit pull requests for feature suggestions, bug fixes, or improvements.

## License

MIT License — see LICENSE file for details.
