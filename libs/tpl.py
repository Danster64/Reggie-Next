#!/usr/bin/python
# -*- coding: latin-1 -*-

# Reggie Next - New Super Mario Bros. Wii Level Editor
# Milestone 4
# Copyright (C) 2009-2020 Treeki, Tempus, angelsl, JasonP27, Kamek64,
# MalStar1000, RoadrunnerWMC, AboodXD, John10v10, TheGrop, CLF78,
# Zementblock, Danster64

# This file is part of Reggie Next.

# Reggie Next is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Reggie Next is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Reggie Next.  If not, see <http://www.gnu.org/licenses/>.


# tpl.py
# TPL image data encoder and decoder in Python.


################################################################
################################################################


# 'data' must be RGBA8 raw data
def decodeRGB4A3(data, width, height, noAlpha):
    result = bytearray(width * height * 4)

    i = 0
    for yTile in range(0, height, 4):
        for xTile in range(0, width, 4):
            for y in range(yTile, yTile + 4):
                for x in range(xTile, xTile + 4):
                    pixel = (data[i] << 8) | data[i+1]

                    if pixel & 0x8000:
                        r = (pixel & 0x1F) * 255 // 0x1F
                        g = ((pixel >> 5) & 0x1F) * 255 // 0x1F
                        b = ((pixel >> 10) & 0x1F) * 255 // 0x1F

                    else:
                        r = (pixel & 0xF) * 255 // 0xF
                        g = ((pixel & 0xF0) >> 4) * 255 // 0xF
                        b = ((pixel & 0xF00) >> 8) * 255 // 0xF

                    if noAlpha or pixel & 0x8000:
                        a = 0xFF

                    else:
                        a = ((pixel & 0x7000) >> 12) * 255 // 0x7

                    pos = (y * width + x) * 4

                    result[pos] = r
                    result[pos + 1] = g
                    result[pos + 2] = b
                    result[pos + 3] = a

                    i += 2 

    return bytes(result)


# 'data' must be RGBA8 raw data
def encodeRGB4A3(tex, width, height):
    result = bytearray(width * height * 2)

    i = 0
    for yTile in range(0, height, 4):
        for xTile in range(0, width, 4):
            for y in range(yTile, yTile + 4):
                for x in range(xTile, xTile + 4):
                    pos = (y * width + x) * 4

                    r = data_[pos]
                    g = data_[pos + 1]
                    b = data_[pos + 2]
                    a = data_[pos + 3]
                    
                    if a < 0xF7:
                        a //= 32
                        r //= 16
                        g //= 16
                        b //= 16

                        rgb = b | (g << 4) | (r << 8) | (a << 12)
                
                    else:
                        r //= 8
                        g //= 8
                        b //= 8
                        
                        rgb = b | (g << 5) | (r << 10) | 0x8000
                                                                                                            
                    result[i] = rgb >> 8
                    result[i + 1] = rgb & 0xFF

                    i += 2
                    
    return bytes(result)
