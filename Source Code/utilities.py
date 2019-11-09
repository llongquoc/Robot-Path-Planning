import math
from collections import namedtuple

# Common
Cell = namedtuple('Cell', 'x y')

# A Star
CellDetails = namedtuple("CellDetails", "parent_x parent_y f g h")

# common functions
def isValid(cell, R, C):
	return (cell.x >= 0) and (cell.x < R) and (cell.y >= 0) and (cell.y < C)

def isUnblocked(matrix, cell):
	return matrix[cell.x][cell.y] == 0

def isDestination(cell, dest):
	return cell.x == dest.x and cell.y == dest.y

def calculateHValue(cell, dest):
	return math.sqrt((cell.x - dest.x)**2 + (cell.y - dest.y)**2)

def canMove(matrix, fromCell, toCell):
	if matrix[toCell.x][toCell.y] != 0:
		return False

	if( toCell.x - fromCell.x != 0 and toCell.y - fromCell.y != 0 and
            matrix[toCell.x][fromCell.y] == matrix[fromCell.x][toCell.y] and matrix[fromCell.x][toCell.y]!=0):
		return False

	return True

def isValidInput(matrix, src, dest, R, C):
	if isValid(src, R, C) == False:
		print ("Source is invalid")
		return False

	if isValid(dest, R, C) == False:
		print ("Destination is invalid")
		return False

	if isUnblocked(matrix, src) == False or isUnblocked(matrix, dest) == False:
		print ("Source or the destination is blocked")
		return False

	if isDestination(src, dest):
		print ("We are already at the destination")
		return False

	return True