from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def text_to_pdf(text, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    # Set font and size
    c.setFont("Helvetica", 12)

    # Split text into lines
    lines = text.split("\n")

    # Calculate line height
    line_height = 14

    # Write lines to PDF
    y = height - 50  # Start writing from the top of the page
    for line in lines:
        if line.strip():  # Skip drawing if line is blank
            print("Drawing line:", line)  # Debugging print statement
            c.drawString(50, y, line)
            y -= line_height

            # Check if reached end of page
            if y <= 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 50

    c.save()

# Read text from scraped_data.txt
with open("scraped_data.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Convert text to PDF
text_to_pdf(text, "scraped_data.pdf")
