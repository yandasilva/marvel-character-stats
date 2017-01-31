#!/usr/bin/python -tt

#-----------------------------------------------------------------------------------------
#Developed by Yan Ramos da Silva (yandasilva.com)
#Generates statistics from data of Marvel characters and the universes where they appear
#Usage: ./generate-stats.py [n]
#n: number of entries to plot; defaults to 20.
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#Imports
#-----------------------------------------------------------------------------------------
import numpy as nmp
import pandas as pnd
import matplotlib.pyplot as plt
from collections import defaultdict
import os.path, sys, csv, requests, re

#-----------------------------------------------------------------------------------------
#Scrapes marvel.wikia.com pages and saves data to a .csv file
#-----------------------------------------------------------------------------------------
def generate_csv():

  #Sets the Wikia API URL for fetching 10k articles from the Character catagory
  offset = ''
  list_url = 'http://marvel.wikia.com/api/v1/Articles/List?category=Characters&limit=10000'
  #Creates data structure
  char_dict = defaultdict(set)
  universes = set()
  
  #Repeats until HTTP error (out of pages to scrape)
  try:
    while True:
      #Requests data starting from the desired offset
      r = requests.get(list_url + offset)
      response = r.json()
      
      #For each article in the response JSON:
      for item in response['items']:
        #Applies regex to separate character's name from universe of origin
        m = re.match(r'(.+)\s\(([^\)]+)\)', item['title'])
        #If there was a match (some page titles have typos that mess with the regex):
        if m:
          #Adds universe to the character's entry in char_dict and to the set of all
          #distinct universes
          universe = str(m.group(2))
          char_dict[m.group(1).encode('utf-8')].add(universe)
          universes.add(universe)
      #Changes offset to the one in the JSON object in order to continue fetching
      offset = '&offset=' + response['offset']
  
  #An exception will be thrown when the scraping reaches the last article of the list and
  #the code isn't able to find an offset, meaning that we're done
  except Exception as exc:
    print str(exc)
    pass
    
  #After all data has been scraped:
  finally:
    #Counts how many distinct Marvel universes are there
    k = len(universes)
    #Creates a new dict by zipping the alphabetically ordered list of universes and the
    #numbers from 1 to k. This step makes sure that the dataframe columns are sorted for
    #better readabilty
    univ_dict = dict(zip(sorted(universes), list(range(1, k + 1))))
    #Creates the table header
    header = ['Character'] + list(sorted(universes))
    #Initializes the dataframe with the header
    data = [header]
    
    #For every distinct Marvel character:
    for character in sorted(char_dict.keys()):
      #Initializes a new table line as its name + k 'False" values, one for each universe
      line = [character] + [False] * k
      #If a character has appeared in an universe, change the value on its column to 'True'
      for universe in char_dict[character]:
        line[univ_dict[universe]] = True
      #Adds line to dataframe
      data.append(line)
      
    #Writes the .csv file
    f = open('data.csv', 'w')
    w = csv.writer(f)
    w.writerows(data)
    f.close()
    
    #Returns the scraped data
    return pnd.DataFrame(data[1:], columns=data[0])
    
#-----------------------------------------------------------------------------------------
#Plots a horizontal bar graph of the dataframe
#-----------------------------------------------------------------------------------------
def plot_barh(df, column):
  
  #Plots graph using dataframe data
  barplot = df.plot(kind='barh', stacked='True', figsize=(16, 9))
  #Removes the y-axis label for better readability
  barplot.set_ylabel('')
  #Inverts the y-axis so the length of the bars decreases from top to bottom
  plt.gca().invert_yaxis()
  #Changes legend position so it doesn't overlap with the longest bar
  plt.legend(loc='lower right')
  #Saves graph to disk
  plt.savefig(column + '_bars.png')

#-----------------------------------------------------------------------------------------
#Plots a box & whiskers diagram of the dataframe
#-----------------------------------------------------------------------------------------
def plot_box(df, column):

  #Plots box & whiskers diagram using dataframe data
  box = df.plot.box()
  #Saves diagram to disk
  plt.savefig(column + '_box.png')

