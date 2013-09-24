import csv
import hashlib
import collections

answers = {}
filteredAnswers = {}
questions = {}
users = set()
games = {0: -100}   # Default game, lowest score
maxGameByUser = collections.defaultdict(lambda: 0)

# Anonymize the answer data
def anonymize():
    with open('data/Answers-anonymous.csv','w') as output:
        with open('data/Answers.csv','r') as csvfile:
            output.write(csvfile.readline())
            answerreader = csv.reader(csvfile, delimiter=",", quotechar='"')
            answerwriter = csv.writer(output, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
            for row in answerreader:
                hasher = hashlib.md5()
                hasher.update(row[2]) # Note: Salt was added to this in the example provided to provide protection to anonymize the data.  Rerunning this on the data will produce different results
                row[2] = hasher.hexdigest()
                answerwriter.writerow(row)
    with open('data/Games-anonymous.csv','w') as output:
        with open('data/Games.csv','r') as csvfile:
            output.write(csvfile.readline())
            gamereader = csv.reader(csvfile, delimiter=",", quotechar='"')
            gamewriter = csv.writer(output, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
            for row in gamereader:
                hasher = hashlib.md5()
                hasher.update(row[1] + '8') # Note: Salt was added to this in the example provided to provide protection to anonymize the data.  Rerunning this on the data will produce different results
                row[1] = hasher.hexdigest()
                gamewriter.writerow(row)

def readGames():
    with open('data/Games-anonymous.csv', 'r') as gamefile:
        gamefile.readline()
        gamereader = csv.reader(gamefile, delimiter=",", quotechar='"')
        for game in gamereader:
            games[game[0]] = game[2]


def readMaxGamesByUser():
    with open('data/Games-anonymous.csv', 'r') as gamefile:
        gamefile.readline()
        gamereader = csv.reader(gamefile, delimiter=",", quotechar='"')
        for game in gamereader:
            if games[maxGameByUser[game[1]]] < game[2]:
                maxGameByUser[game[1]] = game[0]


def readUsers():
    with open('data/Answers-anonymous.csv','r') as answerfile:
        answerreader = csv.reader(answerfile, delimiter=",", quotechar='"')
        for row in answerreader:
            users.add(row[2])

def readAnswers():
    """
    Note: Only the answers corresponding to the top game of some user are kept
    """
    global filteredAnswers
    with open('data/Answers-anonymous.csv','r') as answerfile:
        answerreader = csv.reader(answerfile, delimiter=",", quotechar='"')
        for row in answerreader:
            answers[row[0]] = {"id": row[0], "question_id": row[1], "player_id": row[2], "playerAnswer": row[3], 
                "game_id": row[4], "correct": row[5]}
    topgames = set(maxGameByUser.values())
    filteredAnswers = {k:answers[k] for k in answers if answers[k]["game_id"] in topgames}


def readQuestions():
    with open('data/Questions.csv','r') as questionfile:
        questionreader = csv.reader(questionfile, delimiter=",", quotechar='"')
        for row in questionreader:
            questions[row[0]] = {"text": row[0], "correctAnswer": row[1], "questionType": row[2]}

def findBestQuestion():
    for answer in answers:
        pass

def findWorstQuestion():
    pass

def findBestCategory():
    pass

def findWorstCategory():
    pass

def findQuestionsAnsweredDistribution():
    pass

def findQuestionsAnsweredCorrectDistribution():
    pass

def findMostCommonCategory():
    pass

def findMostScarceCategory():
    pass

def calculateQuestionsAnsweredPerSecond():
    pass

def calculateAverageNumberOfWrongAnswers():
    pass

def calculateNumberOfAnswers():
    return len(filteredAnswers)

def calculateNumberOfPlayers():
    return len(users)
                
# Preparation
# anonymize()

readGames()
readMaxGamesByUser()
readUsers()
readAnswers()
readQuestions()

# Run analyses
print("Total number of answers: %s" % calculateNumberOfAnswers())
print("Total number of players: %s" % calculateNumberOfPlayers())
