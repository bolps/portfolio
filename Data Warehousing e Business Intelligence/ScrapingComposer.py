import pandas as pd

# Faccio scraping della tabella con read_html messo a disposizione da pandas
df = pd.read_html('http://www.beatlesarchive.net/composer-singer-beatles-songs.html')
df = pd.concat(df)

# Visualizzo una preview del dataframe
df.head()

# Salvo il dataframe in un file csv
df.to_csv('Composer_Beatles.csv', index=False)
