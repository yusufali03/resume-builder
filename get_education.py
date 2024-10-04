def get_education():
    education_list = []
    try:
        while True:
            education = input("Enter education (MIT university, 2020-2024, Artificial Intelligence BC): ")
            education_list.append(education)
            sign = input("Enter sign + to add or - to exit: ")
            if sign == "-":
                break
            elif sign != "+":
                print("Invalid input")
                break
    except EOFError as e:
        print(e)
    return education_list
