from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import os
import tempfile

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


def create_resume_pdf(firstName, lastName, dateOfBirth,summary, phoneNumber, emailAddress, fullAdress, university,grad_year, workExperience, skills,profileImg):
    pdf = canvas.Canvas(f"resume-{firstName.upper()}.pdf", pagesize=letter)
    width, height = letter

    # Load image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        profileImg.save(temp_file.name)

    # Draw Image (Center it at the top of the page)
    image_width, image_height = 150, 150  # Set the image size
    pdf.drawImage(temp_file.name, (width - image_width) / 2, height - 150 - 20, width=image_width, height=image_height)

    pdf.setTitle(f"{firstName.upper()} {lastName.upper()}'s Resume")

    # Title Section (Below Image)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(width / 2.0, height - 180 - 20, f"{firstName.upper()} {lastName.upper()}")  # Moved down by 20

    # Contact Info
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2.0, height - 210 - 20,
                          f"Email: {emailAddress} | Phone: {phoneNumber} | LinkedIn: linkedin.com")  # Moved down by 20

    # Summary Section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 250 - 20, "Summary:")  # Moved down by 20
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 270 - 20, f"{summary}")  # Moved down by 20

    # About Section
    pdf.setFont("Helvetica", 16)
    pdf.drawString(100, height - 300 - 20, f"I was born in {dateOfBirth}")  # Moved down by 20

    # Education Section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 320 - 20, "Education:")  # Moved down by 20
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 340 - 20, f"{university}")  # Moved down by 20
    pdf.drawString(100, height - 355 - 20, f"{grad_year}")  # Moved down by 20

    # Experience Section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 390 - 20, "Experience:")  # Moved down by 20
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 410 - 20, "Python Developer Intern")  # Moved down by 20
    pdf.drawString(100, height - 425 - 20, "Tech Solutions | January 2023 - Present")  # Moved down by 20
    pdf.drawString(100, height - 445 - 20, "- Worked on automating data pipelines for AI models")  # Moved down by 20
    pdf.drawString(100, height - 460 - 20, "- Built web scraping scripts using Python")  # Moved down by 20
    pdf.drawString(100, height - 475 - 20, "- Contributed to AI model performance monitoring tools")  # Moved down by 20

    # Skills Section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 510 - 20, "Skills:")  # Moved down by 20
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 530 - 20, "- Python, SQL, MySQL")  # Moved down by 20
    pdf.drawString(100, height - 545 - 20, "- HTML, CSS, JavaScript")  # Moved down by 20
    pdf.drawString(100, height - 560 - 20, "- Machine Learning (Beginner)")  # Moved down by 20

    # Save PDF
    pdf.save()


if __name__ == '__main__':
    profile_image_path = get_image_path()
    profile_image = resize_circle_image(profile_image_path)
    while True:
        try:
            # first_name = input('Enter your first name: ')
            first_name = "yusufali"
            # last_name = input('Enter your last name: ')
            last_name = "kromitdinov"
            date_of_birth = "2003-06-06"
            phone_number = "+15555555555"
            email_address = "aaa@gmail.com"
            full_adress = "Uzbekistan, Tashkent, Tashkent city"
            university = "IDU"
            graduation = "2026"
            work_experience = "2"
            skills = "Python, SQL, MySQL"
            summary = "I am AI developer"
            # date_of_birth = input('Enter your date of birth(YYYY-MM-DD): ')
            # phone_number = input('Enter your phone number: ')
            # email_adress = input('Enter your gmail address: ')
            # full_adress = input('Enter your adress(Country, State, City): ')
            # print("Enter your Education")
            # university = input("Enter your university: ")
            # graduation = input("Enter your graduation: ")
            # work_experience = input('Enter your work experience: ')
            # skills = input('Enter your skills: ')
            # summary = input('Enter your summary: ')
            print("Your Resume Is Building to PDF Please wait! \n Thank You!")
            break
        except ValueError:
            print("Please enter numbers for (Date of Birth and Phone Number)")
    create_resume_pdf(first_name, last_name, date_of_birth,summary, phone_number,email_address, full_adress, university, graduation, work_experience, skills, profile_image)
