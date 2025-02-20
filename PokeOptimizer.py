

'''This code aims to solve the problem of choosing the best possible Pokemon and move when faced with
    a given opponent. As the world of competitive Pokemon battling is very complex, I will approach this
    problem with many restrictions on the mechanics of the game. The first restriction is on the quantity
    of Pokemon involved in this problem. For simplicity's sake, I will only include the first 151 Pokemon
    in the National Pokedex. The second restriction is the omission of status moves and abilities. For
    example, this means that abilities such as Levitate will not grant immunity to ground type moves.
    This is an accurate representation of what battling in generation 1 Pokemon was like. The third
    restriction is that Pokemon can only have a maximum of two moves, and a minimum of one move. This is
    because Pokemon can have a minimum of one typing, and a maximum of two typings. This is in accordance
    with the no status moves restriction, and only same-type attack moves allowed. The last restriction
    is that the opponent is really sleepy, so the opponent will be unable to attack for the entirety of
    the duration (assume that the Pokemon is a CS major, so it is chronically sleepy).

    To start this code off, the user will be prompted to enter seven Pokemon names. The first up to and
    including the sixth name will correspond to six Pokemon in the user's party. The seventh and last
    Pokemon the user is prompted to input will determine the enemy Pokemon.
    This configuration is much like what one would see in a random encounter battle (6 vs 1).
    After the contents of this code are executed, the ideal Pokemon to be sent out, the move that would
    be the ideal move against the given opponent, and the effectiveness of the move will be printed
    '''


'''
The first step is to create an empty list for the list of names of all 151 Pokemon in the Kanto region.
Opens the file containing the names of all 151 Pokemon and using a for loop, strip the "\n" off of each
Pokemon name and append it to the list
 '''
listAllNames = []
with open('PokeNames.txt', 'r') as nameHandle:
    for name in nameHandle:
        name = name.strip()
        listAllNames.append(name)

'''
The second step is to create an empty list for the list of types of all 151 Pokemon in the Kanto region.
Opens the file containing the names of all 151 Pokemon and using a for loop, strip the "\n" off of each 
Pokemon type corresponding to each of the 151 Pokemon and append it to the list.
Using split at each comma, the list will now contain sublists that are the typing(s) of each Pokemon.
Note: for Pokemon with dual typing, there will be two typings within the sublist.
'''
listAllTypes = []
with open('PokeTypes.txt', 'r', encoding ='utf-8-sig') as typeHandle:
    for typing in typeHandle:
        typing = typing.strip()

        listAllTypes.append(typing.split(","))

'''
Create an empty list for the names of the Pokemon in the user's party, and an empty list for the 
type(s) of the Pokemon
'''
listPokeNames = []
listPokeTypes = []

'''
This function will first take the input, which in this case is a name of a Pokemon, and loop through
all the names of the 151 Kanto Pokemon and see if there is a match. If there is in fact a match, 
the name of the Pokemon and the type of the Pokemon will be appended to the appropriate list in the 
global scope. The name of the Pokemon and the type of Pokemon are linked by their index number. 
'''
def pokeInput(instructions):
    # using 'global' for the list of names and types enables change from within the scope of this function
    global listPokeNames
    global listPokeTypes
    # use a while loop that runs if a match is found. If so, else block will execute.
    # if a match is found, nameFound will be set to True, which will end the loop.
    nameFound = False
    while nameFound == False:
        poke = input(instructions)
        # .lower() is used for both the variable 'poke' and the name of the Pokemon in the entire name list
        # this is to ensure that no matter how the user inputs the name, it will stop work
        # i.e. this is to ensure that the input is not case-sensitive
        poke = poke.lower()
        for i in range(len(listAllNames)):
            if poke == listAllNames[i].lower():
                listPokeNames.append(listAllNames[i])
                listPokeTypes.append(listAllTypes[i])
                nameFound = True
        # if a match is not found, the user will continuously be prompted to enter a valid name
        # this is because the while loop has not been exited if a match has not been found
        if nameFound == False:
            print("Please enter a valid Pokemon name")

