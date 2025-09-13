sol = [[1,2,3],[4,5,6],[7,8,0]]
moves_list = [[['r','d'],['l','r','d'],['l','d']], 
            [['r','u','d'], ['l','r','u','d'],['l', 'u','d']], 
            [['r','u'], ['l','r','u'],['l', 'u']]]

class Tablero:
    def __init__(self, nums=[[1,2,3],[4,5,6],[7,8,0]]):  
        self.nums = nums
        
    def isSolution(self):
        return self.nums == sol
    
    def empty(self):
        for ir, r in enumerate(self.nums):
            for ic, c in enumerate(r):
                if c == 0:
                    return ir, ic
    
    def moves(self):
        r, c = self.empty()
        return moves_list[r][c]
    
    def make_move(self, dir):
        r, c = self.empty()

        if dir == 'l':
            aux = self.nums[r][c]
            self.nums[r][c] = self.nums[r][c-1]
            self.nums[r][c-1] = aux
        elif dir == 'r':
            aux = self.nums[r][c]
            self.nums[r][c] = self.nums[r][c+1]
            self.nums[r][c+1] = aux
        elif dir == 'u':
            aux = self.nums[r][c]
            self.nums[r][c] = self.nums[r-1][c]
            self.nums[r-1][c] = aux
        elif dir == 'd':
            aux = self.nums[r][c]
            self.nums[r][c] = self.nums[r+1][c]
            self.nums[r+1][c] = aux