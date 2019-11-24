from tools.bintree import BinTree
from tools.heap import Heap
import time
import sys

def btoa(e_str):
	if e_str == "":
		return ""
	ret = str(8 - (len(e_str) % 8))
	if ret == "8":
		ret = "0"
	while len(e_str) % 8 > 0:
		e_str += "0"
	while e_str != "":
		ret += chr(int(e_str[:8], 2))
		e_str = e_str[8:]
	return ret

def atob(s):
	ret = ""
	if s == "":
		return ""
	end = (len(s) * 8) - int(s[0]) - 8
	s = s[1:]
	for i in s:
		ret += "{:08b}".format(ord(i))
	ret = ret[:end]
	return ret

class Huffman():
	def __init__(self, data="", tree="", e_data="", e_tree=""):
		#encode
		self.tree = None
		self.data = data
		#decode
		self.e_tree = atob(e_tree)
		self.e_data = atob(e_data)
		self.d_path = dict()

	def occ(self):
		d_occ = dict()
		for l in self.data:
			try:
				d_occ[l] += 1
			except:
				d_occ[l] = 1
		self.l_tree = []
		for l in d_occ:
			self.l_tree.append(BinTree(l, None, None, d_occ[l]))

	def min_ltree(self):
		if len(self.l_tree) < 2:
			return None
		min1 = self.l_tree[0]
		min2 = self.l_tree[1]
		for i in self.l_tree:
			if min1.prob > i.prob:
				min2 = min1
				min1 = i
			elif min2.prob > i.prob and min1 != i:
				min2 = i
		return min1, min2

	def d_create_tree(self, e_tree, tree):
		if e_tree and e_tree[0] == "0":
			tree.left = BinTree(None, None, None, 0)
			e_tree = self.d_create_tree(e_tree[1:], tree.left)
			tree.right = BinTree(None, None, None, 0)
			e_tree = self.d_create_tree(e_tree, tree.right)
			return e_tree
		if e_tree and e_tree[0] == "1":
			tree.key = chr(int(e_tree[1:9], 2))
			if len(e_tree[9:]) == 0:
				return None
			return e_tree[9:]
		return e_tree

	def e_create_tree(self):
		while len(self.l_tree) > 1:
			min1, min2 = self.min_ltree()
			self.l_tree.append(BinTree(None, min1, min2, min1.prob + min2.prob))
			self.l_tree.remove(min1)
			self.l_tree.remove(min2)
		self.tree = self.l_tree[0]

	def encode_tree(self, tree):
		if tree.key:
			self.e_tree += "1"
			self.e_tree += "{:08b}".format(ord(tree.key))
			return
		if tree.left:
			self.e_tree += "0"
			self.encode_tree(tree.left)
		if tree.right:
			self.encode_tree(tree.right)

	def create_d_path(self, tree, path=""):
		if tree.key:
			self.d_path[tree.key] = path
			return
		if tree.left:
			self.create_d_path(tree.left, path + "0")
		if tree.right:
			self.create_d_path(tree.right, path + "1")

	def encode_data(self):
		for l in self.data:
			self.e_data += self.d_path[l]

	def decode_data(self):
		tree = self.tree
		for l in self.e_data:
			if tree.key:
				self.data += tree.key
				tree = self.tree
			if l == "0":
				tree = tree.left
			elif l == "1":
				tree = tree.right
		if tree.key:
			self.data += tree.key
			tree = self.tree

	def encrypt(self):
		occ = self.occ() # occurence
		self.e_create_tree() # generate tree
		self.encode_tree(self.tree) # encode tree
		self.tree.display() # print tree
		self.create_d_path(self.tree)
		self.encode_data() #  encode data
		return (btoa(self.e_tree), btoa(self.e_data))
	
	def decrypt(self):
		self.tree = BinTree(None, None, None, 0)
		self.d_create_tree(self.e_tree, self.tree) # recreate tree
		self.tree.display() # print tree
		self.decode_data() # decode data 
		return self.data

f_data = open(sys.argv[1], 'r', encoding="utf-8").read()
huff = Huffman(f_data)
tu = huff.encrypt()

de = Huffman(e_tree=tu[0], e_data=tu[1])
data = de.decrypt()
print("---------------------------------------------")
if data == f_data:
	print("OK")
else:
	print("NoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooN")
	print("data:",  f_data)
	print("data:",  data)
print((len(tu[1]) / (len(f_data))) * 100)
