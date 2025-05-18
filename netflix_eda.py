import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import Counter

# Set seaborn style
sns.set(style="darkgrid")

# Create output folder if it doesn't exist
if not os.path.exists("output"):
    os.makedirs("output")

# Load the dataset with latin1 encoding
df = pd.read_csv("netflix_titles.csv", encoding="latin1")

# Data Cleaning
df.dropna(subset=["title", "type"], inplace=True)
df['country'] = df['country'].fillna("Unknown")
df['rating'] = df['rating'].fillna("Not Rated")
df['duration'] = df['duration'].fillna("Unknown")

# Convert 'date_added' to datetime without format to allow flexible parsing
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Extract year from 'date_added'
df['year_added'] = df['date_added'].dt.year

# Summary Statistics
total_titles = len(df)
num_movies = df[df['type'] == 'Movie'].shape[0]
num_shows = df[df['type'] == 'TV Show'].shape[0]

years = df['year_added'].dropna()
earliest_year = int(years.min()) if not years.empty else 'Unknown'
latest_year = int(years.max()) if not years.empty else 'Unknown'

top_country = df['country'].value_counts().idxmax()
unique_countries = df['country'].nunique()

genre_counts = Counter()
df['listed_in'].dropna().apply(lambda x: genre_counts.update(x.split(', ')))
top_genre, top_genre_count = genre_counts.most_common(1)[0]

print(f"Total titles: {total_titles}")
print(f"Movies: {num_movies} ({num_movies/total_titles:.1%}), TV Shows: {num_shows} ({num_shows/total_titles:.1%})")
print(f"Content added from {earliest_year} to {latest_year}")
print(f"Most content produced by: {top_country} (among {unique_countries} countries total)")
print(f"Top genre on Netflix: {top_genre} with {top_genre_count} titles")

# Save summary to a text file
with open("output/summary.txt", "w") as f:
    f.write(f"Total titles: {total_titles}\n")
    f.write(f"Movies: {num_movies} ({num_movies/total_titles:.1%}), TV Shows: {num_shows} ({num_shows/total_titles:.1%})\n")
    f.write(f"Content added from {earliest_year} to {latest_year}\n")
    f.write(f"Most content produced by: {top_country} (among {unique_countries} countries total)\n")
    f.write(f"Top genre on Netflix: {top_genre} with {top_genre_count} titles\n")

# === Plots ===

plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='type')
plt.title("Movies vs TV Shows")
plt.xlabel("Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("output/type_distribution.png")
plt.close()

df_years = df.dropna(subset=['year_added'])

if df_years.empty:
    print("No valid dates to plot content added per year.")
else:
    year_count = df_years['year_added'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    year_count.plot(kind='bar')
    plt.title("Content Added Per Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Titles")
    plt.tight_layout()
    plt.savefig("output/content_by_year.png")
    plt.close()

top_countries = df['country'].value_counts().head(10)
plt.figure(figsize=(8, 6))
sns.barplot(x=top_countries.values, y=top_countries.index)
plt.title("Top 10 Countries by Content Volume")
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("output/top_countries.png")
plt.close()

top_genres = genre_counts.most_common(10)
genres, counts = zip(*top_genres)
plt.figure(figsize=(8, 6))
sns.barplot(x=list(counts), y=list(genres))
plt.title("Top 10 Genres on Netflix")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig("output/top_genres.png")
plt.close()

print("✅ Analysis complete! All plots saved in the 'output' folder and summary.txt created.")
