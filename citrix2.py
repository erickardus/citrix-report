from bs4 import BeautifulSoup

report_file = "./XenAppServerHealthCheckResults.htm"


def parse_html_table(table):
    """
    :param table: Expects a table object structure from BeautifulSoup
    :return: Returns a list of dictionaries, that contain a mapping of the relationship header<->value
    e.g [ {'server_name': 'host1.domain', 'IP': '10.10.11.11', 'ping': 'ok'},
        {'server_name': 'host3.domain', 'IP': '192.168.1.20', 'ping': 'ok'} ]
    """

    # Creates a list with the table header values, please note we consider the headers to be in row[0]
    headers = [x.string for x in table.find_all('tr')[0] if x != '\n']     #

    # Remove the first row of the table, so we only see values
    rows = table.find_all('tr')[1:]

    # For every row, combine the 'headers' list with the row into a dictionary and append the result in a list of dict.
    result = []
    for row in rows:
        values = [x.string for x in row.find_all('td')]
        dictionary = dict(zip(headers, values))
        result.append(dictionary)

    return result

# Parse the HTML report file into a BeautifulSoup object
with open(report_file) as fh:
    soup = BeautifulSoup(fh.read().replace('\x00', ''), 'html.parser')

# Parse every table into dictionaries. Make sure to only use tables with desired content.
list_of_tables = soup.find_all('table')
chosen_tables = [list_of_tables[2]]   # Only interested in table num 2

for table in chosen_tables:
    print(parse_html_table(table))
    print()


