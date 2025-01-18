import simplegui
import random

#defining functions

#count total number of plastic bags in all rooms
def update_total_bags():
    global total_bags
    total_bags = sum(len(room["bags"]) for room in rooms.values())

#random events
def random_event():
    global encounter_message
    event_chance = random.randint(1, 9) #theres a chance below 50% that one of the random events will occur
    
    if event_chance == 1:
        # a helper gives you more plastic bags
        bags_found = random.randint(1, 3)
        encounter_message = f"A helper gives you {bags_found} plastic bags they found!"
        for _ in range(bags_found):
            new_bag_position = (random.randint(100, 500), random.randint(200, 350))
            rooms[current_room]["bags"].append(new_bag_position)
    
    elif event_chance == 2:
        # monster makes more plastic bags appear
        bags_generated = random.randint(1, 3)
        encounter_message = f"A wild monster appears and drops {bags_generated} plastic bags!"
        for _ in range(bags_generated):
            new_bag_position = (random.randint(100, 500), random.randint(200, 350))
            rooms[current_room]["bags"].append(new_bag_position)
    
    elif event_chance == 3:
        #treasure chest gives you more plastic bags
        bags_found = random.randint(1, 3)
        encounter_message = f"You found a treasure chest! It contains {bags_found} plastic bags!"
        for _ in range(bags_found):
            new_bag_position = (random.randint(100, 500), random.randint(200, 350))
            rooms[current_room]["bags"].append(new_bag_position)
    
    else:
        #nothing
        encounter_message = ""

#beach background
def beachBackground(canvas):
    canvas.draw_polygon([(0, 0), (600, 0), (600, 200), (0, 200)], 1, "SkyBlue", "SkyBlue")
    canvas.draw_polygon([(0, 200), (600, 200), (600, 400), (0, 400)], 1, "SandyBrown", "SandyBrown")
    canvas.draw_circle((500, 100), 50, 2, "Yellow", "Yellow")

#forest background
def forestBackground(canvas):
    canvas.draw_polygon([(0, 0), (600, 0), (600, 200), (0, 200)], 1, "SkyBlue", "SkyBlue")
    canvas.draw_polygon([(0, 200), (600, 200), (600, 400), (0, 400)], 1, "ForestGreen", "ForestGreen")
    for x in range(100, 600, 150):
        canvas.draw_polygon([(x-10, 300), (x+10, 300), (x+10, 400), (x-10, 400)], 1, "SaddleBrown", "SaddleBrown")
        canvas.draw_polygon([(x, 200), (x-40, 300), (x+40, 300)], 1, "DarkGreen", "DarkGreen")
        canvas.draw_polygon([(x, 150), (x-50, 250), (x+50, 250)], 1, "DarkGreen", "DarkGreen")

#park background
def parkBackground(canvas):
    canvas.draw_polygon([(0, 0), (600, 0), (600, 200), (0, 200)], 1, "SkyBlue", "SkyBlue")
    canvas.draw_polygon([(0, 200), (600, 200), (600, 400), (0, 400)], 1, "LimeGreen", "LimeGreen")
    for x in range(100, 600, 150):
        canvas.draw_line((x, 250), (x, 350), 6, "SaddleBrown")
        canvas.draw_line((x+100, 250), (x+100, 350), 6, "SaddleBrown")
    for x in range(100, 600, 150):
        canvas.draw_line((x, 250), (x+100, 250), 6, "DarkSlateGray")
        canvas.draw_line((x, 300), (x+100, 300), 6, "DarkSlateGray")
    canvas.draw_polygon([(200, 230), (250, 230), (250, 220), (200, 220)], 1, "GoldenRod", "GoldenRod")
    canvas.draw_line((225, 220), (225, 180), 3, "Black")
    canvas.draw_line((225, 180), (275, 180), 3, "Black")
    canvas.draw_line((275, 180), (275, 220), 3, "Black")
    canvas.draw_polygon([(400, 220), (500, 220), (500, 240), (400, 240)], 1, "SaddleBrown", "SaddleBrown")
    canvas.draw_line((400, 240), (500, 350), 6, "LightSkyBlue")
    for i in range(5):
        canvas.draw_line((450, 240 + i*20), (460, 240 + i*20), 3, "SaddleBrown")

