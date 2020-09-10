#
#
#   Sunrise And Sunset Calculator
#   (C)Copyright 2020 Team-RYOUN
# 
#   MIT Licence:
#   Copyright © 2020 Team-RYOUN
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#   The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#   THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
import math

PI = 3.141592653589793
h = -0.833333333
leapYear=[31,29,31,30,31,30,31,31,30,31,30,31]
commonYear=[31,28,31,30,31,30,31,31,30,31,30,31]

def leap_year(year:int):
    if((year%400==0)or(year % 100 != 0) and (year%4==0)):
        return 1
    else:
        return 0
#Determine whether it is a leap year: if it is a leap year, return 1; if it is not a leap year, return 0

def days(year:int,month:int,date:int):
    i:int = 2000
    a:int = 0
    while(i < year):
        if(leap_year(i)):
            a+=366
        else:
            a+=365
        i+=1
    
    if(leap_year(year)):
        i = 0
        while(i < month-1):
            a+=leapYear[i]
            i+=1
    else:
        i = 0
        while(i < month-1):
            a+=commonYear[i]
            i+=1


    a+=date
    return a
#Calculate the number of days from Greenwich Mean Time on January 1, 2000 to the calculation date 
   
def t_century(days:int,UTo:float):
    return float((float(days)+UTo/360)/36525)
#Calculate the number of centuries t from January 1, 2000 to the calculation date in Greenwich Mean Time

def L_sun(t_century:float):
    return float(280.460+36000.770*t_century) 
#Calculate the sun's eclipse

def G_sun(t_century:float):
    return float(357.528+35999.050*t_century)
#Calculate the mean anomaly of the sun

def ecliptic_longitude(L_sun:float,G_sun:float):
    return float(L_sun+1.915*math.sin(G_sun*PI/180)+0.02*math.sin(2*G_sun*PI/180))
#Calculate the ecliptic longitude
def earth_tilt(t_century:float):
    return float(23.4393-0.0130*t_century)
#Calculate the inclination of the earth

def sun_deviation(earth_tilt:float,ecliptic_longitude:float):
    return float(180/PI*math.asin(math.sin(PI/180*earth_tilt)*math.sin(PI/180*ecliptic_longitude)))
#Calculate The Solar deviation

def GHA(UTo:float,G_sun:float,ecliptic_longitude:float):
    return float(
        UTo-180-1.915*math.sin(
            G_sun*PI/180
        )-0.02*math.sin(
            2*G_sun*PI/180
        )+2.466*math.sin(
            2*ecliptic_longitude*PI/180
            )-0.053*math.sin(4*ecliptic_longitude*PI/180))
#Calculate the solar time angle GHA in Greenwich Mean Time

def e(h:float,glat:float,sun_deviation:float):
    G = glat*PI/180
    D=sun_deviation*PI/180
    H=h*PI/180
    return float(180/PI*math.acos((math.sin(H)-math.sin(G)*math.sin(D))/(math.cos(G)*math.cos(D))))
#Calculate the correction value e

def UT_rise(UTo:float,GHA:float,glong:float,e:float):
    return float(UTo-(GHA+glong+e))
#Calculate sunrise time

def UT_set(UTo:float,GHA:float,glong:float,e:float):
    return float(UTo-(GHA+glong-e))
#Calculate sunset time

def result_rise(UT:float,UTo:float,glong:float,glat:float,year:int,month:int,date:int):
    d:float
    if(UT>=UTo):
        d = UT-UTo
    else:
        d=UTo-UT
    
    if(d >= 0.1):
        UTo=UT
        
        TC = t_century(days(year,month,date),UTo)
        GS = G_sun(TC)
        LS = L_sun(TC)
        Gha = GHA(UTo,GS,ecliptic_longitude(LS,GS))
        E = e(h,glat,sun_deviation(earth_tilt(TC),ecliptic_longitude(LS,GS)))
        
        UT = UT_rise(UTo,Gha,glong,E)
        result_rise(UT,UTo,glong,glat,year,month,date)
    
    return UT
#Analyzing and returns the result of sunrise

def result_set(UT:float,UTo:float,glong:float,glat:float,year:int,month:int,date:int):
    d:float
    if(UT>=UTo):
        d = UT-UTo
    else:
        d=UTo-UT

    if(d>=0.1):
        UTo=UT
        TC = t_century(days(year,month,date),UTo)
        GS = G_sun(TC)
        LS = L_sun(TC)
        Gha = GHA(UTo,GS,ecliptic_longitude(LS,GS))
        E = e(h,glat,sun_deviation(earth_tilt(TC),ecliptic_longitude(LS,GS)))
        UT=UT_set(UTo,Gha,glong,E)
        result_set(UT,UTo,glong,glat,year,month,date)
    return float(UT)
#Analyzing and returns the result of sunset

def Zone(glong:float):
    if(glong>=0):
        return int(int(glong/15.0)+1)
    else:
        return int(int(glong/15.0)-1)
#Calculate the TimeZone

def output(rise:float,Set:float,glong:float):
    '''0 SUNRISE HOUR'''
    '''1 SUNRISE MINUTE'''
    '''2 SUNSET HOUR'''
    '''3 SUNSET MINUTE'''
    return (
        int(rise/15+Zone(glong)),
        int(60*(rise/15+Zone(glong)-(int)(rise/15+Zone(glong)))),
        int(Set/15+Zone(glong)),
        int(60*(Set/15+Zone(glong)-(int)(Set/15+Zone(glong))))
        )
    

'''

def calc(year:int,month:int,date:int,latitude:list,longitude:list):
    
    UTo:float = 180.0
    glat=latitude[0]+latitude[1]/60+latitude[2]/3600
    glong=longitude[0]+longitude[1]/60+longitude[2]/3600  
    TC = t_century(days(year,month,date),UTo)
    GS = G_sun(TC)
    LS = L_sun(TC)
    Gha = GHA(UTo,GS,ecliptic_longitude(LS,GS))
    E = e(h,glat,sun_deviation(earth_tilt(TC),ecliptic_longitude(LS,GS)))
    
    UT = UT_rise(UTo,Gha,glong,E)
    Rise:float=result_rise(UT_rise(UTo,Gha,glong,E),UTo,glong,glat,year,month,date)

    UT = UT_set(UTo,Gha,glong,E)
    Set:float=result_set(UT,UTo,glong,glat,year,month,date); 
    return output(Rise,Set,glong)
'''

def calc(year:int,month:int,date:int,LAT:list,LON:list):
    
    UTo:float = 180.0
    glat=LAT[0]+LAT[1]/60+LAT[2]/3600
    glong=LON[0]+LON[1]/60+LON[2]/3600  
    TC = t_century(days(year,month,date),UTo)
    GS = G_sun(TC)
    LS = L_sun(TC)
    Gha = GHA(UTo,GS,ecliptic_longitude(LS,GS))
    E = e(h,glat,sun_deviation(earth_tilt(TC),ecliptic_longitude(LS,GS)))
    
    UT = UT_rise(UTo,Gha,glong,E)
    Rise:float=result_rise(UT_rise(UTo,Gha,glong,E),UTo,glong,glat,year,month,date)

    UT = UT_set(UTo,Gha,glong,E)
    Set:float=result_set(UT,UTo,glong,glat,year,month,date)
    return output(Rise,Set,glong)

