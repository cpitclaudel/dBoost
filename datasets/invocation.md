# No correlations

    ./dboost/dboost-stdin.py --statistical 1 --histogram 0.8 0.2 datasets/real/csail.txt
    ./dboost/dboost-stdin.py --statistical 1 --histogram 0.8 0.2 datasets/real/csail-tiny.txt
    ./dboost/dboost-stdin.py --statistical 1 --gaussian 3 datasets/real/csail-tiny.txt -vv

These find suspicious-looking values in {a subset of,} the CSAIL directory

# Discreet correlations

## FizzBuzz

    ./datasets/synthetic/fizzbuzz.py
    ./dboost/dboost-stdin.py --histogram 0.8 0.05 --discretestats 8 2 datasets/synthetic/fizzbuzz -v
    ./dboost/dboost-stdin.py --partitionedhistogram 5 0.8 0.05 --discretestats 8 2 datasets/synthetic/fizzbuzz -vv

This example shows how adding a few extraction rules manages to capture relatively complex behavior; this provides a much nicer way to specify rules than explicitly encoding the rules of FizzBuzz.

## Logins

    ./datasets/synthetic/logins.py

An example of suspect behavior detection. User 0 always logs in from the same country; user 1 logs in from different countries on week-days and week-ends. User 2 doesn't follow any particular pattern.

    ./dboost/dboost-stdin.py --histogram 0.6 0.05 --discretestats 8 2 datasets/synthetic/logins0
    ./dboost/dboost-stdin.py --histogram 0.6 0.05 --discretestats 8 2 datasets/synthetic/logins1
    ./dboost/dboost-stdin.py --histogram 0.6 0.05 --discretestats 8 2 datasets/synthetic/logins2

The three invocations test for proper detection of outliers on the three users, individually

    ./dboost/dboost-stdin.py --histogram 0.6 0.05 --discretestats 8 2 <(cat datasets/synthetic/logins{0,1}) -d div -d mod --in-memory
    ./dboost/dboost-stdin.py --partitionedhistogram 2 0.9 0.03 --discretestats 16 3 <(cat datasets/synthetic/logins{0,1,2}) -d div -d mod -d bits --in-memory -d unix2date

These ones merge multiple datasets

## TCPH

    ./dboost/dboost-stdin.py --histogram 0.9 0.01 --discretestats 8 2 datasets/real/tcph/tcph-clean -F "	" -v -d div -d bits -d unix2date_float -d unix2date -d string_case -d is_weekend

# Continuous correlations

## Intel

    ./dboost/dboost-stdin.py -F ' ' --statistical .7 --mixture 2 .1 datasets/real/intel/sensors-1000_dataonly.txt -d unix2date_float