#draw plastic bag
def draw_plastic_bag(canvas, center, size):
    x, y = center
    body_width = size
    body_height = size * 1.5
    canvas.draw_polygon([(x - body_width // 2, y - body_height // 2),
                         (x + body_width // 2, y - body_height // 2),
                         (x + body_width // 2, y + body_height // 2),
                         (x - body_width // 2, y + body_height // 2)], 1, "LightBlue", "White")

    handle_width = size // 5
    handle_height = size // 2
    canvas.draw_polygon([(x - body_width // 2 - handle_width, y - body_height // 2),
                         (x - body_width // 2, y - body_height // 2),
                         (x - body_width // 2, y - body_height // 2 + handle_height),
                         (x - body_width // 2 - handle_width, y - body_height // 2 + handle_height)], 1, "LightBlue", "White")
    
    canvas.draw_polygon([(x + body_width // 2, y - body_height // 2),
                         (x + body_width // 2 + handle_width, y - body_height // 2),
                         (x + body_width // 2 + handle_width, y - body_height // 2 + handle_height),
                         (x + body_width // 2, y - body_height // 2 + handle_height)], 1, "LightBlue", "White")

#update display for different rooms
def draw(canvas):
    global plastic_bag_count
    
    if current_room == "beach":
        beachBackground(canvas)
    elif current_room == "forest":
        forestBackground(canvas)
    elif current_room == "park":
        parkBackground(canvas)
    
    #putting plastic bags in current room
    for bag in rooms[current_room]["bags"]:
        draw_plastic_bag(canvas, bag, 20)
    
    # Draw the description of the room
    canvas.draw_text(rooms[current_room]["description"], (20, 100), 20, "White")

    #write encounter message
    if encounter_message:
        canvas.draw_text(encounter_message, (20, 300), 20, "Yellow")

    #check player winning
    if plastic_bag_count == total_bags:
        canvas.draw_text("You Win!", (250, 200), 50, "Gold")
        canvas.draw_text("Total Bags Collected: " + str(plastic_bag_count), (200, 250), 30, "White")
        for bag in rooms[current_room]["bags"]:
            rooms[current_room]["bags"].remove(bag)

#mouse click to collect bags
def mouseclick(pos):
    global plastic_bag_count
    x, y = pos
    for bag in rooms[current_room]["bags"]:
        bag_x, bag_y = bag
        if abs(bag_x - x) < 20 and abs(bag_y - y) < 20:
            rooms[current_room]["bags"].remove(bag)
            plastic_bag_count += 1
            random_event()  #random events can occur when a bag is clicked

#moving between rooms
def move(direction):
    global current_room
    if direction in rooms[current_room]["exits"]:
        current_room = rooms[current_room]["exits"][direction]

        
#defining global variables
plastic_bag_count = 0  #counts plastic bags collected
total_bags = 0  #total plastic bags in all rooms
current_room = "beach"  #starting room
encounter_message = ""  #to store random event messages



#room layouts/descriptions
rooms = {
    "beach": {
        "description": "You are on a sandy beach. Pick up the plastic bags to save the earth!",
        "bags": [(random.randint(100, 500), random.randint(200, 350)),
                 (random.randint(100, 500), random.randint(200, 350))],
        "exits": {"north": "forest", "south": "park", "east": "forest", "west": "park"},
    },
    "forest": {
        "description": "You are in a dense forest. Pick up the plastic bags to save the earth!",
        "bags": [(random.randint(100, 500), random.randint(200, 350)),
                 (random.randint(100, 500), random.randint(200, 350)),
                 (random.randint(100, 500), random.randint(200, 350))],
        "exits": {"north": "park", "south": "beach", "east": "park", "west": "beach"},
    },
    "park": {
        "description": "You are taking a stroll in the park. Pick up the plastic bags to save the earth!.",
        "bags": [(random.randint(100, 500), random.randint(200, 350)),
                 (random.randint(100, 500), random.randint(200, 350)),
                 (random.randint(100, 500), random.randint(200, 350))],
        "exits": {"north": "beach", "south": "forest", "east": "beach", "west": "forest"},
    }
}

# Create the frame
frame = simplegui.create_frame("Plastic Bag Collector", 600, 400)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouseclick)

# Add buttons for room navigation
frame.add_button("Go North", lambda: move("north"), 100)
frame.add_button("Go South", lambda: move("south"), 100)
frame.add_button("Go East", lambda: move("east"), 100)
frame.add_button("Go West", lambda: move("west"), 100)

update_total_bags()

frame.start()

