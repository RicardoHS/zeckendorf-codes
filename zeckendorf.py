from itertools import takewhile 
import sys
import math

def __gzeck(k, first=1, second=1): 
    a, b = first, second
    while True: 
        yield b 
        a, b = b, a + b*k 

#return a descomposition in terms of general fibonacci's series using the zeckendorf theorem as [value, multiplier]
def GZeck(k,n): 
    for f in reversed(list(takewhile(lambda f: f <= n, __gzeck(k)))): 
        if f <= n: 
            for i in reversed(range(1,k+1)):
                if f*i <= n:
                    n -= f*i
                    yield [f,i]

#same as GZeck but the return value is [index, multiplier]
def __GZeck(k,n):
    if n == 1:
        yield [0,1]
    descomposition = list(reversed(list(takewhile(lambda f: f <= n, __gzeck(k)))))
    for f in descomposition: 
        if f <= n: 
            for i in reversed(range(1,k+1)):
                if f*i <= n:
                    n -= f*i
                    yield [list(reversed(descomposition)).index(f), i]

def numToByte(n):
    return format(n, '08b')

def byteToNum(n):
    return int(n,2)

#get the given number as a GZeck compressed binary representation
def compressNumAsGZeck(k,n):
    indexes = list(reversed(list(__GZeck(k,n))))
    compressedByte = ""
    numBitsPerIndex = int(math.ceil(math.log(k+1,2)))
    for i in range(indexes[-1][0]+1):
        indexesIndex = list(indexes[x][0] for x in range(len(indexes)))
        if i in indexesIndex:
            compressedByte += format(indexes[indexesIndex.index(i)][1],'0'+str(numBitsPerIndex)+'b')
        else:
            compressedByte += format(0,'0'+str(numBitsPerIndex)+'b')
    return compressedByte

def compressFileAsGZeck(f, k=6, output='', valueFit=96, maxValueToCompress=255):
    numBitsPerIndex = int(math.ceil(math.log(k+1,2)))
    if (output == ''):
        output=f+'.gzk' + str(k)

    compressedBytes = ""
    finalWord=''
    for i in range(numBitsPerIndex):
        finalWord += '1'

    with open(f, "rb") as f:
        byte = f.read(1)
        while byte != "":
            # Do stuff with byte.
            compressedBytes += compressNumAsGZeck(k,((ord(byte)-valueFit)%maxValueToCompress)+    1)
            #compressedBytes += compressNumAsGZeck(k,(ord(byte)+1))
            compressedBytes += finalWord
            byte = f.read(1)
    
    with open (output, "wb") as f:
        while len(compressedBytes)%8 != 0:
            compressedBytes+='0'
        arrayToWrite = [compressedBytes[i:i+8] for i in range(0, len(compressedBytes), 8)] 
        f.write(bytearray([byteToNum(i) for i in arrayToWrite]))

def getDecompressionMatrix(k, n, first=1, second=1):
    matrix = []
    a, b = first, second 
    while b<=n: 
        matrix.append(b) 
        a, b = b, a + k*b
    return matrix


def decompressNum(k, n, decompressionMatrix):
    numBitsPerIndex = int(math.ceil(math.log(k+1,2)))
    decompressedNum=0
    for i in range(len(n)/numBitsPerIndex):
        decompressedNum+=decompressionMatrix[i]*byteToNum(n[i*numBitsPerIndex:(i*numBitsPerIndex)+numBitsPerIndex])
    return decompressedNum

#TODO (fin de palabra si se encuentra an=k y an-1!=0 )
def decompressFileAsGZeck(f, k=6, output="", valueFit=96,maxValueToDecompress=255):
    numBitsPerIndex = int(math.ceil(math.log(k+1,2)))
    if(output == ''):
        output = f + ".d"

    dMatrix = getDecompressionMatrix(k,2**8)
    compressedBytes=""
    with open(f, "rb") as f:
        byte = f.read(1)
        while byte != "" :
            compressedBytes += numToByte(ord(byte))
            byte = f.read(1)

    compressedNum=""
    decompressedFile=""
    nullWordFlag=True
    nullWord=''
    finalWord=''
    for i in range(numBitsPerIndex):
        finalWord+='1'
        nullWord+='0'

    for i in [ compressedBytes[a:a+numBitsPerIndex] for a in range(0,len(compressedBytes),numBitsPerIndex) ]:
        if i == finalWord and nullWordFlag == False:
            decompressedNum = decompressNum(k,compressedNum, dMatrix)
            decompressedFile+=chr(((decompressedNum+valueFit-1) % maxValueToDecompress))
            #decompressedFile+=chr(decompressedNum-1) 
            compressedNum=""
            nullWordFlag=True
            continue
        else:
            compressedNum+=i

        if i == nullWord:
            nullWordFlag=True
        else:
            nullWordFlag=False

    with open(output, "wb") as f:
        f.write(decompressedFile)
        f.write('\n')

