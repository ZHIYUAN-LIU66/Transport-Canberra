"""
COMP1730/6730 assignment template.

Collaborators: <u6511430
                u6543401
                u6753610>
"""

import csv
import random
import numpy as np

def load_stops(path):
    '''
    Load a csv file with bus stop information.
    The argument should be a string, which is the path to the file.
    The return value is a list of stops, as described in the assignment
    specification.
    '''
    with open(path) as bus_stop_file:
        reader = csv.reader(bus_stop_file)
        next(reader) # skip header
        return [ (int(id_), float(lat), float(lon), name)
                 for id_, lat, lon, name in reader]
    
def load_routes(path):
    '''
    Load a csv file with bus route information.
    The argument should be a string, which is the path to the file.
    The return value is a list of routes, as described in the assignment
    specification.
    '''
    with open(path) as routes_file:
        reader = csv.reader(routes_file)
        return [
            (route[0], [int(stop) for stop in route[1:]])
            for route in reader]

def print_journey(journey):
    '''
    Print a bus journey.
    The argument should be a valid journey data structure, as
    described in the assignment specification.
    The function does not return a value.
    '''
    print('Start at {}.'.format(journey[0][1]))
    for stop_number, (route, stop_a, stop_b) in enumerate(journey):
        print('{}. Take {} from {} to {}.'.format(
            stop_number + 1, route, stop_a, stop_b))
    print('Arrived at {}.'.format(journey[-1][2]))


# Question 1
#Q1-1
def southernmost_stop(stops):
    '''
    This function is to get the most southern stop name
    '''
    stops = load_stops("bus_stops.csv")
    min_lat = min([row[1] for row in stops])#to get the lowest latitude
    southernmost = [row for row in stops if row[1]==min_lat]
    return southernmost[0][3]# to get exact the name of stop

#Q1-2
def closest_stop_to_csit(stops):
    '''
    This function returns the name of the stop which is the closest one 
    to CSIT(Building 108) at ANU. 
    The latitude and longitude of CSIT(Building 108) on Google map is
    -35.275323 and 149.120650 respectively. 
    '''
    stops = load_stops('bus_stops.csv')
    # assign an extreamly large value to closest_distance
    closest_distance = 1e100 
    CSIT_lat = -35.275323
    CSIT_lon = 149.120650
    for stop in stops: 
        # the square of the distance between stop and CSIT
        if ((stop[1] - CSIT_lat)**2 + (stop[2] - CSIT_lon)**2) < closest_distance:
            closest_distance = (stop[1] - CSIT_lat)**2 + (stop[2] - CSIT_lon)**2
            closest_bus_stop = stop
    #return the name of the closest_bus_stop
    return closest_bus_stop[3]

#Q1-3
def most_common_number(routes): 
    '''
    This function returns the route number which appears the most amongst route names. 
    If there are more than one route numbers that appears the most amongst route names, 
    it will return all of these route numbers as a list. 
    
    '''
    routes = load_routes('bus_routes.csv')
    # get the route numbers from the route name
    route_numbers = all_route_numbers(routes)
    route_numbers_count = []
    most_common_candidates = []
    for route_number in route_numbers: 
        #count the route_number in route_numbers         
        route_numbers_count.append(route_numbers.count(route_number))
    # k is the index of element in route_numbers_count and route_numbers
    for k in range(0, len(route_numbers_count)):
        if route_numbers_count[k] == max(route_numbers_count):
            # avoid duplicate of route numbers
            if route_numbers[k] not in most_common_candidates:
                # find and append the corresponding route number
                most_common_candidates.append(route_numbers[k])
    return most_common_candidates

def all_route_numbers(routes):
    '''
    This function returns a list of route numbers included in the route names.
    '''
    routes = load_routes('bus_routes.csv')
    route_names = [row[0] for row in routes]
    route_numbers = []
    #route_number is string for plusing the element of route_name which is string
    route_number = ""
    for route_name in route_names:    
        j = 0
        # get all elements of route_name before the blank space
        while route_name[j] != " ":
            route_number = route_number + route_name[j]
            j += 1
        route_number = int(route_number)
        route_numbers.append(route_number)
        route_number = ""
    return route_numbers
                        
