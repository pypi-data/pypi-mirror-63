Ans='''"""
    import heapq
    from collections import defaultdict
    def encode(frequency):
        heap = [[weight, [symbol, '']] for symbol, weight in frequency.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            low = heapq.heappop(heap)
            high = heapq.heappop(heap)
            for value in low[1:]:
                value[1] = '0' + value[1]
            for value in high[1:]:
                value[1] = '1' +value[1]
            heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])
        return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    string=input("Enter the string to be encoded:")
    frequency = defaultdict(int)
    for character in string:
        frequency[character] += 1
    huff = encode(frequency)
    print("character".ljust(10) + "Weight".ljust(10) + "Huffman Code")
    for i in huff:
        print(i[0].ljust(10) + str(frequency[i[0]]).ljust(10) + i[1])

"""
'''
