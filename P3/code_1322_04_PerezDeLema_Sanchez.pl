write_log(S) :- open('error_logs.txt', append, Out), write(Out, S), write(Out, '\n'), close(Out).

% EJERCICIO 1

   % P18 (**):  Extract a slice from a list

   % slice(L1,I,K,L2) :- L2 is the list of the elements of L1 between
   %    index I and index K (both included).
   %    (list,integer,integer,list) (?,+,+,?)

   slice([X|_],1,1,[X]).
   slice([X|Xs],1,K,[X|Ys]) :- K > 1, 
      K1 is K - 1, slice(Xs,1,K1,Ys).
   slice([_|Xs],I,K,Ys) :- I > 1, 
      I1 is I - 1, K1 is K - 1, slice(Xs,I1,K1,Ys).


/***************
* EJERCICIO 2. sum_pot_prod/4
*
*	ENTRADA:
*		X: Vector de entrada de numeros de valor real.
*		Y: Vector de entrada de numeros de valor real.
*		Potencia: Numero de valor entero, potencia.
*	SALIDA:
*		Resultado: Numero de valor real resultado de la operacion sum_pot_prod. 
*
****************/
   % EJERCICIO 2

   sum_pot_prod(X, Y, Potencia, Resultado) :- prod(X, Y, Potencia, Resultado), error_pot1(Potencia), error_length1(X, Y) .
   /* Errores */
   error_pot1(Potencia) :- (Potencia < 0 -> write_log('ERROR 2.1 Potencia.')).
   error_length1(X, Y) :- length(X, Lenx), length(Y, Leny), (Lenx =\= Leny -> write_log('ERROR 2.2 Longitud.')).

   prod([], [], _, Sum) :- Sum is 0.
   prod([XX|BX], [YY|BY], Potencia, Resultado) :- prod(BX, BY, Potencia, Sum), Resultado is (XX*YY)**Potencia + Sum.

/***************
* EJERCICIO 3. segundo_penultimo/3
*
*       ENTRADA:
*               L: Lista de entrada de numeros de valor real.
*       SALIDA:
*               X : Numero de valor real. Segundo elemento.
*		Y : Numero de valor real. Penultimo elemento.
*
****************/
   segundo_penultimo(L, X, Y) :- seg_pen(L, X, Y).
   /* Error */
   segundo_penultimo([_], _, _) :- writeln('ERROR 3.1 Longitud'), fail.

   seg_pen([Pen|[_]], _, Y) :- Y is Pen.

   seg_pen([_|[Seg|L]], X, Y) :- X is Seg, seg_pen([Seg|L], _, Y).

/***************
* EJERCICIO 4. sublista/5
*
*       ENTRADA:
*		L: Lista de entrada de cadenas de texto.
*		Menor: Numero de valor entero, indice inferior.
*		Mayor: Numero de valor entero, indice superior.
*		E: Elemento, cadena de texto.
*       SALIDA:
*		Sublista: Sublista de salida de cadenas de texto.
*
****************/
   sublista(L, Menor, Mayor, E, Sublista) :- hacerlista(L, Menor, Mayor, Sublista), not(error1(L, E)), not(error2(L, Menor, Mayor)).
   /* Error */
   error1(L, E)  :- (not(estaE(L, E)) -> write_log('ERROR 4.1 Elemento.')).
   estaE([E|_], E).
   estaE([_|TL], E) :- estaE(TL, E).

   error2(L, Menor, Mayor) :- (Menor > Mayor; Menor < 1; length(L, LenL)), LenL < Mayor, write_log('ERROR 4.2 Indices'), !, fail.


   hacerlista([_|B],Menor,Mayor,S):- Menor>0, Menor<Mayor, hacerlista(B,Menor-1,Mayor-1,S).

   hacerlista([A|B],Menor,Mayor,S):- 0 is Menor, Menor<Mayor, N2 is Mayor-1, S=[A|D], hacerlista(B,0,N2,D).
   hacerlista(_,0,0,[]).



