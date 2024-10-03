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
def get_date_of_birth():
    # get_month = input("Enter your birth month(January): ")
    get_month = 'January'
    # get_day = input("Enter your birth day(1): ")
    get_day = '5'
    # get_year = input("Enter your birth year(2000): ")
    get_year = '2003'
    date_of_birth = f"Birthday {get_month} {get_day}, {get_year}"
    return date_of_birth

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


def create_resume_pdf(firstName, lastName,summary, phoneNumber, emailAddress,linkedinProfile, fullAdress, university,grad_year, workExperience, skills,profileImg):
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
    title_y_position = image_y_position - image_height - 10  # 30 points below image
    pdf.drawCentredString(width / 2.0, title_y_position, f"{firstName.upper()} {lastName.upper()}")

    # Contact Info (Move this down further so it's below the title)
    pdf.setFont("Helvetica", 12)
    line_height = 20  # Spacing between lines
    date_of_birth = get_date_of_birth()
    contact_y_position = title_y_position - 20  # 40 points below the title for contact info
    pdf.drawCentredString(width / 2.0, contact_y_position, f"Email: {emailAddress}")
    pdf.drawCentredString(width / 2.0, contact_y_position - line_height, f"Phone: {phoneNumber}")
    pdf.drawCentredString(width / 2.0, contact_y_position - 2 * line_height, f"LinkedIn: {linkedinProfile}")
    pdf.drawCentredString(width / 2.0, contact_y_position - 3 * line_height, date_of_birth)

    # Summary Section (Adjust position dynamically)
    summary_y_position = contact_y_position - 3 * line_height - 40  # 40 points below contact info
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, summary_y_position, "Summary:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, summary_y_position - 20, f"{summary}")

    # Education Section (Move down similarly)
    education_y_position = summary_y_position - 50  # 50 points below summary
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, education_y_position, "Education:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, education_y_position - 20, f"{university}")
    pdf.drawString(100, education_y_position - 35, f"{grad_year}")

    # Experience Section
    experience_y_position = education_y_position - 60  # 60 points below education
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, experience_y_position, "Experience:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, experience_y_position - 20, "Python Developer Intern")
    pdf.drawString(100, experience_y_position - 35, "Tech Solutions | January 2023 - Present")
    pdf.drawString(100, experience_y_position - 55, "- Worked on automating data pipelines for AI models")
    pdf.drawString(100, experience_y_position - 70, "- Built web scraping scripts using Python")
    pdf.drawString(100, experience_y_position - 85, "- Contributed to AI model performance monitoring tools")

    # Skills Section
    skills_y_position = experience_y_position - 120  # 120 points below experience section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, skills_y_position, "Skills:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, skills_y_position - 20, "- Python, SQL, MySQL")
    pdf.drawString(100, skills_y_position - 35, "- HTML, CSS, JavaScript")
    pdf.drawString(100, skills_y_position - 50, "- Machine Learning (Beginner)")

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
            phone_number = "+15555555555"
            email_address = "aaa@gmail.com"
            linkedin_profile = 'jondoe.linkedin.com'
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
    create_resume_pdf(first_name, last_name,summary, phone_number,email_address,linkedin_profile, full_adress, university, graduation, work_experience, skills, profile_image)
