# Discreet correlations

## FizzBuzz

    ./datasets/synthetic/fizzbuzz.py
    ./dboost-stdin.py --histogram 0.8 0.05 --discretestats 8 2 datasets/synthetic/fizzbuzz -v

This example shows how adding a few extraction rules manages to capture relatively complex behavior; this provides a much nicer way to specify rules than explicitly encoding the rules of FizzBuzz.

## Logins

    ./datasets/synthetic/logins.py

An example of suspect behavior detection. User 0 always logs in from the same country; user 1 logs in from different countries on week-days and week-ends. User 2 doesn't follow any particular pattern.

    ./dboost-stdin.py --histogram 0.6 0.05 --discretestats 8 2 datasets/synthetic/logins0
    ./dboost-stdin.py --histogram 0.6 0.05 --discretestats 8 2 datasets/synthetic/logins1
    ./dboost-stdin.py --histogram 0.6 0.05 --discretestats 8 2 datasets/synthetic/logins2

The three invocations test for proper detection of outliers on the three users, individually

    ./dboost-stdin.py --histogram 0.6 0.05 --discretestats 8 2 <(cat datasets/synthetic/logins{0,1}) -d div -d mod --in-memory

This one merges user 0 and user 1.

# Continuous correlations

## Intel

    ./dboost-stdin.py -F ' ' --statistical .7 --mixture 1 .3 datasets/real/intel/sensors-1000_dataonly.txt -d unix2date_float
    ./dboost-stdin.py -F ' ' --statistical .6 --mixture 2 .3 datasets/real/intel/sensors-1000_dataonly.txt -- depracated, worked with buggish preprocessor

