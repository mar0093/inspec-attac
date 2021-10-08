import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import matplotlib.pyplot as plt #library for graphical plotting
#Also requires lxml for pandas.

'''
'''
def url_reader():
    """

    :return:
    """
    # get the response in the form of html
    wikiurl = "https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population"
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(wikiurl)
    print(response.status_code)
    return response


def parse_data(response):

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    wikitable = soup.find('table', {'class': "wikitable"})
    print(wikitable)
    return wikitable


def table2df(wikitable):
    """

    :param wikitable:
    :return:
    """
    df = pd.read_html(str(wikitable))
    # convert list to dataframe
    df = pd.DataFrame(df[0])
    print(df.head())
    df = capture_numerical(df)
    return df


def capture_numerical(df):
    df = df.select_dtypes(['number'])
    print(df.head())
    return df


def plot_numerical_columns(df):
    df.plot.bar()
    plt.show()


def main():
    response = url_reader()
    wikitable = parse_data(response)
    df = table2df(wikitable)
    plot_numerical_columns(df)
    return 0

if __name__ == "__main__":
    main()