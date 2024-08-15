import os
from collections import defaultdict
from itertools import permutations

from pyspark import RDD, SparkContext
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import countDistinct

def cmp(x, y):
   return (x > y) - (x < y)


def restaurant_shift_coworkers(worker_shifts: RDD) -> RDD:
    """
    Takes an RDD that represents the contents of the worker_shifts.txt. Performs a series of MapReduce operations via
    PySpark to calculate the number of shifts worked together by each pair of co-workers. Returns the results as an RDD
    sorted by the number of shifts worked together THEN by the names of co-workers in a DESCENDING order.
    :param worker_shifts: RDD object of the contents of worker_shifts.txt.
    :return: RDD of pairs of co-workers and the number of shifts they worked together sorted in a DESCENDING order by
             the number of shifts then by the names of co-workers.
             Example output: [(('Shreya Chmela', 'Fabian Henderson'), 3),
                              (('Fabian Henderson', 'Shreya Chmela'), 3),
                              (('Shreya Chmela', 'Leila Jager'), 2),
                              (('Leila Jager', 'Shreya Chmela'), 2)]
    """
    '''Logic: First swap dates and name field in first map fucntion, then reduce will create list of names who worked on same date
    with date as Key E.g (2021-09-01)---> Anmol, Shubam, Sam, then we give this to another map function in which we will generate unique pairs from the list of names and after this
    tuple as a key and 1 as value which will be input to another reduce function which will calculate count the no of shifts co-workers worked together.'''
    lines_mapped = worker_shifts.map(lambda data: (data.split(",")[1], [(data.split(",")[0])])). \
        reduceByKey(lambda x, y: x + y)
    #for x in lines_mapped.collect():
     #   x[1].sort()
    pairs = lines_mapped.flatMap(lambda pair: [((x, y), 1) for x in pair[1] for y in pair[1] if x != y ])
    pairs_reduced = pairs.reduceByKey(lambda x, y: x + y)
    counts_sorted = pairs_reduced.sortBy(lambda x: x[1], ascending=False)
    return counts_sorted






def air_flights_most_canceled_flights(flights: DataFrame) -> str:
    """
    Takes the flight data as a DataFrame and finds the airline that had the most canceled flights on Sep. 2021
    :param flights: Spark DataFrame of the flights CSV file.
    :return: The name of the airline with most canceled flights on Sep. 2021.
    """
    #get flights of september month
    cancelled_Flights = flights.filter((flights.FlightDate >= '2021-09-01') & (flights.FlightDate <= '2021-09-30'))
    #Get flights which are cancelled
    cancelled_Flights = cancelled_Flights.filter(cancelled_Flights.Cancelled == True)
    #get count on the basis of Airline, e.g Airline --> flightcancelled
    most_cancelledFlight = cancelled_Flights.groupBy(cancelled_Flights.Airline).count()
    #sort in descending order on the basis of count
    most_cancelledFlight = most_cancelledFlight.orderBy(('count'), ascending=[False])

    return most_cancelledFlight.take(1)[0][0]


def air_flights_diverted_flights(flights: DataFrame) -> int:
    """
    Takes the flight data as a DataFrame and calculates the number of flights that were diverted in the period of 
    20-30 Nov. 2021.
    :param flights: Spark DataFrame of the flights CSV file.
    :return: The number of diverted flights between 20-30 Nov. 2021.
    """
    divertedFlights = flights.filter((flights.FlightDate >= '2021-11-20') & (flights.FlightDate <= '2021-11-30'))

    divertedFlights = divertedFlights.select(divertedFlights.Diverted)

    divertedFlights = divertedFlights.filter(divertedFlights.Diverted == True)

    ans = divertedFlights.groupBy().count().take(1)[0][0]

    return ans


def air_flights_avg_airtime(flights: DataFrame) -> float:
    """
    Takes the flight data as a DataFrame and calculates the average airtime of the flights from Nashville, TN to 
    Chicago, IL.
    :param flights: Spark DataFrame of the flights CSV file.
    :return: The average airtime average airtime of the flights from Nashville, TN to 
    Chicago, IL.
    """
    averageTime = flights.filter((flights.OriginCityName == 'Nashville, TN') & (flights.DestCityName == 'Chicago, IL'))
    averageTime = averageTime.select(flights.AirTime)
    averageTime = averageTime.groupBy().avg()
    return averageTime.take(1)[0][0]


def air_flights_missing_departure_time(flights: DataFrame) -> int:
    """
    Takes the flight data as a DataFrame and find the number of unique dates where the departure time (DepTime) is 
    missing.
    :param flights: Spark DataFrame of the flights CSV file.
    :return: the number of unique dates where DepTime is missing. 
    """
    uniqueDates = flights.filter(flights.DepTime.isNull())
    uniqueDates = uniqueDates.select(countDistinct(uniqueDates.FlightDate))
    return uniqueDates.take(1)[0][0]


def main():
    # initialize SparkContext and SparkSession
    sc = SparkContext('local[*]')
    spark = SparkSession.builder.getOrCreate()

    print('########################## Problem 1 ########################')
    # problem 1: restaurant shift coworkers with Spark and MapReduce
    # read the file
    worker_shifts = sc.textFile('worker_shifts.txt')
    sorted_num_coworking_shifts = restaurant_shift_coworkers(worker_shifts)
    # print the most, least, and average number of shifts together
    sorted_num_coworking_shifts.persist()
    print('Co-Workers with most shifts together:', sorted_num_coworking_shifts.first())
    print('Co-Workers with least shifts together:', sorted_num_coworking_shifts.sortBy(lambda x: (x[1], x[0])).first())
    print('Avg. No. of Shared Shifts:',
          sorted_num_coworking_shifts.map(lambda x: x[1]).reduce(
              lambda x, y: x + y) / sorted_num_coworking_shifts.count())

    print('########################## Problem 2 ########################')
    # problem 2: PySpark DataFrame operations
    # read the file
    flights = spark.read.csv('Combined_Flights_2021.csv', header=True, inferSchema=True)
    print('Q1:', air_flights_most_canceled_flights(flights), 'had the most canceled flights in September 2021.')
    print('Q2:', air_flights_diverted_flights(flights), 'flights were diverted between the period of 20th-30th '
                                                        'November 2021.')
    print('Q3:', air_flights_avg_airtime(flights), 'is the average airtime for flights that were flying from '
                                                   'Nashville to Chicago.')
    print('Q4:', air_flights_missing_departure_time(flights), 'unique dates where departure time (DepTime) was '
                                                              'not recorded.')


if __name__ == '__main__':
    main()
