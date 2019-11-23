from tools.bintree import BinTree
from tools.heap import Heap
import binascii

class Huffman():
	def __init__(self, data):
		self.tree = BinTree(None, None, None)
		self.data = data
		self.e_tree = ""
		self.e_data = ""
		self.l_occ = 0
		print("len data: ", len(bin(int(binascii.hexlify(data.encode()), 16))))

	def occ(self):
		d_occ = dict()
		for l in self.data:
			try:
				d_occ[l] += 1
			except:
				d_occ[l] = 1
		self.l_occ = len(d_occ)
		self.d_occ =  dict()
		for l in d_occ:
			try:
				self.d_occ[d_occ[l]].append(l)
			except:
				self.d_occ[d_occ[l]] = [l]

	def create_tree(self):
		tree = self.tree
		i = 0
		for n in sorted(list(self.d_occ), reverse=True):
			for l in self.d_occ[n]:
				i += 1
				if self.l_occ > i:
					tree.left = BinTree(l, None, None)
					tree.right = BinTree(None, None, None)
					tree = tree.right
				else:
					tree.key = l

	def encode_tree(self, tree):
		if tree.key:
			self.e_tree += "1"
			self.e_tree += " {:08b} ".format(ord(tree.key))
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

	def encrypt(self):
		occ = self.occ()
		print("occ: ", self.d_occ)
		self.create_tree()
		self.encode_tree(self.tree)
		print("encode tree: ", self.e_tree)
		self.encode_data()
		print("encode data: ", len(self.e_data))

huff = Huffman("Article nor prepare chicken you him now. Shy merits say advice ten before lovers innate add. She cordially behaviour can attempted estimable. Trees delay fancy noise manor do as an small. Felicity now law securing breeding likewise extended and. Roused either who favour why ham. ")
huff.encrypt()
