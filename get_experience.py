def get_experience():
    global exp_list
    exp_list = []
    try:
      while True:
          experience = input("Enter your experience(Web developer from 2022 - present ): ")
          exp_list.append(experience)
          sign = input("If you have another experience, enter +, or - to exit: ")
          if sign == "-":
             break
          elif sign != "+":
             print("Invalid input")
             break

    except ValueError:
        print("Please input correct sign")
    return exp_list

