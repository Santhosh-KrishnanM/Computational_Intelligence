% Gender
male(shantanu).
male(bhishma).
male(vichitravirya).
male(pandu).
male(dhritarashtra).
male(vidura).
male(yudhishthira).
male(bhima).
male(arjuna).
male(nakula).
male(sahadeva).
male(duryodhana).
male(karna).
male(abhimanyu).

female(ganga).
female(satyavati).
female(ambika).
female(ambalika).
female(kunti).
female(madri).
female(gandhari).
female(draupadi).
female(subhadra).

% Parent Relationships
parent(shantanu, bhishma).
parent(ganga, bhishma).

parent(shantanu, vichitravirya).
parent(satyavati, vichitravirya).

parent(vichitravirya, dhritarashtra).
parent(ambika, dhritarashtra).

parent(vichitravirya, pandu).
parent(ambalika, pandu).

parent(vichitravirya, vidura).

% Pandavas
parent(pandu, yudhishthira).
parent(kunti, yudhishthira).

parent(pandu, bhima).
parent(kunti, bhima).

parent(pandu, arjuna).
parent(kunti, arjuna).

parent(pandu, nakula).
parent(madri, nakula).

parent(pandu, sahadeva).
parent(madri, sahadeva).

% Kauravas
parent(dhritarashtra, duryodhana).
parent(gandhari, duryodhana).

% Others
parent(kunti, karna).

parent(arjuna, abhimanyu).
parent(subhadra, abhimanyu).


% Father & Mother
father(X,Y) :- parent(X,Y), male(X).
mother(X,Y) :- parent(X,Y), female(X).

% Child
child(X,Y) :- parent(Y,X).

% Siblings
sibling(X,Y) :-
    parent(P,X),
    parent(P,Y),
    X \= Y.

% Brother & Sister
brother(X,Y) :- sibling(X,Y), male(X).
sister(X,Y) :- sibling(X,Y), female(X).

% Grandparent
grandparent(X,Y) :-
    parent(X,Z),
    parent(Z,Y).

% Husband & Wife
husband(X,Y) :-
    parent(X,C),
    parent(Y,C),
    male(X),
    X \= Y.

wife(X,Y) :-
    husband(Y,X).

% Uncle & Aunt
uncle(X,Y) :-
    brother(X,Z),
    parent(Z,Y).

aunt(X,Y) :-
    sister(X,Z),
    parent(Z,Y).

% Cousins
cousin(X,Y) :-
    parent(A,X),
    parent(B,Y),
    sibling(A,B),
    X \= Y.




---------- OUTPUT -------------
?- consult(blood).
true.

?- father(pandu,arjuna).
true .

?- mother(X,yudhishthira).
X = kunti.

?- grandparent(shantanu,X).
X = dhritarashtra ;
X = pandu ;
X = vidura.

?- sibling(arjuna,X).
X = yudhishthira ;
X = bhima ;
X = nakula ;
X = sahadeva ;
X = yudhishthira ;
X = bhima ;
X = karna.

?- father(arjuna,pandu).
false.

?- cousin(yudhishthira,X).
X = duryodhana .
---------------------------

