""" Short, one line description of the project ending with a period.
A longer description of the module with details that may help the user or anybody
reviewing the code later. make sure you outline in detail what the module does and how it can be used.
"""

__author__ = "Amber Williamson"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "amber.williamson@education.nsw.com.au"
__status__ = "Alpha"


""" revision notes:


"""

#import statements for any dependencies


#modules - write your modules here using the templates below


# templates
class LeaderBoard(object):
    """Leader Board to hold top scores and names.

    
    Attributes:
        leaders: An array of the leaders.
        leader_file: file containing the leader board data
    
    """

    def __init__(self):
        """Inits the leader board with data from the file."""
        self.leaders = []
        try:
            leader_file = open('media\leader_board.txt', 'r')
            in_leaders = leader_file.readlines() #read the file
            leader_file.close() #always good practice to close the file ASAP
            
            for l in in_leaders:
                l = l.split(",")
                #change scores to int and strip EOL characters of names
                self.leaders.append([int(l[0]), l[1].strip()])
            # print(self.leaders)
        except FileNotFoundError:
            pass #we will create the file later

    def check(self, score):
        """checks to see if new score makes it on leader board.
        
        Args:
        score: the first argument required by the function.

        Returns:
            True if score needs to go on leader board, or False
        """
        
        new_leader = False
        if len(self.leaders) < 10:
            new_leader = True
            
        for l in self.leaders:
            if score >= l[0]:
                new_leader = True
        
        return new_leader
        
        
    def update(self, score):
        """add a new leader and score on leader board.

        Adds a new leader to the leader board. Write the new leaderboard file
        TODO check names to see if they are nice
        
        Args:
        score: the first argument required by the function.

        Returns:
            True if score needs ot go on leader board, or false
        """
        player_name = input('Please enter your player name: ')
        banned = self.name_banned(player_name)
        while banned == True:
            player_name = input("You can't write that! Try again and be nice: ")
            banned = self.name_banned(player_name)
        
            
        self.leaders.append([score, player_name])
        self.leaders.sort(reverse=True) #sort in descending order
        if len(self.leaders) > 10:
            self.leaders.pop()

        leader_file = open('media\leader_board.txt', 'w+')
        for l in self.leaders:
            leader_file.write("{},{}\n".format(l[0], l[1]))
        leader_file.close() #always good practice to close the file ASAP


    def name_banned(self, name):
        """checks to see if name is on banned list.
        
        Args:
        name: the word to test.

        Returns:
            banned: True if word is banned, or False
        """
        
        banned = False
        banned_file = open('media\swear_words.txt', 'r')
        banned_words = banned_file.readlines()
        banned_file.close() #always good practice to close the file ASAP
        
        for b in banned_words:
            b = b.strip()
            if b in name:
                banned = True
                
        return banned
    
    """Does something amazing.

    a much longer description of the really amazing stuff this function does and how it does it.

    Args:
        arg1: the first argument required by the function.
        arg2: the second argument required by the function.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        description of the stuff that is returned by the function.

    Raises:
        AnError: An error occurred running this function.
    """
    pass



class SampleClass(object):
    """Summary of class here.

    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

   