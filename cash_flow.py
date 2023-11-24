'''This Python programme simulates a simplified debt settlement system for a group of individuals who 
conduct transactions with one another. Participants are represented as instances of the "Participant" class, 
which stores information such as their name, payment modalities, and total transaction amount. 
The main function, "settleDebts," computes and displays the transactions required to efficiently settle 
debts among participants. To limit the overall number of transactions, it employs numerous payment ways and 
a central participant with all payment modalities. The programme accepts user input for the number of participants,
their details, and transaction information, and then displays a clear picture of how participants settle 
their debts through a series of calculated transactions. The code makes use of functions to handle various 
components of the debt settlement process, which improves readability and modularization.'''


# Define a class to represent each participant in the transaction
class Participant:
    def __init__(self):
        self.name = ""               # Participant's name
        self.paymentModes = set()    # Set of payment modes the participant possesses
        self.totalAmount = 0         # Total amount involved in transactions for the participant

# Print the settlement transactions
def printDebtSettlementTransactions(settlementTransactions, numParticipants, participants):

    # Print header for the debt settlement transactions
    print("\nThe transactions for settling debts are as follows: \n")
    
    for i in range(numParticipants):
        for j in range(numParticipants):

            if i == j:
                continue
            
            # Check if there are debts to settle
            if settlementTransactions[i][j]['amount'] != 0 and settlementTransactions[j][i]['amount'] != 0:
                # Determine the payer and payee based on the amount owed
                if settlementTransactions[i][j]['amount'] > settlementTransactions[j][i]['amount']:
                    
                    settlementTransactions[i][j]['amount'] -= settlementTransactions[j][i]['amount']
                    settlementTransactions[j][i]['amount'] = 0
                    # Print the transaction details
                    print(participants[i].name + " pays Rs" + str(settlementTransactions[i][j]['amount']) + " to " + participants[j].name + " via " + settlementTransactions[i][j]['mode'])

                elif settlementTransactions[i][j]['amount'] == settlementTransactions[j][i]['amount']:

                    settlementTransactions[i][j]['amount'] = 0
                    settlementTransactions[j][i]['amount'] = 0

                else:
                    settlementTransactions[j][i]['amount'] -= settlementTransactions[i][j]['amount']
                    settlementTransactions[i][j]['amount'] = 0

                    # Print the transaction details
                    print(participants[j].name + " pays Rs " + str(settlementTransactions[j][i]['amount']) + " to " + participants[i].name + " via " + settlementTransactions[j][i]['mode'])

            elif settlementTransactions[i][j]['amount'] != 0:
                # Print the transaction details for one-way transactions
                print(participants[i].name + " pays Rs " + str(settlementTransactions[i][j]['amount']) + " to " + participants[j].name + " via " + settlementTransactions[i][j]['mode'])

            elif settlementTransactions[j][i]['amount'] != 0:
                # Print the transaction details for one-way transactions
                print(participants[j].name + " pays Rs " + str(settlementTransactions[j][i]['amount']) + " to " + participants[i].name + " via " + settlementTransactions[j][i]['mode'])
            
            # Reset transaction amounts to 0 after settling debts
            settlementTransactions[i][j]['amount'] = 0
            settlementTransactions[j][i]['amount'] = 0
    
    print("\n")

# Function to find the participant with the maximum total amount who shares a common payment type
def findMaxtotalAmountIndexWithCommonType(totalAmountList, numParticipants, minIndexUtil, participants, maxNumTypes):

    type_match = ""
    maxIndexUtil = -1
    maxtotalAmount = float('-inf')
    
    # Iterate through participants to find the one with the maximum total amount and a common payment type
    for i in range(numParticipants):

        if totalAmountList[i].totalAmount == 0 or totalAmountList[i].totalAmount < 0:
            continue
        
        intersection = []
        # Find common payment types between the current participant and the one with the minimum total amount
        for mode in totalAmountList[minIndexUtil].paymentModes:

            if mode in totalAmountList[i].paymentModes:
                intersection.append(mode)
        
        # Update maximum total amount and index if a better candidate is found
        if len(intersection) != 0 and maxtotalAmount < totalAmountList[i].totalAmount:

            maxtotalAmount = totalAmountList[i].totalAmount
            maxIndexUtil = i
            type_match = intersection[0]
    
    return (maxIndexUtil, type_match)

# Function to find the participant with the maximum total amount
def findMaxtotalAmountIndex(totalAmountList, numParticipants):

    maxIndexUtil = -1
    maxtotalAmount = float('-inf')
    
    # Iterate through participants to find the one with the maximum total amount
    for i in range(numParticipants):

        if totalAmountList[i].totalAmount == 0:
            continue
        
        if totalAmountList[i].totalAmount > maxtotalAmount:

            maxtotalAmount = totalAmountList[i].totalAmount
            maxIndexUtil = i
    
    return maxIndexUtil

# Function to find the participant with the minimum total amount
def findMintotalAmountIndex(totalAmountList, numParticipants):

    minIndexUtil = -1
    mintotalAmount = float('inf')
    
    # Iterate through participants to find the one with the minimum total amount
    for i in range(numParticipants):

        if totalAmountList[i].totalAmount == 0:
            continue
        
        elif totalAmountList[i].totalAmount < mintotalAmount:
            mintotalAmount = totalAmountList[i].totalAmount
            minIndexUtil = i
    
    return minIndexUtil

