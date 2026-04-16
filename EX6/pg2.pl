% item(Name, Price, Quantity)
add_item(Name, Price, Qty) :-
    assertz(item(Name, Price, Qty)),
    write('Item added successfully'), nl.

delete_item(Name) :-
    retract(item(Name, _, _)),
    write('Item deleted'), nl.

increase_qty(Name, Inc) :-
    retract(item(Name, Price, Qty)),
    NewQty is Qty + Inc,
    assertz(item(Name, Price, NewQty)),
    write('Quantity increased'), nl.

decrease_qty(Name, Dec) :-
    retract(item(Name, Price, Qty)),
    NewQty is Qty - Dec,
    NewQty >= 0,
    assertz(item(Name, Price, NewQty)),
    write('Quantity decreased'), nl.

display_bill :-
    write('------- GROCERY BILL -------'), nl,
    write('Item    Price   Qty   Subtotal'), nl,
    show_items,
    grand_total(Total),
    write('-----------------------------'), nl,
    write('Grand Total = '), write(Total), nl.

show_items :-
    item(Name, Price, Qty),
    Subtotal is Price * Qty,
    write(Name), write('     '),
    write(Price), write('     '),
    write(Qty), write('     '),
    write(Subtotal), nl,
    fail.
show_items.

grand_total(Total) :-
    findall(Sub, (item(_,Price,Qty), Sub is Price*Qty), List),
    sum_list(List, Total).