/***************
* EJERCICIO 5. espacio_lineal/4
*
*       ENTRADA:
*               Menor: Numero de valor entero, valor inferior del intervalo.
*               Mayor: Numero de valor entero, valor superior del intervalo.
*               Numero_elementos: Numero de valor entero, numero de valores de la rejilla.
*       SALIDA:
*               Rejilla: Vector de numeros de valor real resultante con la rejilla.
*
****************/

   espacio_lineal_recursiv( _, Mayor, 1, Rejilla):- Rejilla = [Mayor].
   espacio_lineal_recursiv( _, _, 0, Rejilla):- Rejilla = [].
   espacio_lineal_recursiv(Menor, Mayor, Numero_elementos, Rejilla) :- 
   Numero_elementos > 1,
   D is (Mayor-Menor)/(Numero_elementos - 1),
   Numero_elementos2 is Numero_elementos - 1, 
   Menor1 is Menor + D,
   espacio_lineal_recursiv(Menor1, Mayor, Numero_elementos2, Rejilla2),
   Rejilla = [Menor|Rejilla2].
         
   espacio_lineal(Menor, Mayor, _, _):- 
   Menor > Mayor,
   /* Error */
   write_log('ERROR 5.1 Indices.'), !, fail.	
      
   /* Inicializa. */
   espacio_lineal(Menor, Mayor, Numero_elementos, Rejilla) :-
   Menor =< Mayor,
   espacio_lineal_recursiv(Menor, Mayor, Numero_elementos, Rejilla).


/***************
* EJERCICIO 6. normalizar/2
*
*       ENTRADA:
*		Distribucion_sin_normalizar: Vector de numeros reales de entrada. Distribucion sin normalizar.
*       SALIDA:
*		Distribucion: Vector de numeros reales de salida. Distribucion normalizada.
*
****************/
   sum_soporte([], Result) :- Result is 0.
   sum_soporte([A|B], Result) :- 
   sum_soporte(B, Result_2),

   Result is A+Result_2.

   /*Caso base*/
   normalizar_rec([], _, Distribucion) :- Distribucion = [].

   /* Control de errores cuando algun numero es menor o igual al 0 */
   normalizar_rec([A|_], _, _) :- A =< 0, write_log('ERROR 6.1.  Negativos.'), !, fail.

   /*Recursion*/
   normalizar_rec([A|B], Suma, Distribucion):-
   Suma \== 0,
   A_2 is A/Suma,
   normalizar_rec(B, Suma, Distribucion_2),
   Distribucion = [A_2|Distribucion_2].

   /* Inicializa. */
   normalizar(Distribucion_sin_normalizar, Distribucion):- 
   sum_soporte(Distribucion_sin_normalizar, Suma),
   normalizar_rec(Distribucion_sin_normalizar, Suma, Distribucion).

