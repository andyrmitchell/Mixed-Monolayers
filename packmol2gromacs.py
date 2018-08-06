# packmol2gromacs.py -- Version 1.0
# Written by Andy Mitchell, Amaro Lab, UCSD CAICE 8/2018

# This script takes a PACKMOL-generated PDB file and fixes it to fit GROMACS style.

# This involves adding residue names, deleting chain designations, and changing the
# atomic naming convetions for water

# Takes the script name, the PACKMOL pdb file, and the name of the file to be generated as input

from sys import argv
script, inputFile, outputFile = argv

# Field variables

# List to hold PACKMOL-assigned chain designations
oldChainList = []

# List to hold user-input residue designations
newResidueList = []

# Create a list to contain all PACKMOL chain names.
# This list will be fed to the user so that he/she can name each residue

# Open the file to which the new file will be written
newFile = open(outputFile, "w+")

# Loop through the PACKMOL output file
for line in open(inputFile):

    # Assign the characters in each line to a list
    characters = list(line)
    
    # Identify ATOM lines
    if  characters[0] == "A":
    
        # Identify the PACKMOL-assigned chain character
        chainName = "".join(characters[21])
        
        # Assume the chain character is not a member of the current oldChainList
        matchIndicator = 0
        
        # Add the chain character if the list is empty
        if len(oldChainList) == 0:
            oldChainList.append(chainName)

        # If the list is nonempty, scroll through the list and determine if it already contains the chain character
        else:
            for item in oldChainList:
                if chainName == item:
                    matchIndicator =+ 1

            # If no match is found, add the chain character to the list
            if matchIndicator == 0:
                oldChainList.append(chainName)

            # If a match is found, reset the match counter for the next loop
            else:
                matchIndicator = 0

# Create a list in parallel that contains the user's given replacement chain names

# Ask for a replacement for each chain

for item in oldChainList:

    # Ask for user inputs for residue names, not to exceed four characters
    while True:
        newResidueName = input("Label the residue denoted by chain " + item.strip() + " : ")
        if (len(newResidueName) > 4):
            print ("Residue name must not exceed 4 characters in length.")
            continue
        else:
            break
    newResidueList.append(newResidueName)

# Replace the old chain names with new residue names to match GROMACS format

# Scan each line of the PACKMOL file
for line in open(inputFile):
    
    # Put the characters into a list
    characters = list(line)
    
    # Identify ATOM lines
    if characters[0] == "A":
    
        # Reference the list of old chains to determine which residue name to insert into the line
        for n in range (0, len(oldChainList)):
        
            # Identify the chain, residue, and atom designation in each ATOM line
            oldChain = "".join(characters[21])
            oldResidue = "".join(characters[17:21])
            atomFlag = "".join(characters[12:15])
            
            # If the atom flag is a PACKMOL water atom, rename it to fit GROMACS conventions
            if atomFlag == " OH":
                atomFlag = "OH2"
            if atomFlag == "1HH":
                atomFlag = "H1 "
            if atomFlag == "2HH":
                atomFlag = "H2 "
            
            # If the atom flag is an incorrectly formatted ion, fix it
            if atomFlag == "Na ":
                atomFlag = "SOD"
            if atomFlag == "Cl ":
                atomFlag = "CLA"
            
            
            # Write a new, GROMACS-friendly line containing the new residue designation to the new file
            if oldChain == oldChainList[n]:
                line = ("".join(characters[0:12]) + " " + atomFlag + " " + newResidueList[n].ljust(4) + " " + "".join(characters[22:76]) + "\n")
                newFile.write(line)

    # If not an ATOM line, copy the line to the new file
    else:
        newFile.write(line)

