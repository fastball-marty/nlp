"""
Description:  This program learns an ngram language model
              from an arbitrary number of plain 
              text files and generates new sentences  
              based on the patterns in the ngram model.

Algorithm:    1) Validate user arguments and text file locations
              2) Read and convert text file contents into tokens
              3) Convert tokens into sentences and iterate through 
              sentences to create ngrams of size n.
              4) Store the frequencies of each ngram throughout 
              all text files into a dictionary.
              5) Generate a sentence by:
                a) Randomly select a starting ngram

                b) Create a key of the last n-1 tokens in the current
                sentence. 

                c) Iterate through all ngrams, and store ngrams whose first 
                n-1 tokens match the key and have a high frequency.
                
                d) From the stored ngrams, randomly select an ngram, and 
                append the last token of that ngram to the current sentence.

                e) Repeat steps b through d until a punctuation mark is found.

                f) Normalize the sentence with spacing and capitalization.

                g) Print the generated sentence.
              
              6) Repeat step 5 m times

Usage:        python3 ngram.py integer1 integer2 textfile1 [textfile2 ...]

  Example:      %python3 ngram.py 3 2 pride_and_prejudice.txt [frankenstein.txt ...]
                ---
                Please confirm your entered arguments below:

                Size of ngrams: 3

                Number of sentences to generate: 2

                Corpus of text files: ['pride_and_prejudice.txt', 'frankenstein.txt']

                Please enter 'y' if these arguments are correct. Else, the program will exit.
                y

                Generating sentences...


                This was such a friend.

                So it does now.
                ---
"""

import os
import sys
import re
import random

def validateArgs():
  """
  This function validates the input arguments 
  and outputs appropriate error messages for invalid args. 
  If any argument is invalid, returns 'None.' Else, returns
  the arguments.
  """
  
  # If user entered no arguments, request them
  if len(sys.argv) < 4:
    print("\nThis program generates random sentences using an ngram model and an input of corpus texts. Below is the format for running this program:\n")
    print("python3 ngram.py integer1 integer2 textfile1 [textfile2 ...]\n")
    n = int(input("Please enter an integer for the size of your ngrams: "))
    m = int(input("Please enter an integer for how many sentences you would like to generate: "))
    text_files = input("Please enter the text files you would like to use, separated by a space: ")
    
    text_files = text_files.split()

    for file in text_files:
      # Ensure .txt 
      if not file.endswith('.txt'):
        print(f"Error: '{file}' is not a valid .txt file.\n")
        return None
      # Ensure file location
      if not os.path.isfile(file):
        print(f"Error: '{file}' not found.\n")
        return None
      
    # Verify arguments with user
    print("\n\n\nPlease confirm your entered arguments below:\n")
    print(f"Size of ngrams: {n}\n")
    print(f"Number of sentences to generate: {m}\n")
    print(f"Corpus of text files: {text_files}\n")

    confirm = input("Please enter 'y' if these arguments are correct. Else, the program will exit.\n")

    # Run if user says args are correct
    if (confirm.lower() == 'y'):
      print("\nGenerating sentences...\n\n")
      return n, m, text_files
    # Else cancel execution

    return None
  
  # Extract & validate integer arguments
  try:
    n = int(sys.argv[1])
    m = int(sys.argv[2])
  except ValueError:
    print("This program generates random sentences using an ngram model and an input of corpus texts. Below is the format for running this program:\n")
    print("python3 ngram.py integer1 integer2 textfile1 [textfile2 ...]\n")
    print("The first two arguments must be integers.\n")
    return None
  
  # Extract & validate text file arguments
  text_files = sys.argv[3:]
  for file in text_files:
    # Ensure .txt 
    if not file.endswith('.txt'):
      print(f"Error: '{file}' is not a valid .txt file.\n")
      return None
    # Ensure file location
    if not os.path.isfile(file):
      print(f"Error: '{file}' not found.\n")
      return None
    
  # Verify arguments with user
  print("\nPlease confirm your entered arguments below:\n")
  print(f"Size of ngrams: {n}\n")
  print(f"Number of sentences to generate: {m}\n")
  print(f"Corpus of text files: {text_files}\n")

  confirm = input("Please enter 'y' if these arguments are correct. Else, the program will exit.\n")

  # Run if user says args are correct
  if (confirm.lower() == 'y'):
    print("\nGenerating sentences...\n\n")
    return n, m, text_files
  # Else cancel execution
  else:
    return None


def tokenize(file):
  """
  This function takes a validated file and returns its
  words, numbers, and punctuation marks [. , ? !] as 
  a list.
  """

  tokens = []

  # Read file contents & convert to lowercase
  file_contents = file.read().lower()

  # Only add words, numbers, or these punctuations [.,?!] to tokens list (greedy)
  tokens = re.findall(r'\w+|[.,?!]', file_contents)

  # Return list of tokens
  return tokens


def create_ngrams(tokens, n):
  """
  This function takes a list of tokens 
  and converts them into sentences, then to 
  ngrams of size n. If a sentence is less than 
  size n, that sentence is discarded. Returns two
  lists of strings: all ngrams, and the ngrams 
  that start a sentence.
  """

  # Punctuation marks that end sentences
  punctuation_mark = ['.', '?', '!']

  ngrams = []

  #Initialize cur_sentence <s> tags 
  cur_sentence = ['<s>'] * (n-1)  

  for cur_token in tokens:
    """
    Iterate over list of all tokens, creating sentences. 
    When sentence is punctuated, convert it to ngrams.
    Convert each ngram to a string and add it to list.
    """

    # Punctuation mark reached
    if (cur_token in punctuation_mark):
      
      # and sentence is longer than n 
      if (len(cur_sentence) > n - 1):
        
        # punctuate
        cur_sentence.append(cur_token)

        # Iterate through each token of the sentence to create ngrams
        for i in range((len(cur_sentence)) - n + 1 ):

          # grab n tokens, merge into string
          ngram = cur_sentence[i:i + n ]
          ngram = " ".join(ngram)

          # Add the ngram
          ngrams.append(ngram)

        # Empty cur_sentence for the next
        cur_sentence = ['<s>'] * (n-1)

      
      # If sentence was too short, empty cur_sentence
      else:
        cur_sentence = ['<s>'] * (n-1)

    else:
      # If sentence hasn't ended, add token to cur_sentence
      cur_sentence.append(cur_token)

  # Return list of ngrams
  return ngrams


