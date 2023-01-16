## <center> <<< *User manual* >>> </center>


*A simple file compressor(archiver) using two popular lossless methods: LZW and Huffman coding.* 

### *The application in short*

It is managed by the command prompt and can operate with files choosing one of the 
mentioned above methods. 
To run the application you have to know the path to the source and the preferred method you want 
to use (Huffman/huff or LZW/lzw). What actions to be done is automatically detected by the application
in dependency of file extension, if it is ".dar" then decompress action is applied, if something 
else - compress.

![img.1](/images/img_1.jpg)

Of course there is a help option if you forget something in the syntax.

![img.2](/images/img_2.jpg)

When you finish the compression final information is displayed, so you'll know what was the size 
of the original file, what is the current size and the time for doing the operation. 

![img.3](/images/img_3.jpg)

In decompression mode there is only info for the taken time.

![img.4](/images/img_4.jpg)

### *Tests*

1. **Testing console input:**\
   1.1. ***ID*** -  ARCH_Test_001\
   1.2. ***Description:*** when user input correct commands and data from console the archiver should make 
   compression and return "File compressed !". If there is incorrect parameter it should return
   "I can't handle with this."\
   1.3. ***Results:*** PASSED, FAILED\
   1.4. ***Algorithm:***
      - Start the program using the described way in the manual and test_text.txt as test file: \
   ***python.exe .\archiver_app.py --comp huff --src examples/test_text.txt***
      - Wait for archiver respond - if data is valid it should display "Please wait..." message while
      algorithm is working and final data as described in the end of work.
2. **Test work of archiver with Huffman compression**\
   2.1. ***ID*** -  ARCH_Test_002\
   2.2. ***Description:*** using input console user enters "huff" as compression and after the 
   program logic is finished "File compressed !" message is displayed plus exit data for compression 
   ratio and the time taken for operation.\
   2.3. ***Results:*** PASSED, FAILED\
   2.4. ***Algorithm:***
      - Start the program using the described way in the manual and test_text.txt as test file: \
   ***python.exe .\archiver_app.py --comp huff --src examples/test_text.txt***
      - Wait for archiver respond - if data is valid it should display "Please wait..." message while
      algorithm is working and final data as described in the end of work.
3. **Test work of archiver with LZW compression**\
   3.1. ***ID*** -  ARCH_Test_003\
   3.2. ***Description:*** using input console user enters "lzw" as compression and after the 
   program logic is finished "File compressed !" message is displayed plus exit data for compression 
   ratio and the time taken for operation.\
   3.3. ***Results:*** PASSED, FAILED\
   3.4. ***Algorithm:***
      - Start the program using the described way in the manual and test_text.txt as test file: \
   ***python.exe .\archiver_app.py --comp lzw --src examples/test_text.txt***
      - Wait for archiver respond - if data is valid it should display "Please wait..." message while
      algorithm is working and final data as described in the end of work.
4. **Test work of archiver with random symbols**\
   4.1. ***ID*** -  ARCH_Test_004\
   4.2. ***Description:*** using test scenario module in "Archiver input.py" file to make a random
       generated string simulating "White noise". Expected low compression rate or a new file bigger 
       than the source.\
   4.3. ***Results:*** PASSED, FAILED\
   4.4. ***Algorithm:***
      - Open file "Archiver_input.py" and uncomment the part under the comment "Use this part for 
   "White noise" simulation". This is a simple generator of random symbols based on ASCII table.
   Uncomment and the part under "Unlock this part when want to test compress and lock it when 
   decompress", made to create a new test file named "sample.txt" with content generated before.
   The part under "Unlock this when want to decompress" should stay commented.
