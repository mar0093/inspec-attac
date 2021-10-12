__author__ = "James Marmarou"
__version__ = "1.0"

'''
This script prompts you to pass a wikipedia URL. E.g.

https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population

It will then provide with a table like below, Containing Metadata about said table.

|-------------------------------------------------------------------------------------|
| Rank |                 Column Name              |         Example      |  Data Type |
|-------------------------------------------------------------------------------------|
| 0    |                                     Rank | 1                    | int64      |
| 1    |    Greater Capital City Statistical Area | Greater Sydney       | object     |
| 2    | 30 June 2020 estimated resident popul... | 5367206              | int64      |
| 3    |                        2019-20 growth[2] | 57107                | int64      |
| 4    |                      2019-20%  change[2] | 1.1                  | float64    |
| 5    |                            Included SUAs | SydneyCentral Coast  | object     |
|-------------------------------------------------------------------------------------|

You will then be prompted with which columns you would like to plot. E.g. 2,3

and which column you would like to label the x-axis ticks with. E.g. 4 

It will then save a version of the of the chjart as a .png file in the root folder. 

!!!

Note that I have not included error handling. Please only pass colunms that are data types
of ints or floats.
'''

import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import matplotlib.pyplot as plt #library for graphical plotting
#Also requires install of lxml for pandas.




def url_reader():
    """
    Prompts User for a Wikipedia Url and returns whether the call to the page was successful.

    :return: repsonse: The response received
    """
    wikiurl = str(input("Enter Wikipedia page with table. Example:\n"
          "https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population\n"))
    response = requests.get(wikiurl)
    print(str(response.status_code) + " Successful Response\n")
    return response


def parse_data(response):
    """
    Takes the response from the Request.get() method and parses
    the html from the wiki page looking for the class object 'wikitable'
    :param response: Request Object
    :return: wikitable: Raw HTML of the table (If there is one)
    """
    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    wikitable = soup.find('table', {'class': "wikitable"})
    return wikitable


def table2df(wikitable):
    """
    Takes The wiki table as the raw html.
    Uses pandas method 'read_html' to convert to a list.
    List is then converted to dataframe.
    :param wikitable: html for wiki table.
    :return: df: A dataframe with the first table appearing within the page.
    """
    list_obj = pd.read_html(str(wikitable))
    df = pd.DataFrame(list_obj[0])     # convert list to dataframe
    #df = capture_numerical(df)
    return df


def capture_numerical(df):
    """
    Takes a dataframe and returns a dataframe that only
    has numerical columns.

    !!! This is no longer used. All columns are displayed to the user.
    !!! See plot numerical column

    :param df: A pandas dataframe object.
    :return: A pandas dataframe object with numerical columns.
    """
    df = df.select_dtypes(['number'])
    return df


def plot_numerical_columns(df):
    """
    This function  Displays all columns found from the first table on the page.
    It will then ask for user input for which columns to plot and which
    to label the x-axis tickers with.
    It will then name the chart and store it in a file.
    :param df:
    :return: png file named 'chart.png'
    """
    print("|-------------------------------------------------------------------------------------|"
          "\n| Rank |                 Column Name              |         Example      |  Data Type |"
          "\n|-------------------------------------------------------------------------------------|")
    column_counter = 0
    column_tuple = []
    for column_name, item in df.iteritems():
        print("| %s | %s | %s | %s |" % (str(column_counter).ljust(4, ' '),
                                         str(column_name).rjust(40, ' '),
                                         str(df[column_name].iloc[0]).ljust(20, ' '),
                                         str(df.dtypes[column_name]).ljust(10, ' ')))
        column_tuple.append([column_counter, column_name])
        column_counter += 1
    print("|-------------------------------------------------------------------------------------|")

    # Takes input to which columns should be plotted.

    requested_columns = input("\nPlease list the rank for each column you wish"
                             " to be plotted. E.g.:\n1,2,4\n")
    list_rc = requested_columns.split(',')
    requested_column_names = []
    for i in list_rc:
        column_name = column_tuple[int(i)][1]
        requested_column_names.append(column_name)
    ax = df[requested_column_names].plot(label=column_name, kind='bar', rot=45)

    # Takes input to which column should be used for labelling tickers.

    ticker_column = input("\nIf you wish to label the ticks put down \n"
                          "the 'Rank' number. Else put n/N or leave blank.\n")
    if ticker_column != 'n' and ticker_column != 'N' and ticker_column != '':
        column_name = column_tuple[int(ticker_column)][1]
        ax.set_xticklabels(df[column_name])
    plt.legend()

    plt.savefig('chart.png')


def main():
    """
    Runs all the functions in a sequenced order.

    """
    response = url_reader()
    wikitable = parse_data(response)
    df = table2df(wikitable)
    plot_numerical_columns(df)


if __name__ == "__main__":
    main()
