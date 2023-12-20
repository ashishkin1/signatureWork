# NOTE: for simplicity, you should assume there is a 
# maximum possible word length of 12

def max_word_split(s, d):
    # TODO: this function should be recursive and 
    # ultimately too slow to run on large strings 
    
    counter = []
    max_word_split_helper(s, d, counter)
    return len(counter)

def max_word_split_helper(s, d, c):
    #Base case
    if (len(s) == 0):
        return 0
    #If the substring is in the dictionary
    elif (s in d):
        #check to see if the length of the string is greater than the current count
        #and see if the length of the string is less than 13
        if (len(s) >= len(c)-1 and len(s) < 13):
            #add 1 to the counter
            c.insert(0, 0)
            return 1
        else:
            return 0
    else:
        #for loop to iterate through the whole string
        for i in range(1, len(s)-1):
            #make the string into a substring
            anotherWord = s[:i]
            #recursivly check to see if the substring is a word
            result = max_word_split_helper(anotherWord, d, c)
            #if the substring is a word
            if (result == 1):
                #recursivly call on the final part of the string
                return max_word_split_helper(s[i:len(s)+1], d, c)
    return max_word_split_helper(s[1:len(s)], d, c)




def max_word_split_dp(s, d):
    # TODO: this function should use dynamic programming
    # WITH A TABLE to compute the same answers as the above 
    # recursive function
    # this version only needs to return the NUMBER of words
    
    #set up table
    ans = [0]*(len(s)+1)
    ans[0] = 0
    #For every letter in the string one at a time
    for k in range(1, len(s)+1):
        ans[k] = float('-inf')
        #To check for each possible substrings of k with a max length of 12
        for j in range(13): 
            #We check to see if the length of the substring is at least the
            #length of the current letter we are at
            if (k-j >= 0):
                if (s[(k-j):k] in d):
                    #ans at spot k is max of ans[k] or ans[k-j] + 1
                    ans[k] = max(ans[k], ans[k-j] + 1)  
                    
    print(ans) 
    return ans[len(s)]


# Extra Credit (+5) if you can also return the list of words with dynamic programming
# Do this in a separate function, if you attempt it.

#Recovery attempt DO at home ()

def max_word_split_rec(s, d):
    # TODO: this function should use dynamic programming
    # WITH A TABLE to compute the same answers as the above 
    # recursive function
    # this version only needs to return the NUMBER of words
    
    #set up table
    ans = [0]*(len(s)+1)
    ans[0] = 0
    words = []
    #For every letter in the string one at a time
    for k in range(1, len(s)+1):
        ans[k] = float('-inf')
        #To check for each possible substrings of k with a max length of 12
        for j in range(13): 
            #We check to see if the length of the substring is at least the
            #length of the current letter we are at
            if (k-j >= 0):
                if (s[(k-j):k] in d):
                    #ans at spot k is max of ans[k] or ans[k-j] + 1
                    ans[k] = max(ans[k], ans[k-j] + 1)  
                    if (ans[k] == max(ans)):
                        words.append(s[(k-j):k])
      
    words = wordHelper(s, ans[len(s)], words)
    print(ans)
    print(words)
    return ans[len(s)]

def wordHelper(string, n, words):
    #I need to grab the string
    for i in range(len(words)):
        if string[0] == words[i]:
            for word in words:
                if (word == words[i]):
                    continue
                elif word in words[i]:
                    words.remove(word)
                    if (len(words) == n):
                        return words
                    else:
                        continue
    #Find words that start with the first letter of the string.
    #Once I get that, I iterate through all the words and remove them if they
        #are in the string.
        #I then take the next string, and keep doing it
        #I then check to see if the length of words is now equal to n
            #if it is done, I need to append all the words together
            #I then check to see if once combined, the words == string
            #If it does:
                #return words
            #else:
                #continue
    

# you will need to specify wordfile.txt to test different dictionaries
# go to https://gist.github.com/deekayen/4148741 for one possible list to use

# it's usually a bad idea to use a dictionary file with every possible word, 
# since each letter by itself is considered a word in such files 

f = open('wordfile.txt', 'r')
good_words = set([word.lower().strip() for word in f])

#test cases
#print(str(max_word_split('thereddogdidfinishfirst', good_words))) #6
#print(str(max_word_split('wantaddabovepathneck', good_words)))  # 5
print(str(max_word_split('warmontheat', good_words)))    # 4

#print(str(max_word_split('mandogfinish', good_words)))   #3
#print(str(max_word_split('chickdearoccurnature', good_words)))   #4
#print(str(max_word_split('steamdadglad', good_words))) #3

# assuming the words are in the word list, should be 6 (the_red_dog_did_finish_first)

#print(str(max_word_split('warmontheat', good_words)))
#print(str(max_word_split_dp('warmontheat', good_words)))
# assuming the words are in the word list, should be 4 (warm_on_the_at instead of war_month_eat)



#print(str(max_word_split_rec('warmontheat', good_words)))
#print(str(max_word_split_rec('thereddogdidfinishfirst', good_words)))






