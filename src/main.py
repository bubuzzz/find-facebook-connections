from algorithms import bfs
from facebook import FacebookClient

cookies = None


class FBTree:
    solution_required = 3  # NUMBER FRIENDS REQUIRED
    client = FacebookClient(cookies)

    def __init__(self):
        self.root = self.client.get_myself_username()
        self.goals = None

    def get_root(self):
        return self.root

    def set_goals(self, username):
        children = self.client.get_children(username)
        self.goals = [child.username for child in children]
        print 'goals: ', self.goals

    def is_goal(self, username):
        return True if username in self.goals else False

    def get_children(self, username):
        return self.client.get_children(username)


if __name__ == '__main__':
    # crawl_friends()
    tree = FBTree()
    tree.set_goals("phithihaiau")
    results = bfs(tree)
    print 'result paths:\n', '\n'.join(results)
