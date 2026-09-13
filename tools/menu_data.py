# -*- coding: utf-8 -*-
"""
menu_data.py — the full ~70-cocktail list used to build the two PDF menus.

EVERYTHING HERE IS A PLACEHOLDER. The cocktails, descriptions and ingredients
are invented but realistic; replace them with your real list, then run:

    python tools/make-pdf.py

Each entry is:
    ("Cocktail name",
     "English description", "English ingredients",
     "Serbian description",  "Serbian ingredients")

Cocktail names stay the same in both languages, the way drink names normally
travel. Only the prose is translated.
"""

BRAND = "Shake&Steer"

# Cover / front-matter copy, per language
FRONT = {
    "en": {
        "tagline": "Craft cocktails, poured where you celebrate.",
        "doc_title": "The Full Cocktail Menu",
        "edition": "Placeholder edition — replace before printing",
        "intro_title": "About this list",
        "intro": (
            "Everything on the following pages can be made at your event. A "
            "typical evening uses five to eight of these drinks; we help you "
            "choose them around your guests, your venue and the time of year. "
            "Every syrup, cordial and infusion listed here is made by hand in "
            "our own workshop, and every drink has an alcohol-free counterpart "
            "if you want one."
        ),
        "contents": "Contents",
        "drinks": "drinks",
        "ingredients": "Ingredients",
        "page": "Page",
        "back_title": "Let's build your menu",
        "back_text": (
            "Tell us the date, the venue and roughly how many guests you "
            "expect, and we will come back with a menu drafted for that one "
            "evening — usually within two working days."
        ),
        "back_note": "Please enjoy responsibly. 18+",
        "placeholder_note": "REPLACE: contact details below",
    },
    "sr": {
        "tagline": "Vrhunski kokteli, tačno tamo gde slavite.",
        "doc_title": "Kompletan koktel meni",
        "edition": "Probno izdanje — zamenite pre štampe",
        "intro_title": "O ovoj listi",
        "intro": (
            "Sve sa narednih stranica možemo da pripremimo na vašem događaju. "
            "Tipično veče koristi pet do osam ovih pića; pomažemo vam da ih "
            "izaberete prema gostima, prostoru i dobu godine. Svaki sirup, "
            "kordijal i infuzija sa ove liste prave se ručno u našoj radionici, "
            "a svako piće ima i bezalkoholnu verziju ako je poželite."
        ),
        "contents": "Sadržaj",
        "drinks": "pića",
        "ingredients": "Sastojci",
        "page": "Strana",
        "back_title": "Da sastavimo vaš meni",
        "back_text": (
            "Recite nam datum, prostor i otprilike koliko gostiju očekujete, i "
            "vraćamo se sa menijem napisanim baš za to veče — obično u roku od "
            "dva radna dana."
        ),
        "back_note": "Uživajte odgovorno. 18+",
        "placeholder_note": "ZAMENITE: kontakt podaci ispod",
    },
}

# Contact block printed on the back page — PLACEHOLDERS, replace these.
CONTACT = {
    "email": "hello@example.com",
    "phone": "+00 000 000 000",
    "web": "www.example.com",
    "social": "@shakeandsteer",
    "city": "City, Country",
}


