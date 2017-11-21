import random
import sys
from Monster import *
from Player import Player
from Home import House
from Weapon import Weapon

#
# Class that contains the actual game, when compiled the person who compiles it can play the game
# relies on composition to mainly solve problems right now it is a 5x5 grid, but could be easily modified in the future
# to any size board, figured a set size avoids confusion
# @Author: Keith Rodgers & Keith Schmitt
#

#Class that will run the game and get input from the user
class Game:
    #constructor to set up the game! When instantiated, we will play!
    def __init__(self):
        
        #initializing the player
        player = Player()
        
        #variable to hold whether the game is over
        gameOver = False

      	#here we could ask for user input for board dimensions, but a 5x5 grid seemed appropriate
      	#all you would need to do is have 
        
        #populating the neighborhood size right now it is a 5 by 5 grid, but easily modified
        #list comprehension is awesome!
        neighborhood = [[0 for y in range(5)] for x in range(5)]
        
        #variable to keep track of the number of monsters in the entire game
        monster_num = 0
        
        #populating the neighborhood and getting the number of monsters in the game
        for i in range(len(neighborhood)):
            for j in range(len(neighborhood[i])):
                neighborhood[i][j] = House()
                monster_num = monster_num + neighborhood[i][j].monster_count
                
        #random start location stored as a tuple
        location = (random.randint(0,len(neighborhood)-1), random.randint(0,len(neighborhood)-1)) 
        
        
        #printing initial message
        print("----------------------------------------------------\n On the eve of Halloween, you wake up and realize that your entire neighborhood has been took over by Monsters! You must take your candy and save the neighborhood by killing each monster! Best of luck... you'll need it...\n --------------------------------------------------- ")
        print("You have this much HP: " + str(player.hp))
        print ("And right now you are at this location: " + str(location))
        playerName = input("What is your Name?")
        print("Welcome... Play at your own risk...")
        
        #Counting the turns of the game
        turnCounter = -1

        #main game 
        while gameOver != True:
            
            turnCounter = turnCounter +1
            
            #print information for each turn
            print("\n\n\n\n\n")
            print("Turn: " +str(turnCounter))
            print("Name: " + playerName)
            print("HP: " + str(player.hp))
            print ("location: " + str(location))
            print ("Monsters in this house: " + str (neighborhood[location[0]-1][location[1]-1].monster_count))
            print("All Monsters left: "+ str(monster_num))
            

            #checking gameOver Conditions
            if monster_num <=0:
                print("CONGRATULATIONS YOU SURVIVED AND SAVED THE NEIGHBORHOOD... At the expense of your candy go ahead and type Yay!")
                gameOver = True
            if player.hp < 0:
                print("You perished... It's not like we didn't warn you...")
                gameOver = True
            

            #taking in commands
            direction = input("Enter a Direction")
            #list off some help
            if direction == "help":
                print("1. go [north,south,east,west]-- Allows you to traverse the neighborhood houses... at your own risk")
                print("2. look around-- looks around the house you are in and examine the monsters in that house")
                print ("3. look at candy-- allows you to check your inventory")
                print("4. attack-- Allows you to start attacking the monsters in the house you are given, attacking a person heals you, but they are not damaged (think of them as checkpoints), so don't waste your nerd bombs on them")
                print("5. exit-- Let's you exit the game, but do you really want to leave?")
                
            #quitting the game
            elif direction.lower() == "exit":
                print("How could you leave us?")
                print("-----------------GAME OVER--------------------------")
                gameOver = True
                
            #go North    
            elif direction.lower().lstrip() == "go north":
                if location[0] != 0:
                    location= (location[0]-1, location[1])
                else:
                    print("Sorry you can't go North out of this neighborhood")
                    
            #go South        
            elif direction.lower().lstrip() == "go south":
                if location[0] != len(neighborhood):
                    location= (location[0]+1, location[1])
                else:
                    print("Sorry you can't go South out of this neighborhood")
                    
            #go East        
            elif direction.lower().lstrip() == "go east":
                if location[1] != len(neighborhood):
                    location= (location[0], location[1]+1)
                else:
                    print("Sorry you can't go South out of this neighborhood")
                    
            #Go West         
            elif direction.lower().lstrip() == "go west":
                if location[1] != 0:
                    location= (location[0], location[1]-1)
                else:
                    print("Sorry you can't go West out of this neighborhood")
                    
            #allows you to see the monsters in the house        
            elif direction.lower().lstrip() == "look around":
                counter = 0
                print("You see: ")
                for i in neighborhood[location[0]][location[1]].monster_list:
                    counter = counter+1
                    print (str(counter) + "-" +str(i.Name) + "  --HP: "+ str(i.Health))
                    
            #checking inventory        
            elif direction.lower().lstrip() == "look at candy":
                counter = 0
                for i in player.weapons:
                    counter = counter +1
                    print (str(counter) + "-" +str(i.Name) +" --qty: " + str(i.qty))
                    
            #attacking Monsters logic        
            elif direction.lower().lstrip() == "attack":
                counter = 0
                #print out monster_list for conveniece :)
                for i in neighborhood[location[0]][location[1]].monster_list:
                    print (str(counter) +"-"+ str(i.Name) +" --" + str(i.Health))
                    counter = counter +1
                directed_attack = input("Which index would you like to attack")
                

                if directed_attack == exit:
                    pass
                

                #checking valid input for the list player is supposed to enter an index in order to do a lookup
                #One problem here is I could not find a way to check a string being an int without casting it as an int beforehand which is a problem :( 
                elif type(int(directed_attack)) is int and int(directed_attack) < len(neighborhood[location[0]][location[1]].monster_list)  and int(directed_attack) >= 0:
                    counter = 0
                    print("\n\n\n\n\n")
                    for i in player.weapons:
                        print (str(counter) + "-" +str(i.Name) +" --qty: " + str(i.qty))
                        counter = counter +1
                    

                    #wanting to know the index of what item the player wants
                    attackItem = input("Enter an index for which weapon you want to use: ")
                    if type(int(attackItem)) is int and int(attackItem) < len(player.weapons) and int(attackItem) >= 0 and player.weapons[int(attackItem)].qty > 0:

                    	#calling getAttackedBy on the monster that the player wants to attack
                        neighborhood[location[0]][location[1]].monster_list[int(directed_attack)].getAttackedBy(player.useItem(int(attackItem)), player.weapons[int(attackItem)].Name)

                        #The player used a weapon, so we now have 1 less of that item
                        player.weapons[int(attackItem)].qty = player.weapons[int(attackItem)].qty - 1

                        #getting the damage appropriate for the monster
                        damage = neighborhood[location[0]][location[1]].monster_list[int(directed_attack)].Attack()
                        #changing print message depending on whether or not the monster is a person or not
                        if neighborhood[location[0]][location[1]].monster_list[int(directed_attack)].Name == "Person":
                            #in case they want to get healed different message
                            print("The person finds you and gives you some orange juice: You feel better: +"+ str(damage*-1) + " HP")
                        else:
                            #printing message for monster attacks
                            print("The " + neighborhood[location[0]][location[1]].monster_list[int(directed_attack)].Name + " Leaps towards you and attacks you for "+ str(damage) + " damage")
                        #updating player health
                        player.hp = player.hp - damage
                        #checking if monster dies, which then we wnat to notify the house and then that will mean that we have 1 less monster
                        if neighborhood[location[0]][location[1]].monster_list[int(directed_attack)].isDead():
                            neighborhood[location[0]][location[1]].update(int(directed_attack))
                            monster_num = monster_num-1
                    else:
                        print("Please enter a correct number next time")
                else:
                    print("please enter a correct number corresponding to a monster")
                    
            else:
                print("Sorry you look around and realize that you can't do that")


#main method, tried to find a way to make an executable, but that kind of required the use of another language but running at compile we figured would work
def main():
   	g = Game()


if __name__ == "__main__":
   	main()