# the while loop above is repeated 7 times. The first 6 inputs are the user's Pokemon.
# the last input is the enemy Pokemon.
pokeInput("Please enter the name of your first Pokemon: ")
pokeInput("Please enter the name of your second Pokemon: ")
pokeInput("Please enter the name of your third Pokemon: ")
pokeInput("Please enter the name of your fourth Pokemon: ")
pokeInput("Please enter the name of your fifth Pokemon: ")
pokeInput("Please enter the name of your sixth Pokemon: ")
pokeInput("Please enter the name of the enemy Pokemon: ")
# As there is only 1 enemy Pokemon, it is extracted from the list of the user's Pokemon
# The enemy Pokemon is given its own name variable and type variable. This makes it easier to work with.
enemyPokeName = listPokeNames[-1]
enemyPokeType = listPokeTypes[-1]
# the enemy Pokemon name is removed from the user's name list and type list.
listPokeNames.pop(-1)
listPokeTypes.pop(-1)

'''
This 2D array below is critical for this code to work. This is the 2D array representation of a 
Pokemon effectiveness type chart that can easily be found online. The online type chart was manually 
transcribed into a 2D array form. This array is 18 by 18, where the index of each sublist corresponds 
to the attack typing and the indexes within the sublists correspond to the defense typing. 
In competitive battling, the chart can be read column first, and then row, for defensive calculations,
or row first, and then column, for offensive calculations. 
For the purposes of this code, it is only used for offensive calculations. This means that the
row will be the first index, and the column will be the second index. An online type chart can be 
referenced for further clarity. 
'''

effectivenessChart = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 1, 1, 3, 1],
    [1, 3, 3, 1, 2, 2, 1, 1, 1, 1, 1, 2, 3, 1, 3, 1, 2, 1],
    [1, 2, 3, 1, 3, 1, 1, 1, 2, 1, 1, 1, 2, 1, 3, 1, 1, 1],
    [1, 1, 2, 3, 3, 1, 1, 1, 0, 2, 1, 1, 1, 1, 3, 1, 1, 1],
    [1, 3, 2, 1, 3, 1, 1, 3, 2, 3, 1, 3, 2, 1, 3, 1, 3, 1],
    [1, 3, 3, 1, 2, 3, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 3, 1],
    [2, 1, 1, 1, 1, 2, 1, 3, 1, 3, 3, 3, 2, 0, 1, 2, 2, 3],
    [1, 1, 1, 1, 2, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 0, 2],
    [1, 2, 1, 2, 3, 1, 1, 2, 1, 0, 1, 3, 2, 1, 1, 1, 2, 1],
    [1, 1, 1, 3, 2, 1, 2, 1, 1, 1, 1, 2, 3, 1, 1, 1, 3, 1],
    [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1, 1, 1, 0, 3, 1],
    [1, 3, 1, 1, 2, 1, 3, 3, 1, 3, 2, 1, 1, 3, 1, 2, 3, 3],
    [1, 2, 1, 1, 1, 2, 3, 1, 3, 2, 1, 2, 1, 1, 1, 1, 3, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 0],
    [1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 3],
    [1, 3, 3, 3, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2],
    [1, 3, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 2, 2, 3, 1]
]

# this is the effectiveness decipher. This exists for the purpose of making the 2D array more readable.
# If 0.5 was written in the array, the numbers would not line up so nicely to form a square.
# Index 0 of effectiveDecipher corresponds to 0 effectiveness.
# Index 1 of effectiveDecipher corresponds to 1 effectiveness.
# Index 2 of effectiveDecipher corresponds to 2 effectiveness.
# Index 3 of effectiveDecipher corresponds to 0.5 effectiveness.
effectiveDecipher = [0, 1, 2, 0.5]

