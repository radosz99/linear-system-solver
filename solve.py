import equations_solver

if __name__ == "__main__":

    left = [[1,2,3],[7,1,7], [3,3,3]]
    right = [8,5,6]

    p = equations_solver.Solver()
    p.solve(3,left,right)
    part_results = str(p)[:-1].split(':')
    for res in part_results:
        print(res)

    right = [8,3,6]
    p.solve(3,left,right)
    part_results = str(p)[:-1].split(':')
    for res in part_results:
        print(res)


