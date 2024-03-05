from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def insert_images_into_pdf(selected_parent_name, start_date, end_date, streamgraph_path, distritos_path, barras_path, output_filename):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter  # Default letter size

    # Title
    title = f"Resumen Ejecutivo -- {selected_parent_name}"
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2.0, height - 40, title)

    # Subtitle with dates
    subtitle = f"{start_date} to {end_date}"
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2.0, height - 60, subtitle)

    # Calculate positions for the images
    # The two images in the same row will be half of the desired width minus a small margin
    desired_width = (width - 60) / 2  # Subtract a margin and divide by 2 for two images
    desired_height = 150

    # Image positions in the same row
    img1, img1_width, img1_height = get_image_size(streamgraph_path, desired_width, desired_height)
    img2, img2_width, img2_height = get_image_size(distritos_path, desired_width, desired_height)

    # Draw the first two images in the same row
    c.drawImage(img1, 30, height - 280, width=img1_width, height=img1_height)
    c.drawImage(img2, width/2 + 15, height - 280, width=img2_width, height=img2_height)

    # Draw the third image below
    img3, img3_width, img3_height = get_image_size(barras_path, width - 60, desired_height)
    c.drawImage(img3, 30, height - 280 - img1_height - 20, width=img3_width, height=img3_height)

    # Save the PDF file
    c.save()

def get_image_size(image_path, desired_width, desired_height):
    """Calculate image size maintaining aspect ratio."""
    img = ImageReader(image_path)
    img_width, img_height = img.getSize()
    aspect_ratio = img_width / float(img_height)
    height = desired_width / aspect_ratio

    # Adjust if the height is too high
    if height > desired_height:
        height = desired_height
        width = desired_height * aspect_ratio
    else:
        width = desired_width

    return img, width, height

    