#-----------------------------------------------------------------------------------------
#Writes dataframe info to disk
#-----------------------------------------------------------------------------------------
def write_data_file(df, column, n):
  
  #Opens file; creates it if it doesn't exist
  f = open(column + '_data.txt', 'w')
  #Writes statistical data of the dataframe to the file
  f.write(str(df.describe()))
  f.write('\n\n')
  
  #Writes the values of the top n positions of the dataframe to the file
  f.write(str(df.head(n)))
  f.write('\n\n')
  
  #Writes dataframe's mode, its frequency and % of appearance to the file
  most_common = df[column].value_counts().idxmax()
  frequency = df[column].value_counts().max()
  total = df.shape[0]
  f.write('Most common value: {} appears {} times ({:.2f}%)'.format(most_common, 
    frequency, 100. * frequency/total))
  
  #Closes file
  f.close()

#-----------------------------------------------------------------------------------------
#Analyses the number of universes in which each character appears
#-----------------------------------------------------------------------------------------
def analyse_chars_data(df, n):

  print 'Analysing data...'
  #Creates a copy of the original dataframe
  dataframe = df.copy()
  #Sums every column the get the total # of universes where each character appears and
  #saves the result in a new column
  dataframe['Universes'] = dataframe.sum(axis=1)
  #Sets the 'Character' column as the dataframe's index, since its values are distinct
  dataframe.set_index('Character', inplace=True)
  #Removes all columns other than the recently created 'Universes'
  dataframe = dataframe[['Universes']]
  #Sorts the dataframe in descending order by the values on the 'Universes' column
  dataframe = dataframe.sort_values('Universes', ascending=False)
  
  print 'Writing results...'
  #Writes data to file before slicing the dataframe so it only considers the top n rows.
  #This is done in order to allow the method to correctly fetch the most frequent values
  #considering the entire dataframe and not only part of it.
  write_data_file(dataframe, 'Universes', n)
  dataframe = dataframe.iloc[:n]
  
  #Plots graphs for the top n entries
  plot_barh(dataframe, 'Characters')
  plot_box(dataframe, 'Characters')

#-----------------------------------------------------------------------------------------
#Analyses the number of characters that appear in each universe
#-----------------------------------------------------------------------------------------
def analyse_univs_data(df, n):
  
  print 'Analysing data...'
  #Creates a copy of the original dataframe
  dataframe = df.copy()
  #Removes the 'Character' column since their names won't be necessary for this analysis
  dataframe = dataframe.drop('Character', axis=1)
  #Sums every row in the dataframe to get the total # of characters in each universe and
  #saves the result in a new row appended to the end of the dataframe
  dataframe = dataframe.append(dataframe.sum(axis=0), ignore_index=True)
  #Deletes all rows other than the recently appended row and transverses the resulting
  #dataframe so it has only one column (variable) instead of only one row (observation)
  dataframe = dataframe.tail(1).T
  #Renames the dataframe's index and column for better readability
  dataframe.index.names = ['Universe']
  dataframe.columns = ['Characters']
  #Sorts the dataframe in descending order by the values on the 'Characters' column
  dataframe = dataframe.sort_values('Characters', ascending=False)
  
  print 'Writing results...'
  #Writes data to file
  write_data_file(dataframe, 'Characters', n)
  #Slices dataframe to consider only its top n entries
  dataframe = dataframe.iloc[:n]

  #Plots graphs for the top n entries
  plot_barh(dataframe, 'Universes')
  plot_box(dataframe, 'Universes')

#-----------------------------------------------------------------------------------------
#Main function
#-----------------------------------------------------------------------------------------
def main():
  try:
    #Checks if the .csv file already exists
    dataframe = pnd.read_csv('data.csv')
  except Exception as exc:
    #If it doesn't, creates the file
    dataframe = generate_csv()
  '''else:
    #If it does, reads the file
    print 'Reading dataframe...'
    dataframe = pnd.read_csv('data.csv')'''

  #Gets script arguments
  args = sys.argv[1:]
  #Gets n from args vector if its not None; else, defaults to 20
  n = 20 if not args else args[0]
    
  #Analyses data
  analyse_chars_data(dataframe, n)
  analyse_univs_data(dataframe, n)
    
    
#-----------------------------------------------------------------------------------------
#Main function call
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
  main()