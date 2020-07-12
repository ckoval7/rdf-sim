import vincenty

def interpolate_two_points(coord1, coord2, speed, resolution):
    distance_and_heading = vincenty.inverse(coord1, coord2)
    distance = distance_and_heading[0]
    #print(f"Distance: {distance}")
    heading = distance_and_heading[1]
    #print(f"Heading: {heading}")
    nsteps = round(((distance/speed)*(1/resolution))/(1/resolution))/resolution
    #print(f"N Steps: {nsteps}")
    step_distance = speed*resolution
    #print(f"Step Distance: {step_distance}")
    steps = [coord1]
    current_coord = coord1
    steps_left = nsteps
    while steps_left > 0:
        #print(f"In the loop, {steps_left} to go.")
        next_coord = vincenty.direct(current_coord[0], current_coord[1], heading, step_distance)
        #print(f"Plotted: {next_coord}")
        steps.append(tuple(next_coord))
        current_coord = next_coord
        steps_left -= 1
    return steps

def interpolate_all_points(waypoints, speed, resolution):
    points_out = []
    try:
        for x in range(len(waypoints)):
            points_out.extend(interpolate_two_points(waypoints[x],  waypoints[x+1], speed, resolution))
    except IndexError:
        points_out.extend(interpolate_two_points(waypoints[-1],  waypoints[0], speed, resolution))
        return points_out

if __name__ == '__main__':
    coord1 = (39.386474, -76.730882)
    coord2 = (39.13057, -76.51524)
    speed = 26
    resolution = 0.5
    coord_list = interpolate_two_points(coord1, coord2, speed, resolution)
    #print(coord_list)
