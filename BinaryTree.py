from __future__ import print_function
from data_structs import Stacks, Queues
import numpy as np

__author__ = 'Kingsley Biney'

'''This class implements the informed and uninformed search algorithms being visualized on graph'''


class BinaryTree:
    def __init__(self):
        self.root = None

    def displayPreOrder(self, node):
        if node == None:
            return
        print(node.getKey(),end='->')
        self.displayPreOrder(node.getLeft())
        self.displayPreOrder(node.getRight())

    def setroot(self, root):
        self.root = root

    def getroot(self):
        return self.root

    def displayPostOrder(self, node):
        if node == None:
            return

        if node.hasLeft():
            self.displayPostOrder(node.getLeft())
        if node.hasRight():
            self.displayPostOrder(node.getRight())
        print(node.getKey(), end='->')

    def searchPreOrder(self, node, searchKey):
        if node == None:
            return

        if node.getKey() == searchKey:
            self.found = node
        else:
            if node.hasLeft():
                self.searchPreOrder(node.getLeft(), searchKey)
            if node.hasRight():
                self.searchPreOrder(node.getRight(), searchKey)

    def displayInOrder(self, node):
        holder = []
        if self.root == None:
            return

        if node.hasLeft():
            self.displayInOrder(node.getLeft())
        print(node.getKey(), end='->' )
        if node.hasRight():
            self.displayInOrder(node.getRight())
        return holder


    def insert(self,parentKey, node, direction):
        if self.root == None:
            self.root = node

        else:
            self.found = None
            self.searchPreOrder(self.root, parentKey)
            if self.found == None:
                # print('The parent key was not found')
                return
            elif direction == 'LEFT':
                node.set_parent(self.found)
                self.found.setLeft(node)
            elif direction == 'RIGHT':
                node.set_parent(self.found)
                self.found.setRight(node)

    # perform depth first search
    def dfs (self, searchKey):
        s = Stacks()
        s.push(self.root)
        path =[]
        while s.isEmpty() == False:
            u = s.pop()
            path.append(u.getKey())
            if u.getKey() != searchKey:
               if u.hasRight():
                   s.push(u.getRight())
               if u.hasLeft():
                   s.push(u.getLeft())

            else:
                return path
        return None

    # calculate the distance to find the minimized  cost
    def f_n_block(self, node1, node2):
        if node1 == None:
            return 0
        x_all = node1.get_x() - node2.get_x()
        y_all = node1.get_y() - node2.get_y()
        f_n = np.sqrt(np.square(x_all) + np.square(y_all))
        return f_n

    # perform breadth first search
    def bfs(self, searchKey):
        q = Queues()
        q.enQueues(self.root)
        path = []
        while q.isEmpty() == False:
            u = q.deQueues()
            path.append(u.getKey())
            if u.getKey() == searchKey:
                return path
            else:
                if u.hasLeft():
                    q.enQueues(u.getLeft())
                if u.hasRight():
                    q.enQueues(u.getRight())
        return None

    # perform the uniform cost search
    def ucs(self, searchKey):
        q = Queues()
        q.enQueues(self.root)
        explored = []
        while q.isEmpty() == False:
            q.QueuesList.sort(key=lambda x: x.get_cost(), reverse=False)
            u = q.deQueues()
            explored.append(u)
            if u.getKey() == searchKey:
                return explored
            else:
                if u.hasLeft():
                    left = u.getLeft()
                    distance = self.f_n_block(u, left)
                    left.set_cost(distance+u.get_cost())
                    q.enQueues(left)
                if u.hasRight():
                    right = u.getRight()
                    distance = self.f_n_block(u, right)
                    right.set_cost(distance + u.get_cost())
                    q.enQueues(right)
        return None

    def backtrack(self, startNode, endNode):
        if startNode == endNode:
            return [startNode]
        nodes = []
        # start from the last node
        currentparent = endNode.get_parent()
        while currentparent != self.root:
            nodes.append(currentparent)
            currentparent = currentparent.get_parent()

        nodes.append(startNode)
        nodes.reverse()
        nodes.append(endNode)
        return nodes