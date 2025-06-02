from rapidfuzz import fuzz
import re


class RefineColumn:
    def __init__(self, col_value: str, course_codes_names_map: dict, section: str, group: int):
        self.col_value = col_value
        self.section = section
        self.group = group
        self.course_codes_pattern = list(set(course_codes_names_map.keys()))
        self.course_names_pattern = list(set(course_codes_names_map.values()))
        self.course_codes_names_map = course_codes_names_map

    def fuzzy_match_course_code(self, input_str, threshold=95):
        input_strs = input_str.strip().split('\n')

        for input_str in input_strs:
            for code in self.course_codes_pattern:
                score = fuzz.ratio(input_str, code)
                if score >= threshold:
                    return code

        return None

    def fuzzy_match_course_name(self, input_str, threshold=60):
        for course in self.course_names_pattern:
            score = fuzz.partial_ratio(course.lower(), input_str.lower())
            if score >= threshold:
                return course

        return None

    def extract_course_codes_from_raw_text_regex(self, text: str) -> str:
        return self.fuzzy_match_course_code(text)

    def extract_course_names_from_raw_text_regex(self, text):
        course_name = self.fuzzy_match_course_name(text)

        if course_name is None:
            return None

        # Use a reverse lookup dictionary for efficiency
        if not hasattr(self, '_name_to_code'):
            self._name_to_code = {v: k for k,
                                  v in self.course_codes_names_map.items()}
        return self._name_to_code.get(course_name)

    def extract_class_blocks(self, text: str):
        # Normalize line breaks and clean up the text
        text = text.strip().replace('\r\n', '\n').replace('\r', '\n')

        # Split by double newlines or more to separate potential blocks
        # Then filter out empty strings
        potential_blocks = [block.strip()
                            for block in re.split(r'\n\s*\n', text) if block.strip()]

        # If no clear separation, try to identify blocks by subject code pattern
        if len(potential_blocks) == 1:
            # Look for subject codes that start new blocks
            subject_pattern = r'^[A-Z]{3,5}\d{3,6}\s?\(?[TP]?\)?'
            lines = text.split('\n')

            blocks = []
            current_block = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Check if this line starts a new block (subject code at the beginning)
                if re.match(subject_pattern, line) and current_block:
                    # Save previous block
                    blocks.append('\n'.join(current_block))
                    current_block = [line]
                else:
                    current_block.append(line)

            # Don't forget the last block
            if current_block:
                blocks.append('\n'.join(current_block))

            return blocks

    def extract_groups_list(self, col_value: str, threshold=80) -> list:
        candidates = re.findall(
            r'\(?\bgr?\s*\.?\s*[a-zA-Z]\s*\d+\)?', col_value, flags=re.IGNORECASE)

        matches = []

        for candidate in candidates:
            cleaned = re.sub(r'[^A-Za-z0-9.]', '', candidate).lower()
            score = fuzz.ratio(
                cleaned, f"gr.{self.section.lower()}{self.group}")

            if score >= threshold:
                number_match = re.search(r'(\d+)', cleaned)
                if number_match:
                    matches.append(number_match.group(1))

        return matches

    def refine(self) -> str:
        if len(self.col_value) == 0:
            return None

        actual_course_code = None
        list_of_groups = self.extract_groups_list(self.col_value)

        if len(list_of_groups) == 0:
            actual_course_code = self.extract_course_codes_from_raw_text_regex(
                self.col_value)

            if actual_course_code is None:
                actual_course_code = self.extract_course_names_from_raw_text_regex(
                    self.col_value)
        else:
            list_of_all_classes: list[str] = self.extract_class_blocks(
                self.col_value)

            my_group_index = list_of_groups.index(
                str(self.group)) if str(self.group) in list_of_groups else -1

            if my_group_index == -1:
                return None

            my_classes = list_of_all_classes[my_group_index]

            actual_course_code = self.extract_course_codes_from_raw_text_regex(
                my_classes)

            if actual_course_code is None:
                actual_course_code = self.extract_course_names_from_raw_text_regex(
                    my_classes)

        return actual_course_code
