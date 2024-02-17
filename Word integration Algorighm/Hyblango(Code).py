import random
from difflib import SequenceMatcher

binary_similarity = []

def similarize(german, dutch):
    pointerf = 0
    german = list(german)
    dutch = list(dutch)
    for i in range(max(len(dutch), len(german))):
        binary_similarity.append(0)                              #set a similarity list based on largest word to avoid EOL errors

    for (german_char, dutch_char, index) in zip(german, dutch, range(len(binary_similarity))):                 #chk from 0th index to right
        if german_char == dutch_char:
            binary_similarity[index] = 1

    for (german_char, dutch_char, index) in zip(reversed(german), reversed(dutch), range(len(binary_similarity) - 1, -1, -1)):                  #chk from -1 index to left
        if german_char == dutch_char:
            binary_similarity[index] = 1

    for i in range(0, len(german), 2):                                                                      #chk from each index to left and right as index size of 2 letters  
        left_index = i
        right_index = min(len(binary_similarity) - i - 1, len(german) - i - 1, len(dutch) - i - 1)

        if left_index < len(german) and right_index >= 0 and left_index < len(dutch):  # making sure both indexes are within range
            if german[left_index] == dutch[left_index]:
                binary_similarity[left_index] += 0.5
                pointerf += 0.5
                if left_index + 1 < len(binary_similarity):
                    binary_similarity[left_index + 1] += 0.5
                    pointerf += 0.5

            if german[right_index] == dutch[right_index]:
                binary_similarity[right_index] += 0.5
                pointerf += 0.5
                if right_index - 1 >= 0:
                    binary_similarity[right_index - 1] += 0.5
                    pointerf += 0.5
    print(binary_similarity)
    initial_similarity = (sum(x for x in binary_similarity) / (len(binary_similarity) + pointerf))
    print(int(initial_similarity * 100), '%')

    if initial_similarity < 0.5:
        print("Not possible to hybridize due to low initial similarity.")
        return False                                                                    #If words are distinct (dog and hund) , they cannot be hybirdized.
    return True                                                                            #but synonmys can be used (hound and hund) is possible :)

def generate_hybrid_word(german, dutch, binary_similarity, unique_words):
    hybrid_word = ""
    while True:
        for sim_score, (german_char, dutch_char) in zip(binary_similarity, zip(german, dutch)):
            if sim_score == 0:
                hybrid_word += random.choice(['', random.choice([german_char, dutch_char])])
            elif sim_score == 2.0:
                hybrid_word += random.choice([german_char, dutch_char])
            else:
                problist = [
                    german_char if random.uniform(0, 1) < (1.0 - sim_score/2.0) else '',
                    dutch_char if random.uniform(0, 1) < (sim_score/2.0) else '',
                ]
                hybrid_word += random.choice(problist)

        if hybrid_word not in unique_words:
            break
        else:
            hybrid_word = ""
    unique_words.add(hybrid_word)
    return hybrid_word
def calculate_similarity(word1, word2):
    len_penalty = abs(len(word1) - len(word2)) / max(len(word1), len(word2))
    similarity_ratio = SequenceMatcher(None, word1, word2).ratio()
    adjusted_similarity = similarity_ratio * (1 - len_penalty)
    return adjusted_similarity

#usage:     (define words beforehand)
german_word = "Schule"
dutch_word = "School"

if not similarize(german_word, dutch_word):
    exit()

# Generate 30 using algorithm
generated_words = set()
for _ in range(30):
    hybrid_word = generate_hybrid_word(german_word, dutch_word, binary_similarity, generated_words)
    if hybrid_word == "":
        break  # Break the loop if unable to generate a hybrid word
    generated_words.add(hybrid_word)

# calculate similarity scores for German, Dutch, and generated words
similarity_scores = [(word, calculate_similarity(german_word, word), calculate_similarity(dutch_word, word)) for word in generated_words]

#ignore if similarity less than 0.6
filtered_similarity_scores = [(word, german_similarity, dutch_similarity) for word, german_similarity, dutch_similarity in similarity_scores if word != german_word and word != dutch_word and german_similarity >= 0.5 and dutch_similarity >= 0.5]

# sorted by highest similarity to both German and Dutch
sorted_similarity_scores = sorted(filtered_similarity_scores, key=lambda x: (x[1] + x[2]), reverse=True)

#print all stuff
for word, german_similarity, dutch_similarity in sorted_similarity_scores:
    print(f"Word: {word}, German Similarity: {german_similarity}, Dutch Similarity: {dutch_similarity}")
#Attention, the words dont have to be specifically dutch or german, but they must contain Latin charachters and must be at least 60% similar
