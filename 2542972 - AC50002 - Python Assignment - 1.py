# Importing the essential libraries
import string
import os


# Main Module : Focuses on user interaction, file handling and overall flow of script
def main():
    
    #Accepting User Inputs
    surname = input("Enter your surname: ")
    input_filename = input("Enter the name of the input file (<input>.txt): ")
    
    #Accessing Input File from the user specification
    input_filepath = os.path.join(os.path.dirname(__file__), input_filename)
    
    #Naming output filename based on user input
    output_file = f"{surname.lower()}_{os.path.splitext(input_filename)[0]}_abbrevs.txt"

    #Open and read the file and copy the data to dataframe - data
    try:
        with open(input_filepath, 'r') as file:
            data = file.readlines()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return
    
    #Process the data read from the input file and generate the list of name-abbreviation pair
    name_and_abbreviations = generate_name_and_abbreviations(data)

    #Display the Table and generate output data file 
    display_table(name_and_abbreviations, output_file)
    print(f"Output written to '{output_file}'")    


# Name and Abbreviation Generation Module : Processing names from the dataframe and generate unique abbreviations for each name
def generate_name_and_abbreviations(data):

    #Initialising an empty set for results and generated_abbreviations
    result = []
    generated_abbreviations = set()

    #Processing Each line, names in the input file and removing unwanted characters
    #Generating abbreviation for each cleaned names
    #Checking Uniqueness of abbreviation generated from generate_abbreviations module
    #Adding the data to the abbreviation dataset
    #Appending the data to the Result dataframe with the Name and Abbreviation
    for line in data:
        name = line.strip()
        abbreviation, _ = generate_abbreviation(name)
        if abbreviation and abbreviation not in generated_abbreviations:
            generated_abbreviations.add(abbreviation)
            result.append({'Name': name, 'Abbreviation': abbreviation})
    return result

# Abbreviation Generation Module : Splitting the names into individual words and proceess them based on the count of words
def generate_abbreviation(name):

    # Split the name into individual words
    words = name.split()

    # Check the count of words is equal to the count of 1. Then return to the "generate_single_word_abbreviation" module
    # Check the count of words is equal to the count of 2. Generate abbreviation from each word and combines them 
    # Check the count of words is equal to the count of 3. Consider the first part of each word for abbreviation
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

# Abbreviation Generation for Single Word Module 
def generate_single_word_abbreviation(word):

    # Filtering and Uppercasing the non-alphabetic characters in the words
    letters = [char.upper() for char in word if char.isalpha()]

    # Generate the abbreviation till the letter count reach 3
    # Retrive first letter of the word
    # Extract the middle letters other than the first and last letters
    # Finding the low scored middle letter in the word
    # Extract the last letter of the word
    # Generate the abbreviation by combining first, middle and last letters together
    # Calculate the abbreviation scores from the calculate_score module
    # Return to tuple containing the 3 character abbreviation scores
    if not letters or len(letters) < 3:
        return None, 0
    first_letter = letters[0]  
    middle_letters = [letters[i] for i in range(1, len(letters) - 1)]
    middle_letter = min(middle_letters, key=lambda letter: calculate_score(letter, middle_letters.index(letter)))
    last_letter = letters[-1]
    abbreviation = first_letter + middle_letter + last_letter
    abbreviation_score = sum(calculate_score(letter, i, i == 2) for i, letter in enumerate(abbreviation))
    return abbreviation[:3], abbreviation_score

# Score Calculation : based on the rules and methods provided in the task.
def calculate_score(letter, position, last_word=False):

    # If the letter is first in the word return the score 1
    # Else if the letter is last in the word and letter is E return the score 20
    # Else If the letter is last in the word return the score 5
    # Else return the score based on the rule and position
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


# Display Output and its Formatting :
def display_table(data, output_file):

    # Open the specific file to write the output.
    # Write the table header with fixed width alignment, make lines to make the table format
    # For each entry in the data, write the name and abbreviations entrirs to the output file with formatting
    with open(output_file, 'w') as file:
        file.write("{:<20} {:<15}\n".format('Name', 'Abbreviation'))
        file.write("="*35 + "\n")
        for entry in data:
            file.write("{:<20} {:<15}\n".format(entry['Name'], entry['Abbreviation']))
            print("{:<20} {:<15}".format(entry['Name'], entry['Abbreviation']))

if __name__ == "__main__":
    main()
    
