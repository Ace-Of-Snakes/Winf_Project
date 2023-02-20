# # make a random array and plot it
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_xlim(0, 2*np.pi)
# ax.set_ylim(-1, 1)

# x = np.arange(0, 2*np.pi, 0.01)
# line, = ax.plot(x, np.sin(x))

# def animate(i):
#     line.set_ydata(np.sin(x + i/10.0))  # update the data
#     return line,

# ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=True)
# plt.show()
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the German version of the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer(lexicon_file="GERVaderLexicon.txt")

# Define a function to get the sentiment score of a word
def get_sentiment(word, analyzer):
    return analyzer.polarity_scores(word).get('compound', 0.0)

# Example usage
text = "Ich liebe dieses Restaurant. Das Essen ist fantastisch!"
words = text.lower().split()
sentiment_scores = [get_sentiment(word, analyzer) for word in words]
print(sentiment_scores)  # Output: [0.6369, 0.0, 0.0, 0.0, 0.5707, 0.0]

