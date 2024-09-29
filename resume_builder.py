from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw

def get_image_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='Choose a picture to your Resume', filetypes=[('Image files', '*.png;, *.jpg;, *.jpeg;, *bmp')])
    return file_path

def resize_circle_image(file_path):
    with Image.open(file_path) as img:
        resized_img = img.resize((400, 400))

        circle_mask = Image.new('L', resized_img.size, 0)
        draw = ImageDraw.Draw(circle_mask)
        draw.ellipse((0, 0, 400, 400), fill=255)

        circular_image = Image.new("RGBA", (400, 400), 255)
        circular_image.paste(resized_img, (0, 0), circle_mask)

        return circular_image


def create_resume_pdf(firstName, lastName, dateOfBirth,summary, phoneNumber, emailAddress, fullAdress, university,grad_year, workExperience, skills,profileImg):
    pdf = canvas.Canvas("resume_with_photo.pdf", pagesize=letter)
    width, height = letter

    # Load image
    image = resize_circle_image(profileImg)

    # Draw Image (Center it at the top of the page)
    image_width, image_height = 100, 100  # Set the image size
    pdf.drawImage(image, (width - image_width) / 2, height - 150, width=image_width, height=image_height)

    # Title Section (Below Image)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(width / 2.0, height - 180, f"{firstName.upper(), lastName.upper()}")

    # Contact Info
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2.0, height - 210,
                          f"Email: {emailAddress} | Phone: {phoneNumber} | LinkedIn: linkedin.com")

    # Summary Section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 250, "Summary:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 270, f"{summary}")

    #about
    pdf.setFont("Helvetica", 16)
    pdf.drawString(100, height - 300, f"I was born in {dateOfBirth}")

    # Education Section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 320, "Education:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 340, f"{university}")
    pdf.drawString(100, height - 355, f"{grad_year}")

    # Experience Section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 390, "Experience:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 410, "Python Developer Intern")
    pdf.drawString(100, height - 425, "Tech Solutions | January 2023 - Present")
    pdf.drawString(100, height - 445, "- Worked on automating data pipelines for AI models")
    pdf.drawString(100, height - 460, "- Built web scraping scripts using Python")
    pdf.drawString(100, height - 475, "- Contributed to AI model performance monitoring tools")

    # Skills Section
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 510, "Skills:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 530, "- Python, SQL, MySQL")
    pdf.drawString(100, height - 545, "- HTML, CSS, JavaScript")
    pdf.drawString(100, height - 560, "- Machine Learning (Beginner)")

    # Save PDF
    pdf.save()

if __name__ == '__main__':
    profile_image = get_image_path()
    while True:
        try:
            # first_name = input('Enter your first name: ')
            first_name = "yusufali"
            # last_name = input('Enter your last name: ')
            last_name = ("kromitdinov")
            date_of_birth = "2003-06-06"
            phone_number = "+15555555555"
            email_address = "aaa@gmail.com"
            full_adress = "Uzbekistan, Tashkent, Tashkent city"
            university = "IDU"
            graduation = "2026"
            work_experience = "2"
            skills = ["Python", "SQL", "MySQL"]
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
