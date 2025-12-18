# http://www.andreasaristidou.com/publications/papers/FABRIK.pdf
def fabrik(positions, target):
    tolerance = 1.5
    last = len(positions)-1

    distances = []
    for i in range(len(positions)-1):
        distances.append(positions[i+1].distance_to(positions[i]))
    
    # See if the target is reachable
    if positions[0].distance_to(target) > sum(distances):
        for i in range(last):
            # Distance between each join and target
            r_i = target.distance_to(positions[i])
            delta = distances[i]/r_i
            # Find new join positions
            positions[i+1] = (1-delta)*positions[i] + delta*target
    else:
        # Reachable target
        b = positions[0].copy()
        
        dist = positions[last].distance_to(target)
        while dist > tolerance:
            positions[last] = target
            for i in range(last-1, -1, -1):
                r_i = positions[i+1].distance_to(positions[i])

                delta = distances[i]/max(r_i, 0.001)
                positions[i] = (1-delta)*positions[i+1] + delta*positions[i]

            positions[0] = b
            for i in range(last):
                r_i = positions[i+1].distance_to(positions[i])

                delta = distances[i]/max(r_i, 0.001)
                positions[i+1] = (1-delta)*positions[i] + delta*positions[i+1]
            

            dist = positions[last].distance_to(target)
            break   

