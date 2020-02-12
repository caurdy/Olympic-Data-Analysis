############################################################################
#
#   Project 8 - Conspiracy Theory: You guys are obsessed with dictionaries
#               
#   Algorithm             
#   
#   Make Functions
#   Make dictionaries with functions
#   Print a cool table about people who are good at things
#   Input Loop:
#       Ask user to input a sport ('q' or 'Q' to quit)
#       Print a cool table about that sport
#       Ask User if he wants a cool plot about data
#       Plot cool plot if he entered 'y' or 'Y'
#   
#
###########################################################################





from operator import itemgetter # optional, if you use itemgetter when sorting
import matplotlib.pyplot as plt
import csv

def open_file(): 
    '''
    Opens an existing text file
    No parameters
    Prompts for file name
    If file exists
        Opens
    If file doesn't exist
        Error Message
        Reprompt
    Return: Text file (obj)
    '''
    
    file_obj = []
    while True:
        file_str = input('Input a file name: ')
        
        try:
            file_obj = open(file_str,'r') 
            break
        
        except FileNotFoundError:
            print('File not found.')
            continue
        
    return file_obj

def get_athlete_stats(fp): 
    '''
    Return a dictionary in the form {Name:[(Info tuple),..]}
    Info tuple in the form (gender, age, height, weight, country_code)
    Input:
        fp: file pointer of a excel file
    
    Read through file pointer
        Try:
            Declare variables for each line
            Create tuple using variables
            Insert new key:value pair to new dictionary
            Or 
            Add tuple to existing matching key
        Except:
            If values are null
            continue
        
    Return: Athlete Dictionary
    '''
    Ath_dict = {}
    reader = csv.reader(fp) # the name “reader” on the left can be any name
    next(reader,None) # skips one header line, repeat if more header lines
    
    for line_list in reader:
        
        try:
            name = line_list[1]
            gender = line_list[2]
            age = int(line_list[3])
            height = int(line_list[4])
            weight = int(line_list[5])
            country_code = line_list[7]
            ath_tup = (gender, age, height, weight, country_code)
            
            if name in Ath_dict:
                Ath_dict[name].append(ath_tup)
            else:
                Ath_dict[name] = list()
                Ath_dict[name].append(ath_tup)
                
        except ValueError:
            continue

    return  Ath_dict

def get_country_stats(fp, Athlete): 
    '''
    Returns a dictionary of in the form {country:[(athlete tuple),...]}
    Athlete tuple in the form (name,team_name,year,sport,event,medal)
    Input:
        fp: file pointer of excel file
        Athlete: dictionary from get_athlete_stats function
    
    Read through file pointer
        Try:
            Declare variables for each line
            Create tuple using variables 
            Check to see if name in athlete dictionary - Ignore if True
                Insert new key:value pair to new dictionary
                or
                Add tuple to existing matching key
        Except:
            If values are null
            continue
    
    Return: Country Dictionary
    '''
    Country_dict = {}
    reader = csv.reader(fp)
    for line_list in reader:
        
        try:
            name = line_list[1]
            team_name = line_list[6]
            country_code = line_list[7]
            year = int(line_list[9])
            sport = line_list[12].lower()
            event = line_list[13].lower()
            medal = line_list[14].lower()
            country_tup = (name,team_name,year,sport,event,medal)
        
            if name in Athlete and medal.lower() != 'na':
                
                
                if country_code in Country_dict:
                    Country_dict[country_code].append(country_tup)
                    
                else:
                    Country_dict[country_code] = list()
                    Country_dict[country_code].append(country_tup)
                
        except ValueError:
            continue
        
    return Country_dict

