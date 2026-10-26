import Parser as p
import Test
import traceback


class Verifier:
    def run_test(self, test_name, test_input, expected_output):
        """
        This function runs the lexer and parser on the test input,
        compares the AST with the expected output or the error message.
        Returns True if the test passes, False otherwise.
        """
        print(f"--- Running {test_name} ---")
        try:
            # Initialize the lexer and tokenize the input
            lexer = p.Lexer(test_input)
            tokens = lexer.tokenize()

            # Initialize the parser and generate the AST
            parser = p.Parser(tokens)
            ast = parser.parse()
            ast_string = ast.to_string()

            # Remove all spaces and newlines for a clean comparison
            ast_string_clean = self.clean_string(ast_string)
            expected_output_string_clean = self.clean_string(expected_output)

            # Compare the result with the expected output
            if ast_string_clean == expected_output_string_clean:
                print(f"{test_name} passed.\n")
                return True
            else:
                print(f"{test_name} failed.\n")
                print("Wrong answer:")
                print(ast_string_clean)
                return False
        except Exception as e:
            print(f"{test_name} failed with an exception: {e}")
            traceback.print_exc()
            print("--------------------")
            return False

    def clean_string(self, s: str) -> str:
        """
        Utility function to clean a string by removing spaces and newlines.
        """
        return s.replace(" ", "").replace("\n", "")


if __name__ == "__main__":
    verifier = Verifier()
    test_cases = [
        ("Test Case 1", Test.test_input_1, Test.expected_output_1),
        ("Test Case 2", Test.test_input_2, Test.expected_output_2),
        ("Test Case 3", Test.test_input_3, Test.expected_output_3),
        ("Test Case 4", Test.test_input_4, Test.expected_output_4),
        ("Test Case 5", Test.test_input_5, Test.expected_output_5),
        ("Test Case 6", Test.test_input_6, Test.expected_output_6),
        ("Test Case 7", Test.test_input_7, Test.expected_output_7),
        ("Test Case 8", Test.test_input_8, Test.expected_output_8),
        ("Test Case 9", Test.test_input_9, Test.expected_output_9),
        ("Test Case 10", Test.test_input_10, Test.expected_output_10),
        ("Test Case 11", Test.test_input_11, Test.expected_output_11),
        ("Test Case 12", Test.test_input_12, Test.expected_output_12),
        ("Test Case 13", Test.test_input_13, Test.expected_output_13),
        ("Test Case 14", Test.test_input_14, Test.expected_output_14),
        ("Test Case 15", Test.test_input_15, Test.expected_output_15),
        ("Test Case 16", Test.test_input_16, Test.expected_output_16),
        ("Test Case 17", Test.test_input_17, Test.expected_output_17),
        ("Test Case 18", Test.test_input_18, Test.expected_output_18),
        ("Test Case 19", Test.test_input_19, Test.expected_output_19),
        ("Test Case 20", Test.test_input_20, Test.expected_output_20),
        ("Test Case 21", Test.test_input_21, Test.expected_output_21),
        ("Test Case 22", Test.test_input_22, Test.expected_output_22),
        ("Test Case 23", Test.test_input_23, Test.expected_output_23),
        ("Test Case 24", Test.test_input_24, Test.expected_output_24),
        ("Test Case 25", Test.test_input_25, Test.expected_output_25),
        ("Test Case 26", Test.test_input_26, Test.expected_output_26),
        ("Test Case 27", Test.test_input_27, Test.expected_output_27),
        ("Test Case 28", Test.test_input_28, Test.expected_output_28),
        ("Test Case 29", Test.test_input_29, Test.expected_output_29),
        ("Test Case 30", Test.test_input_30, Test.expected_output_30),
        ("Test Case 31", Test.test_input_31, Test.expected_output_31),
        ("Test Case 32", Test.test_input_32, Test.expected_output_32),
        ("Test Case 33", Test.test_input_33, Test.expected_output_33),
        ("Test Case 34", Test.test_input_34, Test.expected_output_34),
        ("Test Case 35", Test.test_input_35, Test.expected_output_35),
    ]

    # Run each test case
    for test_name, test_input, expected_output in test_cases:
        verifier.run_test(test_name, test_input, expected_output)
