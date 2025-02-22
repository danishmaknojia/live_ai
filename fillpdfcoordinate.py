from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

pdf_path = "/Users/danishmak/Documents/Hackathon/claimform.pdf"
output_path = "/Users/danishmak/Documents/Hackathon/filled_claimform.pdf"

# Grid spacing
GRID_SPACING = 20  # Adjust for density

# Data to overlay (adjust coordinates as needed)
form_data = {
    "INSURED’S NAME": ("John Doe", 30, 660),
    "INSURED’S ADDRESS": ("123 Main St", 375, 630),
    # "CITY": ("New York", 100, 660),
    # "STATE": ("NY", 250, 660),
    # "ZIP CODE": ("10001", 300, 660),
    # "INSURED’S POLICY GROUP OR FECA NUMBER": ("A12345678", 100, 640),
    # "PATIENT’S NAME": ("Jane Doe", 100, 620),
    # "PATIENT’S BIRTH DATE": ("01/01/1990", 250, 620),
    # "PHYSICIAN’S NAME": ("Dr. Smith", 100, 600),
}

# Load the original PDF
reader = PdfReader(pdf_path)
writer = PdfWriter()

# Create a new PDF overlay with text and grid
packet = BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
width, height = letter  # Get page size

# Draw grid lines
can.setStrokeColorRGB(0.8, 0.8, 0.8)  # Light gray grid color
can.setLineWidth(0.5)

# Vertical grid lines
for x in range(0, int(width), GRID_SPACING):
    can.line(x, 0, x, height)
    can.drawString(x + 2, 5, str(x))  # Label x-axis

# Horizontal grid lines
for y in range(0, int(height), GRID_SPACING):
    can.line(0, y, width, y)
    can.drawString(2, y + 2, str(y))  # Label y-axis

# Draw text at specified positions
can.setStrokeColorRGB(0, 0, 0)  # Black text color
for field, (value, x, y) in form_data.items():
    can.drawString(x, y, value)

can.save()
packet.seek(0)

# Merge overlay with original PDF
overlay_pdf = PdfReader(packet)
for i, page in enumerate(reader.pages):
    page.merge_page(overlay_pdf.pages[0])  # Overlay only the first page
    writer.add_page(page)

# Save the new filled PDF
with open(output_path, "wb") as output_pdf:
    writer.write(output_pdf)

print(f"Filled form with grid saved to {output_path}")
