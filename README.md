# RIC-OP
>***Project about research algorithms***


Si vuole sviluppare una app, destinata ai turisti in arrivo a Ferrara, che pianifica la visita ideale (cosa visitare e in che sequenza) in base alle preferenze del turista, partendo e tornando dal suo albergo.

**DATI:** 
- *la lista di attrazioni*,  
- *il gradimento di ciascuna*, 
- *la durata del percorso da un luogo a un altro*.

<br />

Bisogna tener conto: 
- **Time Windows**: ciascun luogo è accessibile solo durante uno o più intervalli della giornata,  
- un luogo visitato una seconda volta **non fornisce alcun gradimento**. 

<br />

>***Si calcoli il tour di massimo gradimento sapendo che il turista ha a disposizione solo h ore.***  

<br />


<br />

## METODO RISOLUTIVO: 
    1)      GRASP with exaustive local search
    2)      GRASP with stock-VNS
    3)      (1) + Path Relinking
    4)      (2) + Path Relinking