/***************
* EJERCICIO 7. divergencia_kl/3
*
*       ENTRADA:
*		D1: Vector de numeros de valor real. Distribucion.
*		D2: Vector de numeros de valor real. Distribucion.
*       SALIDA:
*		KL: Numero de valor real. Divergencia KL.
*
****************/
   /* Inicializa. */
   divergencia_kl(D1, D2, KL) :- error_control(D1, D2), calculate_divergence_kl(D1, D2, KL).

   error_control(D1, D2) :- not(error_divergence_notDefined(D1, D2)), not(error_divergenceNotDistrib(D1, D2)).
   /* Error */
   error_divergence_notDefined(D1, D2) :- ((find_zeroNegative(D1) ; find_zeroNegative(D2)) -> write_log('ERROR 7.1 Divergencia KL no definida.')).
   find_zeroNegative([HL|_]) :- HL =< 0.
   find_zeroNegative([_|TL]) :- find_zeroNegative(TL).
   /* Error */
   error_divergenceNotDistrib(D1, D2) :- ((not(check_distribution(D1, _)) ; not(check_distribution(D2, _))) -> write_log('ERROR 7.2 Divergencia KL definida solo para distribuciones.')).

   check_distribution(L, E) :- (check_distribution_incr(L, E) ; check_distribution_decr(L, E)).

   /* True if the list follows a increasing distribution */
   check_distribution_incr([HL], HL).
   check_distribution_incr([HL|TL], E) :- check_distribution_incr(TL, PreviousElem), PreviousElem >= HL, E is HL.

   /* True if the list follows a decreasing distribution */
   check_distribution_decr([HL], HL).
   check_distribution_decr([HL|TL], E) :- check_distribution_decr(TL, PreviousElem), PreviousElem =< HL, E is HL.

   calculate_divergence_kl([], [], 0).
   calculate_divergence_kl([H1|T1], [H2|T2], KL) :- calculate_divergence_kl(T1, T2, Sum), KL is Sum + (H1 * log(H1/H2)).


/***************
* EJERCICIO 8. producto_kronecker/3
*
*       ENTRADA:
*		Matriz_A: Matriz de numeros de valor real.
*		Matriz_B: Matriz de numeros de valor real.
*       SALIDA:
*		Matriz_bloques: Matriz de bloques (matriz de matrices) de numeros reales.
*
****************/

   /* Inicializa. */
   producto_kronecker([], _, []).
   producto_kronecker([FilaA|RestoMatrizA], MatrizB, [FilaBloques|RestoMatrizBloques]) :- run_filaA(FilaA, MatrizB, FilaBloques), producto_kronecker(RestoMatrizA, MatrizB, RestoMatrizBloques).
   run_filaA([], _, []).
   /* Error */
   run_filaA([A|_], _, _) :- A < 0, write_log('ERROR 8.1 Elemento menor que cero'), !, fail.
   run_filaA([A|L1], MatrizB, [Bloque|RestoBloques]) :- run_matrizB(A, MatrizB, Bloque), run_filaA(L1, MatrizB, RestoBloques).
   run_matrizB(_, [], []).
   run_matrizB(A, [FilaB|RestoMatrizB], [FilaBloque|RestoFilasBloque]) :- prod_A_fila_B(A, FilaB, FilaBloque), run_matrizB(A, RestoMatrizB, RestoFilasBloque).
   prod_A_fila_B(_, [], []).
   /* Error */
   prod_A_fila_B(_, [B|_], _) :- B < 0, write_log('ERROR 8.1 Elemento menor que cero'), !, fail.
   prod_A_fila_B(A, [B|L2], [C|LBloque]) :- C is A*B, prod_A_fila_B(A, L2, LBloque). 

/***************
* EJERCICIO 9a. distancia_euclidea/3
*
*       ENTRADA:
*               X1: Vector de numeros de valor real. 
*               X2: Vector de numeros de valor real.
*       SALIDA:
*               D: Numero de valor real. Distancia euclidea.
*
****************/

   distancia_euclidea(X1, X2, DistEuclidea) :- sum(X1, X2, Total), DistEuclidea is (Total)^(1/2).
   sum([], [], 0.0).
   sum([A|L1], [B|L2], Total) :- X is (A-B)^2, sum(L1, L2, Sum), Total is Sum+X.

/***************
* EJERCICIO 9b. calcular_distancias/3
*
*       ENTRADA:
*               X_entrenamiento: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector.
*               X_test: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector. Instancias sin etiquetar.
*       SALIDA:
*               Matriz_resultados: Matriz de numeros de valor real donde cada fila es un vector con la distancia de un punto de test al conjunto de entrenamiento X_entrenamiento.
*
****************/
   calcular_distancias(_, [], []).
   calcular_distancias(VectorsEntrenamiento, [VectorT|RestVect], [VectorRst|RestVectRst]) :- calcular_distanciasAUX(VectorsEntrenamiento, VectorT, VectorRst), calcular_distancias(VectorsEntrenamiento, RestVect, RestVectRst).

   calcular_distanciasAUX([], _, []).
   calcular_distanciasAUX([VectorEntrena|RestVectEntrena], VectorT, [Dist|RestDists]) :- distancia_euclidea(VectorEntrena, VectorT, Dist), calcular_distanciasAUX(RestVectEntrena, VectorT, RestDists).

