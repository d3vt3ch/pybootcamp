# Create a character class with attributes for name, health, and strength. Include a method to display the character's information.

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.is_alive = True

    def display_info(self):
        return f"Name: {self.name}, Health: {self.health}, Attack Power: {self.attack_power}"
    
    # method to attack another character
    def attack(self, other_character):  
        """Reduces the health of another character."""
        if self.is_alive:
            print(f"⚔️ {self.name} attacks {other_character.name} for {self.attack_power} damage!")
            other_character.take_damage(self.attack_power)
        else:
            print(f"{self.name} cannot attack because they are defeated.")

    def take_damage(self, damage):
        """Reduces the health of the character and checks if they are still alive."""
        self.health -= damage
        print(f"{self.name} takes {damage} damage! Remaining health: {self.health}")
        if self.health <= 0:
            self.is_alive = False
            print(f"{self.name} has been defeated!")
        else:
            print(f"{self.name} is still alive with {self.health} health remaining.")

    def heal(self, amount):
        """Increases health, but not above the 100 maximum."""
        if self.is_alive:
            self.health += amount
            if self.health > 100:
                self.health = 100
            print(f"{self.name} heals for {amount} points! Current health: {self.health}")
        else:
            print(f"🚫 {self.name} is dead and cannot be healed.")
    
    def status(self):
        """Returns the current status of the character."""
        status = "Alive" if self.is_alive else "Defeated"
        return f"{self.name} - Health: {self.health}, Status: {status}"
    
    # --- Testing the Game Logic ---
# Create two characters
hero = Character("Aragorn", 100, 20)
enemy = Character("Orc", 80, 15)

print("\n--- Battle starts ---\n")
print(hero.status())
print(enemy.status())

print("\n--- 1st Attack Battle ---\n")
# 2. Hero attacks Enemy
hero.attack(enemy)

print("\n--- 2nd Attack Battle ---\n")
# 3. Enemy attacks back
enemy.attack(hero)

print("\n--- Heal  Battle ---\n")
# 4. Hero heals
hero.heal(10) 

print("\n--- Enemy attacks again ---\n")
# 5. Enemy attacks again
enemy.attack(hero)

print("\n--- Battle status ---\n")
# 6. Display final status
print(hero.status())
print(enemy.status())

print("\n--- Final Battle ---\n")
# 5. Hero lands a finishing blow
hero.attack(enemy)

print("\n--- near end Battle ---\n")
hero.attack(enemy)
print("\n--- Last Battle ---\n")

hero.attack(enemy)
print("\n--- Battle status ---\n")
print(hero.status())
print(enemy.status())