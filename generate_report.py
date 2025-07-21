

import os
import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import test_login

def run_tests_and_get_results():
    """
    Runs the integration tests and returns a summary of the results.
    """
    # Redirect stdout to capture the output of the tests
    from io import StringIO
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()

    # Run the main test script
    test_login.main()

    # Restore stdout
    sys.stdout = old_stdout

    # Get the output
    output = captured_output.getvalue()
    
    # Process the output to get results
    results = {
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    for line in output.split('\n'):
        if "[OK]" in line:
            results["passed"] += 1
            results["details"].append(line)
        elif "[ERROR]" in line:
            results["failed"] += 1
            results["details"].append(line)
    
    results["total_tests"] = results["passed"] + results["failed"]
    
    return results, output

def generate_chart(results, filename="test_results.png"):
    """
    Generates a bar chart of the test results.
    """
    labels = ['Passed', 'Failed']
    values = [results['passed'], results['failed']]
    
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['green', 'red'])
    plt.title('Test Results Summary')
    plt.ylabel('Number of Tests')
    plt.savefig(filename)
    plt.close()
    
    return filename

def generate_pdf_report(results, chart_filename, detailed_output, filename="Test_Report.pdf"):
    """
    Generates a PDF report with the test results and chart.
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # --- Insertar logo ---
    try:
        logo_path = "unal.png"
        logo = ImageReader(logo_path)
        logo_width = 100
        logo_height = 100
        logo_x = 40
        logo_y = height - logo_height - 40  # Deja espacio superior
        c.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)
    except Exception as e:
        print(f"[WARNING] No se pudo cargar el logo: {e}")

    # --- Título y fecha alineados a la derecha del logo ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(logo_x + logo_width + 20, height - 50, "Integration Test Report")

    c.setFont("Helvetica", 12)
    c.drawString(logo_x + logo_width + 20, height - 70, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # --- Gráfica ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(logo_x, height - 160, "Test Results Summary")
    c.drawImage(ImageReader(chart_filename), logo_x, height - 370, width=400, height=200)

    # --- Log detallado ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(logo_x, height - 400, "Detailed Log")

    c.setFont("Helvetica", 9)
    text = c.beginText(logo_x, height - 420)
    for line in detailed_output.split('\n'):
        text.textLine(line)
    c.drawText(text)

    c.save()
    print(f"PDF report generated: {filename}")

def main():
    """
    Main function to run tests and generate the report.
    """
    print("Running integration tests...")
    results, detailed_output = run_tests_and_get_results()
    
    print("Generating chart...")
    chart_filename = generate_chart(results)
    
    print("Generating PDF report...")
    generate_pdf_report(results, chart_filename, detailed_output)
    
    # Clean up the chart image
    os.remove(chart_filename)

if __name__ == "__main__":
    main()