/***************
* EJERCICIO 9c. predecir_etiquetas/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Matriz_resultados: Matriz de numeros de valor real donde cada fila es un vector con la distancia de un punto de test al conjunto de entrenamiento X_entrenamiento.
*       SALIDA:
*               Y_test: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_test.
*
****************/

   predecir_etiquetas(_, _, [], []).
   predecir_etiquetas(Y_entrenamiento, K, [VectDist|RestoVectorsDist], [Etiq|RestoEtiqs]) :- predecir_etiquetas(Y_entrenamiento, K, RestoVectorsDist, RestoEtiqs), predecir_etiqueta(Y_entrenamiento, K, VectDist, Etiq).

/***************
* EJERCICIO 9d. predecir_etiqueta/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Vec_distancias: Vector de valores reales correspondiente a una fila de Matriz_resultados.
*       SALIDA:
*               Etiqueta: Elemento de valor alfanumerico.
*
****************/

   predecir_etiqueta(Y_entrenamiento, K, Vec_distancias, Etiqueta) :- calcular_K_etiquetas_mas_relevantes(Y_entrenamiento, K, Vec_distancias, Etiquetas), calcular_etiqueta_mas_relevante(Etiquetas, Etiqueta).

/***************
* EJERCICIO 9e. calcular_K_etiquetas_mas_relevantes/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Vec_distancias: Vector de valores reales correspondiente a una fila de Matriz_resultados.
*       SALIDA:
*		K_etiquetas: Vector de valores alfanumericos de una distribucion categorica.
*
****************/
   calcular_K_etiquetas_mas_relevantes(Y_entrenamiento, K, Vec_distancias, Etiquetas) :- insert_orden(Vec_distancias, _, Y_entrenamiento, SUS2), redux(SUS2, K, Etiquetas).
   redux(_, 0, []).
   redux([A|L1], K, [A|L2]) :- KNext is K-1, redux(L1, KNext, L2).

   insert_orden([], [], [], []).

   insert_orden([A|B], SUS, [C|D], SUS3) :- insert_orden(B, SUS2, D, SUS4), insert(SUS, A, SUS2, SUS3, C, SUS4).

   insert([A|B], D, [A|C], [E|F], H, [E|I]):- D > A, insert(B, D, C, F, H, I).
   insert([B|C], B, C, [D|E], D, E).

/***************
* EJERCICIO 9f. calcular_etiqueta_mas_relevante/2
*
*       ENTRADA:
*               K_etiquetas: Vector de valores alfanumericos de una distribucion categorica.
*       SALIDA:
*               Etiqueta: Elemento de valor alfanumerico.
*
*****************/

   calcular_etiqueta_mas_relevante(K_etiquetas, Etiqueta) :- calcular_contadores(K_etiquetas, Contadores), last(Contadores, [_,Etiqueta]).
   calcular_contadores_recursive2([], _, Ret) :- Ret is 0.

   /* Recursion. */
   calcular_contadores_recursive2([ElemA|Rest], ElemB, Ret) :- ElemA \== ElemB, calcular_contadores_recursive2(Rest, ElemB, Ret).
   calcular_contadores_recursive2([ElemA|Rest], ElemB, Ret) :- ElemA == ElemB, calcular_contadores_recursive2(Rest, ElemB, Ret1), Ret is Ret1+1.
   calcular_contadores_recursive1(_, [], Ret) :- Ret = [].
   calcular_contadores_recursive1(List, [ElemB|Rest], Ret) :- calcular_contadores_recursive2(List, ElemB, Answer), calcular_contadores_recursive1(List, Rest, Ret1), Ret = [[Answer, ElemB]|Ret1].

   /* Inicia la recursion. */
   calcular_contadores(List, Ret) :- sort(List, ListUniq), calcular_contadores_recursive1(List, ListUniq, Ret1), sort(Ret1, Ret).

   
