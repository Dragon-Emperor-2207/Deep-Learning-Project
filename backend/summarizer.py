import requests
def reviews(id):
    url = "https://imdb8.p.rapidapi.com/title/get-user-reviews"
    querystring = {"tconst":id}
    headers = {
	    "X-RapidAPI-Key":"81f06e6ff8msh412817c08531a45p158f86jsn1050cfdaf157",
	    "X-RapidAPI-Host":"imdb8.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    res=response.json()
    for i in range(len(res["reviews"])):
        #print(res["reviews"][i])
        if "authorRating" not in res["reviews"][i].keys():
            with open('./neutral_reviews.txt', 'a', encoding='utf-8') as file:
                x = ':$' + res['reviews'][i]['reviewText']
                file.write(x)
        elif(res["reviews"][i]["authorRating"]>=8):
            with open('./good_reviews.txt', 'a', encoding='utf-8') as file:
                x = ':$' + res['reviews'][i]['reviewText']
                file.write(x)
        elif(res["reviews"][i]["authorRating"]<=7 and res["reviews"][i]["authorRating"]>=6):
            with open('./neutral_reviews.txt', 'a', encoding='utf-8') as file:
                x = ':$' + res['reviews'][i]['reviewText']
                file.write(x)
        elif(res["reviews"][i]["authorRating"]<6):
            with open('./bad_reviews.txt', 'a', encoding='utf-8') as file:
                x = ':$' + res['reviews'][i]['reviewText']
                file.write(x)

def main(id):
  from transformers import pipeline
  import tensorflow as tf
  from transformers import AutoTokenizer, TFAutoModelForCausalLM, TFAutoModelForSequenceClassification, TFAutoModelForSeq2SeqLM
  reviews(id)
  file_path1 = 'good_reviews.txt'
  file_path2 = 'bad_reviews.txt'
  file_path3 = 'neutral_reviews.txt'

  final_summary_good = []
  final_summary_bad = []
  neutral_sammary = ''

  sentiment_input = []
  sentiment_summary = []

  summarizer = pipeline("summarization", model="Falconsai/text_summarization")

  def summary_generator(text,n):

    array= ''
    for i in text:
      summary = summarizer(i, max_length=130, min_length=30, do_sample=False)
      m=summary[0]['summary_text']+ ' '

      if n==1:
        final_summary_good.append(m)

      elif n==2:
        final_summary_bad.append(m)

      else:
        sentiment_summary.append(m)
        sentiment_input.append(i)

  # Initialize the summarization pipeline

  with open(file_path1, 'r', encoding='utf-8') as file:
      text1 = file.read()

  with open(file_path2, 'r', encoding='utf-8') as file:
      text2 = file.read()

  with open(file_path3, 'r', encoding='utf-8') as file:
      text3 = file.read()

  text1=text1[2:]
  text2=text2[2:]
  text3=text3[2:]


  text1=text1.split(':$')
  text2=text2.split(':$')
  text3=text3.split(':$')

  ls=[]

  summary_generator(text1, 1)
  summary_generator(text2, 2)
  summary_generator(text3, 3)

  final_summary_good = ' '.join(final_summary_good)
  final_summary_bad = ' '.join(final_summary_bad)
  c = ' '.join(sentiment_summary)



  def sentiment(input):
    checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = TFAutoModelForSequenceClassification.from_pretrained(checkpoint)

    inputs = tokenizer(input, return_tensors="tf", truncation=True, padding=True, max_length=512)

    outputs = model(inputs)
    logits = outputs.logits
    predictions = tf.nn.softmax(logits)

    predicted_class_id = tf.argmax(predictions, axis=1).numpy()[0]
    class_names = ['negative', 'positive']
    predicted_class_name = class_names[predicted_class_id]

    return predicted_class_name

  for i in range(len(sentiment_input)):
    if(sentiment(sentiment_input[i])=='positive'):
        final_summary_good+=(' ' + sentiment_summary[i])

    else:
        final_summary_bad+=(' ' + sentiment_summary[i])


  # This is the model for the title generation
  from transformers import T5Tokenizer, TFT5ForConditionalGeneration

  def title(text):
      # Load the model and tokenizer for TensorFlow
      model_name = "t5-base"
      tokenizer = T5Tokenizer.from_pretrained(model_name)
      model = TFT5ForConditionalGeneration.from_pretrained(model_name)

      # Prepare the text input by adding the prefix "summarize: "
      input_text = f"summarize: {text}"
      inputs = tokenizer(input_text, return_tensors="tf", max_length=512, truncation=True)

      # Generate output using the model
      summary_ids = model.generate(inputs['input_ids'], num_beams=4, no_repeat_ngram_size=2, min_length=5, max_length=20)
      summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

      return summary

  title1 = title(final_summary_good)
  title2 = title(final_summary_bad)

  summary_dict={'title_good':title1,'title_bad':title2,'good_summary':final_summary_good.replace("\\",""),'bad_summary':final_summary_bad.replace("\\","") }

  # filename = 'summary.json'

  # # Write the dictionary to the file as JSON
  # with open(filename, 'w') as file:
  #     json.dump(summary_dict, file, indent=4)

  from transformers import AutoTokenizer, AutoModel, pipeline
  from transformers import AutoTokenizer, AutoModelForTokenClassification, TokenClassificationPipeline

  text=final_summary_good + final_summary_bad

  def split_into_word_sets(text, max_words=10):
      import re
      # Split text into sentences
      sentences = re.split(r'(?<=[.!?]) +', text)

      sets = []
      current_set = []
      current_word_count = 0

      for sentence in sentences:
          # Count words in the sentence
          words_in_sentence = sentence.split()

          # Check if adding this sentence would exceed the max words
          if current_word_count + len(words_in_sentence) > max_words:
              # If so, start a new set
              sets.append(" ".join(current_set))
              current_set = words_in_sentence
              current_word_count = len(words_in_sentence)
          else:
              # Otherwise, add the words to the current set
              current_set.extend(words_in_sentence)
              current_word_count += len(words_in_sentence)

      # Add the last set if it's not empty
      if current_set:
          sets.append(" ".join(current_set))

      return sets


  ls=[]

  ls= split_into_word_sets(text,50)

  model_name = "QCRI/bert-base-multilingual-cased-pos-english"
  tokenizer = AutoTokenizer.from_pretrained(model_name)
  model = AutoModelForTokenClassification.from_pretrained(model_name)

  pipeline = TokenClassificationPipeline(model=model, tokenizer=tokenizer)

  def postag(text):
    result = pipeline(text)
    return result

  phrases=[]
  final=[]

  def phraseadder(result):
    for i in range(len(result)-1):
      if(result[i]['entity']=='JJ'):
        word=result[i]['word']
        if '#' not in word:
          phrases.append(word)

  for i in ls:
    final.append(postag(i))

  for i in final:
    phraseadder(i)

  from collections import Counter, defaultdict
  import nltk
  from nltk.corpus import wordnet

  nltk.download('wordnet')

  def is_word_in_wordnet(word):
      return bool(wordnet.synsets(word))




  def group_words_by_frequency(words):
      # Count the frequencies of each word
      frequency = Counter(words)

      blacklist=['first','second','third','previous','sequel','prequel','other','many','same','similar','non']
      # Group words by their frequency
      frequency_groups = defaultdict(list)
      for word, count in frequency.items():
          if(word not in blacklist):
            frequency_groups[count].append(word)

      return frequency_groups

  # Example usage:
  words = phrases
  grouped = group_words_by_frequency(words)

  # Print the groups
  for freq, words in sorted(grouped.items()):
      print(f"Frequency {freq}: {words}")

  for i in grouped:
    for j in grouped[i]:
      if(not is_word_in_wordnet(j)):
        grouped[i].remove(j)

  # filename = 'adjectives.json'

  # Write the dictionary to the file as JSON
  # with open(filename, 'w') as file:
  #     json.dump(grouped, file, indent=4)
  print(summary_dict)
  with open(file_path1, mode='w') as f1:
    pass
  with open(file_path2, mode='w') as f1:
    pass
  with open(file_path3, mode='w') as f1:
    pass
  return {'adjectives':grouped,'summaries':summary_dict}
