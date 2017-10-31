# Find political donors

## Challenge summary
For this challenge, we need to take an input file that lists campaign contributions by individual donors and distill it into two output files:

1. `medianvals_by_zip.txt`: contains a calculated running median, total dollar amount and total number of contributions by recipient and zip code

2. `medianvals_by_date.txt`: has the calculated median, total dollar amount and total number of contributions by recipient and date.

## Input file
Every line of input file has many fields, but for purpose of this challenge we only need:

* `CMTE_ID`: identifies the flier, which for our purposes is the recipient of this contribution
* `ZIP_CODE`:  zip code of the contributor (we only want the first five digits/characters)
* `TRANSACTION_DT`: date of the transaction
* `TRANSACTION_AMT`: amount of the transaction
* `OTHER_ID`: a field that denotes whether contribution came from a person or an entity

## Output

1. `medianvals_by_zip.txt`: contains a calculated running median, total dollar amount and total number of contributions by recipient and zip code

2. `medianvals_by_date.txt`: has the calculated median, total dollar amount and total number of contributions by recipient and date.

## Implementation

There are two different outputs: one for results group by id and second one for results group by date.
For storing the results I used Python dictionaries: zipDictionary and dateDictionary. The key of each dictionary is tuple of recipient id and zip or recipient id and date, values for corresponding key is the Contributions object with total number of transactions, running median and total amount so far.

For finding running median I used two approaches:
  1. In first approach input amount stored in the sorted list, it's easy to find the running median in the sorted list. To add a new input amount in the sorted order I used binary search.
  2. In second approach I used max and min heap for stored stream amount so far.

## Tests

I also created several tests for different edge cases:

1. `test_2`: several lines have OTHER_ID.
2. `test_3`: several lines have invalid transactions dates.
3. `test_6_invalid_date`: all lines has invalid date, output file `medianvals_by_date` is empty
4. `test_6_invalid_zip`: all lines has invalid zip code, output file `medianvals_by_zip` is empty

## Run Instructions
1. cd  find-political-donors
2. In command line run `python ./src/find_political_donors.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt
`
3. To run code test:  `cd insight_testsuite/`, `./run_tests.sh`

## Dependencies
Version of Python on my laptop is 2.7.

os
datetime
sys
re
heapq
