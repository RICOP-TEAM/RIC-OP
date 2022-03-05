# RIC-OP
Project about research algorithms

------

Si vuole sviluppare una app, destinata ai turisti in arrivo a Ferrara, che pianifica la visita ideale (cosa visitare e in che sequenza) in base alle preferenze del turista, partendo e tornando dal suo albergo.
Dati: 
    -la lista di attrazioni,  
    -il gradimento di ciascuna, 
    -la durata del percorso da un luogo a un altro,  

Bisogna tener conto: 
    -Time Windows: ciascun luogo è accessibile solo durante uno o più intervalli della giornata,  
    -un luogo visitato una seconda volta non fornisce alcun gradimento. 

Si calcoli il tour di massimo gradimento sapendo che il turista ha a disposizione solo h ore.   

------

METODO RISOLUTIVO --> GRASP (Min_Distance_Greedy/Ratio_Greedy + 2-OPT/Double_Bridge)