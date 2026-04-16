import sys
SIZE = 0
world = []
agent_pos = [0, 0]
has_gold = False
wumpus_alive = True
bump_flag = False
scream_flag = False

def neighbors(x, y):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            yield nx, ny

def init_kb(size):
    global kb, processed_percepts
    kb = [[{
        'pit': 'unknown',
        'wumpus': 'unknown',
        'pit_count': 0,
        'wumpus_count': 0,
        'safe': False,
        'visited': False
    } for _ in range(size)] for _ in range(size)]
    processed_percepts = {}
    ax, ay = agent_pos
    kb[ax][ay]['safe'] = True
    kb[ax][ay]['pit'] = 'no'
    kb[ax][ay]['wumpus'] = 'no'

def create_world(size):
    global world
    world = [["" for _ in range(size)] for _ in range(size)]
    max_cells = size * size
    reserved = {tuple(agent_pos)}
    while True:
        try:
            max_pits = max_cells - len(reserved) - 2
            if max_pits < 0:
                max_pits = 0
            num_pits = int(input(f"Enter number of pits (0-{max_pits}): "))
            if 0 <= num_pits <= max_pits:
                break
            print("Number out of range")
        except ValueError:
            print("Invalid number")
    taken = set(reserved)
    for i in range(num_pits):
        while True:
            try:
                x, y = map(int, input(f"Enter pit {i+1} position (row col): ").split())
                if not (0 <= x < size and 0 <= y < size):
                    print("Out of bounds")
                    continue
                if (x, y) in taken:
                    print("Cell occupied")
                    continue
                world[x][y] = "P"
                taken.add((x, y))
                break
            except:
                print("Invalid input")
    while True:
        try:
            x, y = map(int, input("Enter Wumpus position (row col): ").split())
            if not (0 <= x < size and 0 <= y < size):
                print("Out of bounds")
                continue
            if (x, y) in taken:
                print("Cell occupied")
                continue
            world[x][y] = "W"
            taken.add((x, y))
            break
        except:
            print("Invalid input")
    while True:
        try:
            x, y = map(int, input("Enter Gold position (row col): ").split())
            if not (0 <= x < size and 0 <= y < size):
                print("Out of bounds")
                continue
            if (x, y) in taken:
                print("Cell occupied")
                continue
            world[x][y] = "G"
            taken.add((x, y))
            break
        except:
            print("Invalid input")

def init_display():
    print("\nWorld (True Layout):")
    for i in range(SIZE):
        for j in range(SIZE):
            if [i, j] == agent_pos:
                print("A", end=" ")
            elif world[i][j] == "W":
                print("W", end=" ")
            elif world[i][j] == "P":
                print("P", end=" ")
            elif world[i][j] == "G":
                print("G", end=" ")
            else:
                print(".", end=" ")
        print()
    print("\nA:Agent W:Wumpus P:Pit G:Gold\n")

def display_kb():
    print("\nKnowledge Base Map:")
    for i in range(SIZE):
        for j in range(SIZE):
            if [i, j] == agent_pos:
                symbol = "A"
            else:
                cell = kb[i][j]
                if cell['safe']:
                    if cell['visited']:
                        symbol = "V"
                    else:
                        symbol = "s"
                elif cell['pit'] == 'confirmed':
                    symbol = "P"
                elif cell['wumpus'] == 'confirmed':
                    symbol = "W"
                elif cell['pit'] == 'possible' and cell['wumpus'] == 'possible':
                    symbol = "pW"
                elif cell['pit'] == 'possible':
                    symbol = "p?"
                elif cell['wumpus'] == 'possible':
                    symbol = "w?"
                else:
                    symbol = "."

            print(f"{symbol:>3}", end="")
        print()
    print("\nLegend: A=Agent V=visited safe s=safe(not visited) P=pit W=wumpus pW=possible both\n")

def try_confirm():
    for i in range(SIZE):
        for j in range(SIZE):
            cell = kb[i][j]
            if cell['pit_count'] >= 2 and cell['pit'] != 'confirmed':
                cell['pit'] = 'confirmed'
            if cell['wumpus_count'] >= 2 and cell['wumpus'] != 'confirmed':
                cell['wumpus'] = 'confirmed'

