#!/usr/bin/env
# -*- coding:utf-8 -*-

from __future__ import division
import math
import numpy as np

# http://en.wikipedia.org/wiki/Trilateration
# assuming elevation = 0
# length unit : km

earthR = 6371

class base_station(object):
    def __init__(self, lat, lon, dist):
        self.lat = lat
        self.lon = lon
        self.dist = dist

#using authalic sphere
#if using an ellipsoid this step is slightly different
#Convert geodetic Lat/Long to ECEF xyz
#   1. Convert Lat/Long to radians
#   2. Convert Lat/Long(radians) to ECEF  (Earth-Centered,Earth-Fixed)
def convert_geodetci_to_ecef(base_station):
    x = earthR *(math.cos(math.radians(base_station.lat)) * math.cos(math.radians(base_station.lon)))
    y = earthR *(math.cos(math.radians(base_station.lat)) * math.sin(math.radians(base_station.lon)))
    z = earthR *(math.sin(math.radians(base_station.lat)))
    print x, y, z
    return np.array([x, y, z])

def calculate_trilateration_point_ecef(base_station_list):
    P1, P2, P3 = map(convert_geodetci_to_ecef, base_station_list)
    DistA, DistB, DistC = map(lambda x: x.dist, base_station_list)

    #vector transformation: circle 1 at origin, circle 2 on x axis
    ex = (P2 - P1)/(np.linalg.norm(P2 - P1))
    i = np.dot(ex, P3 - P1)
    ey = (P3 - P1 - i*ex)/(np.linalg.norm(P3 - P1 - i*ex))
    ez = np.cross(ex,ey)
    d = np.linalg.norm(P2 - P1)
    j = np.dot(ey, P3 - P1)

    #plug and chug using above values
    x = (pow(DistA,2) - pow(DistB,2) + pow(d,2))/(2*d)
    y = ((pow(DistA,2) - pow(DistC,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)

    # only one case shown here
    z = np.sqrt(pow(DistA,2) - pow(x,2) - pow(y,2))

    #triPt is an array with ECEF x,y,z of trilateration point
    triPt = P1 + x*ex + y*ey + z*ez

    #convert back to lat/long from ECEF
    #convert to degrees
    lat = math.degrees(math.asin(triPt[2] / earthR))
    lon = math.degrees(math.atan2(triPt[1],triPt[0]))
    return lat, lon

if __name__ == '__main__' :
    baseA = base_station(31.257474, 121.620974, 0.228)
    baseB = base_station(31.260217, 121.621095, 0.123)
    baseC = base_station(31.259148, 121.623835, 0.187)
    base_station_list = [baseA, baseB, baseC]
    lat, lon = calculate_trilateration_point_ecef(base_station_list)
    print  repr(lon) + "," + repr(lat)
