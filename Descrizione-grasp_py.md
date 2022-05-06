### def satisfaction_calc(tour):
Funzione che viene eseguita dopo che è stato trovato un tour completo (tour). 
Calcola il gradimento (sat) il tempo trascorso (time) per vedere ogni attrazione aperta, invece quando si trova un'attrazione nel tour che risulta in quel momento chiusa si aggiunge anche il tempo di attesa necessario affinchè l'attrazione risulti aperta.
- Viene valutata un'attrazione alla volta.
>Si restituisce una lista(tour) contenente [ [ nodi_visti ],gradimento, tempo]

### def first_op():
Viene costruito un primo percorso da utilizzare come migliore soluzione alla prima iterazione della GRASP.

Per ogni attrazione si valuta se questa è già presente nel tour e se è aperta:  
> - in caso positivo si appende l'attrazione (orario apertura, tempo, indice attrazione) tra i candidati visitabili (candidati); 
> - nel caso in cui l'attrazione non sia aperta si aggiunge anche il tempo che passa fin quando l'attrazione non sarà aperta

Nel caso in cui nessuna delle due condizioni avviene si continua il ciclo fin quando non finiscono le attrazioni.
Successivamente si ordina la lista 'candidati' in ordine crescente a seconda di ora di apertura e tempo percorrenza.
Alla fine di ogni iterazione *while(True)* aggiungo il tempo del candidato scelto e il suo indice.
Il controllo alla #linea-43 serve per verificare se un'altra attrazione presente in 'candidati' può essere inserita nel tour. Se non si possono aggiungere altre attrazioni effettuo la *break*.
Alla fine calcolo il gradimento del tour e restituisco 'seed' che contiene [ tour, gradimento, tempo trascorso ]

#

## Greedy
### def neighborhood(node = 0):
Funzione utilizzata per creare una lista contenente tutti i nodi ordinati in base alla distanza con il nodo in cui ci si trova.
> Restituisce la lista ordinata 'rank' 

### def ratio(node = 0): 
Funzione utilizzata per creare una lista contenente tutti i nodi ordinati in base al rapporto tra gradimento ponderato (il gradimento è suddiviso in categorie) e tempo di percorrenza (in ore).
> Restituisce la lista ordinata 'candidate'
#
## **Local Search**
- ## **2-OPT**
    ### def ls_2_opt(attr_tour):
    Inizialmente viane fatta una *deepcopy* del tour in input, in seguito vengono utilizzati due cicli in cascata per effettuare tutti gli scambi 2-opt validi.
    Infine tramite la funzione *satisfaction_calc* si confrontano il percorso trovato con quello migliore.
    > Si restituisce il percorso con il gradimento maggiore

- ## **Double Bridge**
    ### def ls_double_bridge(attr_tour):
    Inizialmente vengono fatte due *deepcopy* del tour in input, in seguito vengono utilizzati quattro cicli in cascata per effettuare gli scambi.
    Infine, tramite la funzione *satisfaction_calc* si confrontano il percorso trovato con quello migliore.
    > Si restituisce il percorso con il gradimento maggiore

# 
## **Principal Functions**
### def greedy_randomized_adaptive_search_procedure(start_tour, iterations, greediness_value):
Questa è la funzione iniziale che viene lanciata dal programma **"Start.py"**.
In ingresso riceve: una soluzione iniziale (calcolata con la funzione *first_op*), il numero di iterazioni della grasp, un valore compreso tra 0 e 1 che determina quanto l'algoritmo deve essere greedy oppure randomico.
 


### def find_solution(greediness_value, greedy):
    