def build_frequency_dict(ngrams):
  """
  This function takes a list of ngrams and converts them
  into dictionary entries, calculating the frequency of each
  ngram over total dictionary size. Returns the dictionary.
  """

  ngram_dict = {}

  # Itereate over each ngram, adding to dictionary
  for ngram in ngrams:
    if ngram not in ngram_dict:
      ngram_dict[ngram] = 1
    else:
      ngram_dict[ngram] += 1
    
  # Divide each ngram_dict entry by total # of ngrams
  for entry in ngram_dict:
    ngram_dict[entry] /= len(ngrams)

  # Retun dictionary
  return ngram_dict


def generate_sentences(n, m, ngrams):
  """
  This function generates m sentences using ngrams of 
  size n from the ngram dictionary. The function takes a random ngram 
  from start_grams to begin the sentence. Then iteratively, using
  the last n-1 tokens in the ngram, adds another token 
  to the sentence, based on a matching ngram of high frequency. 
  Continues adding tokens until a punctuation mark is found. 
  Prints all of the generated sentences.
  """

  # Punctuation marks to look out for
  end_punctuation = ['.', '?', '!']

  # Generate m sentences
  for _ in range(m):

    # Initialize cur_sentence with a start token
    cur_sentence = ['<s>'] * (n-1)

    # Keep adding tokens to cur_sentence until a punctuation mark is added
    while (cur_sentence[-1] not in end_punctuation):

      # To store the potential next ngram
      max_freq = 0
      potential_matches = []
      
      # Isolate the last n-1 tokens in cur_sentence
      key = " ".join(cur_sentence[-(n-1):])

      # Iterate through all of the ngrams in ngram_dict
      for ngram, freq in ngrams.items():

        # Isolate the first n-1 tokens in the ngram, convert to string
        ngram_words = ngram.split()
        ngram_words = " ".join(ngram_words[:-1])

        # If the current ngram matches the key
        if ngram_words == key:
          # If the freq of that ngram is greater than the previous highest frequency 
          if freq >= max_freq:
            # Set the ngram freq to the new max
            max_freq = freq
      
            # Add the ngram to potential_matches
            if ngram not in potential_matches:
              potential_matches.append(ngram)
      
      if potential_matches:
        """
        Select a random ngram from the list of probable, high
        frequency matches, and append the last word 
        of the selected ngram to the current sentence
        """
        matching_ngram = random.choice(potential_matches)

        matching_ngram = matching_ngram.split()
        cur_sentence.extend(matching_ngram[-1:])
      else:
        # If no potential matches, use a random ngram
        random_ngram = random.choice(list(ngrams.keys()))
        cur_sentence.extend(random_ngram.split()[-1:])

    # Once complete, join cur_sentence list into a string
    cur_sentence = " ".join(cur_sentence)
    
    # Normalize cur_sentence
    cur_sentence = normalize_sentence(cur_sentence)

    print(f"{cur_sentence}\n")

  return


def normalize_sentence(sentence):
  """
  This function normalizes an input string by
  capitalizing the first index, and removing spaces 
  before punctuation marks. Returns the 
  normalized sentence. 
  """

  # Punctuation marks to look out for
  punctuation = [",", ".", "!", "?"]

  # Trim start tags and leading spaces
  sentence = re.sub(r'<s>', "", sentence)
  sentence = sentence.strip()

  # Capitalize first letter of sentence
  sentence = sentence[0].upper() + sentence[1:]

  # To store the normalized sentence
  result = ''

  # Iterate through chars in sentence
  for i in range(0, len(sentence)):
    if sentence[i] == ' ' and sentence[i + 1] in punctuation:
      # If current char is a space and the next is punctuation, do not add to result
      continue

    # Capitalize the word 'I' 
    if sentence[i] == 'i' and sentence[i-1] == " " and sentence[i+1] == " ":
      result += sentence[i].upper()

    # Else, add the char
    else:
      result += sentence[i]

  # Return the normalized sentence
  return result


def main():
  """
  Main function to execute program. Collects arguments,
  converts to tokens, creates ngrams, generates sentences,
  and outputs sentences.
  """
  # Validate arguments
  args = validateArgs()

  # Stop execution if arguments are invalid 
  if args is None:
    print("Exiting the program.")
    return 

  else: 
    # Store arguments
    n, m, text_files = args

    # To store all tokens from the files
    all_tokens = []

    # Open & tokenize each file
    for file in text_files:
      try:
        with open(file, 'r') as file:
          # Send file to tokenize(), convert to tokens
          all_tokens.extend(tokenize(file))

      except FileNotFoundError:
        print(f"Error: '{file}' not found.")

    # Create ngrams from the list of all tokens
    ngrams = create_ngrams(all_tokens, n)

    # Build a dictionary of ngram frequencies
    ngram_dict = build_frequency_dict(ngrams)

    # Generate random sentences using the frequency dict
    generate_sentences(n, m, ngram_dict)

    return 
    

if __name__ == "__main__":
  # Execute program
  main()