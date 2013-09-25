import csv
import hashlib
import collections
import numpy

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


# Analysis
def findBestQuestion():
    for answer in answers:
        pass

def findWorstQuestion():
    pass

def findQuestionsAnsweredDistribution():
    answeredByGame = collections.defaultdict(lambda: 0)
    for answer in filteredAnswers:
        answeredByGame[filteredAnswers[answer]['game_id']] += 1
    return numpy.histogram(answeredByGame.values())

def findQuestionsAnsweredCorrectDistribution():
    correctByGameId = collections.defaultdict(lambda: 0)
    for answer in filteredAnswers:
        if filteredAnswers[answer]['correct'] == 't':
            correctByGameId[filteredAnswers[answer]['game_id']] += 1
    return numpy.histogram(correctByGameId.values())


def percentCorrectAnswersByCategoryHist():
    categoryGames = collections.defaultdict(lambda: set())
    categoryTotals = collections.defaultdict(lambda: 0)
    for answer in filteredAnswers:
        if questions[filteredAnswers[answer]["question_id"]]["questionType"] == 'snippetToTech':
            categoryTotals[questions[filteredAnswers[answer]["question_id"]]['correctAnswer']] += 1
            if filteredAnswers[answer]["correct"] != 't':
                continue
            categoryGames[questions[filteredAnswers[answer]["question_id"]]['correctAnswer']].add(filteredAnswers[answer]["game_id"])
        else:
            categoryTotals[questions[filteredAnswers[answer]["question_id"]]['questionType']] += 1
            if filteredAnswers[answer]["correct"] != 't':
                continue
            categoryGames[questions[filteredAnswers[answer]["question_id"]]["questionType"]].add(filteredAnswers[answer]["game_id"])
    categoryHist = {category: (1.0*len(categoryGames[category]))/(1.0*categoryTotals[category]) for category in categoryGames}
    return sorted(categoryHist.items(), lambda x, y: -1 if x[1]<y[1] else 1, reverse=True)

def findNumberOfGamesWhereQuestionsFromEachTechWereAnswered():
    categoryGames = collections.defaultdict(lambda: set())
    for answer in filteredAnswers:
        if questions[filteredAnswers[answer]["question_id"]]["questionType"] == 'snippetToTech':
            categoryGames[questions[filteredAnswers[answer]["question_id"]]['correctAnswer']].add(filteredAnswers[answer]["game_id"])
    categoryHist = {category: len(categoryGames[category]) for category in categoryGames}
    return sorted(categoryHist.items(), lambda x, y: x[1]-y[1], reverse=True)

def calculateQuestionsAnsweredPerMinute():
    return ((1.0*len(filteredAnswers))/(1.0*len(games)))*(60.0/90.0)

def calculateAverageNumberOfWrongAnswers():
    return 1.0*len([x for x in filteredAnswers if filteredAnswers[x]['correct'] == 'f'])/len(users)*1.0

def calculateAverageNumberOfRightAnswers():
    return 1.0*len([x for x in filteredAnswers if filteredAnswers[x]['correct'] == 't'])/len(users)*1.0

def calculateNumberOfAnswers():
    return len(filteredAnswers)

def calculateNumberOfPlayers():
    return len(users)
                
# Preparation
# anonymize()

# Careful, order matters here...
readGames()
readMaxGamesByUser()
readUsers()
readAnswers()
readQuestions()

# Run analyses
print("Total number of answers: %s" % calculateNumberOfAnswers())
print("Total number of players: %s" % calculateNumberOfPlayers())
print("Average number of wrong answers: %s" % calculateAverageNumberOfWrongAnswers())
print("Average number of right answers: %s" % calculateAverageNumberOfRightAnswers())
print("Average number of answers per minute: %s" % calculateQuestionsAnsweredPerMinute())

print("Histogram of techs by number of games:")
answersByTechHist = findNumberOfGamesWhereQuestionsFromEachTechWereAnswered()
for kv in answersByTechHist:
    print("\t%s : %s" % kv)
print("\t--------------------")
print("\tMost popular tech -  %s : %s" % answersByTechHist[0])
print("\tLeast popular tech - %s : %s" % answersByTechHist[-1])
print("\t--------------------")

print("Distribution of Number of Correctly Answered Questions by Game:")
correctPerGameHist = findQuestionsAnsweredCorrectDistribution()
print("\t%s\n\t%s" % correctPerGameHist)

try:
    import matplotlib.pyplot as plt
    plt.hist(correctHist[0], correctHist[1])
    plt.show()
except ImportError, e:
    print("\tMatplotlib not found")


print("Distribution of Number of Answered Questions by Game:")
answeredHist = findQuestionsAnsweredDistribution()
print("\t%s\n\t%s" % answeredHist)

try:
    import matplotlib.pyplot as plt
    plt.hist(answeredHist[0], answeredHist[1])
    plt.show()
except ImportError, e:
    print("\tMatplotlib not found")

print("Percentage of correct answers by category:")
correctByCategoryHist = percentCorrectAnswersByCategoryHist()
for kv in correctByCategoryHist:
    print("\t%s : %s" % kv)
print("\t--------------------")
print("\tBest category: %s : %s" % correctByCategoryHist[0])
print("\tWorst category: %s : %s" % correctByCategoryHist[-1])
print("\t--------------------")
