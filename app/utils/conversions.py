import re

class FileConvert:
    def md_to_flashcard_list(md_file):
        flashcard_list = []
        with open(md_file, 'r') as file:
            prevLine = file.readline()
            for line in file:
                if re.search("^:", line):
                    front = prevLine
                    back = line[1:].lstrip()
                    for next_line in file:
                        prevLine = next_line
                        if next_line.strip() == "":
                            break
                        back += next_line
                    flashcard_list.append({
                        "front": front,
                        "back": back
                    })
                else:
                    prevLine = line
        
        return flashcard_list
                    


if __name__ == '__main__':
    print(FileConvert.md_to_flashcard_list('testmd.md'))
