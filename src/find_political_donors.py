from collections import namedtuple
import re
from datetime import datetime, date
from median_finder_heap import MedianFinder
from contributions import Contributions
import sys
import os.path

def group_median_by_zip_or_date(zip_or_date_dictionary, id, zip_or_date, amt):
    '''
    input: dictionary of contributors group_by (id, zip) or (id, date),
    id of contributor, zip or date and amount

    Check if (id, zip)|(id, date) of contributors already in dictionary and if it's true
    update current value: add input amout to heap, calculate a new median,
    update count, update total amount
    If (id, zip) not in dictionary add a new key value pairs

    dictionary has structure:
      key => (id, zip) or (id, date)
      value => Contributions object with attributes: median, count, total_amt
    '''

    key = (id, zip_or_date)
    if key in zip_or_date_dictionary:
        # key already in a dictionary then update current value

        median_by_zip = zip_or_date_dictionary[key].heap_obj
        median_by_zip.addNumber(amt)
        zip_or_date_dictionary[key].median = median_by_zip.findMedian()
        zip_or_date_dictionary[key].count += 1
        zip_or_date_dictionary[key].total_amt += amt
    else:
        median_by_zip = MedianFinder()
        median_by_zip.addNumber(amt)
        current_contributions = Contributions(median_by_zip.findMedian(), amt, median_by_zip)
        zip_or_date_dictionary[key] = current_contributions
    value = zip_or_date_dictionary[key]

    return [id,
            zip_or_date,
            str(value.median),
            str(value.count),
            str(int(value.total_amt))]


def main(file, output_zip, output_date):
    '''
    This function open input file, read this file line by line and validate each line.
    For every input line calculate running median, total dollar amount and
    total number of contributions by recipient and zip code or recipient and date.
    '''

    zipDictionary = dict()
    dateDictionary = dict()

    if len(file) == 0:
        return
    with open(file, "r") as f, open(output_zip, "w+") as zipoutput:
        for line in f:
            current_line = line.split("|")

            # check if input line is empty then skip and read next
            if len(current_line) == 0 or len(current_line) < 14:
                continue

            CMTE_ID, ZIP_CODE, TRANSACTION_DT = current_line[0], current_line[10], current_line[13]
            TRANSACTION_AMT, OTHER_ID = current_line[14], current_line[15]

            #if any of the next values are missing skip the entire line
            if OTHER_ID or not CMTE_ID or not TRANSACTION_AMT or not validate_amount(TRANSACTION_AMT):
                continue

            if validate_zipcode(ZIP_CODE):
                input = group_median_by_zip_or_date( zipDictionary,
                                                    CMTE_ID,
                                                    ZIP_CODE[:5],
                                                    float(TRANSACTION_AMT))

                # write each line to output file, separate every value by '|'
                zipoutput.write("|".join(input) + "\n")
            if validate_date(TRANSACTION_DT):
                group_median_by_zip_or_date(dateDictionary,
                                            CMTE_ID,
                                            TRANSACTION_DT,
                                            float(TRANSACTION_AMT))

    write_medialvals_by_date(dateDictionary, output_date)



def validate_zipcode(ZIP_CODE):
    '''
    input: zip_code
    Check the length of zipcode and check if zipcode contains only numbers
    output: True/False
    '''

    if len(ZIP_CODE) >= 5 and re.match("^.*?(\d+)$", ZIP_CODE):
        return True
    else:
        return False


def validate_date(TRANSACTION_DT):
    '''
    input: transaction date
    check if input date has a valid format and not greater than current date
    output: True/False
    '''

    if len(TRANSACTION_DT) < 8:
        return False
    try:
        date  = datetime.strptime(TRANSACTION_DT, "%m%d%Y").date()
        return date < date.today()
    except ValueError:
        return False
    # return True


def validate_amount(TRANSACTION_AMT):
    '''
    input: transaction amount
    check if input amount has a valid format
    output: True/False
    '''

    try:
        int(TRANSACTION_AMT)
    except ValueError:
        return False
    return True


def write_medialvals_by_date(dateDictionary, file):
    '''
    Function for writing results to ouput file
    input: file path and dictionary of contributors group_by id and date
    '''

    with open(file, "w+") as f:
        for key in sorted(dateDictionary.keys()):
            id, date = key
            value = dateDictionary[key]
            line = [id, date, str(value.median), str(value.count), str(int(value.total_amt))]
            f.write("|".join(line)+"\n")

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print "Some of the file missing"
        sys.exit()

    input_file = sys.argv[1]
    output_zip = sys.argv[2]
    output_date = sys.argv[3]

    if not os.path.exists(input_file):
        print "Either file is missing or is not readable"
        sys.exit()

    main(input_file, output_zip, output_date)
