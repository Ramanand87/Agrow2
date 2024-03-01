from langdetect import detect

text = "कितनी सिंचाई की आवश्यकता है"  # You can replace this with your text
language = detect(text)

print(f"The detected language is: {language}")
print(type(language))
