import pandas as pd
df= pd.read_csv('final_topics1.csv')

from keybert import KeyBERT

# Initialize the model
model = KeyBERT('distilbert-base-nli-mean-tokens')

# Filter the DataFrame based on the condition where score is less than 0.3
filtered_df = df[df['score'] >= 0.3 ]
filtered_df1=filtered_df[filtered_df['score']<=0.7]
# Concatenate the corresponding 'comment' values into a string
concatenated_comments = ' '.join(filtered_df1['comment'])
print(concatenated_comments)



# Extract keywords with 2-grams and a maximum phrase count of 25
keywords = model.extract_keywords(concatenated_comments, keyphrase_ngram_range=(2, 2), stop_words=None, use_maxsum=True, nr_candidates=25)

# Print the extracted keywords
print("Keywords:", keywords)
