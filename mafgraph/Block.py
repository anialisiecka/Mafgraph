# -*- coding: utf-8 -*-
from Arc import Arc

class Block:
    def __init__(self, block_id, alignment):
        self.id = block_id
        self.alignment = alignment
        self.toroot = self # parent in find-union tree
        self.shift = 0 # order relative to parent
        self.reorder_shift = 0 # modification caused by edges inserted within group
        self.orient = 1 # orientation relative to parent
        self.flanks = {-1: 0, 1: 0} # blocks in group with negative/positive order (only in root)
        self.out_edges = []
        
    def find(self):
        if self.toroot is self:
            return self
        else:
            root = self.toroot.find()
            # let's update atributes for flattened tree structure
            self.orient *= self.toroot.orient
            self.shift = self.shift*self.toroot.orient+self.toroot.shift
            self.reorder_shift *= self.toroot.orient
            self.toroot = root
        return root
    
    def orientation(self):
        self.find()
        return self.orient

    def order(self):
        self.find()
        return self.shift+self.reorder_shift
    
    def reorder(self, n):
        self.reorder_shift += n - self.order()

#    def reorder(self, delta):
#        self.reorder_shift += delta

    def size(self):
        rootflanks = self.find().flanks
        return rootflanks[1]+rootflanks[-1]+1
    
	def minimum(self):
		root = self.find()
		return -root.flanks[-1]
	
	def maximum(self):
		root = self.find()
		return root.flanks[1]		
	
    def unionto(self, other, reverse, flank): # join self to other
        selfroot = self.find()
        otheroot = other.find()
        selfroot.orient = reverse
        selfroot.reorder_shift *= reverse
        selfroot.shift = flank*(otheroot.flanks[flank]+selfroot.flanks[-reverse*flank]+1)
        otheroot.flanks[flank] += selfroot.flanks[-1]+selfroot.flanks[1]+1
        selfroot.toroot = otheroot
        del selfroot.flanks
        
    def orient_block(self):
        # Modify alignment according to block orientation
        if self.orientation() == -1:
            for u in self.alignment:
                u.seq = u.seq.reverse_complement()
                u.annotations["strand"] *= -1
                u.annotations["start"] = u.annotations["srcSize"] - u.annotations["size"] - u.annotations["start"]
        
    def add_out_edges(self, to, edgeType, list_of_seq):
        self.out_edges.append(Arc(to, edgeType, list_of_seq))
