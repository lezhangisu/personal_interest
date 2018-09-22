# This is a problem solver written by Le Zhang, September 2018
# It solves a Water Jug problem
# Problem Definition:
#   We have 3 jugs, each with max volume 10, 5, and 6 litres
#   Initially, we have 5, 0, and 6 litres of water in those jugs
#   How can we get exact 8 litres of water by pouring the water between those jugs?

from itertools import permutations

# Function to calculate the water changes if A pours water in B
def pour_a2b(a, b, a_l, b_l):
  # water in jug B is the min number of A+B or max volume of B
  b_temp = min(a+b, b_l)
  # calculate the water left in A
  a_temp = a+b-b_temp

  return a_temp, b_temp

# Function to determin if the state is goal state
def stop(state):
  # if the first jug has 8 litres of water, goal reached
  if state[0]==8:
    return True
  return False

# Function to get the optimal solution using BFS
def solve_4_mov_seq(moves, max_volume, init_state):

  # initialize current state list
  current = [(list(init_state),[])]
  # set next state list empty
  next = []
  # initialize result move sequence
  res_seq = []
  # initialize goal flag
  goal_flag = False

  # run while current is not empty
  while len(current) != 0:

    # go through each possible state in current list
    for cur in current:

      # get state and move sequence
      state = cur[0]
      mov_seq = cur[1]

      for cur_move in moves:

        # if jug A is empty, skip
        if state[cur_move[0]] == 0:
          continue

        # pour water from jug A to B
        a,b = pour_a2b(state[cur_move[0]], state[cur_move[1]],
                       max_volume[cur_move[0]], max_volume[cur_move[1]])

        # update the current state
        temp_state = list(state)
        temp_state[cur_move[0]] = a
        temp_state[cur_move[1]] = b

        # update the move sequence
        temp_seq = list(mov_seq)
        temp_seq.append(cur_move)

        # check if reached the goal
        if stop(temp_state):
          res_seq = temp_seq
          goal_flag = True
          break

        # if not the goal state, update next list
        next.append((temp_state,temp_seq))

      # if goal state, stop
      if goal_flag:
        break

    # if goal state, stop
    if goal_flag:
      break

    # if not goal yet, update current list with next, empty next list
    current = list(next)
    next = []

  # return the result sequence of moves
  return res_seq

# Function to reproduce the procedure
def reproduce_res(res_seq):
  # set initial state to reproduce
  replay_state = list(init_state)

  num = 0
  print str(num) + ". Initial state: ", replay_state

  # follow each move in the sequence and reproduce the procedure
  for s in res_seq:
    num += 1
    a,b = pour_a2b(replay_state[s[0]], replay_state[s[1]], max_volume[s[0]], max_volume[s[1]])
    replay_state[s[0]] = a
    replay_state[s[1]] = b

    print str(num) + ". move:", s, "; state:", replay_state

## MAIN METHOD
if __name__ == "__main__":
  # initialize all possible moves
  moves = list(permutations([0,1,2], 2))

  # set max volume of jugs
  max_volume = [10, 5, 6]
  # set initial state of jugs
  init_state = [5, 0, 6]

  res_seq = solve_4_mov_seq(moves, max_volume, init_state)
  reproduce_res(res_seq)
