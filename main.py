import argparse


def get_color(color_string: str):
    temp_dict = {'RESET': '\033[0m',
                 "BLACK": '\033[30m',
                 "RED": '\033[31m',
                 "GREEN": '\033[32m',
                 "YELLOW": '\033[33m',
                 "BLUE": '\033[34m',
                 "MAGENTA": '\033[35m',
                 "CYAN": '\033[36m',
                 "WHITE": '\033[37m',
                 '': ''
                 }
    return temp_dict[color_string.upper()]


def main():
    parser = argparse.ArgumentParser(
        description='Process text and outputting the string in a graphic representation using ASCII')
    parser.add_argument('--color', type=str, default='', help='Set a color to paint your letters')
    parser.add_argument('letters', type=str, nargs='?', default='', help='Which letters would you like to color?')
    parser.add_argument('--output', type=str, default='output.txt', help='Name of the output file to store the output')
    parser.add_argument('text', type=str, help='Enter the text that will be represented graphically by ASCII')
    parser.add_argument('mode', type=str, default="standard", nargs='?', help='Which mode would you like to use? '
                                                                              'Additional modes: Shadow, Thinkertoy')
    args = parser.parse_args()
    if args.color == "" and args.letters != "":  # if no color was provided
        args.mode = args.text
        args.text = args.letters
        args.letters = ""
    result = process_text(args.color, args.letters, args.output, args.text, args.mode)
    if args.text != "":
        print(result)

def make_a_dictionary(file_name):
    try:
        with open(f'{file_name}.txt', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        with open('standard.txt', 'r') as file:
            lines = file.readlines()
    char_size = 8  # Size of each character
    char_counter = 0
    myDict = {}  # dictionary,key - letter, value - big Letter
    for i in range(1, len(lines) - char_size, char_size + 1):
        key = chr(32 + char_counter)
        char_counter += 1
        value = ''.join(lines[i: i + char_size])
        myDict[key] = value
    return myDict


def array_from_string(text: str) -> []:  # transforming user_input from string to array
    result = []
    for line in text.split('\\n'):
        words = line.split() or ['']
        char_list = []
        for word in words:
            char_list.extend(list(word))
        result.append(char_list)
    # result = [[char for char in word] for line in text.split('\\n') for word in line.split() or ['']]
    if result and result[0] == []:
        result.pop(0)
    # print(result)
    return result


def process_text(colorName, letters, output_file, user_input, mode):
    colorCode = get_color(colorName)
    myDict = make_a_dictionary(mode)
    result = ""  # output text
    array = array_from_string(user_input)
    for i in range(len(array)):
        if not array[i] and i != len(array) - 1:
            result += "\n"
            continue
        for line_number in range(8):
            counter = 0
            for char in array[i]:
                counter += 1
                if char in letters or (letters == "" and colorName != ''):  # colored output
                    temp = myDict.get(char).split('\n')[line_number]  # it creates an array of Dictionary value, and
                    # [lineNumber] indicates its index
                    result += f'{colorCode}{temp}{get_color("RESET")}'
                else:  # without color
                    result += myDict.get(char).split('\n')[line_number]
            if counter > 0 and line_number != 7:
                result += "\n"
            elif counter > 0:
                if i != len(array) - 1:
                    result += "\n"
    with open(output_file, 'w') as file:
        file.write(result)
    return result


if __name__ == "__main__":
    main()