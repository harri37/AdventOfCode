data = """...s..............................................
...................w......K.......t...............
........s.........................................
.......s......w...............1...................
.........w5.......................................
.......................t.F........................
..................................................
F................................1...........d....
.........................5......................K.
............5.................R..............KZ...
....F.....q.........w..............1.....t........
............8.......I.............................
..........8.................t....................K
...........8.................5.....Z..............
.........q..............................Z...d..U..
...................Y.q...R........................
....................E.....z...............y.......
..........................................U.......
.....F.................................k........S.
............q...................d.................
.................................R................
..x....................................U.........y
.......x.........................E..M...U..d......
......z.......X............................4......
...............I....m....M......R............y....
.......z...................................k..e...
..f..z.......................................e....
...f.I..........7..u..........M................D..
.......X..I.......x.................k.............
.........X.......7....................4.......S...
....................u9...T.....3.Z....o..........6
........f.......D..3....u..................S......
...W...0.........................................D
.....................T................E.......m...
...8....Y............f........T4..................
......Y...........................................
....0.............3...............................
....................3.T.....................k.....
.......................u..............6...........
...........................6..........9........e..
..................4....7.............o..........D.
.................................M...E..o.........
...i.................O...........................Q
.....0.i.....................................m.2..
.......Y.r........7..............S..O..2.......m..
.....r......0.............O.......................
..................................Q...............
........................6................o......Q.
..W...r.................................9.........
.W.........................O........2............."""

PART2 = True

data = data.split("\n")
data = data = [list(line) for line in data]

node_to_coords = {}
for i in range(len(data)):
    for j in range(len(data[0])):
        if data[i][j] != '.':
            if data[i][j] not in node_to_coords:
                node_to_coords[data[i][j]] = [(i, j)]
            else:
                node_to_coords[data[i][j]].append((i, j))

def add_tuple(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def multiply_tuple(c, t):
    return (c * t[0], c * t[1])

def in_bounds(p):
    return p[0] >= 0 and p[0] < len(data) and p[1] >= 0 and p[1] < len(data[0])

antinodes = set()
for node, coords in node_to_coords.items():
    for coord1 in coords:
        for coord2 in coords[coords.index(coord1)+1:]:        
            delta = add_tuple(coord1, multiply_tuple(-1, coord2))
            if not PART2:
                a1, a2 = add_tuple(coord1, delta), add_tuple(coord2, multiply_tuple(-1, delta))
                if in_bounds(a1):
                    antinodes.add(a1)
                if in_bounds(a2):
                    antinodes.add(a2)
            else:
                curr = coord1
                while in_bounds(curr):
                    antinodes.add(curr)
                    curr = add_tuple(curr, delta)
                curr = coord2
                delta = multiply_tuple(-1, delta)
                while in_bounds(curr):
                    antinodes.add(curr)
                    curr = add_tuple(curr, delta)
                    
print(len(antinodes)) 
            
            