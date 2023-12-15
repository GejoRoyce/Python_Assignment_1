
import string

def main():
    filepath = r"E:\\Semester 1\\Programming Languages\\Python\\Assignment 1\\trees.txt"
    output_file = r"E:\\Semester 1\\Programming Languages\\Python\\Assignment 1\\test-output.txt"
    try:
        with open(filepath, 'r') as file:
            data = file.readlines()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return
    name_and_abbreviations = generate_name_and_abbreviations(data)
    display_table(name_and_abbreviations, output_file)
    print("Output written to 'test-output.txt'")


def generate_name_and_abbreviations(data):
    result = []
    generated_abbreviations = set()
    for line in data:
        name = line.strip()
        abbreviation, _ = generate_abbreviation(name)
        if abbreviation and abbreviation not in generated_abbreviations:
            generated_abbreviations.add(abbreviation)
            result.append({'Name': name, 'Abbreviation': abbreviation})
    return result


def generate_abbreviation(name):
    words = name.split()
    if len(words) == 1:
        return generate_single_word_abbreviation(words[0])
    elif len(words) == 2:
        first_part, second_part = words
        first_part_abbr, first_part_score = generate_single_word_abbreviation(first_part)
        second_part_abbr, second_part_score = generate_single_word_abbreviation(second_part)
        return first_part_abbr[0] + second_part_abbr[0] + second_part_abbr[1], first_part_score + second_part_score
    else:    
        parts = [part for word in words for part in word.split('-')]
        abbreviation = ''.join(part[0].upper() for part in parts)[:3] 
        return abbreviation, 0



def generate_single_word_abbreviation(word):
    letters = [char.upper() for char in word if char.isalpha()]
    if not letters or len(letters) < 3:
        return None, 0 
    first_letter = letters[0]
    middle_letters = [letters[i] for i in range(1, len(letters) - 1)]
    middle_letter = min(middle_letters, key=lambda letter: calculate_score(letter, middle_letters.index(letter)))
    last_letter = letters[-1]
    abbreviation = first_letter + middle_letter + last_letter
    abbreviation_score = sum(calculate_score(letter, i, i == 2) for i, letter in enumerate(abbreviation))
    return abbreviation[:3], abbreviation_score


def calculate_score(letter, position, last_word=False):
    if position == 0:  
        return 0 
    elif last_word and letter == 'E': 
        return 20
    elif last_word:
        return 5 
    else:
        common_letters = {'Q': 1, 'Z': 1, 'J': 3, 'X': 3, 'K': 6, 'F': 7, 'H': 7, 'V': 7, 'W': 7, 'Y': 7,
                          'B': 8, 'C': 8, 'M': 8, 'P': 8, 'D': 9, 'G': 9, 'L': 15, 'N': 15, 'R': 15, 'S': 15, 'T': 15,
                          'O': 20, 'U': 20, 'A': 25, 'I': 25, 'E': 35}
        return position + common_letters.get(letter.upper(), 0)


def display_table(data, output_file):
    with open(output_file, 'w') as file:
        file.write("{:<20} {:<15}\n".format('Name', 'Abbreviation'))
        file.write("="*35 + "\n")
        for entry in data:
            file.write("{:<20} {:<15}\n".format(entry['Name'], entry['Abbreviation']))
            print("{:<20} {:<15}".format(entry['Name'], entry['Abbreviation']))


if __name__ == "__main__":
    main()

