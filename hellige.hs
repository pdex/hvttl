module Main(main) where

import Control.Monad
import Data.List
import Data.Maybe

-- note: numMatches * 2 must be an even multiple of numTeams
-- we also need: numMatches / numWeeks <= numTeams / 2
numTeams = 25
numWeeks = 20
numMatches = 175

matches week = (numMatches `div` numWeeks) +
  (if week <= numMatches `mod` numWeeks then 1 else 0)

type Team = Int
type Match = (Team, Team)
type Week = [Match]
type Schedule = [Week]

inWeek :: Team -> Week -> Bool
inWeek t = any $ \(x,y)-> x == t || y == t

matchEq a b p = p == (a,b) || p == (b,a)

played :: Team -> Team -> Schedule -> Bool
played x y = any.any $ matchEq x y

count :: Team -> Schedule -> Int
count t s = length $ s >>= (filter $ \(x,y)-> x == t || y == t)

done :: Team -> Schedule -> Bool
done t s = count t s == 2 * numMatches `div` numTeams

mtchs :: Schedule -> Week -> [Match]
mtchs s w = [(x,y) | x <- [1..numTeams],
                     not (inWeek x w || done x s),
                     y <- [x+1..numTeams], 
                     not (x == y || inWeek y w || played x y s || done y s)]

weeks :: Schedule -> Int -> Week -> [Week]
weeks s 0 w = return w
weeks s i w = do m <- mtchs s w
                 wk <- weeks s (i-1) (m:w)
                 return wk

scheds :: Int -> Schedule -> [Schedule]
scheds 0 s = return s
scheds i s = do w <- weeks s (matches i) []
                s <- scheds (i-1) (w:s)
                return s

search :: [Schedule]
search = scheds numWeeks []

schedule = listToMaybe search

main = case schedule of
         Nothing -> print "Nothing!" 
         Just s -> forM_ s print
