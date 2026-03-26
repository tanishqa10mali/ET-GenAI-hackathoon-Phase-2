import os
import json
from llama_parse import LlamaParse
from openai import OpenAI

def extract_form16_data(pdf_path: str) -> dict:
    """
    The Librarian Agent:
    Reads a Form 16 PDF using LlamaParse, extracts the Gross Salary and HRA using OpenAI,
    and returns a structured dict to be passed to the Accountant Agent.
    """
    # 1. Parse the PDF document
    # Ensure LLAMA_CLOUD_API_KEY is set in your environment
    try:
        print(f"Librarian Agent parsing document at {pdf_path}...")
        parser = LlamaParse(result_type="text")
        documents = parser.load_data(pdf_path)
        
        # Combine all parsed text into a single string
        document_text = "\n".join([doc.text for doc in documents])
        
    except Exception as e:
        print(f"Error parsing PDF with LlamaParse: {e}")
        return {"error": str(e)}

    # 2. Extract numerical data using OpenAI
    # Ensure OPENAI_API_KEY is set in your environment
    try:
        print("Librarian Agent extracting financial figures...")
        client = OpenAI()
        
        prompt = f"""
        Extract the exact numerical values for "Gross Salary" and "HRA" (House Rent Allowance) 
        from the following Form 16 text.
        
        Return ONLY a JSON object exactly matching this format. If a value isn't found, use 0.0:
        {{
            "gross_salary": <float>,
            "hra": <float>
        }}
        
        Text:
        {document_text[:8000]}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise Librarian agent extracting financial data. Output in valid JSON format only."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        # 3. Parse and return the structured data to the Accountant agent
        content = response.choices[0].message.content
        extracted_data = json.loads(content)
        
        print(f"Librarian successfully extracted data: {extracted_data}")
        return extracted_data
        
    except Exception as e:
        print(f"Error extracting data with OpenAI: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Test execution assuming sample_form16.pdf is in the data folder
    test_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "sample_form16.pdf")
    if os.path.exists(test_path):
        result = extract_form16_data(test_path)
        print("\nFinal Librarian output passed to Accountant:", result)
    else:
        print(f"Could not find PDF at {test_path} to test. Please ensure the file exists.")
