import os
from sqlite3 import Time
from threading import Thread
from time import sleep


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


total_tests_count = 0
passed_test_count = 0
for test_dir in os.listdir('PA3_Testcases'):
    total_tests_count += 1
    test_input = "PA3_Testcases/" + test_dir + "/input.txt"
    test_expected = "PA3_Testcases/" + test_dir + "/expected.txt"
    os.system(f"cp {test_input} ./")
    os.system('python3.8 compiler.py')
    print("Running test " + test_dir)
    failed = False
    os.system("./tester > expected.txt")
    os.system("grep PRINT expected.txt > expected2.txt")
    if file_equal(test_expected, "./expected2.txt"):
        passed_test_count += 1
        print("TEST PASSED!")
    else:
        print("TEST FAILED...")
print(str(passed_test_count) + " passed out of " + str(total_tests_count) + " tests.")