def display_best_athletes_per_sport(athlete_dict, country_dict, sports_set):
    '''
    Prints an alphabetical table of sports, best athlete, country and medal cnt
    Input
        athlete_dict: dictionary created through get_athlete_stats func.
        country_dict: dictionary created through get_country_stats func.
        sports_set: Set of all sports that exist in country_dict
        
    Iterate through country_dict to create sport dictionary
        Sport dictionary = {sport:{athlete:medal count}}
    Iterate through sport dict using sorted key list find best athlete
        Create best athlete dictionary that contains only one athlete per sport
    Print alphabetical table of sport, best athlete, country,medals
    Print average intangibles of best athletes in table
    
    No Return
    '''
    
    HEADER = 'Best Athletes Per Sport'
    CLMNS = ['Sport','Athlete Name','Country','Medals']
    sport_dict,best_sport_dict = {},{}
    total_weight,total_height,total_age,ath_cnt,ath_total_cnt = 0,0,0,0,0
    
    #Iterate through each countries list of tuples
    for country_lst in country_dict.values():
        
        #Iterate through each individual tuples(athlete data)
        for ath_tup in country_lst:
            #Create variables for sport/name of athlete - save all the space!
            sport = ath_tup[3]
            ath = ath_tup[0]
            
            #Check if sport is in outer dictionary
            if sport in sport_dict:
                
                #Check if athlete is in inner dictionary
                if ath in sport_dict[sport]:
                    sport_dict[sport][ath] += 1
                
                #Add athlete if not in inner dictionary
                else:
                    sport_dict[sport][ath] = 1
                    
            #Add sport to outer dictionary and athlete to inner dictionary
            else:
                sport_dict[sport] = dict()
                sport_dict[sport][ath] = 1
    
    #Sorting sport_dict into a new dictionary for later use
    for sport in sport_dict:
        try:
            ath_list = list(sport_dict[sport.lower()].items())
            ath_list.sort(key = itemgetter(1),reverse = True)
            ath_list = ath_list[0]
            best_sport_dict[sport.lower()] = ath_list
            
        except KeyError:
            continue
        
    sport_list = sorted(sport_dict.keys())
    
    print("{:^50s}".format('Best Athletes Per Sport '))
    print("{:<25s}{:25s}{:10s}{:10s}".\
          format(CLMNS[0],CLMNS[1],CLMNS[2],CLMNS[3]))
    
    #Printing table of best athlete per sports aplhabetically
    for sport in sport_list:
        ath_total_cnt += 1
        temp_weight,temp_height,temp_age,ath_cnt = 0,0,0,0    
        athl = best_sport_dict[sport][0]
        mdls = best_sport_dict[sport][1]
        cntry = athlete_dict[athl][0][-1]
        print("{:25.20s}{:25.20s}{:10s}{:<10d}".format(sport,athl,cntry,mdls))
        
        #Adding to counts and totals for averages
        for i in athlete_dict[athl]:
            ath_cnt += 1
            temp_age += i[1]
            temp_height += i[2]
            temp_weight += i[3]
            
        temp_age = temp_age/ath_cnt
        temp_height = temp_height/ath_cnt
        temp_weight = temp_weight/ath_cnt        
        total_age += temp_age
        total_height += temp_height
        total_weight += temp_weight
                
    #Printing averages of best athletes 
    print('-'*50)
    print()
    print("Average Age of Best Athletes: {:5.1f} yr".format\
                                                  (total_age/ath_total_cnt))
    print('Average Height of Best Athletes: {:5.1f} cm'.format\
                                                  (total_height/ath_total_cnt))
    print('Average Weight of Best Athletes: {:5.1f} kg'.format\
                                                  (total_weight/ath_total_cnt))
    
    
def display_top_countries_by_sport(country_dict, sport):
    '''
    Prints a table of medals per country per sport sorted by most medals to least
    Input
        country_dict: Dictionary from get_country_stats function
        sport: String of sport for the table 
    
    Creates country medal dictionary by sorting through country_dict dictionary
        format: {Country:[Gold,Silver,Bronze]}
    Make list of lists out of country-medal dict to sort
    Sort list of lists by medal counts and discard null values
    Print values to formatted table
    
    No Return
    '''
    
    #Constants
    HEADER = 'Countries And Amount Of Medals In' + ' ' + sport
    CLMNS = ['Country/Team ',' Gold ',' Silver  ','Bronze ']
    country_medal_dict = {}
    
    #Iterate through values (list of tuples) of country dict
    for tup_list in country_dict.values():
       
        #Iterate through althere tuples of list of tuples
       for ath_tup in tup_list:
           
           #If athlete tuple matches input sport, add country to new dictionary
           #Or if already added, add to value (medal count) 
           if sport in ath_tup:
               country = ath_tup[1]
               medal = ath_tup[-1]
               
               if country in country_medal_dict:
                   if medal == 'gold':
                       country_medal_dict[country][0] += 1
                       
                   elif medal == 'silver':
                       country_medal_dict[country][1] += 1
                       
                   elif medal == 'bronze':
                       country_medal_dict[country][2] += 1
               
               else:
                   
                   country_medal_dict[country] = [0,0,0]
                   if medal == 'gold':
                       country_medal_dict[country][0] += 1
                       
                   elif medal == 'silver':
                       country_medal_dict[country][1] += 1
                       
                   elif medal == 'bronze':
                       country_medal_dict[country][2] += 1
                       
    #Make sortable list out of dictionary and sort using itemgetter
    cnt_mdl_list = []                
    for i in country_medal_dict:
        if country_medal_dict[i] != [0,0,0]:
            temp_lst = [i,country_medal_dict[i]]
            cnt_mdl_list.append(temp_lst)  
           
    cnt_mdl_list.sort(key = itemgetter(1), reverse=True)
 
    #Print sorted and formatted table
    print("{:^50s}".format(HEADER.title()))
    print()
    print("{:<20s}{:10s}{:10s}{:10s}".format\
          (CLMNS[0],CLMNS[1],CLMNS[2],CLMNS[3]))
    for i in cnt_mdl_list:
        print("{:<20.20s}{:<10d}{:<10d}{:<10d}".format\
                                      (i[0],i[1][0],i[1][1],i[1][2]))
    
        
            

