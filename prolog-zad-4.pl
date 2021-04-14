regula([dobre_finanse,dobra_reputacja],dac_kredyt).
regula([dobra_plynnosc,dobra_rentownosc],dobre_finanse).
regula([nie_karany],dobra_reputacja).
regula([zle_finanse],nie_dac_kredytu).
regula([zle_reputacja],nie_dac_kredytu).
regula([zla_plynnosc],zle_finanse).
regula([zla_rentownosc],zle_finanse).
regula([karany],zla_reputacja).
prawda(dobra_plynnosc).
prawda(dobra_rentownosc).
prawda(nie_karany).

wnioskuj([]).
wnioskuj([X|TX]):-prawda(X),wnioskuj(TX).
wnioskuj([X|TX]):-regula(X,Y),wnioskuj(Y),wnioskuj(TX).