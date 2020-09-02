maps = list()

        
def calculateKingdomRegions():
    startPos = list()
    
    for y in range(len(maps)):
        for x in range(len(maps[y])):
            if not(maps[y][x]== '#' or maps[y][x] =='.'):
                kingdomName = maps[y][x]
                startPos.append((y,x, kingdomName))
    print(startPos)
    foundFreeKingdom, checkedKingdom, contestedKingdom = [],[],[]
    for p in startPos:
        if p not in checkedKingdom:
            _foundFreeKingdom, _checkedKingdom, _contestedKingdom = checkRegion( p)
            if len(_foundFreeKingdom)>0:
                foundFreeKingdom.extend(_foundFreeKingdom)
                foundFreeKingdom = list(set(foundFreeKingdom))
            if len(_checkedKingdom)>0:
                checkedKingdom.extend(_checkedKingdom)
                checkedKingdom =list(set(checkedKingdom))
            if len(_contestedKingdom)>0:
                contestedKingdom.extend(_contestedKingdom)
                contestedKingdom = list(set(contestedKingdom))
    
    return foundFreeKingdom, contestedKingdom

def checkRegion(kingdomPos, excludeVertical = False):
    directions = [[0,1],[0,-1]] if excludeVertical else [[0,1],[0,-1], [-1,0], [1,0]]
    foundFreeKingdom, checkedKingdom, contestedKingdom = [],[],[]
    for d in directions:
        _foundFreeKingdom, _checkedKingdom, _contestedKingdom = checkDirection(kingdomPos,d)
        if len(_foundFreeKingdom)>0:
            foundFreeKingdom.extend(_foundFreeKingdom)
        if len(_checkedKingdom)>0:
            checkedKingdom.extend(_checkedKingdom)
        if len(_contestedKingdom)>0:
            contestedKingdom.extend(_contestedKingdom)
        
    return list(set(foundFreeKingdom)), list(set(checkedKingdom)), list(set(contestedKingdom))

def checkDirection(kingdomPos, dir):
    isVertical = dir == [-1,0] or dir == [1,0]
    mountain = '#'
    emptyRegion = '.'
    curLandUse = kingdomPos[2]
    curPos = [kingdomPos[0],kingdomPos[1]]
    kingdomName = kingdomPos[2]

    contestedKingdom = list()
    foundFreeKingdom = list()
    checkedKingdom = list()

    checkedKingdom.append(kingdomPos)
    foundFreeKingdom.append(kingdomPos)
    while(curLandUse is not mountain):

        curPos = [curPos[0]+ dir[0],curPos[1]+dir[1]]
        curLandUse = maps[curPos[0]][curPos[1]] if is_valid_index(maps, curPos[0],curPos[1]) else mountain

        if curLandUse == kingdomName:
            checkedKingdom.append((curPos[0], curPos[1], curLandUse))
        elif curLandUse != kingdomName and not (curLandUse is mountain or curLandUse is emptyRegion):
            """There is another kingdom in the current region"""
            foundFreeKingdom.remove(kingdomPos)
            contestedKingdom.append(kingdomPos)
            checkedKingdom.append((curPos[0], curPos[1], curLandUse))
        elif curLandUse is emptyRegion:
            """Update the empty Landuse as it ruled by current kingdom"""
            if isVertical:
                toUpdate = maps.pop(curPos[0])
                toUpdate = toUpdate[0:curPos[1]-1] + str(kingdomName) + toUpdate[curPos[1]:]
                maps.insert(curPos[0], toUpdate)
        else:
            """ignore mountain"""
    return foundFreeKingdom, checkedKingdom, contestedKingdom

def is_valid_index (maps, line_num, col_num):
    """Checks if the provided line number and column number are valid"""
    if ((line_num >= 0) and (line_num < len(maps))):
        if ((col_num >= 0) and (col_num < len(maps[line_num]))):
            return True
    return False

if __name__ == "__main__":
    tcs = int(input())
    foundFreeKingdom, contestedKingdom = [],[]

    for tc in range(tcs):
        yLen = int(input())
        xLen = int(input())

        for y in range(yLen):
            maps.append(input())
        
        foundFreeKingdom, contestedKingdom = calculateKingdomRegions()
        maps.clear()
        print('Case {0}:'.format(tc+1))
        print(foundFreeKingdom)
        shortedKingdom = dict()
        for kingdom in foundFreeKingdom:
            shortedKingdom[kingdom[2]]= shortedKingdom[kingdom[2]] + 1 if kingdom[2] in shortedKingdom else 1

        for el in shortedKingdom:
            print("{0} {1}".format(el, shortedKingdom[el]))
        
        print("contested {0}".format(len(contestedKingdom)))
        
