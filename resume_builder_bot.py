import telebot
from telebot import types
from resume_builder import create_resume_pdf, resize_circle_image  # Import your resume creation function

API_TOKEN = '7065357045:AAHR0VPIzQDC_W1P3g1aTgR2aLtEpLCD0HY'
bot = telebot.TeleBot(API_TOKEN)

user_data = {}
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello, Welcome to Resume Builder Bot! Type /help to see all commands!")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "Available commands: \n/start - Welcome message \n/help - Show available commands! \n/build_resume - Start building your resume")

@bot.message_handler(commands=['build_resume'])
def build_resume_command(message):
    user_data[message.chat.id] = {}  # Initialize user data
    bot.reply_to(message, "Let's build your resume! Please enter your Image")
    user_data[message.chat.id]["step"] = "PROFILE_IMAGE"


# Function to generate dynamic prompts for fields
def get_prompt_for_field(field_name):
    field_prompts = {
        "first_name": "Please enter your first name:",
        "last_name": "Please enter your last name:",
        "email": "Please enter your email address:",
        "phone": "Please enter your phone number:",
        "linkedin": "Please enter your LinkedIn profile URL:",
        "dob": "Please enter your date of birth (Month Day, Year):",
        "summary": "Please enter your summary:",
        "education": "Please enter your education details (e.g., MIT University, 2020-2024, AI BC):",
        "experience": "Please enter your experience details (e.g., Company Name, Role, Duration):",
        "skills": "Please enter your skills: (Frontend: HTML, CSS, JavaScript)",
        "languages": "Please enter the languages you know (e.g., English, Spanish, etc.):"
    }
    return field_prompts.get(field_name, "Please provide the information:")


# Function to handle multiple entries like education, experience, etc.
def get_multiple_entries(user_id, field_name, message):
    entries = []  # List to collect entries
    prompt = get_prompt_for_field(field_name)  # Get the prompt for the specific field

    def prompt_user():
        bot.send_message(user_id, f"{prompt} Type '+' to add another or '-' to finish.")

    prompt_user()

    @bot.message_handler(func=lambda msg: msg.chat.id == user_id and user_data[user_id].get("step") == field_name.upper())
    def handle_entry(msg):
        entry = msg.text
        if entry == "-":
            user_data[user_id][field_name] = entries  # Save the entries in user_data
            bot.send_message(user_id, f"{field_name.capitalize()} saved! Moving to the next step.")
            bot.clear_step_handler_by_chat_id(user_id)
            # Call the next step based on the field
            if field_name == "education":
                handle_experience(msg)
            elif field_name == "experience":
                handle_skills(msg)
            elif field_name == "skills":
                handle_languages(msg)
            elif field_name == "languages":
                # Handle the final step or any other logic you need
                # For example, you can call a function to build the resume here
                build_resume(msg)
        elif entry == "+":
            prompt_user()  # Prompt for another entry
        else:
            entries.append(entry)
            bot.send_message(user_id, f"{field_name.capitalize()} added! Type + to add another or - to finish.")


# Function to handle user input for each step
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    user_id = message.chat.id
    step = user_data[user_id].get("step")

    if step == "PROFILE_IMAGE":
        user_data[user_id]["profile_image"] = message.photo[-1].file_id  # Get highest quality image
        user_data[user_id]["step"] = "FIRST_NAME"
        bot.reply_to(message, get_prompt_for_field("first_name"))


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "FIRST_NAME")
def handle_first_name(message):
    user_id = message.chat.id
    user_data[user_id]["first_name"] = message.text
    user_data[user_id]["step"] = "LAST_NAME"
    bot.reply_to(message, get_prompt_for_field("last_name"))


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "LAST_NAME")
def handle_last_name(message):
    user_id = message.chat.id
    user_data[user_id]["last_name"] = message.text
    user_data[user_id]["step"] = "EMAIL"
    bot.reply_to(message, get_prompt_for_field("email"))


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "EMAIL")
def handle_email(message):
    user_id = message.chat.id
    user_data[user_id]["email"] = message.text
    user_data[user_id]["step"] = "PHONE"
    bot.reply_to(message, get_prompt_for_field("phone"))


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "PHONE")
def handle_phone(message):
    user_id = message.chat.id
    user_data[user_id]["phone"] = message.text
    user_data[user_id]["step"] = "LINKEDIN"
    bot.reply_to(message, get_prompt_for_field("linkedin"))


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "LINKEDIN")
def handle_linkedin(message):
    user_id = message.chat.id
    user_data[user_id]["linkedin"] = message.text
    user_data[user_id]["step"] = "DOB"
    bot.reply_to(message, get_prompt_for_field("dob"))



@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "DOB")
def handle_dob(message):
    user_id = message.chat.id
    user_data[user_id]["dob"] = message.text
    user_data[user_id]["step"] = "SUMMARY"
    bot.reply_to(message, get_prompt_for_field("summary"))

@bot.message_handler(func = lambda message: user_data.get(message.chat.id, {}).get("step") == "SUMMARY")
def handle_summary(message):
    user_id = message.chat.id
    user_data[user_id]["summary"] = message.text
    user_data[user_id]["step"] = "EDUCATION"
    bot.reply_to(message, get_prompt_for_field("education"))
    handle_education(message)



def handle_education(message):
    user_id = message.chat.id  # Extract chat ID from the message
    user_data[user_id]["step"] = "EDUCATION"  # Fix: Use `user_id` consistently
    get_multiple_entries(user_id, "education", message)

def handle_experience(message):
    user_id = message.chat.id
    user_data[user_id]["step"] = "EXPERIENCE"
    get_multiple_entries(user_id, "experience", message)

def handle_skills(message):
    user_id = message.chat.id
    user_data[user_id]["step"] = "SKILLS"
    get_multiple_entries(user_id, "skills", message)

def handle_languages(message):
    user_id = message.chat.id
    user_data[user_id]["step"] = "LANGUAGES"
    get_multiple_entries(user_id, "languages", message)



# Resume building and PDF creation
def build_resume(message):
    user_id = message.chat.id
    data = user_data[user_id]

    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    phone = data["phone"]
    linkedin = data["linkedin"]
    dob = data["dob"]
    summary = data["summary"]
    education = data["education"]
    experience = data["experience"]
    skills = data["skills"]
    languages = data["languages"]
    langs_array = [languages]
    profile_image_file_id = data["profile_image"]

    # Download the profile image
    profile_image_path = f"profile_image_{first_name}_{last_name}.jpg"
    profile_image = resize_circle_image(profile_image_path)
    file_info = bot.get_file(profile_image_file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(profile_image_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Generate the PDF using the function from `resume_builder.py`
    create_resume_pdf(
        first_name, last_name, email, phone, linkedin, dob, summary,  # Summary can be empty or added
        education, experience, skills, profile_image, langs_array
    )

    # Send the PDF to the user
    with open(f"resume-{first_name.upper()}.pdf", "rb") as pdf_file:
        bot.send_document(chat_id=user_id, document=pdf_file)

    # Cleanup user data
    del user_data[user_id]


if __name__ == '__main__':
    print("Resume Builder Bot is running...")
    bot.polling(none_stop=True)

