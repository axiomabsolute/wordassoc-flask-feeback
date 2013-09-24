import csv
import hashlib
import collections

answers = {}
questions = {}
users = set()

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
                hasher.update(row[1]) # Note: Salt was added to this in the example provided to provide protection to anonymize the data.  Rerunning this on the data will produce different results
                row[1] = hasher.hexdigest()
                gamewriter.writerow(row)


def readUsers():
    with open('data/Answers-anonymous.csv','r') as answerfile:
        answerreader = csv.reader(answerfile, delimiter=",", quotechar='"')
        for row in answerreader:
            users.add(row[2])

def readAnswers():
    """
    Note: Only the top score for each user is kept
    """
    with open('data/Answers-anonymous.csv','r') as answerfile:
        answerreader = csv.reader(answerfile, delimiter=",", quotechar='"')
        for row in answerreader:
            answers[row[0]] = {"id": row[0], "question_id": row[1], "player_id": row[2], "playerAnswer": row[3], 
                "game_id": row[4], "correct": row[5]}

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
    return len(answers.keys())

def calculateNumberOfPlayers():
    return len(set([answer["player_id"] for answer in answers.values()]))

def calculateNumberOfGamesPerPlayer():
    gamesByPlayer = collections.defaultdict(lambda: set())
    for answer in answers:
        gamesByPlayer[answer["player_id"]].add(answer["game_id"])


                
# Preparation
# anonymize()

readUsers()
readAnswers()
readQuestions()

# Run analyses
print("Total number of answers: %s" % calculateNumberOfAnswers())
print("Total number of players: %s" % calculateNumberOfPlayers())