/***************
* EJERCICIO 9g. k_vecinos_proximos/5
*
*       ENTRADA:
*		X_entrenamiento: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector.
*		Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*		K: Numero de valor entero.
*		X_test: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector. Instancias sin etiquetar.
*       SALIDA:
*		Y_test: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_test.
*
****************/
k_vecinos_proximos(X_entrenamiento, Y_entrenamiento, K, X_test, Y_test) :- calcular_distancias(X_entrenamiento, X_test, Matriz), predecir_etiquetas(Y_entrenamiento, K, Matriz, Y_test).


/***************
* EJERCICIO 9h. clasifica_patrones/4
*
*       ENTRADA:
*		F: Fichero con los patrones a clasificar, disponible en Moodle (iris_patrones.csv).
*		G: Fichero con las etiquetas de los patrones a clasificar, disponible en Moodle (iris_etiquetas.csv).
*		K: Numero de vecinos a considerar (valor entero).
*       SALIDA:
*		tasa_aciertos: Tasa de acierto promediada sobre las iteraciones leave-one-out
*
****************/

llenar_matriz([],_):-!.
llenar_matriz([M|N],[S|O]):-
	M=..L,
        L = [_|S],
        llenar_matriz(N,O).

leer_datos(F,G,M_Instancias,L_Etiquetas) :-
   /**Empiezo leyendo instancias y se convierte en una matriz compatible para KNN**/
   csv_read_file(F, Instancias),
   maplist(assertz,Instancias),
   llenar_matriz(Instancias, M_Instancias),
   /**Luego leo etiquetas que las tengo en una sola fila en un CSV y las pongo como lista para KNN**/
   csv_read_file(G,Etiquetas),
   maplist(assertz,Etiquetas),
   Etiquetas=[Sub1|_],
   Sub1=..Sub2,
   Sub2 = [_|L_Etiquetas],
   !.
    
clasifica_patrones(F,G,K,Tasa_aciertos) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.
clasifica_iris(K, Tasa_aciertos) :- clasifica_patrones('iris_patrones.csv','iris_etiquetas.csv',K,Tasa_aciertos).





/***************
* Ejercicio 10
*
*  fractal xd
****************/
 
   fractal :-
      new(D, window('Fractal')),
      send(D, size, size(1400, 600)),
      drawTree(D, 120, 320, 0, 6),
      send(D, open).
   
   
   drawTree(D, X, Y, Angle, Depth) :- drawTree(D, X, Y, Angle, Depth, 1000, _, _).
   
   drawTree(D, X, Y, Angle, 0, Length, XRET, YRET) :- 
      X2 is X + cos(Angle * pi / 180.0) * Length,
      Y2 is Y + sin(Angle * pi / 180.0) * Length,  
      new(Line2, line(X, Y, X2, Y2, none)),
      send(D, display, Line2),
      XRET = X2, YRET = Y2.

   drawTree(D, X1, Y1, Angle, Depth, Length, XRET, YRET) :-
      New_length is Length/3,
      De is Depth - 1,
      A1 is Angle - 60,
      A2 is Angle + 60,
      drawTree(D, X1, Y1, Angle, De, New_length, X2, Y2),
      drawTree(D, X2, Y2, A1, De, New_length, X3, Y3),
      drawTree(D, X3, Y3, A2, De, New_length, X4, Y4),
      drawTree(D, X4, Y4, Angle, De, New_length, X5, Y5),
      XRET = X5, YRET = Y5.