def update_kb_from_percepts(x, y, breeze, stench):
    if breeze:
        for nx, ny in neighbors(x, y):
            if kb[nx][ny]['pit'] != 'no':
                kb[nx][ny]['pit'] = 'possible'
                kb[nx][ny]['pit_count'] += 1
    else:
        for nx, ny in neighbors(x, y):
            kb[nx][ny]['pit'] = 'no'
    if stench:
        for nx, ny in neighbors(x, y):
            if kb[nx][ny]['wumpus'] != 'no':
                kb[nx][ny]['wumpus'] = 'possible'
                kb[nx][ny]['wumpus_count'] += 1
    else:
        for nx, ny in neighbors(x, y):
            kb[nx][ny]['wumpus'] = 'no'
    kb[x][y]['safe'] = True
    kb[x][y]['visited'] = True
    try_confirm()

def sensor():
    global bump_flag, scream_flag
    x, y = agent_pos
    stench = False
    breeze = False
    if wumpus_alive:
        for nx, ny in neighbors(x, y):
            if world[nx][ny] == "W":
                stench = True
    for nx, ny in neighbors(x, y):
        if world[nx][ny] == "P":
            breeze = True

    glitter = world[x][y] == "G"
    percepts = [
        "Stench" if stench else "none",
        "Breeze" if breeze else "none",
        "Glitter" if glitter else "none",
        "Bump" if bump_flag else "none",
        "Scream" if scream_flag else "none"
    ]
    print("\nPercepts:", percepts)
    update_kb_from_percepts(x, y, breeze, stench)
    display_kb()
    bump_flag = False
    scream_flag = False

def move(dx, dy):
    global agent_pos, bump_flag
    x = agent_pos[0] + dx
    y = agent_pos[1] + dy
    if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
        bump_flag = True
        print("Bump Wall")
        sensor()
        return
    agent_pos = [x, y]
    check()
    sensor()

def check():
    x, y = agent_pos
    if world[x][y] == "P":
        print("Fell in Pit Game Over")
        sys.exit()
    if world[x][y] == "W" and wumpus_alive:
        print("Wumpus killed you Game Over")
        sys.exit()

    if world[x][y] == "G":
        print("Gold Found")

def grab():
    global has_gold
    x, y = agent_pos
    if world[x][y] == "G":
        has_gold = True
        world[x][y] = ""
        print("Gold Grabbed. Game Cleared")
        sys.exit()
    else:
        print("No Gold")
    sensor()

def shoot():
    global wumpus_alive, scream_flag
    print("Arrow fired")
    for nx, ny in neighbors(agent_pos[0], agent_pos[1]):
        if world[nx][ny] == "W":
            print("WUMPUS DEAD")
            world[nx][ny] = ""
            wumpus_alive = False
            scream_flag = True
            break
    sensor()

def main():
    global SIZE, agent_pos
    print("WUMPUS WORLD (Knowledge-Based Agent)")
    SIZE = int(input("Enter grid size: "))
    while True:
        try:
            x, y = map(int, input(f"Enter agent start position (row col) (0-{SIZE-1}): ").split())
            if 0 <= x < SIZE and 0 <= y < SIZE:
                agent_pos = [x, y]
                break
            else:
                print("Out of bounds")
        except:
            print("Invalid input")
    init_kb(SIZE)
    create_world(SIZE)
    init_display()
    sensor()
    while True:
        print("\nControls: W-up S-down A-left D-right G-grab F-shoot E-exit")
        key = input("Move: ").upper()
        if key == "W":
            move(-1, 0)
        elif key == "S":
            move(1, 0)
        elif key == "A":
            move(0, -1)
        elif key == "D":
            move(0, 1)
        elif key == "G":
            grab()
        elif key == "F":
            shoot()
        elif key == "E":
            if has_gold:
                print("YOU WON")
            else:
                print("EXITED")
            break
        else:
            print("Invalid")

if __name__ == "__main__":
    main()
