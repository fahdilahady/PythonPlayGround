from bisect import bisect_left

mountain = '#'
emptyRegion = '.'
directions = [[0,1],[0,-1], [-1,0], [1,0]]
maps = None
factory = None

class Region(object):
    def __del__(self):
        self.myKingdom = None
        del self.myKingdomArea
        for area in self.myArea:
            del area    
        del self.myArea

    def __init__(self, area, kingdom = None):
        self.myArea = list()
        self.myArea.append(area)
        self.myKingdomArea = area
        self.myKingdom = kingdom
        self.myContestedRegion = None
    
    def appendArea(self, area):
        if not self.isInMyArea(area):
            self.myArea.append(area)
            self.myArea = list(set(self.myArea))
            self.myArea.sort(key = lambda k:k[0]) #sort by y pos
        pass

    def binary_search(self, a, x, lo=0, hi=None):  # can't use a to specify default for hi
        hi = hi if hi is not None else len(a)  # hi defaults to len(a)   
        pos = bisect_left(a, x, lo, hi)  # find insertion position
        return pos if pos != hi and a[pos] == x else -1  # don't walk off the end

    def isInMyArea(self, thisArea):
        #return self.binary_search(self.myArea, thisArea) != -1
        return thisArea in self.myArea
    
    def expandMyArea(self, startPos= None):
        for d in directions:
            self.checkDirection(d, startPos)

    def getNextArea(self, CurArea, direction):
        return CurArea[0]+ direction[0], CurArea[1] + direction[1]

    def checkDirection(self,d, startPos = None):
        if self.myContestedRegion is not None:
            return

        nPoint = self.getNextArea(startPos if startPos is not None else self.myKingdomArea, d)
        if not self.is_valid_index(nPoint[0], nPoint[1])or self.isInMyArea(nPoint):
            return

        area = maps[nPoint[0]][nPoint[1]]
        kName = self.myKingdom.Name
        if area == kName:
            areaTarget = self.myKingdom.getRegion(nPoint)
            self.myKingdom.mergeRegion(areaTarget, self) 
        elif area !=kName and not (area is mountain or area is  emptyRegion):
            self.myKingdom.setMyContestArena(self, nPoint, area)
            self.appendArea(nPoint)
            if not self.myKingdom.hasConflictArea():
                factory.contestNb +=1 
                self.myKingdom.myConflictAreaNb+=1
            
        elif area is mountain:
            return
        else:
            self.appendArea(nPoint)
        self.expandMyArea(nPoint)

    def is_valid_index (self, line_num, col_num):
        """Checks if the provided line number and column number are valid"""
        if ((line_num >= 0) and (line_num < len(maps))):
            if ((col_num >= 0) and (col_num < len(maps[line_num]))):
                return True
        return False    

class Kingdom(object):
    def __del__(self):
        for reg in self.myRegions:
            del reg

    def __init__(self,area, KingdomName = None):
        self.Name = KingdomName
        self.myRegions = list()
        self.myRegions.append(Region(area, self))
        self.myConflictAreaNb = 0

    def hasConflictArea(self):
        if self.myConflictAreaNb >0:
            return True
        for region in self.myRegions:
            if region.myContestedRegion is not None:
                return True

    def mergeRegion(self, thisRegion, toRegion):
        toRegion.myArea.extend(thisRegion.myArea)
        toRegion.myArea = list(set(toRegion.myArea))
        # for area in thisRegion.myArea:
        #     toRegion.appendArea(area)
        self.myRegions.remove(thisRegion)
        
        thisRegion =None

    def getRegion(self, area):
        for reg in self.myRegions:
            if reg.isInMyArea(area):
                return reg
        reg = Region(area, self)
        self.myRegions.append(reg)
        return reg 
        
    def setMyContestArena(self, conflictRegion, point, landuse):
        neighboardKingdom = factory.getKindomByName(landuse)
        neighboardRegion  = neighboardKingdom.getRegion(point)
        conflictRegion.myContestedRegion = neighboardRegion
        neighboardRegion.myContestedRegion = conflictRegion
        if conflictRegion in self.myRegions:
            self.myRegions.remove(conflictRegion)
        
        if neighboardRegion in neighboardKingdom.myRegions:
            neighboardKingdom.myRegions.remove(neighboardRegion)
        
    def appendArea(self, area):
        reg = self.getRegion(area)
        reg.appendArea(area)
        
    def claimByKingdom(self, KingdomName):
        self.Name = KingdomName
    
    def isInMyArea(self, thisArea):
        for reg in self.myRegions:
            if reg.isInMyArea(thisArea): 
                return True
        return False
    
    def expandMyArea(self):
        for reg in self.myRegions:
            reg.expandMyArea()

class factoryKingdom(object):
    def __init__(self):
        self.myKingdoms = list()
        self.contestNb = 0
    
    def __del__(self):
        # for kingdom in self.myKingdoms:
        #     del kingdom
        del self.myKingdoms

    def appendThisAreaToRelatedKingdom(self, area, KingdomName = None):
        return self.getKingdomOfThisArea(area, KingdomName)

    def getKindomByName(self, kingdomName):
        for kingdom in self.myKingdoms:
            if kingdomName == kingdom.Name:
                return kingdom
        return None

    def getKingdomOfThisArea(self, area, kingdomName = None):
        for kingdom in self.myKingdoms:
                if kingdom.isInMyArea(area):
                    return kingdom
                elif kingdom.Name == kingdomName:
                    kingdom.appendArea(area)
                    return kingdom
        
        kingdom = Kingdom(area, kingdomName)
        self.myKingdoms.append(kingdom)
        return kingdom
    
    def expandKingdoms(self):
        for kingdom in self.myKingdoms:
            if not kingdom.hasConflictArea():
                kingdom.expandMyArea()
    
    def sortMyKingdomList(self):
        self.myKingdoms = sorted(self.myKingdoms, key=lambda kingdom: kingdom.Name)


def calculateKingdom():
    for y in range(len(maps)):
        for x in range(len(maps[y])):
            if not(maps[y][x]== '#' or maps[y][x] =='.'):
                kingdomName = maps[y][x]
                factory.appendThisAreaToRelatedKingdom((y,x), kingdomName)
    
    factory.expandKingdoms()
    factory.sortMyKingdomList()

if __name__ == "__main__":
    tcs = int(input())
    
    for tc in range(tcs):
        yLen = int(input())
        xLen = int(input())
        maps = list()
        for y in range(yLen):
            maps.append(input())
        
        factory = factoryKingdom()
        calculateKingdom()

        print('Case {0}:'.format(tc+1))
        for kingdom in factory.myKingdoms:
            if len(kingdom.myRegions) > 0:
                print("{0} {1}".format(kingdom.Name, len(kingdom.myRegions)))
        
        print("contested {0}".format(factory.contestNb))
        del factory
        del maps