def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (red << 16)| (green << 8) | blue

def rainbowColor(pos, distance):
    """Generate a RGB color based on position through a rainbow of length distance"""
    frac = (pos / float(distance)) % 1
    if frac < 0.333:
	return Color(  0,                   int(255 - frac*255),  int(255*frac) )
    elif frac < 0.666:
	return Color(  int(255*frac),       0,                    int(255 - frac*255) )
    else:
	return Color(  int(255 - 255*frac),  int(frac*255),      0 )

def multiply(digit, color):
    retVal = []
    for row in digit:
        retVal.append([color * x for x in row])
    return retVal