# Import necessary modules
from tests import *
import utils

def main(inputs, help_message, functions, saved_inputs = {}, fail_count = 0):
    """
    The main function to run tests.
    :param inputs: dict, input arguments
    :param help_message: str, help message to be displayed
    :param functions: dict, a dictionary containing the functions to be tested
    :param saved_inputs: dict, a dictionary to store the inputs
    :param fail_count: int, number of test cases failed
    """
    # Get input arguments using command-line interface
    for key, value in utils.cli(utils.settings(help_message)).items():
        inputs[key] = value
        saved_inputs[key] = value
    
    # If 'help' flag is passed, print help message and exit
    if inputs["help"]:
        print(help_message)
    else:
        print("Testing...")
        # Loop through the functions and run tests on selected function(s)
        for function_name in functions:
            if inputs["go"] == "data" or function_name == inputs["go"]:
                # Restore saved inputs
                for key, value in saved_inputs.items():
                    inputs[key] = value
                # Run the selected function and check if it passes or fails
                if functions[function_name]() == False:
                    fail_count = fail_count + 1
                    print(function_name, ": failing")
                else:
                    print(function_name, ": passing")
    exit(fail_count)

# Create a dictionary containing test functions
test_functions = {}
def add_test_function(key, description, function):
    """
    A helper function to add test functions to the dictionary.
    :param key: str, key name for the function
    :param description: str, description of the function
    :param function: function, the test function to be added
    """
    test_functions[key] = function
    # Update help message with the added test function
    inputs.help_string = inputs.help_string + ("  -g  %s\t%s\n" % (key, description))

# Add test functions to the dictionary
add_test_function("sym", "check syms", test_sym)
add_test_function("num", "check nums", test_nums)
add_test_function("the", "show settings", test_the)
add_test_function("repCols", "check repCols", test_repCols)
add_test_function("repRows", "check repRows", test_repRows)
add_test_function("synonyms", "check synonyms", test_synonyms)
add_test_function("prototypes", "check prototypes", test_prototypes)
add_test_function("position", "check position", test_position)
add_test_function("every", "check every", test_every)

# Print the test functions dictionary
print(test_functions)

# Run the tests using the main function
main(inputs.the, inputs.help_string, test_functions)
