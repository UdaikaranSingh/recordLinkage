---
title:  Project Checkpoint 3
author: Ittoop Shinu Shibu, Udaikaran Singh, Wesley Kwan
geometry: margin=3cm
header-includes:
    - \usepackage{multicol}
    - \newcommand{\hideFromPandoc}[1]{#1}
    - \hideFromPandoc{
        \let\Begin\begin
        \let\End\end
      }
---



\begin{center}

\textbf{Abstract}

-- Shinu

\end{center}



\Begin{multicols}{2}

# Introduction

-- Shinu

# Methods

## Overview

The pipeline for our model can be fundamentally broken down into 3 major steps: (1) Graph Embedding, (2) Node2Vec, and (3) a traditional machine learning model. The goal of the graph embeddings is to take the data presented within a tabular format, and embed it within a heterogenous graph structure where the nodes represent the entities within the dataset and the features of the dataset. For example, in our implementation, we assigned a unique key to each row of the datasets. These key nodes would then form undirected edges to the features associated to that row within the dataset. The Node2Vec would allow us to embed the nodes of the heterogenous graph within an Euclidean that allows for a more natural mathematical interpretation of similarity. Lastly, this embedding is used as a feature representation for a traditional machine learning model.

## Graph Embedding

For our graph embedding model, we embedded the 

### Ordinal and Categorical Columns

...

### Quantitative Columns

## Node2Vec

...

## Traditional ML Model

### Logistic Regression

...

### Support Vector Machine

...

### Boosted Decision Trees

-- Udai/Wesley

# Results

**Add a table of the results for the different models as well as the baselines**

**Note: leave a placeholder for the space for the larger results.**

-- Udai

# Discussion

-- Udai/Wesley

\End{multicols}

# References

-- Udai/Wesley

# Appendix

-- Everybody