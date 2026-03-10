# -*- coding: utf-8 -*-
"""
Created on Sat Jun  7 11:53:53 2025

Group Code
Harshal Rajesh Kokitkar- D18000067
Mustafa Oner - D18000070
Shwetali Vitthal Bhuingade - D18000073
"""



from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns

uri = "mongodb+srv://harshal:harshal24@cluster0.5ooitkb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
client = MongoClient(uri)
mydb = client['imdb_project']

# Step 3.3: Create or access 'movies' collection
collection_names = [c['name'] for c in mydb.list_collections()]
if 'movies' not in collection_names:
    my_collection = mydb.create_collection('movies')
else:
    my_collection = mydb['movies']

# Step 3.4: Load CSV file
df = pd.read_csv(r"D:\University Of Naples\AVE Sem 2\ML & BD\Project\BD Project\data\imdb_top_1000.csv")


# Step 3.5: Transform each row into MongoDB document
def transform_row(row):
    try:
        year = int(row['Released_Year']) if str(row['Released_Year']).isdigit() else None
    except:
        year = None

    return {
        "title": row['Series_Title'],
        "year": year,
        "certificate": row.get('Certificate', None),
        "runtime_minutes": int(str(row['Runtime']).split()[0]) if pd.notna(row['Runtime']) else None,
        "genre": [g.strip() for g in row['Genre'].split(',')],
        "rating": float(row['IMDB_Rating']),
        "meta_score": float(row['Meta_score']) if pd.notna(row['Meta_score']) else None,
        "director": row['Director'],
        "cast": [row['Star1'], row['Star2'], row['Star3'], row['Star4']],
        "votes": int(row['No_of_Votes']) if pd.notna(row['No_of_Votes']) else None,
        "gross": int(row['Gross'].replace(',', '')) if pd.notna(row['Gross']) else None
    }


documents = df.apply(transform_row, axis=1).tolist()

# Step 3.6: Insert documents into MongoDB
my_collection.delete_many({})  # Optional: Clear old data if rerunning
my_collection.insert_many(documents)
print(f"{len(documents)} IMDb records inserted.")

# Step 3.7: Print confirmation info
print("Databases:", client.list_database_names())
print("Collections in imdb_project:", [c['name'] for c in mydb.list_collections()])

# === Step 4.1: Most Frequent Genres ===
pipeline_genres = [
    {"$unwind": "$genre"},
    {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]

print("Top 10 Most Frequent Genres:")
for doc in my_collection.aggregate(pipeline_genres):
    pprint(doc)



# Extract data for plotting
genres = []
counts = []

print("Top 10 Most Frequent Genres:")
for doc in my_collection.aggregate(pipeline_genres):
    pprint(doc)
    genres.append(doc['_id'])
    counts.append(doc['count'])
    
# Plotting the bar chart
plt.figure(figsize=(10, 6))
plt.bar(genres, counts, color='orange')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.title('Top 10 Most Frequent Genres')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# === Step 4.2: Average Rating per Genre ===
pipeline_avg_rating = [
    {"$unwind": "$genre"},
    {"$group": {"_id": "$genre", "avg_rating": {"$avg": "$rating"}}},
    {"$sort": {"avg_rating": -1}}
]

print("Average IMDb Rating per Genre:")
for doc in my_collection.aggregate(pipeline_avg_rating):
    pprint(doc)

# Lists to store results
genres = []
avg_ratings = []

print("Average IMDb Rating per Genre:")
for doc in my_collection.aggregate(pipeline_avg_rating):
    pprint(doc)
    genres.append(doc['_id'])
    avg_ratings.append(doc['avg_rating'])

# Plotting: vertical bar chart with corrected scale
plt.figure(figsize=(12, 6))
bars = plt.bar(genres, avg_ratings, color='orange')
plt.xlabel('Genre')
plt.ylabel('Average IMDb Rating')
plt.title('Average IMDb Rating per Genre')
plt.ylim(0, 10)  # Set Y-axis scale to typical IMDb rating range
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Optional: add value labels above bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f'{yval:.1f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# === Step 4.3: Most Frequent Directors ===
pipeline_directors = [
    {"$group": {"_id": "$director", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]

print("Top 10 Most Frequent Directors:")
for doc in my_collection.aggregate(pipeline_directors):
    pprint(doc)

# Lists to store results
directors = []
movie_counts = []

print("Top 10 Most Frequent Directors:")
for doc in my_collection.aggregate(pipeline_directors):
    pprint(doc)
    directors.append(doc['_id'])
    movie_counts.append(doc['count'])

# Plotting: vertical bar chart
plt.figure(figsize=(12, 6))
bars = plt.bar(directors, movie_counts, color='orange')
plt.xlabel('Director')
plt.ylabel('Number of Movies')
plt.title('Top 10 Most Frequent Directors')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add count labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.3, f'{yval}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# === Step 4.4: Most Popular Actors (by Appearances) ===
pipeline_actors = [
    {"$unwind": "$cast"},
    {"$group": {"_id": "$cast", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]

print("Top 10 Most Frequent Actors:")
for doc in my_collection.aggregate(pipeline_actors):
    pprint(doc)

# Lists to store actor names and counts
actors = []
counts = []

print("Top 10 Most Frequent Actors:")
for doc in my_collection.aggregate(pipeline_actors):
    pprint(doc)
    actors.append(doc['_id'])
    counts.append(doc['count'])

# Plotting: vertical bar chart
plt.figure(figsize=(12, 6))
bars = plt.bar(actors, counts, color='orange')
plt.xlabel('Actor')
plt.ylabel('Number of Appearances')
plt.title('Top 10 Most Frequent Actors')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Add count labels above each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.3, f'{yval}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# === Step 4.5: Correlation Between Rating and Gross Revenue ===
import pandas as pd

docs = list(my_collection.find({"gross": {"$ne": None}}, {"_id": 0, "rating": 1, "gross": 1}))
df = pd.DataFrame(docs)

correlation = df["rating"].corr(df["gross"])
print("Correlation between IMDb rating and gross revenue:", round(correlation, 3))

# Calculate correlation
correlation = df["rating"].corr(df["gross"])
print("Correlation between IMDb rating and gross revenue:", round(correlation, 3))

# Plotting: scatter plot with regression line
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x="rating", y="gross", scatter_kws={"alpha": 0.6}, line_kws={"color": "red"})
plt.xlabel("IMDb Rating")
plt.ylabel("Gross Revenue")
plt.title("Correlation Between IMDb Rating and Gross Revenue")
plt.grid(True)
plt.tight_layout()
plt.show()





