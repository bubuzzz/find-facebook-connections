from algorithms import Algorithm
from config import target
from facebook import FacebookClient
from config import cookies

def init(client):
    username = client.get_myself_username()
    goals = client.get_friends(target)
    return (username, goals)

if __name__ == '__main__':
    client = FacebookClient(cookies)
    username, goals = init(client)
    print 'Goals: %s' % goals

    algorithm = Algorithm(username, goals, client)
    results = algorithm.dfs()

    print '------------------------------------------'
    print "RESULT PATHS: %s\n" % '\n'.join(results)
    print '------------------------------------------'
