# Importing the List type from the typing module for type hinting.
# This allows us to specify that certain variables or return values are lists.
from typing import List

# Importing the fuzz module from the rapidfuzz library.
# This module provides functions for fuzzy string matching, which is used to compare strings based on similarity.
from rapidfuzz import fuzz

# Importing the re module for regular expressions.
# Regular expressions are used for pattern matching and text manipulation.
import re


# Defining a class named RefineColumn.
# This class encapsulates methods and attributes for processing and refining column data.
class RefineColumn:
    # The constructor method initializes an instance of the RefineColumn class.
    # It takes several parameters:
    # - col_value: The raw column value (string) to be processed.
    # - course_codes_names_map: A dictionary mapping course codes to course names.
    # - section: The section identifier (string) for the class.
    # - group: The group number (integer) for the class.
    def __init__(self, col_value: str, course_codes_names_map: dict, section: str, group: int):
        # Storing the raw column value in an instance variable for later use.
        self.col_value = col_value
        # Storing the section identifier in an instance variable.
        self.section = section
        # Storing the group number in an instance variable.
        self.group = group
        # Extracting the unique course codes from the dictionary keys and storing them as a list.
        # This is used for pattern matching later.
        self.course_codes_pattern = list(set(course_codes_names_map.keys()))
        # Extracting the unique course names from the dictionary values and storing them as a list.
        # This is also used for pattern matching later.
        self.course_names_pattern = list(set(course_codes_names_map.values()))
        # Storing the course codes-to-names mapping dictionary in an instance variable.
        self.course_codes_names_map = course_codes_names_map

    # Defining a method to perform fuzzy matching on course codes.
    # This method takes an input string and a threshold value (default is 95).
    def fuzzy_match_course_code(self, input_str, threshold=95):
        # Splitting the input string into multiple lines based on newline characters.
        # This allows us to process each line separately.
        input_strs = input_str.strip().split('\n')

        # Iterating over each line in the input string.
        for input_str in input_strs:
            # Iterating over each course code in the course codes pattern list.
            for code in self.course_codes_pattern:
                # Calculating the similarity score between the input string and the course code using fuzz.ratio.
                # fuzz.ratio computes the similarity between two strings as a percentage.
                score = fuzz.ratio(input_str, code)
                # If the similarity score meets or exceeds the threshold, return the matching course code.
                if score >= threshold:
                    return code

        # If no match is found, return None.
        return None

    # Defining a method to perform fuzzy matching on course names.
    # This method takes an input string and a threshold value (default is 60).
    def fuzzy_match_course_name(self, input_str, threshold=60):
        # Iterating over each course name in the course names pattern list.
        for course in self.course_names_pattern:
            # Calculating the similarity score between the input string and the course name using fuzz.partial_ratio.
            # fuzz.partial_ratio computes the similarity between substrings of two strings.
            score = fuzz.partial_ratio(course.lower(), input_str.lower())
            # If the similarity score meets or exceeds the threshold, return the matching course name.
            if score >= threshold:
                return course

        # If no match is found, return None.
        return None

    # Defining a method to extract course codes from raw text using regular expressions.
    # This method takes a text string as input.
    def extract_course_codes_from_raw_text_regex(self, text: str):
        # Calling the fuzzy_match_course_code method to find a matching course code in the text.
        return self.fuzzy_match_course_code(text)

    # Defining a method to extract course names from raw text using regular expressions.
    # This method takes a text string as input.
    def extract_course_names_from_raw_text_regex(self, text):
        # Calling the fuzzy_match_course_name method to find a matching course name in the text.
        course_name = self.fuzzy_match_course_name(text)

        # If no course name is found, return None.
        if course_name is None:
            return None

        # Checking if a reverse lookup dictionary (_name_to_code) exists as an instance attribute.
        # If not, create one by reversing the course_codes_names_map dictionary.
        if not hasattr(self, '_name_to_code'):
            self._name_to_code = {v: k for k,
                                  v in self.course_codes_names_map.items()}
        # Using the reverse lookup dictionary to find the course code corresponding to the course name.
        return self._name_to_code.get(course_name)

    # Defining a method to extract class blocks from a text string.
    # This method takes a text string as input and returns a list of class blocks.
    def extract_class_blocks(self, text: str) -> List[str]:
        # Normalizing line breaks in the text by replacing different newline formats with a single format.
        text = text.strip().replace('\r\n', '\n').replace('\r', '\n')

        # Splitting the text into potential blocks based on double newlines or more.
        # Filtering out empty strings to ensure only meaningful blocks are retained.
        potential_blocks = [block.strip()
                            for block in re.split(r'\n\s*\n', text) if block.strip()]

        # If there is only one potential block, attempt to identify blocks based on a subject code pattern.
        if len(potential_blocks) == 1:
            # Defining a regular expression pattern to match subject codes.
            # Subject codes typically consist of uppercase letters followed by numbers, optionally with additional characters.
            subject_pattern = r'^[A-Z]{3,5}\d{3,6}\s?\(?[TP]?\)?'
            # Splitting the text into individual lines for processing.
            lines = text.split('\n')

            # Initializing an empty list to store identified blocks.
            blocks = []
            # Initializing an empty list to store the current block being processed.
            current_block = []

            # Iterating over each line in the text.
            for line in lines:
                # Stripping whitespace from the line.
                line = line.strip()
                # If the line is empty, skip it.
                if not line:
                    continue

                # If the line matches the subject code pattern and there is an existing block,
                # append the current block to the blocks list and start a new block with the current line.
                if re.match(subject_pattern, line) and current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = [line]
                else:
                    # Otherwise, add the line to the current block.
                    current_block.append(line)

            # If there is a remaining block after processing all lines, append it to the blocks list.
            if current_block:
                blocks.append('\n'.join(current_block))

            # Return the identified blocks if any, otherwise return an empty list.
            return blocks if blocks else []

        # If there is not exactly one potential block, return an empty list.
        return []

    # Defining a method to extract a list of groups from the column value.
    # This method takes the column value and a threshold value (default is 80) as input.
    def extract_groups_list(self, col_value: str, threshold=80) -> list:
        # Using a regular expression to find all potential group identifiers in the column value.
        # Group identifiers typically consist of "gr" followed by a section and group number.
        candidates = re.findall(
            r'\(?\bgr?\s*\.?\s*[a-zA-Z]\s*\d+\)?', col_value, flags=re.IGNORECASE)

        # Initializing an empty list to store matching group numbers.
        matches = []

        # Iterating over each candidate group identifier.
        for candidate in candidates:
            # Cleaning the candidate by removing non-alphanumeric characters and converting it to lowercase.
            cleaned = re.sub(r'[^A-Za-z0-9.]', '', candidate).lower()
            # Calculating the similarity score between the cleaned candidate and the expected group identifier.
            score = fuzz.ratio(
                cleaned, f"gr.{self.section.lower()}{self.group}")

            # If the similarity score meets or exceeds the threshold, extract the group number from the candidate.
            if score >= threshold:
                number_match = re.search(r'(\d+)', cleaned)
                if number_match:
                    matches.append(number_match.group(1))

        # Return the list of matching group numbers.
        return matches

    # Defining a method to refine the column value and extract the actual course code.
    # This method returns the course code or None if no match is found.
    def refine(self) -> str | None:
        # If the column value is empty, return None.
        if len(self.col_value) == 0:
            return None

        # Initializing a variable to store the actual course code.
        actual_course_code = None
        # Extracting a list of groups from the column value.
        list_of_groups = self.extract_groups_list(self.col_value)

        # If no groups are found, attempt to extract the course code directly from the column value.
        if len(list_of_groups) == 0:
            actual_course_code = self.extract_course_codes_from_raw_text_regex(
                self.col_value)

            # If no course code is found, attempt to extract the course name and map it to a course code.
            if actual_course_code is None:
                actual_course_code = self.extract_course_names_from_raw_text_regex(
                    self.col_value)
        else:
            # If groups are found, extract all class blocks from the column value.
            list_of_all_classes: List[str] = self.extract_class_blocks(
                self.col_value)

            # Find the index of the current group in the list of groups.
            my_group_index = list_of_groups.index(
                str(self.group)) if str(self.group) in list_of_groups else -1

            # If the current group is not found, return None.
            if my_group_index == -1:
                return None

            # Extract the class block corresponding to the current group.
            my_classes = list_of_all_classes[my_group_index]

            # Attempt to extract the course code from the class block.
            actual_course_code = self.extract_course_codes_from_raw_text_regex(
                my_classes)

            # If no course code is found, attempt to extract the course name and map it to a course code.
            if actual_course_code is None:
                actual_course_code = self.extract_course_names_from_raw_text_regex(
                    my_classes)

        # Return the actual course code or None if no match is found.
        return actual_course_code