CATEGORIES = [
    # ======================================================================
    ("Signature Creations", "Autorski kokteli",
     "The ten drinks the house is known for, rewritten twice a year.",
     "Deset pića po kojima nas pamte, pišemo ih iznova dvaput godišnje.",
     [
        ("Velvet Sovereign",
         "Aged whisky softened with fig and vanilla, finished with cherrywood smoke released at the table.",
         "Aged bourbon, fig cordial, vanilla bitters, cherrywood smoke, orange oils",
         "Odležali viski omekšan smokvom i vanilom, sa dimom trešnjinog drveta koji se oslobađa za stolom.",
         "Odležali burbon, kordijal od smokve, biters od vanile, dim trešnjinog drveta, ulje pomorandže"),

        ("Gilded Plum",
         "Gin stirred down with plum liqueur and golden chamomile — bright, floral and dangerously easy.",
         "London dry gin, plum liqueur, chamomile syrup, dry vermouth, lemon twist",
         "Džin mešan sa likerom od šljive i zlatnom kamilicom — blistav, cvetan i opasno pitak.",
         "London dry džin, liker od šljive, sirup od kamilice, suvi vermut, kora limuna"),

        ("Rosé Noir",
         "Smoked mezcal, rose and pink grapefruit over clear ice — floral at the front, smoky at the end.",
         "Mezcal espadín, rose cordial, pink grapefruit, agave, saline solution",
         "Dimljeni meskal, ruža i rozi grejpfrut preko bistrog leda — cvetno na početku, zadimljeno na kraju.",
         "Meskal espadín, kordijal od ruže, rozi grejpfrut, agava, rastvor soli"),

        ("Adriatic Mist",
         "Coastal gin, sea-salt tonic and a cordial of green olive and rosemary. Clean and saline.",
         "Mediterranean gin, green olive cordial, rosemary, sea-salt tonic, lemon",
         "Primorski džin, tonik sa morskom soli i kordijal od zelene masline i ruzmarina. Čisto i slankasto.",
         "Mediteranski džin, kordijal od zelene masline, ruzmarin, tonik sa morskom soli, limun"),

        ("Bordeaux Ember",
         "Blackcurrant and burnt orange under a slow pour of champagne, with a single gold leaf.",
         "Blackcurrant liqueur, burnt orange syrup, cognac, brut champagne, gold leaf",
         "Crna ribizla i pečena pomorandža ispod polako dolivanog šampanjca, sa listićem zlata.",
         "Liker od crne ribizle, sirup od pečene pomorandže, konjak, brut šampanjac, listić zlata"),

        ("The Violet Hour",
         "Vodka washed with violet and blackberry, lengthened with sparkling wine.",
         "Vodka, crème de violette, blackberry shrub, lemon, brut sparkling wine",
         "Votka sa ljubičicom i kupinom, produžena penušavim vinom.",
         "Votka, crème de violette, šrab od kupine, limun, brut penušavo vino"),

        ("Garden Room",
         "Cucumber, green apple and lovage with verjus and soda — considered as carefully as any spirit drink.",
         "Cucumber juice, green apple, lovage cordial, verjus, soda water",
         "Krastavac, zelena jabuka i ljupčac sa veržisom i sodom — osmišljen jednako pažljivo kao i pića sa alkoholom.",
         "Sok od krastavca, zelena jabuka, kordijal od ljupčaca, veržis, soda"),

        ("Amber & Anise",
         "Dark rum, roasted pineapple and star anise, poured tall over crushed ice.",
         "Dark rum, roasted pineapple syrup, star anise tincture, lime, cinnamon sugar rim",
         "Tamni rum, pečeni ananas i zvezdasti anis, nalivan u visoku čašu preko drobljenog leda.",
         "Tamni rum, sirup od pečenog ananasa, tinktura zvezdastog anisa, limeta, obod od cimeta i šećera"),

        ("Midnight Harbour",
         "Blanco tequila with butterfly pea, lime and salted honey — it shifts colour as it dilutes.",
         "Blanco tequila, butterfly pea infusion, lime, salted honey cordial, soda",
         "Blanko tekila sa leptirastim grahom, limetom i slanim medom — menja boju dok se led topi.",
         "Blanko tekila, infuzija leptirastog graha, limeta, kordijal od slanog meda, soda"),

        ("Fête Royale",
         "Elderflower, white peach and champagne with a bitters-soaked sugar cube. Our wedding welcome.",
         "Elderflower liqueur, white peach purée, brut champagne, aromatic bitters, sugar cube",
         "Zova, bela breskva i šampanjac sa kockom šećera natopljenom bitersom. Naše piće dobrodošlice za venčanja.",
         "Liker od zove, pire od bele breskve, brut šampanjac, aromatični biters, kocka šećera"),
     ]),

    # ======================================================================
    ("Classics, Reimagined", "Klasici, iznova",
     "The drinks everybody knows, built with our own syrups and better ice.",
     "Pića koja svi znaju, napravljena sa našim sirupima i boljim ledom.",
     [
        ("Old Fashioned No. 7",
         "Bourbon, demerara and two bitters, stirred long over a single hand-cut cube.",
         "Bourbon, demerara syrup, Angostura bitters, orange bitters, orange peel",
         "Burbon, demerara i dva bitersa, dugo mešano preko jedne ručno sečene kocke.",
         "Burbon, demerara sirup, Angostura biters, biters od pomorandže, kora pomorandže"),

        ("Smoked Negroni",
         "Equal parts, rested in a smoked glass so the bitterness arrives with a warm edge.",
         "Gin, Campari, sweet vermouth, applewood smoke, orange peel",
         "Jednaki delovi, odstajalo u zadimljenoj čaši, pa gorčina dolazi sa toplim rubom.",
         "Džin, Campari, slatki vermut, dim jabukovog drveta, kora pomorandže"),

        ("Manhattan Bordeaux",
         "Rye and vermouth with a splash of red-wine reduction for depth and colour.",
         "Rye whiskey, sweet vermouth, red wine reduction, aromatic bitters, brandied cherry",
         "Raž i vermut sa malo redukcije crnog vina, za dubinu i boju.",
         "Ražani viski, slatki vermut, redukcija crnog vina, aromatični biters, višnja u rakiji"),

        ("Espresso Martini Noir",
         "Cold-brew instead of hot espresso, so it stays bitter-sweet rather than burnt.",
         "Vodka, coffee liqueur, cold-brew concentrate, cacao bitters, salt",
         "Hladno ceđena kafa umesto vrućeg espresa, pa ostaje gorko-slatko, a ne zagoreno.",
         "Votka, liker od kafe, koncentrat hladno ceđene kafe, kakao biters, so"),

        ("Daiquiri Blanc",
         "Three ingredients, shaken hard and served very cold. Nothing to hide behind.",
         "White rum, fresh lime juice, cane sugar syrup",
         "Tri sastojka, snažno šejkovano i servirano vrlo hladno. Nema iza čega da se sakrije.",
         "Beli rum, sveže ceđena limeta, sirup od trske"),

        ("Whisky Sour Royale",
         "A proper sour under a float of red wine, the way it was drunk a century ago.",
         "Bourbon, lemon, sugar syrup, egg white, red wine float",
         "Pravi sour ispod sloja crnog vina, onako kako se pio pre sto godina.",
         "Burbon, limun, šećerni sirup, belance, sloj crnog vina"),

        ("Sidecar Doré",
         "Cognac and orange with a caramelised sugar rim that melts slowly into the drink.",
         "VSOP cognac, triple sec, lemon, caramelised sugar rim",
         "Konjak i pomorandža sa obodom od karamelizovanog šećera koji se polako topi u piću.",
         "VSOP konjak, triple sec, limun, obod od karamelizovanog šećera"),

        ("Boulevardier d'Automne",
         "The autumn cousin of the Negroni: whisky, bitter orange and a little spiced fig.",
         "Bourbon, Campari, sweet vermouth, spiced fig syrup, orange peel",
         "Jesenji rođak Negronija: viski, gorka pomorandža i malo začinjene smokve.",
         "Burbon, Campari, slatki vermut, sirup od začinjene smokve, kora pomorandže"),

        ("Margarita Verde",
         "Tequila and lime cut with fresh coriander and a dusting of chilli salt.",
         "Blanco tequila, lime, agave, coriander leaf, chilli salt rim",
         "Tekila i limeta sa svežim korijanderom i prstohvatom čili soli.",
         "Blanko tekila, limeta, agava, list korijandera, obod od čili soli"),

        ("Aviation Violette",
         "Gin, maraschino and violet — pale lilac, bone dry, unexpectedly gentle.",
         "Gin, maraschino liqueur, crème de violette, lemon juice",
         "Džin, maraskino i ljubičica — bledoljubičasto, sasvim suvo i iznenađujuće nežno.",
         "Džin, liker maraskino, crème de violette, sok od limuna"),

        ("Bramble Noir",
         "Crushed ice, gin and a slow bleed of blackberry liqueur through the glass.",
         "Gin, lemon, sugar syrup, crème de mûre, blackberry",
         "Drobljeni led, džin i sporo spuštanje likera od kupine kroz čašu.",
         "Džin, limun, šećerni sirup, crème de mûre, kupina"),

        ("Vesper Steer",
         "Gin and vodka with our own aromatised wine, stirred rather than shaken.",
         "Gin, vodka, house aromatised wine, lemon peel",
         "Džin i votka sa našim aromatizovanim vinom, mešano a ne šejkovano.",
         "Džin, votka, kućno aromatizovano vino, kora limuna"),

        ("Paloma Rosa",
         "Tequila, pink grapefruit and grapefruit soda with a salted rim. Long and refreshing.",
         "Blanco tequila, pink grapefruit, lime, grapefruit soda, salt rim",
         "Tekila, rozi grejpfrut i soda od grejpfruta sa slanim obodom. Dugo i osvežavajuće.",
         "Blanko tekila, rozi grejpfrut, limeta, soda od grejpfruta, slani obod"),

        ("Penicillin Amber",
         "Blended scotch, honey and ginger with a smoky islay float across the top.",
         "Blended scotch, honey-ginger syrup, lemon, peated whisky float, candied ginger",
         "Blend skoča, med i đumbir sa dimljenim islay slojem preko vrha.",
         "Blend skoča, sirup od meda i đumbira, limun, sloj dimljenog viskija, kandirani đumbir"),
     ]),

    # ======================================================================
    ("Sparkling & Champagne", "Penušavo i šampanjac",
     "Aperitif-hour drinks built on bubbles. Ideal for welcomes and toasts.",
     "Pića za aperitiv, na mehurićima. Idealna za dobrodošlicu i zdravice.",
     [
        ("Champagne 75",
         "Gin, lemon and champagne. The welcome drink that has never needed improving.",
         "Gin, lemon, sugar syrup, brut champagne, lemon twist",
         "Džin, limun i šampanjac. Piće dobrodošlice koje nikada nije trebalo popravljati.",
         "Džin, limun, šećerni sirup, brut šampanjac, kora limuna"),

        ("Kir Impérial",
         "Raspberry liqueur with champagne — pink, dry and impossible to serve badly.",
         "Raspberry liqueur, brut champagne, fresh raspberry",
         "Liker od maline sa šampanjcem — roze, suvo i nemoguće loše servirati.",
         "Liker od maline, brut šampanjac, sveža malina"),

        ("Bellini Bianca",
         "White peach purée topped with prosecco, made from fruit we purée the same morning.",
         "White peach purée, peach liqueur, prosecco",
         "Pire od bele breskve preliven prosekom, od voća koje pasiramo istog jutra.",
         "Pire od bele breskve, liker od breskve, proseko"),

        ("Rossini Rubis",
         "Strawberry and sparkling wine, with a drop of balsamic to keep it from being sweet.",
         "Strawberry purée, aged balsamic, sugar syrup, prosecco",
         "Jagoda i penušavo vino, sa kapi balzamika da ne bude preslatko.",
         "Pire od jagode, odležali balzamiko, šećerni sirup, proseko"),

        ("Hugo Blanc",
         "Elderflower, mint and lime with prosecco and soda. The garden-party standard.",
         "Elderflower syrup, mint, lime, prosecco, soda water",
         "Zova, nana i limeta sa prosekom i sodom. Standard za baštenske proslave.",
         "Sirup od zove, nana, limeta, proseko, soda"),

        ("Sgroppino Gold",
         "Lemon sorbet whipped into prosecco and vodka — halfway between a drink and a dessert.",
         "Lemon sorbet, vodka, prosecco, lemon zest",
         "Sorbet od limuna umućen u proseko i votku — na pola puta između pića i deserta.",
         "Sorbet od limuna, votka, proseko, korica limuna"),

        ("Afternoon No. 2",
         "Absinthe and champagne, poured until the glass turns cloudy. Stronger than it looks.",
         "Absinthe, brut champagne, sugar syrup, lemon oils",
         "Apsint i šampanjac, doliva se dok čaša ne postane mutna. Jače nego što izgleda.",
         "Apsint, brut šampanjac, šećerni sirup, ulje limuna"),

        ("Coupe d'Or",
         "Champagne over saffron honey and a thread of bergamot. Our most photographed serve.",
         "Brut champagne, saffron honey, bergamot cordial, gold leaf",
         "Šampanjac preko meda sa šafranom i niti bergamota. Naše najfotografisanije piće.",
         "Brut šampanjac, med sa šafranom, kordijal od bergamota, listić zlata"),
     ]),

    # ======================================================================
    ("Aperitivo & Spritz", "Aperitivi i šprices",
     "Low in alcohol, high in appetite. Best served before the food arrives.",
     "Malo alkohola, mnogo apetita. Najbolje pre nego što stigne hrana.",
     [
        ("Spritz Classico",
         "Bitter orange aperitif, prosecco and soda over plenty of ice. Nothing reinvented.",
         "Bitter orange aperitif, prosecco, soda water, orange slice",
         "Gorki aperitiv od pomorandže, proseko i soda preko mnogo leda. Ništa izmišljeno.",
         "Gorki aperitiv od pomorandže, proseko, soda, kriška pomorandže"),

        ("Spritz Rosso",
         "A deeper, redder spritz with rhubarb bitterness and a grapefruit twist.",
         "Red bitter aperitif, prosecco, soda water, grapefruit peel",
         "Dublji, crveniji šprices sa gorčinom rabarbare i korom grejpfruta.",
         "Crveni gorki aperitiv, proseko, soda, kora grejpfruta"),

        ("Spritz Bianco",
         "White vermouth, elderflower and soda — the version people drink two of.",
         "White vermouth, elderflower liqueur, soda water, lemon, olive",
         "Beli vermut, zova i soda — verzija od koje se popiju dve.",
         "Beli vermut, liker od zove, soda, limun, maslina"),

        ("Amaro Spritz",
         "Artichoke amaro cut with tonic: herbal, dry and surprisingly moreish.",
         "Artichoke amaro, tonic water, orange slice, rosemary",
         "Amaro od artičoke razblažen tonikom: biljno, suvo i iznenađujuće pitko.",
         "Amaro od artičoke, tonik, kriška pomorandže, ruzmarin"),

        ("Limoncello Spritz",
         "Lemon liqueur, prosecco and a sprig of thyme. Loud, yellow and very summer.",
         "Limoncello, prosecco, soda water, thyme, lemon wheel",
         "Liker od limuna, proseko i grančica majčine dušice. Glasno, žuto i vrlo letnje.",
         "Limoncello, proseko, soda, majčina dušica, kolut limuna"),

        ("Americano Lungo",
         "Bitter, vermouth and soda — the drink the Negroni was invented from.",
         "Campari, sweet vermouth, soda water, orange slice",
         "Biter, vermut i soda — piće iz kojeg je nastao Negroni.",
         "Campari, slatki vermut, soda, kriška pomorandže"),

        ("Garibaldi Solare",
         "Bitter aperitif and orange juice whipped until it turns to foam.",
         "Campari, fluffy fresh orange juice, orange peel",
         "Gorki aperitiv i sok od pomorandže umućeni dok se ne pretvore u penu.",
         "Campari, penasto ceđena pomorandža, kora pomorandže"),

        ("Bicicletta",
         "White wine, bitter and soda. Three ingredients, one very civilised afternoon.",
         "Dry white wine, Campari, soda water, lemon wheel",
         "Belo vino, biter i soda. Tri sastojka, jedno vrlo pristojno popodne.",
         "Suvo belo vino, Campari, soda, kolut limuna"),
     ]),

    # ======================================================================
    ("Tropical & Tiki", "Tropsko i tiki",
     "Rum-led, fruit-forward and built for a warm night and a loud room.",
     "Sa rumom u prvom planu, voćno i napravljeno za toplu noć i bučan prostor.",
     [
        ("Mai Tai Reserve",
         "Two rums, almond and lime — the original recipe, with better almond syrup.",
         "Aged rum, rhum agricole, orgeat, orange curaçao, lime",
         "Dva ruma, badem i limeta — originalni recept, sa boljim sirupom od badema.",
         "Odležali rum, rhum agricole, orgeat, orange curaçao, limeta"),

        ("Painkiller No. 4",
         "Pineapple, coconut and orange under a heavy dusting of fresh nutmeg.",
         "Navy rum, pineapple, coconut cream, orange juice, grated nutmeg",
         "Ananas, kokos i pomorandža pod gustim slojem sveže rendanog muskatnog oraščića.",
         "Navy rum, ananas, kokosov krem, sok od pomorandže, rendani muskatni oraščić"),

        ("Jungle Bird Noir",
         "Dark rum and Campari with pineapple — bitter and tropical at the same time.",
         "Blackstrap rum, Campari, pineapple juice, lime, cane syrup",
         "Tamni rum i Campari sa ananasom — istovremeno gorko i tropsko.",
         "Blackstrap rum, Campari, sok od ananasa, limeta, sirup od trske"),

        ("Piña Colada Tostada",
         "Toasted coconut instead of sweet cream, so it tastes like fruit rather than dessert.",
         "White rum, toasted coconut cream, pineapple, lime, pineapple leaf",
         "Tostirani kokos umesto slatke pavlake, pa ima ukus voća, a ne deserta.",
         "Beli rum, krem od tostiranog kokosa, ananas, limeta, list ananasa"),

        ("Zombie Steer",
         "Three rums, grapefruit and absinthe. Strictly one per guest, and we mean it.",
         "White rum, aged rum, overproof rum, grapefruit, cinnamon syrup, absinthe",
         "Tri ruma, grejpfrut i apsint. Strogo po jedan po gostu, i to mislimo ozbiljno.",
         "Beli rum, odležali rum, overproof rum, grejpfrut, sirup od cimeta, apsint"),

        ("Navy Grog",
         "Rum, honey and citrus served over a cone of crushed ice with a straw through it.",
         "Demerara rum, white rum, honey syrup, grapefruit, lime, soda",
         "Rum, med i citrusi servirani preko kupe drobljenog leda, sa slamkom kroz sredinu.",
         "Demerara rum, beli rum, sirup od meda, grejpfrut, limeta, soda"),

        ("Hurricane Rouge",
         "Passion fruit and red berries with dark rum. Loud colour, balanced drink.",
         "Dark rum, passion fruit, red berry purée, lime, sugar syrup",
         "Pasiflora i crveno voće sa tamnim rumom. Jarka boja, izbalansirano piće.",
         "Tamni rum, pasiflora, pire od crvenog voća, limeta, šećerni sirup"),

        ("Saturn Gold",
         "Gin-based tiki: passion fruit, almond and falernum with a citrus ring.",
         "Gin, passion fruit, orgeat, falernum, lemon",
         "Tiki na bazi džina: pasiflora, badem i falernum sa citrusnim prstenom.",
         "Džin, pasiflora, orgeat, falernum, limun"),

        ("Coconut Daiquiri",
         "A daiquiri with coconut water in place of some of the sugar. Cleaner and drier.",
         "White rum, coconut water, lime, cane syrup",
         "Dajkiri sa kokosovom vodom umesto dela šećera. Čistije i suvlje.",
         "Beli rum, kokosova voda, limeta, sirup od trske"),

        ("Tiki Sour Ananas",
         "Roasted pineapple, rum and lime, shaken with egg white for a thick, soft top.",
         "Aged rum, roasted pineapple syrup, lime, egg white, aromatic bitters",
         "Pečeni ananas, rum i limeta, šejkovano sa belancetom za gustu, meku penu.",
         "Odležali rum, sirup od pečenog ananasa, limeta, belance, aromatični biters"),
     ]),

    # ======================================================================
    ("Alcohol-Free", "Bezalkoholno",
     "Built with the same care as the rest of the book — never an afterthought.",
     "Napravljeno sa istom pažnjom kao i ostatak knjige — nikada naknadna misao.",
     [
        ("Green Room Zero",
         "Cucumber, green apple and lovage with verjus and soda. Crisp and savoury.",
         "Cucumber, green apple, lovage cordial, verjus, soda water",
         "Krastavac, zelena jabuka i ljupčac sa veržisom i sodom. Sveže i slankasto.",
         "Krastavac, zelena jabuka, kordijal od ljupčaca, veržis, soda"),

        ("Seville Sunrise",
         "Bitter orange and grapefruit with tonic — all the aperitivo bitterness, none of the alcohol.",
         "Non-alcoholic bitter aperitif, blood orange, grapefruit, tonic water",
         "Gorka pomorandža i grejpfrut sa tonikom — sva gorčina aperitiva, bez alkohola.",
         "Bezalkoholni gorki aperitiv, crvena pomorandža, grejpfrut, tonik"),

        ("Cucumber Collins Zero",
         "Long, cold and green, with just enough acidity to keep you reaching for it.",
         "Non-alcoholic gin alternative, cucumber, lemon, sugar syrup, soda",
         "Dugo, hladno i zeleno, sa taman dovoljno kiseline da ga stalno posežete.",
         "Bezalkoholna alternativa džinu, krastavac, limun, šećerni sirup, soda"),

        ("Rosemary Grey",
         "Cold-brewed earl grey with rosemary and honey. Tannic, warm and grown-up.",
         "Cold-brewed earl grey, rosemary syrup, honey, lemon, soda",
         "Hladno ceđeni erl grej sa ruzmarinom i medom. Taninsko, toplo i ozbiljno.",
         "Hladno ceđeni erl grej, sirup od ruzmarina, med, limun, soda"),

        ("Peach Blossom Zero",
         "White peach and elderflower over crushed ice — the non-alcoholic welcome drink.",
         "White peach purée, elderflower cordial, lemon, sparkling water",
         "Bela breskva i zova preko drobljenog leda — bezalkoholno piće dobrodošlice.",
         "Pire od bele breskve, kordijal od zove, limun, gazirana voda"),

        ("Smoked Apple Zero",
         "Apple juice smoked over applewood, with lemon and a little salt. Autumn in a glass.",
         "Smoked apple juice, lemon, saline solution, cinnamon, apple fan",
         "Sok od jabuke dimljen na jabukovom drvetu, sa limunom i malo soli. Jesen u čaši.",
         "Dimljeni sok od jabuke, limun, rastvor soli, cimet, lepeza od jabuke"),

        ("Verjus Spritz",
         "Unripe grape juice with soda and grapefruit — the driest drink on the list.",
         "Verjus, grapefruit, sugar syrup, soda water, grapefruit peel",
         "Sok od nezrelog grožđa sa sodom i grejpfrutom — najsuvlje piće na listi.",
         "Veržis, grejpfrut, šećerni sirup, soda, kora grejpfruta"),

        ("Coconut Cooler",
         "Coconut water, lime and pineapple, shaken until it is properly cold.",
         "Coconut water, pineapple juice, lime, cane syrup, mint",
         "Kokosova voda, limeta i ananas, šejkovano dok ne postane kako treba hladno.",
         "Kokosova voda, sok od ananasa, limeta, sirup od trske, nana"),

        ("Ginger Blossom",
         "Fresh ginger, lemon and orange blossom — sharp at the front, floral at the finish.",
         "Fresh ginger syrup, lemon, orange blossom water, soda water",
         "Svež đumbir, limun i cvet pomorandže — oštro na početku, cvetno na kraju.",
         "Sirup od svežeg đumbira, limun, voda od cveta pomorandže, soda"),

        ("Hibiscus Refresher",
         "Hibiscus and raspberry with lime. Deep red, tart and very easy to drink.",
         "Hibiscus tea, raspberry shrub, lime, sugar syrup, soda water",
         "Hibiskus i malina sa limetom. Tamnocrveno, kiselkasto i vrlo pitko.",
         "Čaj od hibiskusa, šrab od maline, limeta, šećerni sirup, soda"),

        ("Elderflower Zero",
         "Elderflower, mint and lime with sparkling water. Our alcohol-free Hugo.",
         "Elderflower cordial, mint, lime, sparkling water",
         "Zova, nana i limeta sa gaziranom vodom. Naš bezalkoholni Hugo.",
         "Kordijal od zove, nana, limeta, gazirana voda"),

        ("Espresso Zero",
         "Cold-brew, tonka syrup and oat milk, shaken to a thick foam. Served after dinner.",
         "Cold-brew coffee, tonka syrup, oat milk, cacao dust",
         "Hladno ceđena kafa, sirup od tonke i ovseno mleko, šejkovano do guste pene. Servira se posle večere.",
         "Hladno ceđena kafa, sirup od tonke, ovseno mleko, prah od kakaa"),
     ]),

    # ======================================================================
    ("After Dinner", "Posle večere",
     "Richer, slower drinks for the end of the evening.",
     "Punija, sporija pića za kraj večeri.",
     [
        ("Espresso Old Fashioned",
         "Bourbon stirred with coffee and demerara — a nightcap that still wakes you up.",
         "Bourbon, espresso, demerara syrup, chocolate bitters, orange peel",
         "Burbon mešan sa kafom i demerarom — poslednje piće koje vas ipak razbudi.",
         "Burbon, espreso, demerara sirup, čokoladni biters, kora pomorandže"),

        ("Chocolate Negroni",
         "Gin, bitter and vermouth with cacao — dark, dry, not remotely sweet.",
         "Gin, Campari, sweet vermouth, cacao nib tincture, orange peel",
         "Džin, biter i vermut sa kakaom — tamno, suvo i nimalo slatko.",
         "Džin, Campari, slatki vermut, tinktura od zrna kakaa, kora pomorandže"),

        ("Amaretto Sour Noir",
         "Almond liqueur and bourbon with lemon and egg white, under a line of bitters.",
         "Amaretto, bourbon, lemon, egg white, aromatic bitters",
         "Liker od badema i burbon sa limunom i belancetom, pod linijom bitersa.",
         "Amaretto, burbon, limun, belance, aromatični biters"),

        ("Fernet Flip",
         "Mint-bitter amaro shaken with a whole egg and cream. Difficult to describe, easy to finish.",
         "Fernet, cream, whole egg, sugar syrup, grated nutmeg",
         "Gorki amaro sa nanom šejkovan sa celim jajetom i pavlakom. Teško se opisuje, lako se popije.",
         "Fernet, pavlaka, celo jaje, šećerni sirup, rendani muskatni oraščić"),

        ("Vanilla Rum Nightcap",
         "Aged rum, vanilla and a spoon of salted butter syrup, stirred until silky.",
         "Aged rum, vanilla syrup, salted butter syrup, aromatic bitters",
         "Odležali rum, vanila i kašika sirupa od slanog putera, mešano do svilenkastog.",
         "Odležali rum, sirup od vanile, sirup od slanog putera, aromatični biters"),

        ("Cognac Alexander",
         "Cognac, cacao and cream, dusted with nutmeg. The dessert you drink.",
         "VSOP cognac, crème de cacao, double cream, grated nutmeg",
         "Konjak, kakao i pavlaka, posuto muskatnim oraščićem. Desert koji se pije.",
         "VSOP konjak, crème de cacao, slatka pavlaka, rendani muskatni oraščić"),

        ("Grappa Affogato",
         "A shot of grappa and hot espresso poured over vanilla ice cream at the table.",
         "Grappa, hot espresso, vanilla ice cream, cacao dust",
         "Čašica grape i vrući espreso preliveni preko sladoleda od vanile, za stolom.",
         "Grapa, vrući espreso, sladoled od vanile, prah od kakaa"),

        ("Port & Fig",
         "Tawny port with fig and orange, served long over ice like a late-night spritz.",
         "Tawny port, fig syrup, orange, soda water, dried fig",
         "Tawny porto sa smokvom i pomorandžom, servirano dugo preko leda, kao kasnonoćni šprices.",
         "Tawny porto, sirup od smokve, pomorandža, soda, suva smokva"),
     ]),
]


def count():
    """How many cocktails are on the list."""
    return sum(len(category[4]) for category in CATEGORIES)


if __name__ == "__main__":
    print("%d cocktails in %d categories" % (count(), len(CATEGORIES)))