# this typeToIndex is a dictionary that returns the corresponding index number when the type is inputted
typeToIndex = {'Normal': 0, 'Fire': 1, 'Water': 2, 'Electric': 3, 'Grass': 4, 'Ice': 5, 'Fighting': 6,
               'Poison': 7, 'Ground': 8, 'Flying': 9, 'Psychic': 10, 'Bug': 11, 'Rock': 12, 'Ghost': 13,
               'Dragon': 14, 'Dark': 15, 'Steel': 16, 'Fairy': 17}

# the max effectiveness is set to 0.
# This is the lowest possible effectiveness in Pokemon, making it a safe variable initializer
# The max Pokemon means the best Pokemon. It's set to an empty string.
# The max attack type means the best attack type of the Pokemon against the enemy (eg. for dual types)
# Max attack type is also set to empty string.
maxEffectiveness = 0
maxPokemon = ""
maxAttackType = ""
# for loop to loop through the different types that correspond to the user's Pokemon
# since it's possible for the Pokemon to have more than one type, a nested for loop is used
# this is to check each and every one of the Pokemon's individual types
for i in range(len(listPokeTypes)):
    monTypes = listPokeTypes[i]
    for monType in monTypes:
        # product is set to 1 because for the first loop through, anything multiplied by 1 is anything
        product = 1
        # this other nested for loop is to do the effectiveness calculations
        '''
        for each type within the list of types of the user's Pokemon,
        it will loop through the enemy's types and calculate the effectiveness.
        when the loop finishes running, the overall effectiveness of one of the types of one
        of the user's Pokemon is equal to the product
        '''
        for enemyType in enemyPokeType:
            attackType = typeToIndex[monType]
            defenseType = typeToIndex[enemyType]
            effectiveness = effectiveDecipher[effectivenessChart[attackType][defenseType]]
            product = product * effectiveness

        overallEffectiveness = product
        '''
        if this type is more effective against the enemy Pokemon compared to the current most 
        effective type, then the variable for the Pokemon that would be the most effective will
        be updated to the Pokemon from the user's list using the index, and the corresponding best 
        attack type and the effectiveness value will also be set. If there are more than one
        types that have the same attack effectiveness value, the Pokemon that is closer to being the 
        last Pokemon in the user's list of Pokemon will be selected, and the best move attack type 
        of that Pokemon against the enemy will be updated as usual. 
        '''
        if overallEffectiveness >= maxEffectiveness:
            maxPokemon = listPokeNames[i]
            maxAttackType = monType
            maxEffectiveness = overallEffectiveness
'''
this prints out to the console the name of the best Pokemon, the best move attack type of that Pokemon, 
and the effectiveness of that move against the enemy
'''

print("The best Pokemon to have out is " + maxPokemon + ", and the move type will be " \
      + maxAttackType + " and the effectiveness is",maxEffectiveness)

# the input is set to be wrong so that the while loop runs
# if the output is either Yes or No, the corresponding print statement will be written
# otherwise, the while loop will continue to run because the input will not have been set to correct
# Note that .lower() is used to remove the case sensitivity of the user's input.
inputCorrect = False

while inputCorrect == False:
    satisfaction = input("Were you satisfied with your experience? (enter 'Yes' or 'No'): ").lower()
    if satisfaction == 'yes':
        print("Awesome! I'm glad you enjoyed this service! :)")
        inputCorrect = True
    elif satisfaction == 'no':
        print("I'm sorry that this service did not satisfy you.")
        inputCorrect = True
    else:
        print("Please enter a valid answer!")

'''
This creates and writes to the output file the name of the best Pokemon to be sent out, 
the best move attack type of that Pokemon to use, and the effectiveness of that move against the enemy
'''
with open('Poke_output.txt', 'w') as outputHandle:
    outputHandle.write("Don't worry... Now you'll never make a bad move again." +
          " This code will enable you to send in the ideal Pokemon when faced with an enemy." +
          " The best Pokemon to have out is " + maxPokemon + ", and the move type will be " +
          maxAttackType + " and the effectiveness is " + str(maxEffectiveness))

