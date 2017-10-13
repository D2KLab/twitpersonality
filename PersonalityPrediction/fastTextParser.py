def parseData():
    data = {}
    dataset = open("../FastText/dataset.vec", "r", encoding="utf8")
    [num_words, embedding_size] = dataset.readline().split(" ")
    i=1
    print("Reading dataset file...")
    for line in dataset:
        [word, embedding] = line[:-1].split(" ",1)
        data[word] = embedding
        percentage = round( (100*(i/int(num_words))),1 )
        i += 1
        print("  %.1f%% complete" %percentage, end="\r")

        if percentage > 2.0:
            break;

    dataset.close()
    return data
