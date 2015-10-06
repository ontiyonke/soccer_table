## Ranking Table for a Soccer League

Project forked from [Ian Kelling] (https://github.com/ian-kelling/python-example-soccer-table)

### Changes
------------
* Made code base work with python 3 (sorted cmp has been deprecated in python 3; replace with key option).
* Encapsulated the code.
* handles exception for files not found.
* handles encoding (this is unicode **utf-8**).

command-line application that will calculate the ranking table for a soccer league.


### Input/output
----------------
* The input and output will be text. Either using stdin/stdout or taking filenames on the command line is fine.
* The input contains results of games, one per line. See “Sample input” for details.
* The output should be ordered from most to least points, following the format specified in “Expected output”.


### Getting up and running
---------------------------

##### Basics

Help:

* Command line help is available with no arguments and no standard input, or an argument of -h or --help

Run **solutions.py ** for a file input:

*  $ python solutions.py sample-input.txt


### Results
-----------
The input is game results, one per line (see sample-input.txt). The output is a ranking of teams and their points,
one per line (see expected-output.txt). We expect that the input will be well-formed.

In this league, teams accumulate points by winning (3 points) or drawing (1point).
If two teams have the same number of points, they are ranked equally and are output in alphabetical order.


##### Test coverage

To run the tests, check your test coverage:

* Tests are in test.py and can be run by executing test.py. The tests assume solution.py is in the same directory
or in the module path.
