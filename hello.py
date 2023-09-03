import re

def replace(text):
    word_counting = 0
    words = text.split()
    for i in range(len(words)):
        if words[i] == "terrible":
            word_counting += 1
            if word_counting % 2 == 0:
                words[i] = "pathetic"
            else:
                words[i] = "marvellous"
        if words[i] == "terrible!":
            words[i] = "marvellous!"

    Done_text = ' '.join(words)
    return Done_text, word_counting


def main():

    f = open("file_to_read.txt", "r",encoding='UTF-8')
    print("Terribe appeared %d times" % len(re.findall('terrible',f.read())))
    f.close()

    with open("file_to_read.txt", "r") as file:
        text = file.read()
    Done_text, word_counting = replace(text)
    
    with open("result.txt", "w") as file:
        file.write(Done_text)
    
    print("Done!")


if __name__ == "__main__":
    main()