# Q1-4
def  most_stops(routes):
    '''
    the function is supposed to find the name of the route which has the most stops 
    '''
    routes = load_routes('bus_routes.csv')
    longest_len = 0 
    the_candidate_route = []
    the_longest_route = []
    for row in routes:
        if len(row[1]) >= longest_len: # compare the amount of stations in every route
            the_longest_route = []
            longest_len = len(row[1]) 
            name = row[0]
            the_candidate_route.append(longest_len)
            the_candidate_route.append(name )
            the_longest_route.append(tuple(the_candidate_route)) #incase there are two or more routes that have the same amount of stops
            the_candidate_route = [] 
    return   the_longest_route

# Question 2 
def find_route(stops, routes, stop_a, stop_b):
    '''
    this function returns a route that the bus can go straightly from stop_a to stop_b
    '''
    stops = load_stops('bus_stops.csv')
    routes = load_routes('bus_routes.csv')
    journey = []
    for route in routes:
        try:
            # if both stop_b and stop_a are in this route, and stop_b is after stop_a
            if route[1].index(stop_a[0]) >= 0 and route[1].index(stop_b[0]) > route[1].index(stop_a[0]):
                journey.append((route[0], find_stop_name(stops, stop_a[0]), find_stop_name(stops, stop_b[0])))                           
                break
        except ValueError:
            journey=journey
    return journey

def find_stop_name(stops, stop_ID):
    '''
    This function returns the name of the stop whose ID is stop_ID. 
    '''
    stops = load_stops("bus_stops.csv")
    for stop in stops:
        if stop[0] == stop_ID:
           return stop[3]  
       
# Question 3  
def random_bus_journey(stops, routes, first_stop, n_repeats):
    '''
    This function returns the journey of Maeve, 
    who wants to get on a random bus at a given bus stop, 
    travel one stop and get off, 
    and repeat this process n times.
    It is assumed that if Maeve arrives at a stop where no bus for getting on, 
    then the journey will be finished in advance, and returns the previous journey. 
    '''
    stops = load_stops('bus_stops.csv')
    routes = load_routes('bus_routes.csv')
    route_stops = [row[1] for row in routes]
    final_route = []#a list of all the routes that Maeve transfers within n times
    first_stop = first_stop[0]
    while n_repeats >0:
        one_stop = []
        one_stop_name = []
        for i in range(0,len(route_stops)):# to get all the routes Maeve transfers
            for j in range(0,len(route_stops[i])-1):
                if route_stops[i][j]==first_stop:
                    one_stop.append([routes[i][0], first_stop, route_stops[i][j+1]])
                    one_stop_name.append((routes[i][0],stops[first_stop][3],stops[route_stops[i][j+1]][3]))                  
        if len(one_stop)!=0: #there are available routes that Maeve can transfer in this stop          
            stop_index = random.randrange(0,len(one_stop)) #randomly find the next stop
            final_route.append(one_stop_name[stop_index])
            first_stop = one_stop[stop_index][2]         
            n_repeats -=1 
        else: #if there is no route that Maeve can transfer to or there is no available stop_a in routes
            print("no more bus for getting on to complete your journey")
            break#return all the routes Maeve has taken previously    
    return final_route

