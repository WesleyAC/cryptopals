#!/usr/bin/env python3

import codecs

# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == "__main__":
    for line in open("data.txt").readlines():
        cyphertext = codecs.decode(line.strip(), "hex")
        chunked = list(chunks(cyphertext, 16))
        if len(chunked) != len(set(chunked)):
            print(codecs.encode(cyphertext, "hex"))
