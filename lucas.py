from itertools import takewhile
import sys

#get the given number as a byte representation
def numToByte(n):
    return format(n, '08b')

def byteToNum(n):
    return int(n,2)

def __fibonacci(first, second):
    a, b = first, second
    while True:
        yield b
        a, b = b, a + b

#get the given number n in terms of lucas numbers, lucas matrix is [2,1,3,4,7,11...]
def Lucas(n):
    lucasList = list(reversed(list(takewhile(lambda f: f <= n, __fibonacci(2,1)))))
    lucasList.insert(-1,2)
    for f in lucasList:
        if f <= n:
            n -= f
            yield f

def __NLucas(n):
    descomposition = list(reversed(list(takewhile(lambda f: f <= n, __fibonacci(2,1)))))
    descomposition.append(2)
    for f in descomposition:
        if f <= n:
            if n == 2 :
                n-=f
                yield 0
            else:
                n -= f
                yield list(reversed(descomposition)).index(f)

def getDecompressionMatrix(n, first=0, second=1):
    matrix = []
    a, b = first, second
    while b<=n:
        matrix.append(b)
        a, b = b, a + b
    matrix.pop(0)
    return matrix

def decompressNum(n, decompressionMatrix):
    decompressedNum=0
    try:
        for i in range(len(n)):
            if n[i] == '1':
                decompressedNum+=decompressionMatrix[i]
    except IndexError:
        print "ERROR: Value out of range."
        raise
    return decompressedNum


#the compress matrix is [2, 1, 3, 7, 11, ...]
def compressNumAsLucas(n):
    indexes = list(reversed(list(__NLucas(n))))
    compressedByte = ""
    for i in range(indexes[-1]+1):
        if i in indexes:
            compressedByte += '1'
        else:
            compressedByte += '0'
    return compressedByte

def compressFileAsLucas(f, output='', maxValueToCompress=255, valueFit=96):
    if (output == ''):
        output=f+'.lc'

    compressedBytes = ""

    with open(f, "rb") as f:
        byte = f.read(1)
        while byte != "":
            # Do stuff with byte.
            compressedBytes += compressNumAsLucas(((ord(byte)-valueFit)%maxValueToCompress)+1)
            compressedBytes += "1"
            byte = f.read(1)

    with open (output, "wb") as f:
        arrayToWrite = [compressedBytes[i:i+8] for i in range(0, len(compressedBytes), 8)]
        f.write(bytearray([byteToNum(i) for i in arrayToWrite]))

def decompressFileAsLucas(f, output="", maxValueToDecompress=255, valueFit=96):
    if(output == ''):
        output = f[:-3] + ".ld"

    dMatrix = getDecompressionMatrix(maxValueToDecompress,first=2,second=1)
    dMatrix.insert(0,1)
    dMatrix.insert(0,2)
    compressedBytes=""
    with open(f, "rb") as f:
        byte = f.read(1)
        while byte != "" :
            compressedBytes += numToByte(ord(byte))
            byte = f.read(1)

    compressedNum=""
    endNumFlag = False
    decompressedFile=""
    for i in compressedBytes:
        if i == '1' :
            if endNumFlag == False:
                endNumFlag = True
                compressedNum += i
            else:
                try:
                    decompressedNum = decompressNum(compressedNum, dMatrix)
                    decompressedFile+=chr(((decompressedNum+valueFit-1) % maxValueToDecompress))
                except:
                    print "Ignoring char"
                compressedNum=""
                endNumFlag = False
        else:
            endNumFlag = False
            compressedNum+=i

    with open(output, "wb") as f:
        f.write(decompressedFile)
        f.write('\n')

