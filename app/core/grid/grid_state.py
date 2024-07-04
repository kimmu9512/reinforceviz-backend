class GridState:
    """
    GridState class

    Members:
        x & y: represent the position of GridState in the grid
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """
        Overriding str function to be used by the internal hash function
        """
        return str(self.x) +","+ str(self.y)

    def __hash__(self):
        """
        Overriding hash function for faster state lookups when stored in a set or 
        dictionary
        """
        return hash(str(self))

    def __eq__(self, other):
        """
        Two nodes are equal if they are in the same row and col in grid
        
        :param other: other GridState object to compare
        """
        if other is None:
            return False

        return self.x == other.x and self.y == other.y