#Question 4
def find_path(stops, routes,stop_a, stop_b) :
    '''
    this function is to get the routes stop by stop between 2 stops involving changing
    buses, it takes a sub-function max_one_change to process the situation of no change 
    or one change. This function will return a journey including route name, and 
    intermidiate stop names. It will return a notice when there is no way to get to 
    destination stop or the given stop_a doesn't exist in the route table.
    It may take more time processing more changes and there will be a notice to be printed
    '''
    stops = load_stops('bus_stops.csv')
    routes = load_routes('bus_routes.csv')
    final_route = []
    only_routes = []
    transfer_station = []
    a_main_stop = []
    b_main_stop = []
    result = max_one_change(stops, routes, stop_a, stop_b)
    if result==[] :#if need to change route for more than once
        print("Processing...")
        table = [row[1] for row in routes]
        for i in range(0,len(table))    :
            only_routes = list(np.concatenate((only_routes, table[i]))) #all the stops showing in all routes  
        for i in range(0, len(only_routes)):
            if only_routes.count(only_routes[i])!=1:# certain stop shows up for more than once and can be a transfer station                
                transfer_station.append((only_routes.count(only_routes[i]),int(only_routes[i])))
        transfer_station = sorted(set(transfer_station),reverse = True)   
        #main transfer station sorted and presented according to frequency of occurrence
        
        for i in range(0, len(transfer_station)):
            if max_one_change(stops,routes, stop_a, transfer_station[i][1])!=[]:
                a_main_stop.append(transfer_station[i][1]) #transfer station stop_a can get to within one change               
            if max_one_change(stops,routes, transfer_station[i][1], stop_b)!=[]:
                b_main_stop.append(transfer_station[i][1])#transfer station can get to stop_b within one change
            
            if a_main_stop!=[] and b_main_stop!=[]: #stop_a can reach stop_b through certain transfer station               
                for j in range(0, len(a_main_stop)):
                    if a_main_stop[j] in b_main_stop:#
                        a_to_mainstop =max_one_change(stops,routes, stop_a, a_main_stop[j])
                        for certain_stop in a_to_mainstop:
                            final_route.append(certain_stop) #route from a to transfer station                           
                        mainstop_to_b=max_one_change(stops,routes, a_main_stop[j],stop_b)
                        for certain_stop in mainstop_to_b:
                            final_route.append(certain_stop)#route from transfer station to b
                        return final_route 
                if final_route==[]:#need to change n stops(>2) 
                    for i in range(0, len(a_main_stop)):
                        for j in range(0, len(b_main_stop)):
                            if find_path(stops,routes, a_main_stop[i],b_main_stop[j])!=[]:
                               a_to_mainstop = max_one_change(stops,routes, stop_a, a_main_stop[i])
                               for certain_stop in a_to_mainstop:    
                                   final_route.append(certain_stop)
                               between_mainstops =find_path(stops,routes, a_main_stop[i],b_main_stop[j])
                               #to get the routes between 2 main transfer stations can each get to stop a and b
                               for certain_stop in between_mainstops:    
                                   final_route.append(certain_stop)
                               mainstop_to_b = max_one_change(stops,routes, b_main_stop[j], stop_b)
                               for certain_stop in mainstop_to_b:
                                   final_route.append(certain_stop)
                               break
                            break
                        break
                print("Processing")
                return final_route
            elif a_main_stop==[]:
                return "there is no stop_a"
    else:
        return result       
     
