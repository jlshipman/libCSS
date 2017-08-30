#!/usr/bin/python
def dirWithoutDate(str):
	list = str.split('_')
	list.pop()
	list.pop()
	list.pop()
	result='_'.join(list)
	return result