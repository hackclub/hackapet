
"""

data structure wanted:

text form:

20;40;10

20 = food
40 = happiness
10 = food have
2 = special item (e.g stardrop)


"json" form:
{
    "food": 20,
    "happiness": 40,
    "food_have": 10,
    "special": 2
}

"""

def load_save_file():
    try:
        with open("save.txt","r") as file:
            save_data = file.read()

            # turn text data into json data
            save_data = save_data.split(";")
            save_data = {
                "food": int(save_data[0]),
                "happiness": int(save_data[1]),
                "food_have": int(save_data[2]),
                "special": int(save_data[3] or 0) or 0
            }
            return save_data
    except:
        return None


def save_data(data):
    # turn save data into text form for optimisation!
    save_text = f"{data['food']};{data['happiness']};{data['food_have']};{data['special']}"

    with open("save.txt","w") as file:
        file.write(save_text)