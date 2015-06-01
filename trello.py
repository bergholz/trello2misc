''' trello.py
Contains the TrelloBoard and TrelloCard classes 
plus methods related to Trello.
'''

import urllib.request, json, re, datetime
import utils

# A Trello board contains the identifier, a name, and an indicators
# whether the board closed.
class TrelloBoard:

    # The constructor.
    def __init__(self, identifier, name, closed):
        self.identifier = identifier.strip()
        self.name = name.strip()
        self.closed = closed
        
    # The string representation.
    def __repr__(self):
        string = "Trello Board"
        if len(self.identifier) > 0:
            string += " " + self.identifier
        string += ": " + self.name
        return string

# A Trello card contains the identifier, a name, a due date, a label, 
# a board id, a list id, and an indicator whether the card is closed.
class TrelloCard:
    
    # The constructor.
    def __init__(self, identifier, name, due, labels, closed, board, listt, pos):
        self.identifier = identifier.strip()
        self.name = name.strip()
        self.due = due
        self.labels = list(map(utils.strip, labels))
        self.closed = closed
        self.board = board.strip()
        self.list = listt.strip()
        self.pos = pos

    # The string representation.
    def __repr__(self):
        string = "Trello Card %s: %s" % (self.identifier, self.name)
        if self.due is not None:
            stripped = datetime.datetime.strptime(self.due, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            string += " %s" % (stripped)
        if len(self.labels) > 0:
            string += " ("
            for label in self.labels:
                string += "%s " % (label)
            string = string.strip()
            string += ")"
        return string


# Returns a list of JSON objects for a given Trello API URL.
# Automatically adds Trello authentication (applicatoin key and 
# user token).
def get_json_response(url):
    config = utils.readconfig("trello2misc.ini")
    key = config.get("trello", "key")
    token = config.get("trello", "token")
    authorizedUrl = url + "?key=" + key + "&token=" + token
    response = urllib.request.urlopen(authorizedUrl)
    content = response.read()
    jsonList = json.loads(content.decode('utf-8'))
    return jsonList

# Returns a dictionary of my Trello boards. The board identifiers
# are the keys of the dictionary, the board objects are the values.
def read_my_trello_boards():
    boards = {}
    url = "https://api.trello.com/1"
    url += "/members/me/boards"
    jsonList = get_json_response(url)
    for jsonObject in jsonList:
        boardId = jsonObject["id"]
        name = jsonObject["name"]
        closed = jsonObject["closed"]
        if not closed:
            boards[boardId] = TrelloBoard(boardId, name, closed)
    return boards

# Returns a dictionary of Trello lists for a given list of Trello boards.
# The list identifiers are the keys of the dictionary, the list names
# are the values.
def read_trello_lists(boards):
    lists = {}
    for boardId in boards.keys():
        url = "https://api.trello.com/1"
        url += "/boards/" + boardId + "/lists"
        jsonList = get_json_response(url)
        for jsonObject in jsonList:
            listId = jsonObject["id"]
            name = jsonObject["name"]
            name = re.sub("\s+\\[\d+\\]$", "", name)
            lists[listId] = name
    return lists

# Returns a dictionary of all Trello cards for a given list of board names
# to be selected from all boards. The card identifiers are the keys 
# of the dictionary, the card objects are the values.
def read_all_trello_cards(boardNames, boards):
    cards = {}
    boardIds = []
    for boardId in boards.keys():
        if boards[boardId].name in boardNames:
            boardIds.append(boardId)
    for boardId in boardIds:
        url = "https://trello.com/1"
        url += "/boards/" + boardId + "/cards"
        jsonList = get_json_response(url)
        for jsonObject in jsonList:
            cardId = jsonObject["id"]
            name = jsonObject["name"]
            boardId = jsonObject["idBoard"]
            listId = jsonObject["idList"]
            pos = jsonObject["pos"]
            due = jsonObject["badges"]["due"]
            labels = jsonObject["labels"]
            labelNames = []
            for label in labels:
                labelName = label["name"]
                if len(labelName) == 0:
                    labelName = label["color"]
                labelNames.append(labelName)
            closed = jsonObject["closed"]
            cards[cardId] = TrelloCard(cardId, name, due, labelNames, closed, boardId, listId, pos)
    return cards

# Returns a dictionary of Trello cards assigned to me for a given list 
# of board names to be selected from all boards. The card identifiers 
# are the keys of the dictionary, the card objects are the values.
def read_my_trello_cards(boardNames, boards):
    cards = {}
    boardIds = []
    for boardId in boards.keys():
        if boards[boardId].name in boardNames:
            boardIds.append(boardId)
    url = "https://trello.com/1"
    url += "/members/me/cards"
    jsonList = get_json_response(url)
    for jsonObject in jsonList:
        cardId = jsonObject["id"]
        name = jsonObject["name"]
        boardId = jsonObject["idBoard"]
        listId = jsonObject["idList"]
        pos = jsonObject["pos"]
        due = jsonObject["badges"]["due"]
        labels = jsonObject["labels"]
        labelNames = []
        for label in labels:
            labelName = label["name"]
            if len(labelName) == 0:
                labelName = label["color"]
            labelNames.append(labelName)
        closed = jsonObject["closed"]
        if boardId in boardIds:
            cards[cardId] = TrelloCard(cardId, name, due, labelNames, closed, boardId, listId, pos)
    return cards

# Returns a dictionary of Trello boards, where boards, whose names are not
# in the list of names given, are removed.
def filter_trello_boards(boardNames, boards):
    filteredIds = []
    for boardId in boards.keys():
        if not boards[boardId].name in boardNames:
            filteredIds.append(boardId)
    for boardId in filteredIds:
        del boards[boardId]
    return boards

# Returns a dictionary of Trello cards, where cards, whose list identifier
# corresponds to a list name to be ignored, are removed.
def filter_cards(cards, lists):
    config = utils.readconfig("trello2misc.ini")
    ignoredLists = config.get("trello", "ignoredLists")
    ignoredNames = []
    for name in ignoredLists.split(","):
        ignoredNames.append(name.replace("\"","").strip())
    filteredIds = []
    for cardId in cards.keys():
        listId = cards[cardId].list
        if lists[listId] in ignoredNames:
            filteredIds.append(cardId)
    for cardId in filteredIds:
        del cards[cardId]
    return cards

# Sorts the incoming cards by priority and position in a Trello list.
def sort_cards(cards, lists):
    config = utils.readconfig("trello2misc.ini")
    aLists = config.get("trello", "aLists")
    bLists = config.get("trello", "bLists")
    cLists = config.get("trello", "cLists")
    aList = []
    bList = []
    cList = []
    for name in aLists.split(","):
        aList.append(name.replace("\"","").strip())
    for name in bLists.split(","):
        bList.append(name.replace("\"","").strip())
    for name in cLists.split(","):
        cList.append(name.replace("\"","").strip())
    listOrder = aList + bList + cList
    cardsByPriority = {}
    cardsByPriority["A"] = []
    cardsByPriority["B"] = []
    cardsByPriority["C"] = []
    otherCards = []
    sortedCards = []
    for cardId in cards.keys():
        card = cards[cardId]
        listId = card.list
        listName = lists[listId]
        if listName in aList:
            cardsByPriority["A"].append(card)
        elif listName in bList:
            cardsByPriority["B"].append(card)
        elif listName in cList:
            cardsByPriority["C"].append(card)
        else:
            otherCards.append(card)
    cardsByPriority["A"].sort(key=lambda x: (x.due or str(datetime.MAXYEAR), x.pos), reverse=False)
    cardsByPriority["B"].sort(key=lambda x: (x.due or str(datetime.MAXYEAR), x.pos), reverse=False)
    cardsByPriority["C"].sort(key=lambda x: (x.due or str(datetime.MAXYEAR), x.pos), reverse=False)
    sortedCards.extend(cardsByPriority["A"])
    sortedCards.extend(cardsByPriority["B"])
    sortedCards.extend(cardsByPriority["C"])
    sortedCards.extend(otherCards)
    return sortedCards

