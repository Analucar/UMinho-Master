//*** CIRCUITO EULERIANO ***

// MODELO DE DOMÍNIO

sig Nodo {
    aresta : set Nodo,
    var visitado: set Nodo
}

var one sig NodoInicial in Nodo{}
var one sig NodoAtual in Nodo{}


// FACTOS DO SISTEMA

fact {

    //as arestas são bidirencionais
    aresta = ~aresta      

    //toda os nodos tem de estar conectados
    all n : Nodo | Nodo in n.^aresta

}

// MODELAÇÃO COMPORTAMENTAL
fact Init {

    some Nodo
    no visitado
    one n: Nodo | NodoAtual = n and NodoInicial = n

}

pred circuito[n: Nodo]{

    //Guards
    n in NodoAtual.aresta 
    NodoAtual not in n.visitado

    //Effects
    NodoAtual' = n
    visitado' = visitado + NodoAtual->n + n->NodoAtual
    
    //Frame Conditions
    NodoInicial' = NodoInicial
}

pred nop{

    //guards
    visitado = aresta
    NodoAtual = NodoInicial

    //Frame Conditions
    NodoInicial' = NodoInicial
    NodoAtual' = NodoAtual
    visitado' = visitado
}

fact Traces{
    always {
        nop or
        (some n: Nodo| circuito[n]) 
    }
}


run {
    //o grafo tem de ser completo
    aresta = Nodo -> Nodo - iden

}for exactly 5 Nodo, 20 steps