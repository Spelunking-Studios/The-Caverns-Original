import pygame
import math

def angle_between(vec_1, vec_2):
    return (vec_1.dot(vec_2))/(vec_1.length()*vec_2.length())

def distance(tup1, tup2):
    return math.sqrt((tup1[0]-tup2[0])**2 + (tup1[1]-tup2[1])**2)


def distance_squared(tup1, tup2):
    return (tup1[0]-tup2[0])**2 + (tup1[1]-tup2[1])**2