5. **Test work of archiver with one or many symbols with equal probability to exist in the string**\
   5.1. ***ID*** -  ARCH_Test_005\
   5.2. ***Description:*** using test scenario module in "Archiver input.py" file to make a string 
   simulating "Constant signal". Expected high compression rate.\
   5.3. ***Results:*** PASSED, FAILED\
   5.4. ***Algorithm:***
      - Open file "Archiver_input.py" and uncomment the part under the comment "For use in generic 
   way". In the string you can specify what to be written and how many times to be reproduced. 
   For the purposes of "Constant signal" and best representation of this, you should write only one 
   symbol or one symbol repeated many times, for example "A" or "A" * 15000.
   Uncomment and the part under "Unlock this part when want to test compress and lock it when 
   decompress", made to create a new test file named "sample.txt" with content generated before.
   The part under "Unlock this when want to decompress" should stay commented.
6. **Test work of archiver with random, user generated string**\
   6.1. ***ID*** -  ARCH_Test_006\
   6.2. ***Description:*** using test scenario module in "Archiver input.py" file to make custom 
   string simulating you can write your own string and choose how many times to be repeated, making 
   fast and easy '.txt' file with different size. \
   6.3. ***Results:*** PASSED, FAILED\
   6.4. ***Algorithm:***
      - Open file "Archiver_input.py" and uncomment the part under the comment "For use in generic 
   way". In the string you can specify what to be written and how many times to be reproduced.
   Uncomment and the part under "Unlock this part when want to test compress and lock it when 
   decompress", made to create a new test file named "sample.txt" with content generated before.
   The part under "Unlock this when want to decompress" should stay commented.



### *A little bit theory.....*

1. **Huffman Coding** is a technique of compressing data to reduce its size without losing any of the
details. It was first developed by David Huffman. Huffman Coding is generally useful to compress the
data in which there are frequently occurring characters. First all the string is observed and a tree
is made based on the frequency of each character in it. For decoding the code, we can take the code 
and traverse through the tree to find the character. 
   * Huffman coding is used in conventional compression formats like GZIP, BZIP2, PKZIP, etc. 
   * For text and fax transmissions.

2. **Lempel–Ziv–Welch (LZW) Algorithm**  is a very common compression technique. 
It is lossless, meaning no data is lost when compressing. The algorithm is simple to implement and 
has the potential for very high throughput in hardware implementations. The Idea relies on 
reoccurring patterns to save data space. LZW is the foremost technique for general-purpose data 
compression due to its simplicity and versatility. It is the basis of many PC utilities that claim 
to “double the capacity of your hard drive”. 
   * *LZW compression works* by reading a sequence of symbols,
grouping the symbols into strings, and converting the strings into codes. Because the codes take up
less space than the strings they replace, we get compression. Characteristic features of LZW 
includes, LZW compression uses a code table, with 4096 as a common choice for the number of table 
entries. Codes 0-255 in the code table are always assigned to represent single bytes from the input 
file. When encoding begins the code table contains only the first 256 entries, with the remainder of
the table being blanks. Compression is achieved by using codes 256 through 4095 to represent 
sequences of bytes. As the encoding continues, LZW identifies repeated sequences in the data and 
adds them to the code table. Decoding is achieved by taking each code from the compressed file and 
translating it through the code table to find what character or characters it represents.
    * *Implementation* - The idea of the compression algorithm is the following: as the input data is 
being processed, a dictionary keeps a correspondence between the longest encountered words and a 
list of code values. The words are replaced by their corresponding codes and so the input file is 
compressed. Therefore, the efficiency of the algorithm increases as the number of long, repetitive 
words in the input data increases.
    * This algorithm compresses repetitive sequences of data very well. Since the codewords are 
12 bits, any single encoded character will expand the data size rather than reduce it.
    * *This algorithm is typically used* in GIF and optionally in PDF and TIFF. Unix’s ‘compress’ 
command, among other uses.  It is the algorithm of the widely used Unix file compression utility 
compress and is used in the GIF image format.

3. **Advantages of LZW over Huffman:**
    1. LZW requires no prior information about the input data stream.
    2. LZW can compress the input stream in one single pass.
    3. Another advantage of LZW is its simplicity, allowing fast execution and better compression rate.

### References:

https://www.programiz.com/dsa/heap-sort \
https://www.geeksforgeeks.org/lzw-lempel-ziv-welch-compression-technique
https://github.com/bhrigu123/huffman-coding
https://github.com/adityagupta3006/LZW-Compressor-in-Python