def max_one_change(stops, routes, stop_a, stop_b):
    '''
    This function is a sub-function of function find_path(), it will process '
    the journey between two stops needing most one change. If the destination 
    stop_b is not included in any route or only acts as a starting stop, it 
    will return a notice, otherwise it will return the journey including route
    name, stop names stop by stop
    '''
    stops = load_stops('bus_stops.csv')
    routes = load_routes('bus_routes.csv')
    abline = []
    a_route_list = []
    b_route_list = []
    length = []
    final_route = []
    route_name = ""
    a_name = ""
    b_name = ""
    if type(stop_a)!= int:
        stop_a = stop_a[0]
    if type(stop_b)!= int:
        stop_b = stop_b[0]
    for i in range(0, len(routes)):#route[i] is the index of a certain line
        for j in range(0, len(routes[i][1])-1):#routes[i][1] is the list of bus stop numbers
            if routes[i][1][j] == stop_a:
                for x in range(j+1,len(routes[i][1])):# to see if stop_b is after stop_a
                    if routes[i][1][x] not in a_route_list:
                        a_route_list.append(routes[i][1][x])#all the stops can reach straightly from stop_a
                    if routes[i][1][x]==stop_b:
                        abline.append((i, routes[i][1][j], routes[i][1][x],j,x));  
    if len(abline)!=0:#stop_a to stop_b without change
        for i in range(0, len(abline)) :
            length.append(abline[i][4]-abline[i][3])
        for i in range(0,len(abline))  :
            if abline[i][4]-abline[i][3]==min(length):#to get the shortest route without change
                route_name = routes[abline[i][0]][0]
                for j in range(abline[i][3], abline[i][4]):
                    a_name = stops[routes[abline[i][0]][1][j]][3]
                    b_name = stops[routes[abline[i][0]][1][j+1]][3]# to have the exact name of two stops
                    final_route.append((route_name, a_name, b_name))
                break#once the final_route is processed
        return final_route
    else: #need to change bus from stop_a to stop_b
        for i in range(0, len(routes)):
            for j in range(1, len(routes[i][1])):
                if routes[i][1][j] == stop_b:
                    for x in range(0,len(routes[i][1][0:j])):
                        if routes[i][1][x] not in b_route_list:
                            b_route_list.append(routes[i][1][x])#all the stops can get to stop_b
        if b_route_list ==[]:#stop_b is only a starting station in all routes or there is no stop_a or b in routes table
            return  "There is no way to get to stop_b"                     
        for i in range(0, len(a_route_list)):
            if a_route_list[i] in b_route_list:#stop_a to stop_b with one change
               first_route = max_one_change(stops, routes, stop_a, a_route_list[i])
               for certain_stop in first_route:
                   final_route.append(certain_stop)#route from stop_a to change stop
               second_route = max_one_change(stops, routes, a_route_list[i], stop_b)
               for certain_stop in second_route:
                   final_route.append(certain_stop)#route from change stop to stop_b
               break
        return final_route
    
# Question 5a
def load_times(path):
    '''
    Load a csv file with bus time information.
    The argument should be a string, which is the path to the file.
    The return value is a list of schedules, each schedule is a tuple, 
    containing route name, stop ID, and a list of times when bus arrives at this stop.
    '''
    with open(path) as times_file:
        reader = csv.reader(times_file)
        next(reader) # skip header
        return [(schedule[0],int(schedule[1]), [str(time) for time in schedule[2:]])
            for schedule in reader]   

# Question 5b
def time_journey(journey, stops, routes, times):
    '''
    this function returns how long in minutes it takes to travel the Maeve's journey;
    it is assumed that Maeve takes the earlist bus at the first stop, then she 
    always catch the first bus right after she arrives at each stop;
    it is assumed that every bus would arrive at the bus stop on time;
    the bus waiting time at each stop is not considered!
    it is assumed that the journey does not present the intermediate stops
    '''
    stops = load_stops('bus_stops.csv')
    routes = load_routes('bus_routes.csv')
    times = load_times('times.csv')
    
    if journey == [] or type(journey) == str:
        return "（There is no bus journey for Maeve to complete）"
    M_journey_time = 0
    n= len(journey) # the number of times that Maeve gets off the bus in the original journey
    i = 0
    while i<n:        
        if i == 0: # the first bus that Maeve gets on
            get_on_route = journey[0][0]     
            get_on_stop = find_stopID(journey[0][1])   
            get_on_time = find_get_on_time_first(get_on_route, get_on_stop)[0] # the time that Maeve gets on the first bus          
            get_on_time_first = get_on_time          
            get_on_time_index = find_get_on_time_first(get_on_route, get_on_stop)[1]           
            get_off_stop = find_get_off_stop(get_on_route, journey)[0]   
            get_off_time = find_get_off_time(get_on_route, find_stopID(get_off_stop), get_on_time_index, get_on_time)   
            journey = update_journey(journey, get_on_route, M_journey_time) # the updated journey excludes the previous routes that Maeve had taken           
            get_on_route = find_get_off_stop(get_on_route, journey)[1] # the next route that Maeve will take  
        else: # from the second bus that Maeve gets on   
            get_on_stop = get_off_stop          
            try:
                get_on_time = find_get_on_time(get_off_time, find_stopID(get_on_stop), get_on_route)[0]  #the time that Maeve gets on the next bus 
                get_on_time_index = find_get_on_time(get_off_time, find_stopID(get_on_stop), get_on_route)[1] #index for finding getoff time of that bus            
            except TypeError:
                return "(YOU cannot get on at ", get_on_stop, " and we cannot calculate journey time for this journey!)"              
            get_off_stop = find_get_off_stop(get_on_route, journey)[0]    
            try:
                get_off_time = find_get_off_time(get_on_route, find_stopID(get_off_stop), get_on_time_index, get_on_time)  
            except TypeError:
                return "(YOU cannot get off at ", get_off_stop, " and we cannot calculate journey time for this journey!)"
            try:
                journey = update_journey(journey, get_on_route, M_journey_time) 
                if journey == []:
                    break
                get_on_route = find_get_off_stop(get_on_route, journey)[1]      
            except TypeError:
                break           
        i+=1
    M_journey_time =M_journey_time + calculate_time(get_on_time_first, get_off_time) # how long in minute that Maeve takes in the journey
    return M_journey_time

