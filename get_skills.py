
def get_skills():
    skills_list =[]
    try:
      while True:
          skills = input("Please enter a list of skills (Frontend: HTML, CSS, JavaScript): ")
          skills_list.append(skills)
          sign = input("Please enter a sign + to add or - to exit : ")
          if sign == "-":
              break
          elif sign != "+":
              print("Please invalid input sign")
              break
    except ValueError:
        print("Please input valid sign")
    return skills_list


