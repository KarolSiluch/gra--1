Jest to gra stworzona tak naprawdę z nudów. Pracowałem nad nią w wakacje przed pójściem na studia, więc mój sposób pisania kodu trochę się zmienił od tego czasu.

Projekt została stworzona w pythonie, co nie jest raczej częstym wyborem przy tworzeniu gier. Ze wzgędu na niekorzystanie z silnika, każdą najmniejszą funkcjonalność musiałem napisać sam. Zdecydowałem się na takie rozwiązanie, ponieważ znajomość pythona wydaje się użyteczna nie tylko przy gamedevie.

Gra polega na pokonywaniu fal robocików i ostatniego bossa. Po drodze można zdobywać ulepszenia, które w różny sposób zmieniają zachowanie broni.
Nie ma tu samouczka, więc postaram się szybko wytłumaczyć zasady i sterowanie.

Na mapie znajdują się czerwone kamienie, którymi aktywuje się fale przeciwników. Aby oddziaływać z otoczeniem, należy podejść wystarczająco blisko konkretnego przedmiotu i nacisnąć przycisk e.

Po otrzymaniu ulepszenia trzeba je podnieść, otworzyć ekwipunek przyciskiem q i ustawić w jednym z trzech miejsc:
- górny: główny sposób ataku (lewy przycisk myszy)
- środkowy: dodatkowa umiejętność (prawy przycisk myszy)
- dolny: pasywna umiejętność

Nie wszystkie ulepszenia mają zaimplementowane wszystkie 3 właściwości. Da się je umieścić w każdym z miejsc, ale mogą nic nie robić.

Po wyczyszczeniu 5 pięter pojawi się boss.

Sterowanie:
- chodzenie: w, a, s, d
- unik: shift
- ekwipunek: q
- interakcja z otoczeniem: e
- atak: lewy przycisk myszy
- dodatkowa umiejętność: prawy przycisk myszy

Przykładowy gameplay:
https://www.youtube.com/watch?v=LjaWqMJYKeA

Ten projekt był fundamentem dla mojego frameworka, dzięki któremu pisanie przyszłych projektów będzie dużo łatwiejsze.
W zakładce releases znajduje się plik exe z grą. Życzę miłej zabawy.
