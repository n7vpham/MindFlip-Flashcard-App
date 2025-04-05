import re

class FileConvert:
    def md_to_flashcard_list(md_file):
        """Takes a markdown and and converts certain blocks into flashcards.
        Example of flashcard syntax in markdown:

        Front
        : Back

        The function reads the back of the card until it reaches an empty line.

        Args:
            md_file (string): The filepath to the markdown file to be converted.

        Returns:
            list: A list of json like objects, ready to be inserted in MongoDB.
        """
        flashcard_list = []
        with open(md_file, 'r') as file:
            prev_line = file.readline()
            for line in file:
                if re.search("^:", line):
                    front = prev_line
                    back = line[1:].lstrip()
                    for next_line in file:
                        prev_line = next_line
                        if next_line.strip() == "":
                            break
                        back += next_line
                    flashcard_list.append({
                        "front": front,
                        "back": back
                    })
                else:
                    prev_line = line
        
        return flashcard_list
                    


if __name__ == '__main__':
    print(FileConvert.md_to_flashcard_list('testmd.md'))
