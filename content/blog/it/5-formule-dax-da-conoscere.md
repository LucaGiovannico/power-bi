---
slug: 5-formule-dax-da-conoscere
lang: it
title: 5 formule DAX da conoscere davvero in Power BI
card_title: 5 formule DAX da conoscere davvero
description: Cinque formule DAX fondamentali per lavorare meglio in Power BI, con esempi pratici su CALCULATE, FILTER, SUMX, DIVIDE e SELECTEDVALUE.
card_description: Cinque formule e pattern DAX che ricorrono spesso nei modelli Power BI, spiegati con esempi pratici.
category: DAX
date: 2026-10-24
reading_time: 7
image: ../assets/images/blog/5-formule-dax-da-conoscere.png
image_alt: Visual editoriale DAX con cinque formule fondamentali per Power BI
image_fit: contain
featured: false
published: true
---

Imparare DAX non significa memorizzare decine di funzioni.

Nella maggior parte dei modelli Power BI, alcune formule e alcuni pattern ricorrono molto più spesso di altri. Capirli bene permette di costruire misure più leggibili, gestire correttamente il contesto di filtro e affrontare calcoli che vanno oltre una semplice somma.

In questo articolo vediamo cinque funzioni DAX particolarmente utili: CALCULATE, FILTER, SUMX, DIVIDE e SELECTEDVALUE.

Non sono le uniche da conoscere, ma rappresentano una base molto solida per comprendere il modo in cui DAX ragiona.

## 1. CALCULATE: modificare il contesto del calcolo

CALCULATE è probabilmente una delle funzioni più importanti di DAX.

Il suo ruolo è valutare un'espressione modificando il contesto di filtro in cui quella stessa espressione viene calcolata.

Supponiamo di avere già una misura:

```DAX
Total Sales =
SUM(
    Sales[Sales Amount]
)
```

e di voler calcolare soltanto le vendite relative al mercato italiano:

```DAX
Sales Italy =
CALCULATE(
    [Total Sales],
    Customer[Country] = "Italy"
)
```

La misura di partenza non cambia. È CALCULATE che modifica il contesto nel quale viene valutata, applicando il filtro sul paese.

Questo principio è alla base di moltissimi calcoli DAX: confronti tra periodi, percentuali sul totale, KPI filtrati, analisi per segmento e misure che devono ignorare o sostituire determinati filtri.

Il punto importante è quindi non leggere CALCULATE semplicemente come una funzione che aggiunge una condizione.

CALCULATE permette di controllare il contesto nel quale una misura viene valutata.

## 2. FILTER: costruire condizioni più articolate

FILTER restituisce una tabella contenente soltanto le righe che rispettano una determinata condizione.

Può essere utile quando il filtro necessario non può essere espresso in modo sufficientemente semplice oppure quando bisogna valutare una condizione riga per riga.

Per esempio, possiamo calcolare le vendite relative alle sole transazioni superiori a 1.000:

```DAX
High Value Sales =
CALCULATE(
    [Total Sales],
    FILTER(
        Sales,
        Sales[Sales Amount] > 1000
    )
)
```

FILTER scorre la tabella indicata, valuta la condizione per ogni riga e restituisce soltanto le righe che la soddisfano.

È una funzione molto potente, ma proprio per questo non dovrebbe essere utilizzata automaticamente ogni volta che serve applicare un filtro.

Quando CALCULATE può utilizzare direttamente una semplice espressione booleana, quella soluzione è spesso più chiara.

FILTER diventa particolarmente utile quando la logica è più complessa, quando bisogna lavorare su una tabella derivata oppure quando la condizione richiede una valutazione riga per riga.

La distinzione è importante perché scrivere DAX efficace non significa soltanto ottenere il risultato corretto, ma anche costruire misure comprensibili e mantenibili.

## 3. SUMX: calcolare un'espressione riga per riga

SUM e SUMX possono sembrare simili, ma rispondono a esigenze differenti.

SUM somma direttamente i valori presenti in una colonna.

SUMX, invece, è una funzione iteratrice: valuta un'espressione per ogni riga di una tabella e successivamente somma i risultati ottenuti.

Immaginiamo di avere quantità, prezzo unitario e costo unitario e di voler calcolare il margine complessivo:

```DAX
Gross Margin =
SUMX(
    Sales,
    Sales[Quantity]
        * (
            Sales[Unit Price]
            - Sales[Unit Cost]
        )
)
```

Per ogni riga della tabella Sales viene calcolato il margine della singola transazione. Solo dopo questi risultati vengono sommati.

