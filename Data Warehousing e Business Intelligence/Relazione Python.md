Relazione Python - Beatlemania e Data Science
=======
*Marco Bolpagni, Marco Broglio, Andrea Innocenzi, Tommaso Ulivieri*

*Università degli Studi di Roma - Tor Vergata* 

La seguente relazione si inserisce nella cornice più ampia del progetto congiunto di *"DWBI e Text Analytics and Opinion mining"*. Questo documento vuole essere un accompagnamento agli script python prodotti, attraverso l'esposizione delle scelte e dei ragionamenti che vi stanno alla base. 
Per le analisi che abbiamo immaginato è emersa la necessità di reperire dei dati aggiuntivi sui brani (oltre al dato testuale richiesto), nello specifico quelli relativi agli autori del testo e alla popolarità dei brani (ai giorni nostri).

Di seguito sono esposte tre sezioni riguardanti i nostri tre obiettivi:
* Scaricare i testi dell'artista ([AZLyrics Scraper](#azlyrics-scraper))
* Identificare gli autori dei testi ([Compositori secondo Beatlesarchive](#compositori-secondo-beatlesarchive))
* Reperire i dati sulla popolarità ([Spotify API](#spotify-api))

AZLyrics Scraper
-----------

### Obiettivo: 

Eseguire lo scraping web da un sito qualunque pubblico di lyrics di almeno 100 canzoni

### Sito web selezionato: 

Per lo scraping dei testi dei Beatles è stato selezionato [AZLyrics](https://www.azlyrics.com/) in quanto:
* è un sito web statico
* ha una struttura html relativamente semplice
* ha testi di qualsiasi artista, lingua e epoca
* è aggiornato

### Difficoltà riscontrate e soluzioni:

AzLyrcis pone in essere alcune contromisure per contrastare lo scraping, nello specifico blocca le richieste provenienti dai crawler, dalla rete tor e impone un ritmo di navigazione compatibile con il comportamento umano (per esempio non è possibile richiedere un testo al secondo senza incorrere in un blocco).
Per ovviare a queste difficoltà abbiamo deciso di utilizzare la libreria selenium che permette di automatizzare le richieste utilizzando un browser vero e proprio (nel nostro caso Chrome). Per simulare il comportamento umano abbiamo inserito tra la richiesta di un testo e quella successiva una pausa dalla durata casuale all'interno di un range di lettura umano (tra 5 e 20 secondi).

### Come funziona:

Descrizione del funzionamento logico dello scraper:
1. Homepage
    * apre homepage
    * scrive chiave di ricerca nella barra search
    * click bottone search
2. Pagina risultati ricerca
    * trova il box artist results
    * individua il nome corretto dell'artista
    * click sul link dell'artista (porta a lista canzoni)
3. Pagina testi artista
    * individua il titolo e il link di ogni canzone
4. Pagina canzone
    * per ogni canzone apre link
    * individua il testo della canzone
    * individua il nome dell'album e l'anno di uscita
    * individua il nome dei compositori
    
### Approccio e librerie utilizzate:

Per la realizzazione dello scraper è stato utilizzato un approccio basato sul paradigma di programmazione a oggetti per via della sua intrinseca modularità, per la migliore  organizzazione del codice e per garantire la trasferibilità del prodotto finale in altri progetti.

Per lo scraping sono state utilizzate le librerie:
* *Selenium (3.141.0)*
* *Beautifoulsoup (4.9.1)*

### Breve descrizione dei metodi della classe AzLyricsScraper:

La classe AzLyricsScraper si avvale di tre metodi che vengono usati per lo scraping e il salvataggio del dataset:
* *getBasicInfo()*: che permette di reperire le informazioni basilari per lo scraping, ovvero il nome corretto dell'artista, i titoli e i link delle canzoni appartenenti alla discografia.
* *getLyrics()*: che si occupa di recuperare il testo delle canzoni e le informazioni aggiuntive (album di appartenenza, data di rilascio, compositore).
* *dumpCSV()*: che consente il salvataggio in formato csv delle informazioni ottenute dallo scraper

### Funzionalità aggiuntive:

All'interno del codice sono state inserite alcune funzionalità aggiuntive, nello specifico:
* Riconoscimento automatico della lingua del testo con la libreria *langdetect (1.0.8)*
* Gestione degli errori che permette allo scraper di non interrompersi se incontra incosistenze nell'html, ban o problemi di rete. L'utente viene informato al momento del dump del csv delle eventuali problematiche.
* Possibilità di estrarre un campione casuale di testi di un determinato artista
* Opzioni di regolazione della velocità delle richieste effettuate dallo scraper
* Modalità headless opzionale (con simulazione degli header di un browser con fingerprint comune)

### Come si utlizza lo script:

Lo script si può utilizzare direttamente da linea di comando:

`python AzlyricsScraper.py --artist "Beatles"`

E' possibile inoltre specificare argomenti opzionali per la regolare la velocità dello scraping, richiedere l'esecuzione in background o l'estrazione diun campione casuale:

`python AzlyricsScraper.py --artist "Beatles" --sample 10 --minsleep 2 --maxsleep 5 --headless`

### Che dati vengono scaricati:

Il programma realizzato scarica le seguenti informazioni relative ai brani:

* *Artist*: nome dell'artista
* *Year*: anno di rilascio del brano
* *Album*: nome dell'album di appartenenza
* *Title*: titolo della canzone
* *Authors*: compositori del testo
* *Lyric*: testo della canzone
* *Language*: lingua in cui è scritto il testo
* *Links*: link della risorsa su azlyrics

### Note sulla qualità dell'output:

Lo scraper fornisce le tutte le informazioni disponibili in modo corretto, va però notato che non sempre le informazioni fornite da AzLyrics relative all'autore di uno specifico testo sono attendibili.

Compositori secondo Beatlesarchive
-----------

### Obiettivo: 

Scaricare la tabella relativa ai compositori dei vari brani dal sito [beatlesarchive](http://www.beatlesarchive.net/composer-singer-beatles-songs.html) (gestito dai fan) che fornisce un'informazione più precisa rispetto ad azlyrics

### Approccio e librerie utilizzate:

Le informazioni circa i compositori messe a disposizione dal sito beatlesarchive, memorizzate in una tabella html, sono state scaricate utilizzando il metodo *read_html()* della libreria *Pandas* che permette lo scaricamento di tale tabella e la trasformazione in DataFrame.

### Che dati vengono scaricati:

Il programma realizzato scarica i seguenti dati:
* *Song*: nome del brano
* *Main composer*: nome del compositore del testo
* *Singer*: nome del membro del gruppo che canta il brano

Spotify API
-----------

### Obiettivo: 

Ottenere informazioni circa popolarità e caratteristiche sonore dei brani (intera discografia) di un determinato artista.

### Approccio e librerie utilizzate:

Le informazioni circa la popolarità di un brano e le sue caratteristiche sonore possono essere scaricate grazie alle API messe a disposizione gratuitamente da Spotify. Per accedere alle API è necessario registrarsi come sviluppatori sul portale [Spotify for Developers](https://developer.spotify.com/).

Tra le varie librerie python che permettono di dialogare con le API Spotify è stato scelto di utilizzare *Spotipy (2.16.1)*.

### Come funziona:

Prima di spiegare il funzionamento logico del programma è bene precisare che le API Spotify utilizzano l'URI per identificare le risorse da richiedere (artisti, album, canzoni).

In massima sintesi il flusso logico seguito dal programma si può riassumere nei seguenti punti:
1) Creazione della sessione
2) Interrogazione API per trovare l'URI dell'artista dalla chiave di ricerca (nome)
3) Attraverso l'URI dell'artista si interrogano nuovamente le API per trovare URI e nomi degli album pubblicati dell'artista
4) Per ogni album, per ogni canzone: interrogo le API per trovare: nome, caratteristiche audio e popolarità

*Per organizzare i dati è stato creata una classe "song"*

### Come si utlizza lo script:

Lo script si può utilizzare direttamente da linea di comando:

`python SpotifyFeatureDownloader.py --artist "Beatles"`

### Che dati vengono scaricati:

Il programma realizzato scarica le seguenti informazioni relative ai brani:

* *artist*: nome dell'artista
* *name*: nome del brano
* *uri*: uri del brano
* *release_date*: data di rilascio del brano 
* *album*: album di appartenenza del brano
* *track_number*: numero del brano nell'album
* *acousticness*: valore (0<x<1)  che indica se si tratta di un brano acustico (tanto più è ballabile tanto più il valore sarà vicino a 1)
* *danceability*: valore (0<x<1)  che indica il grado di ballabilità di un brano (tanto più è ballabile tanto più il valore sarà vicino a 1)
* *energy*: valore (0<x<1)  che rappresenta la percezione di intensità e attività (tanto più è energica tanto più il valore sarà vicino a 1)
* *instrumentalness*: valore (0<x<1)  che indica se si tratta di un brano strumentale (tanto più è strumentale tanto più il valore sarà vicino a 1)
* *liveness*: valore (0<x<1)  che indica se si tratta di una registrazione di un live (tanto più è live tanto più il valore sarà vicino a 1)
* *loudness*: valore (0<x<1)  che indica la "rumorosità" di una traccia (tanto più è "rumorosa" tanto più il valore sarà vicino a 1)
* *speechiness*: valore (0<x<1)  che indica se si tratta di un brano parlato (tanto più è parlato tanto più il valore sarà vicino a 1)
* *tempo*: valore (0<x<1) che indica i battiti per minuto (BPM)
* *valence*: valore (0<x<1) che indica la positività della traccia. Brani con alta valenza trasmettono emozioni positive(felicità, euforia), al contrario di quelle con bassi valori che trasmettono un mood triste, depresso o rabbioso.
* *popularity*: valore (0<x<100) che indica la popolarità del brano (tanto più è popolare tanto più il valore sarà vicino a 100)
