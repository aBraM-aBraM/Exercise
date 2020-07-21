import python_parser
from spellchecker import SpellChecker

# global variables 
name_denormalizer = python_parser.NameDenormalizer()
spell = SpellChecker()

def countUniqueNames(billFirstName, billLastName, shipFirstName, shipLastName, billNameOnCard):
    
    uniqueCount = 1
    
    # handle middle names and capitalization
    billFirstName = billFirstName.split(" ")[0].lower()
    shipFirstName = shipFirstName.split(" ")[0].lower()

    billLastName = billLastName.lower()
    shipLastName = shipLastName.lower()
    
    # construct variables to handle billNameOnCard
    billFirstNameOnCard = billNameOnCard.split(" ")[0].lower()
    billLastNameOnCard = billNameOnCard.split(" ")[len(billNameOnCard.split(" ")) - 1].lower()

    # fix misspelled names
    billFirstName = spell.correction(billFirstName)
    billLastName = spell.correction(billLastName)
    shipFirstName = spell.correction(shipFirstName)
    shipLastName = spell.correction(shipLastName)
    billFirstNameOnCard = spell.correction(billFirstNameOnCard)
    billLastNameOnCard = spell.correction(billLastNameOnCard)

    # check for nicknames
    uniqueNickCount = uniqueByNickname(billFirstName, shipFirstName, billFirstNameOnCard + " " + billLastNameOnCard)
    uniqueCount += uniqueNickCount - 1
    
    return uniqueCount


   

def uniqueByNickname(billName, shipName, cardName):
    uniqueNickCount = 1
    test_count = uniqueNickCount

    # dividing cardname to 'first' and 'last' names
    # there is no guarantee that the order is correct
    # therefore a thorough checking is done  
    cardFirstName = cardName.split(" ")[0].lower()
    cardLastName = cardName.split(" ")[len(cardName.split(" ")) - 1].lower()


    # First test considering the billFirstName as the 'master name'
    try:
        if(billName != shipName):
            similar_names = name_denormalizer.__getitem__(billName)
            if(not similar_names.__contains__(shipName)): test_count += 1
    except:
        test_count += 1
    try:
        if(not (billName == cardFirstName or billName == cardLastName)):
            similar_names = name_denormalizer.__getitem__(billName)
            if(not similar_names.__contains__(cardFirstName) and not similar_names.__contains__(cardLastName)): 
                test_count += 1
    except:
        test_count += 1


    # Second test considering the shipFirstName as the 'master name'
    # this test is done to avoid overcounting uniqueNames when the shipname and cardname 
    # are the same but different from the billname
    if(test_count != uniqueNickCount):
        first_test = test_count
        test_count = uniqueNickCount
        try:
            if(shipName != billName):
                similar_names = name_denormalizer.__getitem__(shipName)
                if(not similar_names.__contains__(billName)): test_count += 1
        except:
            test_count += 1
        try:
            if(not (shipName == cardFirstName or shipName == cardLastName)):
                similar_names = name_denormalizer.__getitem__(shipName)
                if(not similar_names.__contains__(cardFirstName) and not similar_names.__contains__(cardLastName)): 
                    test_count += 1
        except:
            test_count += 1
        uniqueNickCount = min([first_test, test_count])

    return uniqueNickCount

print(countUniqueNames("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli"))
print(countUniqueNames("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli"))
print(countUniqueNames("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli"))
print(countUniqueNames("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah"))
print(countUniqueNames("Michele", "Egli", "Deborah", "Egli", "Michele Egli"))