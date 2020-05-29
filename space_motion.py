"""
Simulate the stars/planets/satellites motion in 2D space. Every two objects in the universe are attracted by the gravitational force

$$\vec{F_{ij}} = \frac{G m_i m_j}{r_{ij}^2} \frac{\vec{r_{ij}}}{\|r_{ij}\|}.$$ 

The force that acts on the object $i$ is the vectorial sum of the forces induced by all other (massive) objects

$$\vec{F_i} = \sum_{j \neq i} \vec{F_{ij}}$$

Use SI units, don't be concerned with the speed of the code - do not optimize!!!

Write function that takes any number of space objects (named tuples) as arguments (may not be a list of named tuples for any function!!!) plus the size of the time step and number of time steps. For each object it calculates the force caused by other objects (vector sum of attractive forces). It returns the dictionary with name of the object as a key and tuple of lists of coordinates (one list of x, one of y, every time step one item in list). 

Write a decorator that measures number of calling of each function and their runtime of the functions. The information should be printed to standard output in a form "function_name - number_of_calls - time units\n". The decorator takes optional parameter units which allows to specify time units for printing (default is ms). You can implement the unit measurement only for ns, ms, s, min, h and days.

Below is description of all steps for calculating the update. If you are unsure of precise interface see test script for examples of calling the function.
"""
from functools import wraps
from collections import namedtuple
import math
import time # measuring time

#Define universal gravitation constant
G=6.67408e-11 #N-m2/kg2
SpaceObject = namedtuple('SpaceObject', 'name mass x y vx vy color')
Force = namedtuple('Force', 'fx fy')

def timeForm(time, format):
    if format == 's':
        return time
    elif format == 'ns':
        return time*1000000000
    elif format == 'ms':
        return time*1000
    elif format == 'min':
        return time/60.0
    elif format == 'h':
        return time/3600.0
    elif format == 'day':
        return time/(3600.0*24)

def logging(unit='ms'):
    def real_logger(fn):
        @wraps(fn)
        def wrapper(*args,**kwargs):
            #print(fn.__name__)
            if str(fn.__name__) == 'simulate_motion':
                if not hasattr(fn, "counter_SM"):
                    fn.counter_SN = 0  # it doesn't exist yet, so initialize it
                fn.counter_SN += 1
                time_start = time.time()
                res = fn(*args,**kwargs)
                time_end = time.time()
                final_time = timeForm(time_end - time_start,unit)
                print(fn.__name__, "-", fn.counter_SN,"-", final_time," ",unit)
                return res
            elif str(fn.__name__) == 'update_motion':
                if not hasattr(fn, "counter_UM"):
                    fn.counter_UM = 0  # it doesn't exist yet, so initialize it
                fn.counter_UM += 1
                time_start = time.time()
                res =  fn(*args,**kwargs)
                time_end = time.time()
                final_time = timeForm(time_end - time_start,unit)
                print(fn.__name__, "-", fn.counter_UM,"-", final_time,unit)
                return res
            elif str(fn.__name__) == 'update_space_object':
                if not hasattr(fn, "counter_UPO"):
                    fn.counter_UPO = 0  # it doesn't exist yet, so initialize it
                fn.counter_UPO += 1
                time_start = time.time()
                res = fn(*args,**kwargs)
                time_end = time.time()
                final_time = timeForm(time_end - time_start,unit)
                print(fn.__name__, "-", fn.counter_UPO, "-", final_time,unit)
                return res
            elif str(fn.__name__) == 'calculate_force':
                if not hasattr(fn, "counter_CF"):
                    fn.counter_CF = 0  # it doesn't exist yet, so initialize it
                fn.counter_CF += 1
                time_start = time.time()
                res = fn(*args,**kwargs)
                time_end = time.time()
                final_time = timeForm(time_end - time_start,unit)
                print(fn.__name__, "-", fn.counter_CF, "-", final_time,unit)
                return res
        return wrapper
    return real_logger


@logging(unit='ms')
def calculate_force(space_obj, *args):

    # input: one of the space objects (indexed as i in below formulas), other space objects (indexed as j, may be any number of them)
    # returns named tuple (see above) that represents x and y components of the gravitational force
    # calculate force (vector) for each pair (space_object, other_space_object):
    # |F_ij| = G*m_i*m_j/distance^2
    # F_x = |F_ij| * (other_object.x-space_object.x)/distance
    # analogous for F_y
    # for each coordinate (x, y) it sums force from all other space objects

    for other_obj in args:
        #other_obj = j[0]
        if space_obj.x > other_obj.x:
            X_diff = space_obj.x - other_obj.x
        else:
            X_diff = other_obj.x - space_obj.x
        if space_obj.y > other_obj.y:
            Y_diff = space_obj.y - other_obj.y
        else:
            Y_diff = other_obj.y - space_obj.y
        distance = math.sqrt(X_diff**2 + Y_diff**2)
        F_ij = G * space_obj.mass*other_obj.mass/distance**2
        F_x = F_ij * (other_obj.x - space_obj.x)/distance
        F_y = F_ij * (other_obj.y - space_obj.y)/distance
        force_x =+ F_x
        force_y =+ F_y

    force = Force(fx = force_x, fy = force_y)
    #print(force.fx )
    return force


@logging(unit='s')
def update_space_object(obj, force,timestep):
    # here we update coordinates and speed of the object based on the force that acts on it
    # input: space_object we want to update (evolve in time), force (from all other objects) that acts on it, size of timestep
    # returns: named tuple (see above) that contains updated coordinates and speed for given space_object
    # hint:
    # acceleration_x = force_x/mass
    # same for y
    # speed_change_x = acceleration_x * timestep
    # same for y
    # speed_new_x = speed_old_x + speed_change_x
    # same for y
    # x_final = x_old + speed_new_x * timestep

    acceleration_x = force.fx / obj.mass
    acceleration_y = force.fy / obj.mass
    speed_change_x = acceleration_x * timestep
    speed_change_y = acceleration_y * timestep
    speed_new_x = obj.vx + speed_change_x
    speed_new_y = obj.vy + speed_change_y
    x_final = obj.x + speed_new_x * timestep
    y_final = obj.y + speed_new_y * timestep

    space_object = SpaceObject(name = obj.name, mass = obj.mass, x = x_final, y=y_final, vx = speed_new_x, vy = speed_new_y , color = obj.color)
    return space_object


@logging(unit='ms')
def update_motion(timestep,*args):

    # input: timestep and space objects we want to simulate (as named tuples above)
    # returns: list or tuple with updated objects
    # hint:
    # iterate over space objects, for given space object calculate_force with function above, update
    updated_space_objects = list()
    for i in args:
        new_list = [j for j in args if j is not i]
        force = calculate_force(i, *new_list)
        updated_space_objects.append(update_space_object(i,force,timestep))


    return updated_space_objects  # (named tuple with x and y)


@logging()
def simulate_motion(timestep,no_timestep, *args):
# generator that in every iteration yields dictionary with name of the objects as a key and named tuple SpaceObject as a value
# input size of timestep, number of timesteps (integer), space objects (any number of them)
    list_of_space_objects = args
    for i in range(no_timestep):
        list_of_space_objects = update_motion(timestep,*list_of_space_objects)
        dictionary = dict()
        for j in list_of_space_objects:
            dictionary[j.name] = (j.x, j.y)
        yield dictionary
