class Node:
    def __init__(self,value=None):
        self.value=value
        self.next=None
class singlylinkedlist:
    def __init__(self):
        self.head=Node()
    def insert(self,nodevalue):
        if(self.head.value==None):
            self.head.value=nodevalue
        new_node=Node(nodevalue)
        current_node=self.head
        while(current_node.next!=None):
            current_node=current_node.next
        current_node.next=new_node
    def multipleinsert(self,listvalues):
        for nodevalue in listvalues:
            if(self.head.value==None):
                self.head.value=nodevalue
            new_node=Node(nodevalue)
            current_node=self.head
            while(current_node.next!=None):
                current_node=current_node.next
            current_node.next=new_node
    def deletebyvalue(self,data):
        current_node=self.head
        while(current_node.next.value!=data):
            current_node=current_node.next
            if(current_node.next==None):
                raise ValueError("no such value")
        temp=current_node.next
        current_node.next=temp.next
        del temp
    def deletebyindex(self,data):
        index=0
        done=0
        current_node=self.head
        while(current_node.next!=None):
            current_node=current_node.next
            if(index==data):
                self.deletebyvalue(current_node.value)
                done=1
                break    
            index=index+1
        if(done!=1):
            raise IndexError("index out of bound")
    def findindex(self,data):
        current_node=self.head
        index=0
        done=0
        while(current_node.next.value!=None):
            current_node=current_node.next
            if(current_node.value==data):
                done=1
                return index
            index=index+1
        if(done!=1):
            raise ValueError("no such value")
    def findvalue(self,indexdata):
        index=0
        done=0
        current_node=self.head
        while(current_node.next!=None):
            current_node=current_node.next
            if(index==indexdata):
                return current_node.value
                done=1
                break
            index=index+1
        if(done!=1):
            raise IndexError("index out of bound")
    def isempty(self):
        if(self.head.value==None):
            return True
        else:
            return False
    def islast(self,data):
        traverse_node=self.head
        while(traverse_node.next!=None):
            traverse_node=traverse_node.next
        if(traverse_node.value==data):
            return True
        else:
            return False
    def len(self):
        count=0
        traverse_node=self.head
        while(traverse_node.next!=None):
            traverse_node=traverse_node.next
            count=count+1
        return count
    
    def display(self):
        traverse_node=self.head
        while(traverse_node.next!=None):
            traverse_node=traverse_node.next
            print("{}->".format(traverse_node.value),end="")
        print("None")



