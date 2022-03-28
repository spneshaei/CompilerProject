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
for test_dir in os.listdir('PA1_Testcases'):
    total_tests_count += 1
    test_tokens = "PA1_Testcases/" + test_dir + "/tokens.txt"
    test_errors = "PA1_Testcases/" + test_dir + "/lexical_errors.txt"
    test_symbols = "PA1_Testcases/" + test_dir + "/symbol_table.txt"
    os.system('cp PA1_Testcases/' + test_dir + "/input.txt ./")
    os.system('python3.8 compiler.py')
    print("Running test " + test_dir)
    failed = False
    if not file_equal(test_tokens, './tokens.txt'):
        print("TEST " + test_dir + " FAILED IN TOKENS")
        failed = True
    if not file_equal(test_errors, './lexical_errors.txt'):
        print("TEST " + test_dir + " FAILED IN ERRORS")
        failed = True
    if not file_equal(test_symbols, './symbol_table.txt'):
        print("TEST " + test_dir + " FAILED IN SYMBOLS")
        failed = True
    if not failed:
        passed_test_count += 1
        print("TEST PASSED")
print(str(passed_test_count) + " passed out of " + str(total_tests_count) + " tests.")
