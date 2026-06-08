import os
import heapq
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:

    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}

    def build_frequency_table(self, text):
        return Counter(text)

    def build_heap(self, frequency):
        heap = []

        for char, freq in frequency.items():
            heapq.heappush(heap, Node(char, freq))

        return heap

    def build_huffman_tree(self, heap):

        while len(heap) > 1:

            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = Node(None,
                          left.freq + right.freq)

            merged.left = left
            merged.right = right

            heapq.heappush(heap, merged)

        return heap[0]

    def generate_codes(self, node, code=""):

        if node is None:
            return

        if node.char is not None:
            self.codes[node.char] = code
            self.reverse_codes[code] = node.char

        self.generate_codes(node.left, code + "0")
        self.generate_codes(node.right, code + "1")

    def compress(self, text):

        encoded_text = ""

        for char in text:
            encoded_text += self.codes[char]

        return encoded_text

    def decompress(self, encoded_text):

        current_code = ""
        decoded_text = ""

        for bit in encoded_text:

            current_code += bit

            if current_code in self.reverse_codes:
                decoded_text += self.reverse_codes[current_code]
                current_code = ""

        return decoded_text


def compression_ratio(original_file, compressed_file):

    original_size = os.path.getsize(original_file)

    compressed_size = os.path.getsize(compressed_file)

    ratio = ((original_size - compressed_size)
             / original_size) * 100

    return ratio


def main():

    input_path = "input_files/sample.txt"

    with open(input_path,
              "r",
              encoding="utf-8") as file:

        text = file.read()

    huffman = HuffmanCoding()

    frequency = huffman.build_frequency_table(text)

    print("\nFrequency Table:\n")

    for char, freq in frequency.items():
        print(repr(char), ":", freq)

    heap = huffman.build_heap(frequency)

    root = huffman.build_huffman_tree(heap)

    huffman.generate_codes(root)

    print("\nHuffman Codes:\n")

    for char, code in huffman.codes.items():
        print(repr(char), "->", code)

    compressed_text = huffman.compress(text)

    compressed_file = "compressed_files/compressed.bin"

    with open(compressed_file, "w") as file:
        file.write(compressed_text)

    decompressed_text = huffman.decompress(compressed_text)

    output_file = "decompressed_files/restored.txt"

    with open(output_file,
              "w",
              encoding="utf-8") as file:
        file.write(decompressed_text)

    ratio = compression_ratio(input_path,
                              compressed_file)

    print("\nCompression Ratio:",
          round(ratio, 2), "%")

    print("\nCompression Successful")

    if text == decompressed_text:
        print("Verification Passed")
    else:
        print("Verification Failed")


if __name__ == "__main__":
    main()