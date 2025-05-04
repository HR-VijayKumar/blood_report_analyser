import gradio as gr
import os
import json
import tempfile
import shutil
from datetime import datetime
from PIL import Image
from blood_report_analyser import analyze_blood_report
from pdf_generator import generate_pdf

def process_image(image):
    """Process the blood report image and generate analysis and PDF"""
    if image is None:
        return "Please upload a blood test report image.", None, None
    
    # Create a temp directory to store our files
    temp_dir = os.path.join(tempfile.gettempdir(), "blood_report_analyzer")
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Save the image to a temporary file
        img_path = os.path.join(temp_dir, f"blood_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
        if isinstance(image, str):  # If image is a file path
            shutil.copy(image, img_path)
        else:  # If image is a PIL Image
            image.save(img_path, format="JPEG")
        
        # Analyze image
        json_data = analyze_blood_report(img_path)
        
        # Generate PDF
        pdf_path = os.path.join(temp_dir, f"blood_report_analysis_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
        generate_pdf(json_data, pdf_path)
        
        # Create a nicely formatted version of the JSON for display
        try:
            parsed_json = json.loads(json_data)
            formatted_output = format_json_for_display(parsed_json)
        except:
            formatted_output = json_data
            
        return formatted_output, json_data, pdf_path
            
    except Exception as e:
        return f"Error: {str(e)}", None, None

def format_json_for_display(data):
    """Format JSON data for readable display in the UI"""
    output = []
    
    # Patient details
    if "patient_details" in data:
        output.append("## Patient Details")
        pd = data["patient_details"]
        if pd.get("name"): output.append(f"**Name:** {pd['name']}")
        if pd.get("age"): output.append(f"**Age:** {pd['age']}")
        if pd.get("gender"): output.append(f"**Gender:** {pd['gender']}")
        if pd.get("id"): output.append(f"**ID:** {pd['id']}")
        output.append("")
    
    # Test date
    if "test_date" in data:
        output.append(f"**Test Date:** {data['test_date']}")
        output.append("")
    
    # Blood parameters
    if "blood_parameters" in data:
        output.append("## Blood Parameters")
        for param in data["blood_parameters"]:
            status_indicator = "[ABNORMAL]" if param.get("status", "").lower() == "abnormal" else "[NORMAL]"
            output.append(f"**{param['parameter']}:** {param.get('value', 'N/A')} " +
                         f"(Reference: {param.get('reference_range', 'N/A')}) {status_indicator}")
        output.append("")
    
    # Summary
    if "summary" in data:
        output.append("## Summary")
        for i, point in enumerate(data["summary"], 1):
            output.append(f"{i}. {point}")
        output.append("")
    
    # Disclaimer
    if "disclaimer" in data:
        output.append("## Disclaimer")
        for i, point in enumerate(data["disclaimer"], 1):
            output.append(f"{i}. {point}")
    
    return "\n".join(output)

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# Blood Test Report Analyzer")
    gr.Markdown("""
    Upload a blood test report image to get a simple analysis of the key parameters.
    The system will explain your results in plain language and provide a downloadable PDF report.
    
    **Note:** This tool is for informational purposes only and does not replace professional medical advice.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(type="pil", label="Upload Blood Test Report")
            analyze_btn = gr.Button("Analyze Report", variant="primary")
        
        with gr.Column(scale=2):
            with gr.Tab("Analysis"):
                output_text = gr.Markdown(label="Analysis Results")
            with gr.Tab("Raw JSON"):
                raw_json = gr.JSON(label="Raw Data")
            output_file = gr.File(label="Download PDF Report")
    
    analyze_btn.click(
        fn=process_image,
        inputs=input_image,
        outputs=[output_text, raw_json, output_file]
    )
    
    gr.Markdown("""
    ### How to use:
    1. Upload a clear image of your blood test report
    2. Click "Analyze Report"
    3. Review the analysis and download the PDF for your records
    
    ### Important:
    - Make sure the report is clearly visible in the image
    - This tool works best with standard blood test reports
    - Always consult with a healthcare professional about your test results
    """)

# Launch the app
if __name__ == "__main__":
    # Clean up any existing temp files on startup
    temp_dir = os.path.join(tempfile.gettempdir(), "blood_report_analyzer")
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except:
            pass  # If we can't remove it, that's okay
    
    app.launch(share=False)  # Set share=True if you want to generate a public link