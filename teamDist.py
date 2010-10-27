#!/usr/bin/python

import operator
import itertools

class Team:
    def __init__(self, num, name):
        self.num = num
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

class Match:
    def __init__(self, home, away):
        self.home = home
        self.away = away
    def __str__(self):
        return "%s vs %s" %(self.home.name, self.away.name)
    def __eq__(self, other):
        if (( self.home.num == other.home.num or self.home.num == other.away.num ) and
           ( self.away.num == other.away.num or self.away.num == other.home.num )):
            return True
        return False

class GameDay:
    def __init__(self):
        self.matches = []
    def add(self, match):
        self.matches.append(match)
    def full(self):
        return len(self.matches) >= self.limit
    def __getitem__(self, key):
        if key >= len(self.matches):
            return ""
        #print key, len(self.matches)
        return self.matches[key]
    def __contains__(self, team):
        for match in self.matches:
            if match.away.num == team.num:
                return True
            if match.home.num == team.num:
                return True
        return False
class Sunday(GameDay):
    limit = 5
class Tuesday(GameDay):
    limit = 4

class Week:
    def __init__(self, num, sunday, tuesday):
        self.num = num
        self.sunday = sunday
        self.tuesday = tuesday
    def add(self, match):
        if not self.sunday.full():
            self.sunday.add(match)
        else:
            self.tuesday.add(match)
    def full(self):
        return self.sunday.full() and self.tuesday.full()
    def __str__(self):
        lines = list()
        lines.append("Week%02d %20s %20s" % (self.num, "Sunday", "Tuesday"))
        lines.extend([ "      %20s %20s" % ( self.sunday[i], self.tuesday[i] ) for i in range(5) ])
        return "\n".join(lines)
    def __contains__(self, team):
        if team in self.sunday:
            return True
        elif team in self.tuesday:
            return True
        return False

class League:
    def __init__(self):
        self.nextWeek = 1
        self.weeks = []
        self.addWeek()
        self.allMatches = []
    def addWeek(self):
        self.weeks.append( Week( self.nextWeek, Sunday(), Tuesday() ) )
        self.nextWeek += 1
        return self.weeks[-1]
    def canPlay(self, team):
        thisWeek = self.weeks[-1]
        if team in thisWeek:
            return False
        return True
    def matchExists(self, match):
        return match in self.allMatches
    def add(self, match):
        week = self.weeks[-1]
        if week.full():
            week = self.addWeek()
        week.add( match )
        self.allMatches.append( match )
    def full(self):
        return len(self.weeks) == 20 and self.weeks[-1].full()
    def __str__(self):
        return "\n".join(map(str, self.weeks))

factorial=lambda x: reduce(operator.mul, range(2,x+1), 1)
def countCombinations(length, choose):
   return factorial(length) / (factorial(choose) * factorial(length - choose))

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n-r, -1)
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

def makeTeams():
    return [ Team( i-1, "Team%02d" % i ) for i in range(1,26) ]


def graphy():
    teams = makeTeams()
    league = League()
    homeTeams = itertools.cycle(teams)
    awayTeams = itertools.cycle(teams)
    for homeTeam in homeTeams:
        if league.canPlay(homeTeam):
            for awayTeam in awayTeams:
                if homeTeam.num == awayTeam.num:
                    continue
                match = Match( homeTeam, awayTeam )
                if league.canPlay(awayTeam) and not league.matchExists( match ):
                    print homeTeam, awayTeam
                    #league.add( Match( homeTeam, awayTeam ) )
                    league.add( match )
                    break
        if league.full():
            break
    return league

if __name__ == '__main__':
    import sys
    import random
    teams = makeTeams()
    #for team in teams:
    #    print "%s" % team
    print countCombinations(25, 2)
    #combos = dict()
    #allPossible = list( combinations(teams, 2) )
    #random.shuffle(allPossible)
    #for match in allPossible[:9]:
    #    print match
    league = graphy()
    print league
    """
    for combo in permutations( combinations( teams, 2 ), 2 ):
        print combo
    """
    """
    i = 0
    for combo in combinations(teams, 2):
        if i % 2 == 0:
            matches = combos.setdefault(combo[0], [])
            matches.append(combo)
        else:
            matches = combos.setdefault(combo[1], [])
            matches.append(tuple(reversed(combo)))
        i += 1

    for key in sorted(combos.keys()):
        print key, key.num, len(combos[key])
        print key, "\n\t".join(map(str, combos[key]))
    sys.exit(0)

    for key in sorted(combos.keys()):
        if key.num % 2 == 1:
            combos[key].reverse()
        print key, key.num, len(combos[key])
        print key, "\n\t".join(map(str, combos[key]))
    for i in range(12):
        for team in teams[:-1]:
            if league.full():
                break
            combo = combos[team][i]
            #print combo
            league.add( Match( combo[0], combo[1] ) )
            #print team, combos[team][i]
    #print combos
    print league
    """

    """
    home = None
    away = None
    league = League()
    while not league.full():
        for i in range(len(teams)):
            if i % 2 == 0:
                home = teams[i]
            if i % 2 == 1:
                away = teams[i]
            if home != None and away != None:
                match = Match(home, away)
                league.add(match)
                home = None
                away = None
    """
