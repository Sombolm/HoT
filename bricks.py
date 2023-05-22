import sys
# import time
from collections import Counter


def end():
    print("klops")
    exit(0)

# klasa wrapper
class Instructions:
    def __init__(self):
        # kontenery
        self.instructions = {}
        self.box = Counter()

        # zmienne do zliczania danych
        self.blocksUsed = 0
        self.blocksMissing = 0
        self.buildingsBuilt = 0
        self.buildingsNotBuilt = 0

    # dodaje klocek do pudelka
    def fillBox(self, block):
        self.box[block] += 1

    # dodaje instrukcje do kontenera
    def addInstruction(self, instruction):
        index, block = instruction
        self.instructions.setdefault(index, []).append(block)

    # buduje budynek
    def buildBuilding(self, index):
        instruction = self.instructions[index]
        removedBlocks = []
        flag = False
        for block in instruction:
            if self.box[block] >= 1:
                self.box[block] -= 1
                removedBlocks.append(block)
            else:
                flag = True
                self.blocksMissing += 1

        # jezeli nie udalo sie zbudowac budynku
        if flag:
            # wkladam klocki spowrotem do pudelka
            for block in removedBlocks:
                self.box[block] += 1
            self.buildingsNotBuilt += 1
            return

        self.buildingsBuilt += 1
        self.blocksUsed += len(instruction)


def readInput(instructions):
    # set na instrukcje podzielne przez 3
    todo = set()
    # przetwarzanie strumienia wejsciowego
    for line in sys.stdin:
        line = line.strip()
        if line:
            line = line.split(":")
            if line[0].isdecimal():
                number = int(line[0])
                block = line[1].strip(";")
                # walidacja danych
                if 0 <= number and len(block) == 4 and all('A' <= b <= 'O' for b in block) and block.isupper():
                    if number == 0:
                        instructions.fillBox(block)
                    elif (all(b != "O" for b in block)):
                        instructions.addInstruction((number, block))
                        if number % 3 == 0:
                            todo.add(number)
                    else:
                        end()
                else:
                    end()
            else:
                end()

    todo = sorted(todo)
    instructions.instructions = {k: instructions.instructions[k] for k in sorted(instructions.instructions)}

    for index in todo:
        instructions.buildBuilding(index)
        # po wybudowaniu moge usunac wykonane instrukcje co nieco przyspieszy faze druga
        instructions.instructions.pop(index)


# faza druga, budowanie budynkow o niskim priorytecie
def secondPhase(instructions):
    for instruction in instructions.instructions:
        instructions.buildBuilding(instruction)


def displayStats(instructions, usedBlocksPhaseOne):
    print(str(usedBlocksPhaseOne))
    print(str(instructions.blocksUsed))
    print(str(sum(instructions.box.values())))
    print(str(instructions.blocksMissing))
    print(str(instructions.buildingsBuilt))
    print(str(instructions.buildingsNotBuilt))


def main():
    instructions = Instructions()

    # readInput polaczylem z faza pierwsza, mimo dodatkowego seta todo jest to szybsze niz dwukrotne iterowanie po instrukcjach
    readInput(instructions)
    # pobieram liczbe uzytych klockow w fazie pierwszej i zeruje licznik
    usedBlocksPhaseOne = instructions.blocksUsed
    instructions.blocksUsed = 0
    # druga faza
    secondPhase(instructions)
    # wyswietlanie statystyk
    displayStats(instructions, usedBlocksPhaseOne)


if __name__ == "__main__":
    # start = time.process_time()
    main()
    # end = time.process_time()
    # print("Execution time: ", end - start)
