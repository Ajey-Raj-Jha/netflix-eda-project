import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set(style="darkgrid")


#load and explore data
df = pd.read_csv("netflix_titles.csv")
print(df.shape)
print(df.head())
print(df.info())


# data cleaning
# Check for nulls
print(df.isnull().sum())

# Drop rows with missing titles or types (if any)
df.dropna(subset=["title", "type"], inplace=True)

# Fill or drop other missing columns
df['country'].fillna("Unknown", inplace=True)
df['rating'].fillna("Not Rated", inplace=True)
df['duration'].fillna("Unknown", inplace=True)


# Count of Movies vs TV Shows
sns.countplot(data=df, x='type')
plt.title("Distribution of Movies and TV Shows")
plt.show()

# Content Added Over the Years

df['date_added'] = pd.to_datetime(df['date_added'])
df['year_added'] = df['date_added'].dt.year

df['year_added'].value_counts().sort_index().plot(kind='bar', figsize=(12,6))
plt.title("Content Added to Netflix Over the Years")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.show()

#Top 10 Countries Producing Content
top_countries = df['country'].value_counts().head(10)
sns.barplot(y=top_countries.index, x=top_countries.values)
plt.title("Top 10 Countries by Content Volume")
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.show()

#Most Common Genres
from collections import Counter

genre_counts = Counter()
df['listed_in'].dropna().apply(lambda x: genre_counts.update(x.split(', ')))

top_genres = genre_counts.most_common(10)
genres, counts = zip(*top_genres)

sns.barplot(x=list(counts), y=list(genres))
plt.title("Top 10 Genres on Netflix")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
plt.show()