def update_journey(journey, get_on_route, M_journey_time):
    '''
    this function returns the new journey excluding the previous route (get_on_route) that Maeve had taken 
    '''
    try:       
        updated_journey = journey[1:]
    except IndexError:        
        return M_journey_time
    return updated_journey    
 
def find_get_off_time(get_on_route, stopID, getonindex, get_on_time):
    '''
    this function returns the time that Maeve will get off the bus (get_on_route)
    at the stop (stopID)
    getonindex is the index of the time that Maeve gets on the bus
    '''
    times = load_times('times.csv')
    for schedule in times:
        if schedule[0] == get_on_route and schedule[1] == stopID:
            try:
                if compare_time(find_time_string(schedule[2][getonindex]), find_time_string(get_on_time)):               
                    return schedule[2][getonindex]           
                else:
                    for time in schedule[2]:
                        if compare_time(find_time_string(time), find_time_string(get_on_time)):
                            return time
            except IndexError:
                return 2 + "a" #in order to return TypeError
    return 2 + "a" #in order to return TypeError

def compare_time(timea, timeb):
    '''
    if timea is larger than or equal timeb, this function will return True. 
    otherwise, it will return False
    '''
    if timea[0] > timeb[0]:
        return True
    elif timea[0] == timeb[0]:
        if timea[1] >= timeb[1]:
            return True
        else:
            return False
    else:
        return False
    
def find_get_on_time(get_off_time, stopID, routename):
    '''
    this function returns the time that Maeve can get on the route (routename)
    after she getting off at the getoff time (get_off_time) at the stop (stopID)
    '''
    times = load_times('times.csv')
    get_off_time = find_time_string(get_off_time)# get_off_time is the list of ints transformed from a time string 
    for schedule in times:
        if schedule[0] == routename and schedule[1] == stopID:
            Mschedule_str = schedule[2]   # Mschedule_str is the row in times file which contains only time of the next rout at next certain stopID    
    Mschedule_list = []    
    for time_str in Mschedule_str:
        time_list = find_time_string(time_str)
        Mschedule_list.append(time_list) # Mschedule_list is the list of list of ints transformed from a list of string 
    for time_int in Mschedule_list:# in order to find the very first geton time that is later than last getoff time
        if time_int[0] == get_off_time[0]: # if time hour == the last getoff time hour
            if time_int[1] >= get_off_time[1]:   # if time minute >= the last getoff time minute             
                time_int_str = str(time_int[0]) + ":" + str(time_int[1])
                return  time_int_str, Mschedule_list.index(time_int)
        elif time_int[0] > get_off_time[0]:# if time hour > the last getoff time hour
            time_int_str = str(time_int[0]) + ":" + str(time_int[1])
            return time_int_str, Mschedule_list.index(time_int)
                                          
