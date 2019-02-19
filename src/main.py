from facebook import FacebookClient
from algorithms import bfs


class Node:
    def __init__(self, username, name=None):
        self.username = username
        self.name = name


class FBTree:
    cookies = None
    solution_required = 1  # NUMBER FRIENDS REQUIRED
    client = FacebookClient(cookies)

    def __init__(self):
        self.root = self.client.get_myself_username()
        self.goals = None

    def get_root(self):
        return self.root

    def set_goals(self, username):
        children = self.client.get_children(username)
        self.goals = children.values()
        print 'goals: ', self.goals

    def is_goal(self, username):
        return True if username in self.goals else False

    def get_children(self, username):
        children = self.client.get_children(username)
        return children.values()


if __name__ == '__main__':
    # crawl_friends()
    tree = FBTree()
    tree.set_goals("kenichi.ogw")
    results = bfs(tree)
    # print results
