# add to view.py

from django.db import connection, reset_queries
import time
import functools

def query_debugger(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func


#decorator to put above a function
@query_debugger

# ie
#
# @query_debugger
# def index(request):






    # list_of_families = ["observation", "communication", "electrical", "optics"]

    # list_of_elements = [
    #             {
    #                 "element": "airDensity",
    #                 "families": ["observation", "communication"]
    #             },
    #             {
    #                 "element": "camera",
    #                 "families": ["electrical", "optics"]
    #             },
    #             {
    #                 "element": "coating",
    #                 "families": ["communication", "optics"]
    #             },
    #             {
    #                 "element": "amplitude",
    #                 "families": ["observation", "electrical"]
    #             }

    #         ]

    # famgroups = {
    #                 "observation" : ["amplitude","airDensity"],
    #                 "optics" : ["camera", "coating"],
    #                 "communication" : ["airDensity", "coating"],
    #                 "electrical" : ["camera","amplitude"],
    #             }
