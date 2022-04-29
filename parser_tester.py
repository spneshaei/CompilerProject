import os


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
for test_dir in os.listdir('PA2_Testcases'):
    total_tests_count += 1
    test_tree = "PA2_Testcases/" + test_dir + "/parse_tree.txt"
    test_errors = "PA2_Testcases/" + test_dir + "/syntax_errors.txt"
    os.system('cp PA2_Testcases/' + test_dir + "/input.txt ./")
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
print(str(passed_test_count) + " passed out of " + str(total_tests_count) + " tests.")