def find_get_on_time_first(routename, stopa):
    '''
    this function returns the time that Maeve gets on the first bus (routename) at stopa
    '''
    times = load_times('times.csv')
    time_int_list = []
    for schedule in times: #in order to find the earlest time for the first geton route
        if schedule[0] == routename and schedule[1] == stopa:
            for time in schedule[2]:
                time_int_list.append(find_first_time_string(time))
            mintime = str(min(time_int_list))
            return str(mintime[:-2]) + ":" + str(mintime[-2:]), time_int_list.index(min(time_int_list))
        
def find_get_off_stop(get_on_route, journey):
    '''
    this function returns the stop that Maeve will get off the bus (get_on_route)
    '''
    try: 
                   
        get_off_stop = journey[0][2]  
        get_on_route = journey[0][0]
    except IndexError:
        get_off_stop = journey[len(journey)-1][2]        
    return get_off_stop, get_on_route
        
def find_stopID(stopname):
    ''' 
    this function returns the ID of stopname
    '''
    stops = load_stops('bus_stops.csv')
    for stop in stops:
        if stop[3] == stopname:
            return stop[0]

def calculate_time(M_geton_time, M_getoff_time):
    '''
    this function returns how long from M_geton_time to M_getoff_time
    '''
    minute=0
    timea = find_time_string(M_geton_time)
    timeb = find_time_string(M_getoff_time)
    if timea[0] == timeb[0]:
        minute = timeb[1] - timea[1]
    elif timea[0] < timeb[0]:
        if timea[1] < timeb[1]:
            minute = timeb[1] - timea[1] + (timeb[0] - timea[0]) * 60            
        else:
            minute = 60 - timea[1] + timeb[1] + (timeb[0] - timea[0] - 1) * 60
    return minute
        
def find_time_string(time_string):   
    '''
     this function returns a list of two integers transformed from the time_string 
     '''
    single_time_str = []
    colon_index = time_string.index(':')
    single_time_str.append(int(time_string[:colon_index]))
    single_time_str.append(int(time_string[colon_index+1:]))
    return  single_time_str            
    
def find_first_time_string(time_string):  
    '''
    this function transfers the time from a string to an integer
    ''' 
    return  int(time_string[0:2] + time_string[3:])

if __name__ == '__main__':
    # You can write any testing of your function that you want to
    # run here. The following is just an example, showing how to
    # use the loading function and the print_journey function.
    
    stops = load_stops('bus_stops.csv')
    routes = load_routes('bus_routes.csv')
    times = load_times('times.csv')
    example_journey = [("10 Denman Prospect", "City West Marcus Clarke St", "Cotter Rd After Streeton Dr"),
                       ("10 Denman Prospect", "Cotter Rd After Streeton Dr", "Holborow Av after Greenwood St")]
    print_journey(example_journey)

#     #Question 1
#    print('southernmost_stop:', southernmost_stop(stops))
#    print('closest_stop_to_csit:', closest_stop_to_csit(stops))
#    print('most_routes:', most_common_number(routes))
#    print('most_stops:', most_stops(routes))
#
#     #Question 2
#    print('To get from stop 533 to stop 1070, catch bus',
#           find_route(stops, routes, stops[533], stops[1070]))
#
#     #Question 3
#    maeve_journey = random_bus_journey(stops, routes, stops[533], 5)
#    print('Maeve\'s journey:', maeve_journey)
#
#     #Question 4
#    print('The route between City West and the Old Bus Depot Markets is',
#           find_path(stops, routes, stops[533], stops[851]))
#
#     #Question 5a
#    times = load_times('times.csv')
#
#     #Question 5b
#    print('Maeve\'s journey took',
#           time_journey(maeve_journey, stops, routes, times),
#           'minutes.')

#     Don't forget that your answers to Question 6 (written individual
#     report) must be provided in a separate file (answers.pdf).