# Function to settle debts between participants
def settleDebts(numParticipants, participants, participantIndex, numTransactions, transactionAmounts, maxNumTypes):

    # Create a list to store total amounts for each participant
    totalAmountList = [Participant() for _ in range(numParticipants)]
    numZerototalAmounts = 0
    
    # Calculate the total amount for each participant
    for i in range(numParticipants):
        amount = 0
        
        totalAmountList[i].name = participants[i].name
        totalAmountList[i].paymentModes = participants[i].paymentModes
        
        # Calculate total amount owed and received by each participant
        for j in range(numParticipants):
            amount += transactionAmounts[j][i]
        
        for k in range(numParticipants):
            amount += ((-1) * transactionAmounts[i][k])
        
        totalAmountList[i].totalAmount = amount
    
    # Create a matrix to store settlement transactions
    settlementTransactions = [[{'amount': 0, 'mode': ""} for _ in range(numParticipants)] for _ in range(numParticipants)]
    
    # Count participants with zero total amounts
    for i in range(numParticipants):

        if totalAmountList[i].totalAmount == 0:
            numZerototalAmounts += 1
    
    # Iterate until all participants have settled debts
    while numZerototalAmounts != numParticipants:

        minIndexUtil = findMintotalAmountIndex(totalAmountList, numParticipants)
        maxParticipant = findMaxtotalAmountIndexWithCommonType(totalAmountList, numParticipants, minIndexUtil, participants, maxNumTypes)

        maxIndexUtil = maxParticipant[0]
        
        # Check if there is a participant with a positive total amount
        if maxIndexUtil != -1:
            amountToSettle = min(abs(totalAmountList[minIndexUtil].totalAmount), totalAmountList[maxIndexUtil].totalAmount)
            
            # Update settlement transactions
            settlementTransactions[minIndexUtil][maxIndexUtil]['amount'] += amountToSettle
            settlementTransactions[minIndexUtil][maxIndexUtil]['mode'] = maxParticipant[1]
            
            # Update total amounts for the participants involved in the transaction
            totalAmountList[minIndexUtil].totalAmount += amountToSettle
            totalAmountList[maxIndexUtil].totalAmount -= amountToSettle
            
            # Update counts if total amounts become zero
            if totalAmountList[maxIndexUtil].totalAmount == 0:
                numZerototalAmounts += 1

            if totalAmountList[minIndexUtil].totalAmount == 0:
                numZerototalAmounts += 1

        elif maxIndexUtil == -1:
           # Update settlement transactions
            settlementTransactions[minIndexUtil][0]['amount'] += abs(totalAmountList[minIndexUtil].totalAmount)
            settlementTransactions[minIndexUtil][0]['mode'] = next(iter(participants[minIndexUtil].paymentModes))

            # Find a participant with the maximum total amount
            simplemaxIndexUtil = findMaxtotalAmountIndex(totalAmountList, numParticipants)

            # Update settlement transactions
            settlementTransactions[0][simplemaxIndexUtil]['amount'] += abs(totalAmountList[minIndexUtil].totalAmount)
            settlementTransactions[0][simplemaxIndexUtil]['mode'] = next(iter(participants[simplemaxIndexUtil].paymentModes))

            
            # Update total amounts for the participants involved in the transaction
            totalAmountList[simplemaxIndexUtil].totalAmount += totalAmountList[minIndexUtil].totalAmount
            totalAmountList[minIndexUtil].totalAmount = 0
            
            # Update counts if total amounts become zero
            if totalAmountList[simplemaxIndexUtil].totalAmount == 0:
                numZerototalAmounts += 1
            if totalAmountList[minIndexUtil].totalAmount == 0:
                numZerototalAmounts += 1
    
    # Print the settlement transactions
    printDebtSettlementTransactions(settlementTransactions, numParticipants, participants)

# Main program
print("This program reduces the amount of transactions between numerous participants by utilizing various payment methods. To serve as a middleman between parties lacking a common payment method, there is a single central participant who possesses all payment modes.")
numParticipants = int(input("Enter the total number of participants in the transaction:\n"))
participantIndex = {}
participants = [Participant() for _ in range(numParticipants)]

# Input participant information
print("Enter the following information about the participants and transactions:")
print("Participant name, the number of payment modes it has, and the payment modes.")
print("There shouldn't be any spaces in the participant name or payment methods.")

for i in range(numParticipants):

    if i == 0:
        print("Central Participant: ", end="")
    else:
        print("Participant " + str(i) + ": ", end="")

    participants[i].name = input()
    participantIndex[participants[i].name] = i

    numModes = int(input())

    if i == 0:
        maxNumPaymentModes = numModes

    while numModes > 0:
        mode = input()
        participants[i].paymentModes.add(mode)
        numModes -= 1

numTransactions = int(input("Enter the number of transactions:\n"))
transactionAmounts = [[0 for _ in range(numParticipants)] for _ in range(numParticipants)]

# Input transaction information
print("Enter the following information for each transaction:")
print("Debtor Participant, Creditor Participant, and amount")
print("Transactions can take place in any sequence.")

for i in range(numTransactions):

    print(str(i) + "th transaction: ", end="")

    debtor, creditor, amount = input().split()
    amount = int(amount)

    transactionAmounts[participantIndex[debtor]][participantIndex[creditor]] = amount

# Settle debts and print the result
settleDebts(numParticipants, participants, participantIndex, numTransactions, transactionAmounts, maxNumPaymentModes)
