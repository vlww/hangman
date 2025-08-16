print("Welcome to hangman!")

from PyDictionary import PyDictionary
d = PyDictionary()
import random
from os import system, name

print("Loading game...")

#The following lines create the word lists used for determining difficulty (length of words)

# Opens the file in read mode
long_dict_file = open("long_dictionary.txt", "r")
# Reads the file
long_data = long_dict_file.read()
# Creates a list, splitting each word at a line break
long_word_list = long_data.split("\n")
# Close the file
long_dict_file.close()

# Opens the file in read mode
medium_dict_file = open("medium_dictionary.txt", "r")
# Reads the file
medium_data = medium_dict_file.read()
# Creates a list, splitting each word at a line break
medium_word_list = medium_data.split("\n")
# Close the file
medium_dict_file.close()

# Opens the file in read mode
short_dict_file = open("short_dictionary.txt", "r")
# Reads the file
short_data = short_dict_file.read()
# Creates a list, splitting each word at a line break
short_word_list = short_data.split("\n")
# Close the file
short_dict_file.close()

# Clears screen
def clear(): 
    if name == 'nt':
        _ = system('cls')
 
    else:
        _ = system('clear')
      
# Used to check if PyDictionary has a definition for the chosen word
def find_def(word):
  print("Loading word definition...")
  try:
    check = d.meaning(word, disable_errors = True)
  except:
    return False
  else:
    return bool(check)

# Stores the ASCII art of hangman
hangman = (

"""
   ________
    |/   |   
    |              
    |                
    |                 
    |               
    |                   
  __|___                 
    \n""",

"""
   ________
    |/   |      
    |    O         
    |                
    |                 
    |               
    |                   
  __|___                 
    H\n""",

"""
   ________       
    |/   |              
    |    O
    |    |                    
    |                       
    |                         
    |                          
  __|___                       
    HA\n""",

"""
   ________               
    |/   |                   
    |    O                  
    |    |                     
    |    |                    
    |                           
    |                            
  __|___                    
    HAN\n""",


"""
   ________             
    |/   |               
    |    O                   
    |   /|                     
    |    |                    
    |                        
    |                          
  __|___                          
    HANG\n""",


"""
   ________              
    |/   |                     
    |    O                     
    |   /|\                    
    |    |                       
    |                             
    |                            
  __|___                          
    HANGM\n""",



"""
   ________                   
    |/   |                         
    |    O                      
    |   /|\                             
    |    |                          
    |   /                            
    |                                  
  __|___                              
    HANGMA\n""",


"""
   ________
    |/   |     
    |    O    
    |   /|\           
    |    |        
    |   / \        
    |               
  __|___           
    HANGMAN\n""")

display_list=[]
win_count=[]
  
 #Run game: Runs one game of hangman.
def run_game(dif):
  if str(dif).lower()=="short":
    chosen_word = random.choice(short_word_list)
  elif str(dif).lower()=="medium":
    chosen_word = random.choice(medium_word_list)
  elif str(dif).lower()=="long":
    chosen_word = random.choice(long_word_list)
  else:
    chosen_word = random.choice(medium_word_list)
  chosen_def = str(d.meaning(chosen_word))
  display_list.clear()
  for i in range(len(chosen_word)):
    display_list.append("_")

  alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] 
  g=0
  x=0
  
  while True:
    if x==1:
      g=g+1
    x=1
        
    #Checks for loss
    if g == 7:
      clear()
      print(*alphabet, sep=" ")
      print(hangman[7])
      print("The word was " + chosen_word + "!\n")
     
      if find_def(chosen_word) == True:
        chosen_def = chosen_def.replace('{', '').replace('}', '').replace('\'', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '')
        print("Definition: " + chosen_def)
        
      else:
        print("A definition for " + chosen_word + " could not be found in the dictionary. Try looking it up yourself!")
      print("\nYou lose!\n")
      win_count.append(0)
      break
      
   #Checks for win
    joined_display="".join(display_list)
    if joined_display == chosen_word:
      clear()
      print(*alphabet, sep=" ")
      print(hangman[g])
      print("The word was " + chosen_word + "!\n")
      
      if find_def(chosen_word) == True:
        chosen_def = chosen_def.replace('{', '').replace('}', '').replace('\'', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '')
        print("Definition - " + chosen_def)
      
      else:
        print("A definition for " + chosen_word + " could not be found in the dictionary. Try looking it up yourself!")
      print("\nYou win!\n")
      win_count.append(1)
      break

   # Prints interface
    clear()
    print(*alphabet, sep=" ")
    print(hangman[g])
    print(' '.join(display_list) + "\n")
    player_letter = input("What letter would you like to guess?\n")
    while True:
      if len(player_letter)==1:
        if player_letter.isalpha()==True:
          break
      player_letter = input("\nPlease make sure your input is a single letter. \n")
    
      #Changes alphabet list
    for i in range(len(alphabet)-1):
      if alphabet[i].lower() == player_letter.lower():
        alphabet.remove(alphabet[i])
          
      #Changes word display under the Hangman drawing   
      for i in range(len(chosen_word)):
        if player_letter is chosen_word[i]:
          display_list[i] = chosen_word[i]
          x=0

def play():
  win=0
  loss=0
  cur_streak=0
  high_streak=0
  
  while True:
    win=0
    loss=0
    cur_streak=0
    high_streak=0
    for i in range(len(win_count)):
      if win_count[i]==1:
        win=win+1
        cur_streak=cur_streak+1
        if cur_streak>high_streak:
          high_streak=cur_streak
      else:
        loss=loss+1
        cur_streak=0
    if loss==0:
      win_rate=100
    else:
      win_rate = win/(win+loss)
      win_rate = int(round(win_rate * 100, 0))

    print("Wins:",win)
    print("Losses:",loss)
    print("Current Streak:",cur_streak)
    print("Highest Streak:",high_streak)
    print("Win Rate:", str(win_rate) + "%\n")
    
    again = input("Do you want to play again? Yes or no?\n")   
    if again.lower() == "no" or again.lower() == "n" or again.lower() == "no thanks" or again.lower() == "nah":
      print("\nAlright. See you later!")
      break
    else:
      if again.lower() == "yes" or again.lower() == "y":
        print("\nGreat! Let's keep going.")
      else:
        print("\nThat's not a no...")
      difchange = input("\nWhat word length would you like to play? Short, medium, or long?\n").lower()
      while True:
        if difchange == "short" or difchange == "medium" or difchange == "long":
          break
        difchange=input("\nPlease make sure you are spelling out the word length fully and correctly. Short, medium, or long?\n")
      print("\nLoading next word...")
      run_game(difchange)

run_game("medium")
play()

# Sources:
# (txt file of ~100000 most common English words) https://www.daniweb.com/programming/software-development/threads/32007/projects-for-the-beginner#post160495
# (converts txt file into an array) https://www.geeksforgeeks.org/how-to-read-text-file-into-list-in-python/
# (clears board) https://www.geeksforgeeks.org/clear-screen-python/