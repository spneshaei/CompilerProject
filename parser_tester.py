import os
import sys


def file_equal(file1, file2):
    f1 = open(file1, "r")
    f2 = open(file2, "r")
    for line1 in f1:
        for line2 in f2:
            # matching line1 from both files
            if line1.strip() != line2.strip():
                print("LINE1: ", line1)
                print("LINE2: ", line2)
                f1.close()
                f2.close()
                return False
            break

    # closing files
    f1.close()
    f2.close()
    return True


tests_dir = ""

if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if i == 1:
            tests_dir = arg

if tests_dir == "":
    raise Exception("No test directory provided")


total_tests_count = 0
passed_test_count = 0
for test_dir in os.listdir(tests_dir):
    total_tests_count += 1
    test_tree = tests_dir + "/" + test_dir + "/parse_tree.txt"
    test_errors = tests_dir + "/" + test_dir + "/syntax_errors.txt"
    os.system('cp ' + tests_dir + '/' + test_dir + "/input.txt ./")
    os.system('python3.8 compiler.py')
    print("Running test " + test_dir)
    failed = False
    if not file_equal(test_tree, './parse_tree.txt'):
        print("TEST " + test_dir + " FAILED IN PARSE TREE")
        failed = True
    if not file_equal(test_errors, './syntax_errors.txt'):
        print("TEST " + test_dir + " FAILED IN ERRORS")
        failed = True
    if not failed:
        passed_test_count += 1
        print("TEST PASSED")
print(str(passed_test_count) + " passed out of " +
      str(total_tests_count) + " tests.")
