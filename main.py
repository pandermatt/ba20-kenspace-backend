from word_analytics.word_analytics import generate_cluster

if __name__ == '__main__':
    s_data = generate_cluster()

    words = {}
    for curr in s_data:
        print("title: " + curr.text + "\ncluster: " + str(curr.cluster) + "\n")
        for i in curr.cluster:
            if i in words:
                words[i] = words[i] + 1
            else:
                words[i] = 1
    x = sorted(words.items(), key=lambda kv: kv[1], reverse=True)
    print(x)
