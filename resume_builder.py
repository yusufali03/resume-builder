from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import os
import tempfile

# HELPER FUNCTIONS
from date_birth import get_date_of_birth
from get_experience import get_experience
from get_skills import get_skills
from get_education import get_education


def get_image_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='Choose a picture to your Resume', filetypes=[('Image files', '*.png;, *.jpg;, *.jpeg;, *bmp')])
    return file_path


def resize_circle_image(file_path):
    with Image.open(file_path) as img:
        img.thumbnail((400, 400))

        circle_mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(circle_mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)

        # Create a new image with a transparent background
        circular_image = Image.new("RGBA", (400, 400), (255, 255, 255, 0))
        circular_image.paste(img, (0, 0), circle_mask)

        return circular_image


def create_resume_pdf(firstName, lastName,emailAddress,phoneNumber,linkedinProfile,date_of_birth,summary,  education_list, exp_list, skills_list,profileImg):
    pdf = canvas.Canvas(f"resume-{firstName.upper()}.pdf", pagesize=letter)
    width, height = letter

    # Load image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        profileImg.save(temp_file.name)

    # Draw Image (Center it at the top of the page)
    image_width, image_height = 150, 150  # Set the image size
    image_y_position = height - 150 - 20  # Y-position for image
    pdf.drawImage(temp_file.name, (width - image_width) / 2, image_y_position, width=image_width, height=image_height)

    pdf.setTitle(f"{firstName.upper()} {lastName.upper()}'s Resume")
    # Title Section (Below Image)
    pdf.setFont("Helvetica-Bold", 24)
    title_y_position = image_y_position-50  # 30 points below image
    pdf.drawCentredString(width / 2.0, title_y_position, f"{firstName.upper()} {lastName.upper()}")

    # Contact Info (Move this down further so it's below the title)
    # pdf.setFont("Helvetica", 12)
    # line_height = 20  # Spacing between lines
    # contact_y_position = title_y_position - 25  # 25 points below the title for contact info
    # pdf.drawCentredString(width / 2.5, contact_y_position, "Email: ")
    # pdf.setFillColorRGB(0,0,1)
    # pdf.drawCentredString(width / 2.0, contact_y_position, f"{emailAddress}")
    #
    #
    # pdf.setFillColorRGB(0,0,0)
    # pdf.drawCentredString(width / 2.0, contact_y_position - line_height, f"Phone: {phoneNumber}")
    # pdf.drawCentredString(width / 2.7, contact_y_position -2 * line_height, "Linkedin: ")
    #
    #
    # pdf.setFillColorRGB(0,0,1)
    # pdf.drawCentredString(width / 2.0, contact_y_position - 2 * line_height, f"{linkedinProfile}")
    #
    #
    # pdf.setFillColorRGB(0,0,0)
    # pdf.drawCentredString(width / 2.0, contact_y_position - 3 * line_height, date_of_birth)
    # Set the font and sizes for labels and content
    # Set font and line height
    pdf.setFont("Helvetica", 12)
    line_height = 20  # Spacing between lines
    contact_y_position = title_y_position - 40  # Adjust spacing for contact info

    # Helper function to center the label and content, but left-align them
    def draw_left_aligned_label_content(pdf, label, content, y_position):
        label_width = pdf.stringWidth(label, "Helvetica", 12)  # Width of the label
        content_width = pdf.stringWidth(content, "Helvetica", 12)  # Width of the content
        total_width = label_width + content_width  # Total width of label + content
        x_position = (width - total_width) / 2  # Calculate x position to center the total width
        pdf.drawString(x_position, y_position, label)  # Draw the label
        pdf.setFillColorRGB(0, 0, 1)  # Blue color for the content
        pdf.drawString(x_position + label_width, y_position, content)  # Draw the content right after the label
        pdf.setFillColorRGB(0, 0, 0)  # Reset to black

    # Email
    draw_left_aligned_label_content(pdf, "Email: ", emailAddress, contact_y_position)

    # Phone Number
    draw_left_aligned_label_content(pdf, "Phone: ", phoneNumber, contact_y_position - line_height)

    # LinkedIn
    draw_left_aligned_label_content(pdf, "LinkedIn: ", linkedinProfile, contact_y_position - 2 * line_height)

    # Date of Birth
    draw_left_aligned_label_content(pdf, "Date of Birth: ", date_of_birth, contact_y_position - 3 * line_height)

    # Summary Section (Adjust position dynamically)
    summary_y_position = contact_y_position - 3 * line_height - 30  # 40 points below contact info
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, summary_y_position, "Summary")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, summary_y_position - 20, f"{summary}")

    # Education Section (Move down similarly)
    education_y_position = summary_y_position - 50  # 50 points below summary
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, education_y_position, "Education")
    pdf.setFont("Helvetica", 12)
    for education in education_list:
        pdf.drawString(100, education_y_position -20, f"- {education}")
        education_y_position -= 25

    # Experience Section

    # Add experience section to the PDF
    experience_y_position = education_y_position - 60
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, experience_y_position, "Experience:")

    pdf.setFont("Helvetica", 12)
     # 60 points below education

    # Loop through the experiences and display them in bullet points
    for experience in exp_list:
        pdf.drawString(100, experience_y_position-20, f"• {experience}")
        experience_y_position -= 25  # Move down for the next experience


    # Skills Section
    skills_y_position = experience_y_position - 30  # 60 points below experience section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, skills_y_position, "Skills")
    pdf.setFont("Helvetica", 12)


    for skill in skills_list:
        pdf.drawString(100, skills_y_position - 20, f"- {skill}")
        skills_y_position -= 25

    # Save PDF
    pdf.save()


if __name__ == '__main__':
    profile_image_path = get_image_path()
    profile_image = resize_circle_image(profile_image_path)
    while True:
        try:
            first_name = input('Enter your first name: ')
            # first_name = "yusufali"
            last_name = input('Enter your last name: ')
            email_address = input('Enter your gmail address: ')
            phone_number = input('Enter your phone number: ')
            linkedin_profile = input('Enter your linkedin profile link: ')
            date_of_birth = get_date_of_birth()
            summary = input('Enter your summary: ')
            education_list = get_education()
            exp_list = get_experience()
            skills_list = get_skills()
            # last_name = "kromitdinov"
            # phone_number = "+15555555555"
            # email_address = "aaa@gmail.com"
            # linkedin_profile = 'jondoe.linkedin.com'




            # print("Enter your Education")

            print("Your Resume Is Building to PDF Please wait! \n Thank You!")
            break
        except ValueError:
            print("Please enter numbers for (Date of Birth and Phone Number)")
    create_resume_pdf(first_name, last_name,email_address,phone_number,linkedin_profile,date_of_birth,summary, education_list, exp_list, skills_list, profile_image)
