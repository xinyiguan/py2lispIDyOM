---
title: 'py2lispIDyOM: A Python package for IDyOM'
tags:
    - Python
    - IDyOM
    - music cognition
authors:
    - name: Xinyi Guan
      orcid: 0000-0002-4570-906X
      affiliation: 1
    - name: Zeng Ren
      orcid: 0000-0002-9097-2633
      affiliation: 2
    - name: Claire Pelofi
      orcid: 0000-0001-5960-8174
      affiliation: 1
    
affiliations:
 - name: Max Planck NYU Center for Language, Music and Emotion, New York, NY 10003 USA
   index: 1
 - name: Digital and Cognitive Musicology Lab, École Polytechnique Fédérale de Lausanne, Lausanne, VD 1015 Switzerland
   index: 2
   
date: 20 May 2022
bibliography: paper.bib
---


# Statement of need

Music is a complex, multi-layered signal that displays structures along a variety of dimensions - among which melodic and rhythmic sequences play a crucial role across styles and cultures [@PearceWiggins2006]. Empirical studies have consistently demonstrated that listeners have strong and well-defined musical predictions [@Margulis2005, @Morgan2019] that reflect the long-range statistical regularities present in the music they have heard across their lifespan. These statistics are learned through passive exposure to the music in everyday life [@Bigand2006, @Eerola2009, @Rohrmeier2011].

The Information Dynamics of Music (IDyOM) has been a well-established computational model for melodic expectation in the music cognition community and has been empirically tested in various studies. Based on variable-order Markov models [@Pearce2005, @Pearce2018], IDyOM simulates listeners’ expectations while listening to music. It operates by learning the statistical structure over n-orders of note sequences presented in MIDI format. Its long-term component is trained on a large musical corpus and its short-term component dynamically learns the local statistics of a melody, simulating long-term learning of musical statistics and short-term learning of musical patterns respectively. 

For each note in a melody, IDyOM outputs a probability derived by merging the long-term and short-term distributions. From this distribution, two information-theoretic measures characterize the predictions of the model. Surprisal (or Information Content) represents the expectedness (i.e. the note predicted matched the note heard) of each note given the long term (corpus statistics) and short term (melody statistics) context. Entropy corresponds to the degree of uncertainty of the prediction being made. Entropy and surprisal are intended to simulate listeners' dynamical updating expectations–their predictions–when listening to music.

Although the model has been firmly established as a powerful tool to model listener’s experience, the Common Lisp ecosystem, in which the IDyOM model is built in, entails a significant entry barrier for researchers who intend to use the model. On the one hand, Common Lisp is a fairly niche programming language for data analysis and gathers a rather small community of users in the music psychology and music cognition. On the other hand, to use the IDyOM model, it is assumed that users, who are often new to the Lisp language, are familiar with Emacs and SLIME, which themselves can take up a lot of time and energy to learn. Therefore, obtaining the IDyOM outputs can be discouraging and time consuming.

As a result, to help researchers further bring insights in the music cognition domain, we introduce the `py2lispIDyOM` package which aims to fill this gap by providing an easy-to-use Python-based interface to run IDyOM model and harness the extensive support libraries in Python to conduct IDyOM-based analysis. With `py2lispIDyOM`,  we reduce the challenge of writing Lisp codes and hide the complexities of the necessary interactions with Lisp in Emacs from the users. 


# Summary
`py2lispIDyOM` serves as a unifying Python interface that simplifies and streamlines the research workflow for running the IDyOM model and analyzing output data. It is broadly aimed at researchers conducting IDyOM-based analysis. 

Running an IDyOM experiment in `py2lispIDyOM` usually consists of the following main steps: (i) running the IDyOM model, (ii) post-IDyOM data processing and analysis (optional). While this package is not meant to be a Python-implementation of the model, to use `py2lispIDyOM`,  users will have to go through the IDyOM installation process to have it installed in the local machine. For post-IDyOM data processing and analysis, we implemented three modules: `extract`, `export`, and `visualization`. Each module contains methods that we frequently used in our previous research projects. For example, in the `visualization` module, we included several types of figures as shown below. The package includes tutorials in the form of Jupyter notebooks on the github repository. These tutorials demonstrate the usage of the aforementioned functionalities.

![pitch-pred-chor-003{fig:pitch-pred-chor-003}](pitch-pred-chor-003.png){width=50%}

![groundtruth-surprisal-chor-003{fig:groundtruth-surprisal-chor-003}](groundtruth-surprisal-chor-003.png){width=50%}

![all-surprisals-chor-003.png{fig:all-surprisals-chor-003.png}](all-surprisals-chor-003.png.png){width=50%}

![surprisal-entropy-chor-003{fig:surprisal-entropy-chor-003}](surprisal-entropy-chor-003.png){width=50%}


Finally, to improve the reproducibility of data, running an IDyOM experiment with `py2lispIDyOM` will trigger the generation of an experiment log folder which automatically records all data and parameters used in that experiment. This logger serves as an IDyOM experiment repository that can be shared with other researchers to verify and replicate the experiment results. 


`py2lispIDyOM` has been used in several ongoing research projects at the Max Planck - NYU Center for Language, Music and Emotion. Therefore, we hope this package can bring similar values to other research groups working on IDyOM-based analysis.



# References