Questo rende SUMX particolarmente utile quando il valore che ci interessa non esiste già come colonna pronta da sommare.

Lo stesso principio può essere applicato a ricavi calcolati, costi, margini, valori ponderati e molti altri indicatori.

Comprendere le funzioni iteratrici è un passaggio importante nello studio di DAX perché introduce chiaramente il concetto di row context.

## 4. DIVIDE: gestire i rapporti in modo più robusto

Dashboard e report contengono continuamente rapporti tra misure: margine percentuale, conversion rate, incidenza sul totale, crescita, tassi e altri KPI.

Una divisione potrebbe essere scritta utilizzando semplicemente l'operatore `/`.

In molti casi, però, DIVIDE rende il calcolo più robusto perché gestisce direttamente la situazione in cui il denominatore è zero o vuoto.

Per esempio:

```DAX
Conversion Rate =
DIVIDE(
    [Orders],
    [Leads]
)
```

Se `[Leads]` è zero o BLANK, DIVIDE restituisce BLANK per impostazione predefinita invece di costringerci a costruire manualmente un controllo sul denominatore.

È anche possibile specificare un risultato alternativo:

```DAX
Conversion Rate =
DIVIDE(
    [Orders],
    [Leads],
    0
)
```

In questo caso, quando la divisione non può essere eseguita, la misura restituisce zero.

La scelta tra BLANK e zero non è soltanto tecnica.

In un report può cambiare l'interpretazione del dato: zero significa che il KPI ha effettivamente valore zero, mentre BLANK può indicare che non esistono le condizioni necessarie per calcolarlo.

Anche una funzione apparentemente semplice come DIVIDE contribuisce quindi a rendere le misure più affidabili e semanticamente corrette.

## 5. SELECTEDVALUE: utilizzare le selezioni dell'utente

SELECTEDVALUE è particolarmente utile nei report interattivi.

Restituisce il valore di una colonna quando, nel contesto corrente, è presente un solo valore distinto. Se invece non esiste una selezione univoca, può restituire un valore alternativo.

Per esempio:

```DAX
Selected Region =
SELECTEDVALUE(
    Geography[Region],
    "Multiple regions"
)
```

Se l'utente seleziona una sola regione, la misura restituisce il nome di quella regione.

Se vengono selezionate più regioni, oppure il contesto non identifica un singolo valore, viene restituito il testo `Multiple regions`.

Questo pattern è molto utile per creare titoli dinamici, messaggi contestuali e indicatori che reagiscono alle selezioni effettuate negli slicer.

Per esempio, una card potrebbe mostrare quale area geografica si sta analizzando oppure un titolo potrebbe cambiare automaticamente in base al segmento selezionato.

SELECTEDVALUE aiuta quindi a collegare la logica DAX all'esperienza di utilizzo del report.

## Cosa cambia davvero nel lavoro quotidiano

Queste cinque funzioni coprono problemi differenti, ma insieme permettono di affrontare una parte significativa dei calcoli che ricorrono nei normali progetti Power BI.

CALCULATE permette di controllare il contesto di filtro.

FILTER consente di costruire subset di dati quando la condizione diventa più articolata.

SUMX permette di valutare espressioni riga per riga.

DIVIDE rende più robusti rapporti e percentuali.

SELECTEDVALUE consente alle misure di reagire in modo più intelligente alle selezioni dell'utente.

Il vero salto di qualità arriva quando si smette di pensare alle funzioni come elementi isolati e si inizia a combinarle.

Una misura reale può utilizzare CALCULATE insieme a FILTER, basarsi su un risultato ottenuto con SUMX oppure modificare il proprio comportamento in funzione di una selezione recuperata con SELECTEDVALUE.

È in queste combinazioni che DAX diventa uno strumento di modellazione analitica, non soltanto un linguaggio per scrivere formule.

## In sintesi

Per lavorare bene con DAX non serve conoscere immediatamente ogni funzione disponibile.

È molto più utile comprendere a fondo alcuni concetti fondamentali e imparare a riconoscere quando utilizzarli.

CALCULATE è essenziale per comprendere il filter context. FILTER permette di costruire condizioni più articolate. SUMX introduce il lavoro riga per riga. DIVIDE rende più affidabili rapporti e percentuali. SELECTEDVALUE collega invece il calcolo al contesto selezionato dall'utente.

Padroneggiare questi cinque strumenti non significa aver imparato tutto DAX, ma significa avere una base concreta per leggere, scrivere e soprattutto ragionare su misure Power BI più strutturate.