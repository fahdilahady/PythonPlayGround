def find_word (wordsearch, word):
    """Trys to find word in wordsearch"""
    # Store first character positions in array
    start_pos = []
    first_char = word[0]
    for i in range(0, len(wordsearch)):
        for j in range(0, len(wordsearch[i])):
            if (wordsearch[i][j] == first_char):
                start_pos.append([i,j])

    # Check all starting positions for word
    wordsFound = 0
    for p in start_pos:
        wordsFound += check_start(wordsearch, word, p)

    return wordsFound


def check_start (wordsearch, word, start_pos):
    """Checks if the word starts at the startPos. Returns True if word found"""
    directions = [[-1,1], [0,1], [1,1], [-1,0], [1,0], [-1,-1], [0,-1], [1,-1]]
    # Iterate through all directions and check each for the word
    wordsFound = 0
    for d in directions:
        if (check_dir(wordsearch, word, start_pos, d)):
            wordsFound +=1
    return wordsFound

def check_dir (wordsearch, word, start_pos, dir):
    """Checks if the word is in a direction dir from the start_pos position in the wordsearch. Returns True and prints result if word found"""
    found_chars = [word[0]] # Characters found in direction. Already found the first character
    current_pos = start_pos # Position we are looking at
    pos = [start_pos] # Positions we have looked at
    while (chars_match(found_chars, word)):
        if (len(found_chars) == len(word)):
            return True
        # Have not found enough letters so look at the next one
        current_pos = [current_pos[0] + dir[0], current_pos[1] + dir[1]]
        pos.append(current_pos)
        if (is_valid_index(wordsearch, current_pos[0], current_pos[1])):
            found_chars.append(wordsearch[current_pos[0]][current_pos[1]])
        else:
            # Reached edge of wordsearch and not found word
            return

def chars_match (found, word):
    """Checks if the leters found are the start of the word we are looking for"""
    index = 0
    for i in found:
        if (i != word[index]):
            return False
        index += 1
    return True

def is_valid_index (wordsearch, line_num, col_num):
    """Checks if the provided line number and column number are valid"""
    if ((line_num >= 0) and (line_num < len(wordsearch))):
        if ((col_num >= 0) and (col_num < len(wordsearch[line_num]))):
            return True
    return False

if __name__ == "__main__":
    isFromFile = False
    isExpectOutFile = False
    if (input('is the test cases read from a file? y/n: ').lower() == 'y'):
        isFromFile = True
        _file = input('select the testcase file? (in ext) ')
        isExpectOutFile = input('would you mind to save the result? y/n: ').lower() == 'y'
        _outFile = 'wordsearch' + '/' +_file + 'testResult.log'
        testFile = open('wordsearch' + '/'+_file).read().splitlines()

    testCaseNb = int(testFile.pop(0)) if isFromFile else int(input())
    
    result = list()
    for i in range(testCaseNb):
        rawLen = int(testFile.pop(0)) if isFromFile else int(input())
        columnLen = int(testFile.pop(0)) if isFromFile else int(input())
        wordMatrix = list()

        for r in range(rawLen):
            wordMatrix.append(str(testFile.pop(0)) if isFromFile else input())
        
        wordToFind = str(testFile.pop(0)) if isFromFile else input()
        foundWord = find_word(wordMatrix, wordToFind)
        toPrint = 'Case {0}: {1}'.format(i+1, foundWord)
        result.append(toPrint)
    
    if isExpectOutFile:
        open(_outFile, 'w').close()
        f = open(_outFile, 'a')
        for res in result:
            f.write(res + "\n")
        
        f.close()
    else:
        for res in result:
            print(res)

    
        