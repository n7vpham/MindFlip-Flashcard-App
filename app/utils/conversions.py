import re

class FileConvert:
    
    # This way of handling files allows us to add other filetypes in the future
    @classmethod
    def handle_file(file, mimetype):
        """
        Args:
            file (string): The filepath of the file to convert
            mimetype: The file type
        Returns:
            list: a list of json like objects
        """
        conversions = {
            'text/markdown': convert_markdown,
            'text/x-markdown': convert_markdown,
        }

        converter = conversions.get(mimetype)
        if not converter:
            raise ValueError(f"Unsupported file type: {mimetype}")
        return converter(file)

    @classmethod
    def convert_markdown(md_file):
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
