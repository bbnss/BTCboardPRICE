import tkinter as tk
import requests
import random
import time

# Funzione per ottenere il prezzo di Bitcoin dall'API 
def get_btc_price():
    api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(api_url)
    data = response.json()
    return data['bpi']['USD']['rate_float']

# Funzione per aggiornare l'interfaccia con il nuovo prezzo
def update_labels(price):
    price_str = '{:,.2f}'.format(price).replace(',', '')
    digits = [d if d == ',' else int(d) for d in price_str]
    for label, digit in zip(labels[1:], digits):  # Inizia da 1 per saltare il simbolo del dollaro
        label.config(text=str(digit))

# Funzione per l'effetto di rotazione dei numeri per ogni etichetta
def rotate_label(label, index, stop_time):
    if time.time() < stop_time:
        label.config(text=str(random.randint(0, 9)))
        label.after(50, lambda: rotate_label(label, index, stop_time))
    else:
        # Aggiorna l'etichetta con il numero corretto dal prezzo
        if index < len(current_price_str):  # Controlla per evitare errori di indice
            label.config(text=str(current_price_str[index-1]))  # -1 perché il primo elemento è il simbolo del dollaro

def start_rotating():
    global current_price_str
    current_price = get_btc_price()
    current_price_str = '{:,.2f}'.format(current_price).replace(',', '')
    # Avvia la rotazione per ogni etichetta con un tempo di arresto casuale
    for i, label in enumerate(labels[1:], 1):  # Inizia da 1 per saltare il simbolo del dollaro, i inizia da 1 per l'indice corretto
        stop_time = time.time() + random.randint(2, 6)
        rotate_label(label, i, stop_time)
    root.after(60000, start_rotating)    

# Creazione della GUI    
root = tk.Tk()
root.configure(bg='black')
root.overrideredirect(True)

# Imposta le dimensioni della finestra
window_width = 550
window_height = 30

# Ottieni le dimensioni dello schermo
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcola la posizione x e y per centrare la finestra nella parte bassa dello schermo
x = (screen_width - window_width) / 2
y = screen_height - window_height   # Regoli altezza pixel dall'alto Es. - 50 pixel dal basso dello schermo

# Imposta la dimensione della finestra e la posiziona
root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))


labels = []
# Aggiungi un'etichetta per il simbolo del dollaro
dollar_label = tk.Label(root, bg="black", fg="white", font=("Arial", 18), width=6, text="$")
dollar_label.grid(row=0, column=0)
labels.append(dollar_label)

# Aggiungi le etichette per il prezzo
for i in range(1, 9):  # Inizia da 1 per lasciare spazio al simbolo del dollaro
    label = tk.Label(root, bg="black", fg="white", font=("Arial", 18), width=4)
    label.grid(row=0, column=i)
    labels.append(label)

# Pulsante per avviare la rotazione
# update_button = tk.Button(root, text="Aggiorna", command=start_rotating)
# update_button.grid(row=1, column=0, columnspan=9)  # Aggiornato columnspan per includere il simbolo del dollaro

# Variabile globale per memorizzare la stringa del prezzo corrente
current_price_str = ''

# Ottenere il prezzo iniziale e avviare la rotazione
start_rotating()

root.mainloop()
