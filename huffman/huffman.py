from tools.bintree import BinTree
from tools.heap import Heap
import binascii

class Huffman():
	def __init__(self, data="", tree="", e_data="", e_tree=""):
		#encode
		self.tree = None
		self.data = data
		#decode
		self.e_tree = e_tree
		self.e_data = e_data
		#print("len data: ", len(bin(int(binascii.hexlify(data.encode()), 16))))

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

	def create_tree(self):
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

	def search_letter(self, letter, tree, path=""):
		if tree.key == letter:
			return path
		elif tree.key != None:
			return None
		ret = None
		if tree.left:
			ret = self.search_letter(letter, tree.left, path + "0")
		if ret == None and tree.right:
			ret = self.search_letter(letter, tree.right, path + "1")
		return ret


	def encode_data(self):
		for l in self.data:
			self.e_data += self.search_letter(l, self.tree)

	def decode_data(self):
		tree = self.tree
		for l in self.e_data:
			if tree.key != None:
				self.data += tree.key
				tree = self.tree
			if l == "0":
				tree = tree.left
			elif l == "1":
				tree = tree.right

	def encrypt(self):
		print(self.data)
		occ = self.occ()
		self.create_tree()
		self.encode_tree(self.tree)
		self.tree.display()
		self.encode_data()
		return (self.e_tree, self.e_data)
	
	def decrypt(self):
		self.tree = BinTree(None, None, None, 0)
		self.d_create_tree(self.e_tree, self.tree)
		self.tree.display()
		self.decode_data()
		print(self.data)

huff = Huffman("Article nor prepare chicken you him now. Shy merits say advice ten before lovers innate add. She cordially behaviour can attempted estimable. Trees delay fancy noise manor do as an small. Felicity now law securing breeding likewise extended and. Roused either who favour why ham. ")
tu = huff.encrypt()

de = Huffman(e_tree=tu[0], e_data=tu[1])
de.decrypt()