def prepare_plot(country_lst):
    
    '''
    Returns four sorted lists based off the inputted list of tuples
    One list of years, three lists for each medal count ordered to the year list
    Input
        country_lst: A list of tuples from the country_stats dictionary
    
    Creates a dictionary of year(key) and medals for that year (value)
    Creates a year list by sorting the list of keys from created dictionary
    Creates ordered medal lists by accessing  year/medal dict using year list
    
    Return: tuple of year and medal lists 
    '''

    year_medal_dict = {}
    gold_lst,silv_lst,bronze_lst,return_lst = [],[],[],[] 
    
   
    for ath_tup in country_lst:
        
        if ath_tup[2] in year_medal_dict:
            year_medal_dict[ath_tup[2]].append(ath_tup[-1])
            
        else:
            year_medal_dict[ath_tup[2]] = list()
            year_medal_dict[ath_tup[2]].append(ath_tup[-1])
    
    year_list = sorted(year_medal_dict.keys())
    
    for year in year_list:
        gold_cnt, silv_cnt, bronze_cnt = 0,0,0
        
        for i in year_medal_dict[year]:
            
            if i == 'gold':
                gold_cnt += 1
                
            elif i == 'silver':
                silv_cnt += 1
                
            elif i == 'bronze':
                bronze_cnt += 1
                
        gold_lst.append(gold_cnt)
        silv_lst.append(silv_cnt)
        bronze_lst.append(bronze_cnt)
        
    return_lst.extend((year_list,gold_lst,silv_lst,bronze_lst))
    
    return tuple(return_lst)
    
    
def plot_country_medals_per_year(year, gold, silver, bronze, country):
    
    plt.plot(year, gold, 'yo')
    plt.plot(year, silver, 'bs')
    plt.plot(year, bronze, 'ro')
    plt.title("Number of Medals Over the Years For {}".format(country))
    plt.xlabel('Years'), plt.ylabel('Number of medals')
    plt.legend(['gold','silver','bronze'])
    #plt.show()
    country=country.replace(" ","_")
    plt.savefig(f"{country}_plot.png")
    plt.clf()
    
def main():
    '''
    Display tables of data about olympics
    No Input
    
    Create file poiner using excel file containing data
    Build two dictionaries using file pointer
        Athlete dictionary
        Country Stats dictionary
    Print alphabetic table of best athlete for all sports
    Prompt user until enter valid dindiviudal sport (q to quit program)
        Print best countries for each sport by medal count
        Prompt user for plot option (plot if Yes)
        Continue until user enters 'q' or 'Q'
        
    No return
    '''
    #Make file pointer, create dictionaries and valid sport set
    fp = open_file()
    athlete_stats_dict = get_athlete_stats(fp)
    fp.seek(0)
    country_stats_dict = get_country_stats(fp,athlete_stats_dict)
    sports_set = set()
    
    for tup_list in country_stats_dict.values():
        for i in tup_list:
            sports_set.add(i[3])
    
    #Print best athlete per sport table
    display_best_athletes_per_sport(athlete_stats_dict,\
                                    country_stats_dict,sports_set)
    
    #Input loop - COuntry/Sport table + Graphing
    print()
    input_str = ' '
    while input_str != 'q':      
        
        #Checking valid input
        input_str = input('Please enter a sport: ').lower()
        if input_str == 'q':
            return
        
        while input_str not in sports_set:
            input_str = input('Invalid input. Please enter another sport: ')
        
        #Display table
        print()
        display_top_countries_by_sport(country_stats_dict, input_str)
        ans_str = input('Do you want to plot (y/n): ')
        
        #Graph if statement
        if ans_str.lower() == 'y':
            print()
            plot_str = input('Please enter a country code:')
            country_str = country_stats_dict[plot_str][1][1]
            year,gold,silv,bronze = prepare_plot(country_stats_dict[plot_str])
            plot_country_medals_per_year(year,gold,silv,bronze,country_str)
                   
    
###### Main Code ######
if __name__ == "__main__":
    main()
