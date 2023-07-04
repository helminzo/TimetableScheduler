from z3 import *

def find_optimal_solution(win, draw, loss, stake):
    # Define variables
    x = Real('x')
    y = Real('y')
    z = Real('z')

    # Define expressions
    expr1 = win*x - (x+y+z)
    expr2 = draw*y - (x+y+z)
    expr3 = loss*z - (x+y+z)

    # Define a new variable t to represent the minimum value of the three expressions
    t = Real('t')
    constraints = [
        t <= expr1,
        t <= expr2,
        t <= expr3
    ]

    # Define constraints
    constraints += [
        x + y + z == stake,  # Equality constraint
        x >= 0,          # Non-negativity constraint
        y >= 0,
        z >= 0,
    ]
    # Create Z3 solver and add constraints
    solver = Optimize()
    for constraint in constraints:
        solver.add(constraint)

    # Maximize the minimum value of the expressions by maximizing the variable t
    solver.maximize(t)

    # Check if there is a solution and print the optimal values
    if solver.check() == sat:
        model = solver.model()
        optimal_x = model[x].as_decimal(10)
        optimal_y = model[y].as_decimal(10)
        optimal_z = model[z].as_decimal(10)
        print(f"Optimal solution: w={optimal_x}, d={optimal_y}, l={optimal_z}")
        # Print optimal value of t
        print(f"Optimal value of t: {model[t].as_decimal(10)}")
    else:
        print("No solution found")

find_optimal_solution(2.28,3.52,3.72, 10000)