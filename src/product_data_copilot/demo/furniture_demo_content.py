"""Prepared offline content variants for the German furniture demo.

The demo content is deterministic and does not call an AI provider. Each text
uses only facts from the demo furniture spreadsheet so the presentation can show
a safe human-in-the-loop content workflow without invented product claims.
"""

FURNITURE_DEMO_DEFAULT_SKU = "PDC-MOB-001"
FURNITURE_DEMO_VARIANTS = ("variant_a", "variant_b")
FURNITURE_DEMO_REVIEW_OPEN = "Noch nicht freigegeben"
FURNITURE_DEMO_REVIEW_APPROVED = "Freigegeben"
FURNITURE_DEMO_REVIEW_SECTION_KEYS = ("bulletpoints", "html_de", "html_en")
FURNITURE_DEMO_REVIEW_SECTION_LABELS = {
    "bulletpoints": "Bullet Points",
    "html_de": "HTML Deutsch",
    "html_en": "HTML English",
}


FURNITURE_DEMO_CONTENT = {
    "PDC-MOB-001": {
        "variant_a": {
            "bulletpoints_de": [
                "Großzügiges 3-Sitzer-Sofa in elegantem Hellgrau",
                "Webstoffbezug mit pflegeleichter Oberfläche",
                "Konische Holzfüße aus Massivholz Eiche",
                "Abnehmbare Sitzkissen für einen flexiblen Alltag",
                "Klares Wohnformat mit 220 x 84 x 92 cm",
            ],
            "html_de": (
                "<p><strong>Nordic Lounge Sofa 3-Sitzer</strong> bringt eine ruhige, "
                "moderne Atmosphäre in dein Wohnzimmer. Der hellgraue Webstoff wirkt "
                "freundlich und lässt sich vielseitig mit hellen Hölzern, dunklen "
                "Akzenten oder natürlichen Wohnfarben kombinieren.</p>"
                "<p>Konische Holzfüße aus Massivholz Eiche geben dem Sofa eine warme "
                "Note, während die abnehmbaren Sitzkissen den Look angenehm locker "
                "halten. Mit 220 x 84 x 92 cm bietet der 3-Sitzer ein großzügiges "
                "Format für entspannte Wohnbereiche.</p>"
            ),
            "html_en": (
                "<p><strong>Nordic Lounge 3-Seater Sofa</strong> brings a calm, modern "
                "look to the living room. The light grey woven fabric can be combined "
                "with natural wood tones, darker accents or soft neutral colours.</p>"
                "<p>Tapered solid oak legs add warmth, while the removable seat "
                "cushions keep the design relaxed and practical. With dimensions of "
                "220 x 84 x 92 cm, this 3-seater offers a generous format for lounge "
                "and living spaces.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Hellgraues Sofa mit wohnlicher Webstoffstruktur",
                "Massivholz Eiche als natürlicher Materialakzent",
                "Abnehmbare Sitzkissen für eine lockere Optik",
                "Konische Holzfüße unterstreichen die klare Form",
                "Maße: 220 x 84 x 92 cm",
            ],
            "html_de": (
                "<p><strong>Nordic Lounge Sofa 3-Sitzer</strong> verbindet ein "
                "großzügiges Sofaformat mit einer angenehm zurückhaltenden Farbgebung. "
                "Hellgrauer Webstoff sorgt für einen freundlichen Eindruck und macht "
                "das Sofa zu einem vielseitigen Mittelpunkt im Wohnraum.</p>"
                "<p>Die konischen Holzfüße aus Eiche setzen einen natürlichen Akzent. "
                "Abnehmbare Sitzkissen und der pflegeleichte Webstoff runden das "
                "Möbelstück alltagstauglich ab. Die angegebenen Maße betragen "
                "220 x 84 x 92 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Nordic Lounge 3-Seater Sofa</strong> combines a spacious "
                "sofa format with a calm light grey colour. The woven fabric gives the "
                "piece a friendly look and makes it easy to place in different living "
                "room styles.</p>"
                "<p>Tapered oak legs add a natural accent. Removable seat cushions "
                "and easy-care woven fabric complete the practical everyday character "
                "of the sofa. The listed dimensions are 220 x 84 x 92 cm.</p>"
            ),
        },
    },
    "PDC-MOB-002": {
        "variant_a": {
            "bulletpoints_de": [
                "Esstisch aus geöltem Massivholz Eiche",
                "Ausziehbar von 180 cm auf 230 cm",
                "Natürlicher Farbton für ein warmes Esszimmer",
                "Abgerundete Kanten als ruhiges Designdetail",
                "Platz für 6 bis 8 Personen",
            ],
            "html_de": (
                "<p><strong>Eichenholz Esstisch Arvid</strong> bringt die natürliche "
                "Wirkung geölter Eiche in den Essbereich. Die warme Holzoptik und die "
                "geradlinige Form schaffen einen einladenden Mittelpunkt für Alltag, "
                "Familienessen und gesellige Abende.</p>"
                "<p>Besonders praktisch ist die Ausziehfunktion von 180 cm auf 230 cm. "
                "So bleibt der Tisch kompakt, wenn wenig Platz gebraucht wird, und "
                "bietet bei Bedarf Raum für 6 bis 8 Personen. Abgerundete Kanten "
                "ergänzen das ruhige Gesamtbild.</p>"
            ),
            "html_en": (
                "<p><strong>Arvid Oak Dining Table</strong> brings the natural look of "
                "oiled oak into the dining area. Its warm wood tone and clean shape "
                "create an inviting centrepiece for everyday meals and shared evenings.</p>"
                "<p>The extension from 180 cm to 230 cm adds flexibility. The table "
                "stays compact when less space is needed and can seat 6 to 8 people "
                "when extended. Rounded edges complete the calm design.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Natürlicher Esstisch in geölter Eiche",
                "Flexible Länge dank Ausziehfunktion",
                "Ausziehbar bis 230 cm für größere Runden",
                "Abgerundete Kanten für eine weiche Linienführung",
                "Maße im Grundformat: 180 x 75 x 90 cm",
            ],
            "html_de": (
                "<p><strong>Eichenholz Esstisch Arvid</strong> setzt auf die klare "
                "Schönheit von Massivholz Eiche. Die geölte Oberfläche betont den "
                "natürlichen Charakter und macht den Tisch zu einem warmen Mittelpunkt "
                "im Esszimmer.</p>"
                "<p>Wenn Besuch kommt, lässt sich Arvid von 180 cm auf 230 cm "
                "verlängern. Mit Platz für 6 bis 8 Personen und abgerundeten Kanten "
                "passt der Tisch zu entspannten Essen ebenso wie zu längeren Abenden "
                "mit Familie und Freunden.</p>"
            ),
            "html_en": (
                "<p><strong>Arvid Oak Dining Table</strong> focuses on the clean beauty "
                "of solid oak wood. The oiled surface highlights the natural character "
                "and makes the table a warm centrepiece in the dining room.</p>"
                "<p>When guests arrive, Arvid can be extended from 180 cm to 230 cm. "
                "With space for 6 to 8 people and rounded edges, it suits relaxed "
                "meals as well as long evenings with family and friends.</p>"
            ),
        },
    },
    "PDC-MOB-003": {
        "variant_a": {
            "bulletpoints_de": [
                "2er-Set Polsterstühle in Smaragdgrün",
                "Samtbezug mit gepolsterter Sitzfläche",
                "Metallgestell mit pulverbeschichteter Oberfläche",
                "Materialmix aus Metall, Samtstoff und Schaumstoff",
                "Je Stuhl 52 x 84 x 58 cm",
            ],
            "html_de": (
                "<p><strong>Polsterstuhl Maja 2er-Set</strong> bringt mit Smaragdgrün "
                "einen ausdrucksstarken Farbakzent an den Esstisch. Der Samtbezug und "
                "die gepolsterte Sitzfläche schaffen eine weiche, wohnliche Optik.</p>"
                "<p>Das pulverbeschichtete Metallgestell setzt einen klaren Kontrast "
                "zum Stoff und gibt dem Set eine moderne Linie. Mit 52 x 84 x 58 cm je "
                "Stuhl lässt sich Maja gut an Esstischen oder kleinen Sitzbereichen "
                "einplanen.</p>"
            ),
            "html_en": (
                "<p><strong>Maja Upholstered Chair Set of 2</strong> adds an expressive "
                "emerald green accent to the dining area. The velvet cover and padded "
                "seat create a soft, inviting look.</p>"
                "<p>The powder-coated metal frame provides a clean contrast to the "
                "fabric and gives the set a modern line. Each chair measures "
                "52 x 84 x 58 cm, making Maja easy to place at dining tables or small "
                "seating areas.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Zwei Polsterstühle im intensiven Grünton",
                "Samtstoff und Schaumstoff für eine weiche Anmutung",
                "Pulverbeschichtetes Metallgestell als moderner Akzent",
                "Gepolsterte Sitzfläche für ein wohnliches Erscheinungsbild",
                "Kompaktes Maß je Stuhl: 52 x 84 x 58 cm",
            ],
            "html_de": (
                "<p><strong>Polsterstuhl Maja 2er-Set</strong> macht den Essplatz "
                "farblich lebendiger. Smaragdgrüner Samtstoff trifft auf eine "
                "gepolsterte Sitzfläche und bringt eine weiche, dekorative Wirkung in "
                "den Raum.</p>"
                "<p>Das Metallgestell mit pulverbeschichteter Oberfläche ergänzt den "
                "Look mit einer klaren Form. Das 2er-Set eignet sich besonders für "
                "Essbereiche, kleine Tische oder als Akzentstühle in offenen "
                "Wohnräumen.</p>"
            ),
            "html_en": (
                "<p><strong>Maja Upholstered Chair Set of 2</strong> brings more colour "
                "to the dining area. Emerald green velvet fabric and a padded seat "
                "create a soft, decorative look.</p>"
                "<p>The powder-coated metal frame adds a clean, modern shape. This "
                "set of two works well for dining areas, smaller tables or as accent "
                "chairs in open living spaces.</p>"
            ),
        },
    },
    "PDC-MOB-004": {
        "variant_a": {
            "bulletpoints_de": [
                "Dreitüriges Sideboard in Eiche / Schwarz",
                "MDF, Eichenfurnier und Metall kombiniert",
                "Zwei höhenverstellbare Einlegeböden",
                "Integrierte Kabelführung für mehr Ordnung",
                "Schwarze Metallgriffe als klarer Akzent",
            ],
            "html_de": (
                "<p><strong>Sideboard Lino mit 3 Türen</strong> verbindet warme "
                "Eichenoptik mit schwarzen Details. Die Kombination aus MDF, "
                "Eichenfurnier und Metall wirkt modern und passt gut in Wohn- oder "
                "Essbereiche mit klarer Einrichtung.</p>"
                "<p>Hinter drei Türen entsteht Stauraum für Geschirr, Medienzubehör "
                "oder Alltagsgegenstände. Zwei höhenverstellbare Einlegeböden und "
                "eine Kabelführung machen Lino flexibel nutzbar. Die Maße betragen "
                "160 x 78 x 42 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Lino Sideboard with 3 Doors</strong> combines warm oak "
                "looks with black details. MDF, oak veneer and metal create a modern "
                "appearance for living or dining areas with clean interiors.</p>"
                "<p>Behind three doors, the sideboard offers space for tableware, "
                "media accessories or everyday items. Two adjustable shelves and "
                "cable management add practical flexibility. The dimensions are "
                "160 x 78 x 42 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Sideboard mit drei Türen und ruhiger Front",
                "Eiche / Schwarz für einen modernen Kontrast",
                "Zwei verstellbare Einlegeböden innen",
                "Kabelführung für Medien- und Wohnbereiche",
                "Format: 160 x 78 x 42 cm",
            ],
            "html_de": (
                "<p><strong>Sideboard Lino mit 3 Türen</strong> bringt Stauraum und "
                "einen klaren Materialkontrast zusammen. Eichenfurnier trifft auf "
                "schwarze Metallgriffe und verleiht dem Möbel eine ruhige, moderne "
                "Ausstrahlung.</p>"
                "<p>Die drei Türen halten den Inhalt optisch aufgeräumt. Mit zwei "
                "höhenverstellbaren Einlegeböden und Kabelführung eignet sich Lino "
                "auch für Medienzubehör oder Wohnbereiche, in denen Technik ordentlich "
                "verstaut werden soll.</p>"
            ),
            "html_en": (
                "<p><strong>Lino Sideboard with 3 Doors</strong> brings storage and a "
                "clear material contrast together. Oak veneer meets black metal "
                "handles for a calm, modern appearance.</p>"
                "<p>The three doors keep stored items visually tidy. With two "
                "adjustable shelves and cable management, Lino also works for media "
                "accessories or living areas where technology needs an orderly place.</p>"
            ),
        },
    },
    "PDC-MOB-005": {
        "variant_a": {
            "bulletpoints_de": [
                "Polsterbett in Creme mit Bouclé-Stoff",
                "Liegefläche 160 x 200 cm",
                "Gepolstertes Kopfteil für eine weiche Optik",
                "Lattenrost inklusive",
                "Stauraum als praktisches Ausstattungsmerkmal",
            ],
            "html_de": (
                "<p><strong>Polsterbett Haven 160 x 200 cm</strong> bringt eine ruhige "
                "Cremefarbe und Bouclé-Stoff ins Schlafzimmer. Das gepolsterte "
                "Kopfteil setzt einen weichen Akzent und macht das Bett zum "
                "freundlichen Mittelpunkt des Raums.</p>"
                "<p>Die Liegefläche von 160 x 200 cm ist für ein großzügiges "
                "Schlafzimmerformat ausgelegt. Lattenrost inklusive und Stauraum "
                "ergänzen Haven um praktische Details. Die Gesamtmaße betragen "
                "178 x 108 x 218 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Haven Upholstered Bed 160 x 200 cm</strong> brings a calm "
                "cream tone and bouclé fabric into the bedroom. The padded headboard "
                "adds a soft visual accent and makes the bed a friendly focal point.</p>"
                "<p>The 160 x 200 cm sleeping area offers a generous bed format. An "
                "included slatted frame and storage add practical details. The overall "
                "dimensions are 178 x 108 x 218 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Cremefarbenes Bett mit weichem Bouclé-Look",
                "Gepolstertes Kopfteil als wohnlicher Blickfang",
                "Holzwerkstoff und Metall als Materialbasis",
                "Lattenrost und Stauraum bereits vorgesehen",
                "Maße: 178 x 108 x 218 cm",
            ],
            "html_de": (
                "<p><strong>Polsterbett Haven 160 x 200 cm</strong> setzt auf eine "
                "helle, sanfte Wirkung. Cremefarbener Bouclé-Stoff und ein gepolstertes "
                "Kopfteil schaffen ein Schlafzimmerbild, das warm und ruhig wirkt.</p>"
                "<p>Holzwerkstoff und Metall bilden die Basis des Betts. Die "
                "Liegefläche von 160 x 200 cm, der enthaltene Lattenrost und der "
                "Stauraum machen Haven zu einer praktischen Lösung für den "
                "Schlafbereich.</p>"
            ),
            "html_en": (
                "<p><strong>Haven Upholstered Bed 160 x 200 cm</strong> focuses on a "
                "bright, soft look. Cream-coloured bouclé fabric and a padded headboard "
                "create a calm and warm bedroom impression.</p>"
                "<p>Engineered wood and metal form the base of the bed. The "
                "160 x 200 cm sleeping area, included slatted frame and storage make "
                "Haven a practical choice for the bedroom.</p>"
            ),
        },
    },
    "PDC-MOB-006": {
        "variant_a": {
            "bulletpoints_de": [
                "Kompakter Schreibtisch in Weiß / Eiche",
                "Arbeitsfläche mit integrierter Kabelöffnung",
                "Schublade für kleine Büroartikel",
                "Offene Ablage für Unterlagen oder Zubehör",
                "Maße: 120 x 76 x 60 cm",
            ],
            "html_de": (
                "<p><strong>Schreibtisch Nova Compact</strong> bringt eine helle "
                "Kombination aus Weiß und Eiche in Homeoffice, Jugendzimmer oder "
                "Arbeitsbereich. Die klare Form hält den Arbeitsplatz optisch ruhig "
                "und gut strukturierbar.</p>"
                "<p>Eine Schublade nimmt kleinere Büroartikel auf, während die offene "
                "Ablage Platz für Unterlagen oder Zubehör bietet. Die integrierte "
                "Kabelöffnung hilft dabei, Ladekabel und Technik sauber zu führen.</p>"
            ),
            "html_en": (
                "<p><strong>Nova Compact Desk</strong> brings a bright white and oak "
                "combination into a home office, study corner or bedroom workspace. "
                "The clean shape keeps the desk area visually calm and easy to arrange.</p>"
                "<p>A drawer stores smaller office items, while the open shelf offers "
                "space for papers or accessories. The integrated cable opening helps "
                "guide charging cables and devices neatly.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Schreibtisch mit klarer Arbeitsfläche",
                "Holzwerkstoff und Stahl kombiniert",
                "Schublade und offene Ablage für Ordnung",
                "Kabelöffnung für eine aufgeräumte Technikführung",
                "Kompaktes Format für kleinere Räume",
            ],
            "html_de": (
                "<p><strong>Schreibtisch Nova Compact</strong> ist für Räume gedacht, "
                "in denen ein übersichtlicher Arbeitsplatz zählt. Weiß / Eiche bringt "
                "eine freundliche Optik, während Holzwerkstoff und Stahl die klare "
                "Form unterstreichen.</p>"
                "<p>Schublade, offene Ablage und Kabelöffnung unterstützen einen "
                "geordneten Arbeitsalltag. Mit 120 x 76 x 60 cm bleibt Nova Compact "
                "platzsparend und trotzdem funktional nutzbar.</p>"
            ),
            "html_en": (
                "<p><strong>Nova Compact Desk</strong> is made for rooms where a clear "
                "workspace matters. White and oak colouring creates a friendly look, "
                "while engineered wood and steel underline the clean shape.</p>"
                "<p>The drawer, open shelf and cable opening support an organised work "
                "routine. With dimensions of 120 x 76 x 60 cm, Nova Compact remains "
                "space-saving while still practical.</p>"
            ),
        },
    },
    "PDC-MOB-007": {
        "variant_a": {
            "bulletpoints_de": [
                "Zweitüriger Kleiderschrank in Weiß",
                "Spiegeltür für einen hellen Raumeindruck",
                "Kleiderstange für hängende Kleidung",
                "Drei Einlegeböden für gefaltete Textilien",
                "Soft-Close-Scharniere als komfortables Detail",
            ],
            "html_de": (
                "<p><strong>Kleiderschrank Vela 2-türig</strong> bringt Ordnung und "
                "eine helle Optik ins Schlafzimmer oder Ankleidezimmer. Die weiße "
                "Front wirkt zurückhaltend, während das Spiegelglas den Raum optisch "
                "öffnet.</p>"
                "<p>Innen bietet Vela eine Kleiderstange und drei Einlegeböden. So "
                "finden hängende Kleidung, gefaltete Textilien und Accessoires ihren "
                "Platz. Soft-Close-Scharniere ergänzen den Schrank um ein angenehm "
                "ruhiges Bediengefühl.</p>"
            ),
            "html_en": (
                "<p><strong>Vela 2-Door Wardrobe</strong> brings storage and a bright "
                "look to the bedroom or dressing area. The white front feels calm, "
                "while the mirror glass visually opens the room.</p>"
                "<p>Inside, Vela offers a clothes rail and three shelves. Hanging "
                "garments, folded textiles and accessories can be arranged clearly. "
                "Soft-close hinges add a smooth everyday detail.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Weißer Kleiderschrank mit zwei Türen",
                "Spiegelglas als funktionales Frontdetail",
                "Innenaufteilung mit Stange und drei Böden",
                "Soft-Close-Scharniere für ruhiges Schließen",
                "Schrankmaß: 120 x 200 x 58 cm",
            ],
            "html_de": (
                "<p><strong>Kleiderschrank Vela 2-türig</strong> verbindet eine "
                "schlichte weiße Oberfläche mit einem praktischen Spiegelelement. So "
                "passt der Schrank gut in moderne Schlafzimmer, Gästezimmer oder "
                "Ankleidebereiche.</p>"
                "<p>Die Kleiderstange eignet sich für Jacken, Hemden oder Kleider; "
                "drei Einlegeböden strukturieren gefaltete Kleidung. Mit 120 x 200 x "
                "58 cm ist Vela klar dimensioniert und leicht einplanbar.</p>"
            ),
            "html_en": (
                "<p><strong>Vela 2-Door Wardrobe</strong> combines a simple white "
                "surface with a practical mirror element. It fits well into modern "
                "bedrooms, guest rooms or dressing areas.</p>"
                "<p>The clothes rail is suited for jackets, shirts or dresses, while "
                "three shelves organise folded clothing. With dimensions of 120 x "
                "200 x 58 cm, Vela is clearly defined and easy to plan.</p>"
            ),
        },
    },
    "PDC-MOB-008": {
        "variant_a": {
            "bulletpoints_de": [
                "Runder Couchtisch in Dunkelbraun / Schwarz",
                "Mangoholz und Metall im Materialmix",
                "Offenes Metallgestell für eine leichte Wirkung",
                "Ablagefläche für Bücher, Deko oder Fernbedienung",
                "Maße: 80 x 42 x 80 cm",
            ],
            "html_de": (
                "<p><strong>Couchtisch Rune rund</strong> bringt Dunkelbraun und "
                "Schwarz in ein markantes, rundes Tischdesign. Die Holzoptik der "
                "Tischplatte trifft auf ein offenes Metallgestell und setzt im "
                "Wohnzimmer einen klaren Akzent.</p>"
                "<p>Die zusätzliche Ablagefläche schafft Platz für Bücher, Deko oder "
                "Fernbedienung. Mit 80 x 42 x 80 cm bleibt Rune kompakt und ergänzt "
                "Sofa- oder Loungezonen ohne schwer zu wirken.</p>"
            ),
            "html_en": (
                "<p><strong>Rune Round Coffee Table</strong> combines dark brown and "
                "black in a distinctive round table design. The wood look of the top "
                "meets an open metal frame and creates a clear accent in the living "
                "room.</p>"
                "<p>The additional shelf offers space for books, decor or a remote "
                "control. With dimensions of 80 x 42 x 80 cm, Rune stays compact and "
                "complements sofa or lounge areas without looking heavy.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Couchtisch mit runder Tischplatte",
                "Dunkelbraune Holzoptik mit schwarzem Metall",
                "Offenes Gestell für eine klare Silhouette",
                "Praktische Ablagefläche unter der Tischplatte",
                "Kompaktes Format für den Wohnbereich",
            ],
            "html_de": (
                "<p><strong>Couchtisch Rune rund</strong> setzt auf eine runde "
                "Tischplatte und die Kombination aus Mangoholz und Metall. Dunkelbraun "
                "und Schwarz geben dem Tisch eine markante, aber gut kombinierbare "
                "Wirkung.</p>"
                "<p>Das offene Gestell lässt den Couchtisch leichter erscheinen. Die "
                "Ablagefläche unter der Platte ist ideal für Dinge, die im Alltag "
                "schnell griffbereit sein sollen.</p>"
            ),
            "html_en": (
                "<p><strong>Rune Round Coffee Table</strong> focuses on a round "
                "tabletop and the combination of mango wood and metal. Dark brown and "
                "black give the table a distinctive yet easy-to-combine look.</p>"
                "<p>The open frame makes the coffee table appear lighter. The shelf "
                "below the top is useful for items that should stay close at hand in "
                "everyday living.</p>"
            ),
        },
    },
    "PDC-MOB-009": {
        "variant_a": {
            "bulletpoints_de": [
                "TV-Lowboard in Anthrazit mit 180 cm Breite",
                "Zwei Klappen und ein offenes Fach",
                "Kabeldurchlass für angeschlossene Geräte",
                "Matte Fronten für eine ruhige Wohnwand",
                "Holzwerkstoff und Metall kombiniert",
            ],
            "html_de": (
                "<p><strong>TV-Lowboard Sora 180</strong> schafft eine ruhige Basis "
                "für Fernseher, Receiver und Medienzubehör. Anthrazitfarbene, matte "
                "Fronten passen gut zu modernen Wohnbereichen und lassen Technik "
                "optisch geordneter wirken.</p>"
                "<p>Zwei Klappen verbergen Zubehör, während das offene Fach schnellen "
                "Zugriff auf Geräte ermöglicht. Der Kabeldurchlass unterstützt eine "
                "saubere Kabelführung. Mit 180 x 50 x 40 cm ist Sora breit und flach "
                "dimensioniert.</p>"
            ),
            "html_en": (
                "<p><strong>Sora 180 TV Lowboard</strong> creates a calm base for a TV, "
                "receiver and media accessories. Anthracite matt fronts suit modern "
                "living rooms and help technology look more organised.</p>"
                "<p>Two flap doors hide accessories, while the open compartment keeps "
                "devices easy to access. The cable outlet supports tidy cable routing. "
                "At 180 x 50 x 40 cm, Sora has a wide and low format.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Anthrazitfarbenes Lowboard für TV-Bereiche",
                "Matte Fronten mit ruhiger Optik",
                "Offenes Fach für Receiver oder Konsole",
                "Zwei Klappen für verdeckten Stauraum",
                "Kabeldurchlass für mehr Ordnung",
            ],
            "html_de": (
                "<p><strong>TV-Lowboard Sora 180</strong> bringt Ordnung in den "
                "Medienbereich. Die anthrazitfarbene Oberfläche und die matten Fronten "
                "wirken zurückhaltend und lassen sich gut mit hellen wie dunklen "
                "Wohnkonzepten kombinieren.</p>"
                "<p>Das offene Fach bietet Platz für Geräte, die direkt erreichbar "
                "bleiben sollen. Hinter zwei Klappen verschwinden Zubehör, Kabel oder "
                "kleinere Alltagsgegenstände. Der Kabeldurchlass erleichtert eine "
                "aufgeräumte Technikzone.</p>"
            ),
            "html_en": (
                "<p><strong>Sora 180 TV Lowboard</strong> brings order to the media "
                "area. The anthracite surface and matt fronts feel understated and "
                "combine well with both light and dark interior concepts.</p>"
                "<p>The open compartment holds devices that need to stay accessible. "
                "Behind two flap doors, accessories, cables or smaller everyday items "
                "can be stored out of sight. The cable outlet helps create a tidy "
                "media setup.</p>"
            ),
        },
    },
    "PDC-MOB-010": {
        "variant_a": {
            "bulletpoints_de": [
                "Kommode in sanftem Salbeigrün",
                "Vier Schubladen für geordneten Stauraum",
                "Griffloses Design für eine ruhige Front",
                "Filigrane Metallfüße als leichter Akzent",
                "Pflegeleichte Oberfläche für den Alltag",
            ],
            "html_de": (
                "<p><strong>Kommode Elba 4 Schubladen</strong> bringt mit Salbeigrün "
                "einen sanften Farbakzent in Flur, Schlafzimmer oder Wohnbereich. Die "
                "grifflose Front wirkt besonders ruhig und lässt die Farbe klar zur "
                "Geltung kommen.</p>"
                "<p>Vier Schubladen bieten Platz für Kleidung, Accessoires oder "
                "Alltagsgegenstände. Filigrane Metallfüße heben die Kommode optisch an, "
                "während die pflegeleichte Oberfläche den Einsatz im Alltag angenehm "
                "unkompliziert macht.</p>"
            ),
            "html_en": (
                "<p><strong>Elba Chest of 4 Drawers</strong> adds a soft sage green "
                "accent to the hallway, bedroom or living area. The handleless front "
                "looks calm and lets the colour stand out clearly.</p>"
                "<p>Four drawers provide space for clothing, accessories or everyday "
                "items. Slim metal feet visually lift the chest of drawers, while the "
                "easy-care surface makes everyday use simple.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Salbeigrüne Kommode mit vier Schubladen",
                "Grifflose Front für ein klares Erscheinungsbild",
                "MDF und Metall als Materialkombination",
                "Filigrane Metallfüße setzen einen modernen Akzent",
                "Kompaktes Maß: 100 x 85 x 40 cm",
            ],
            "html_de": (
                "<p><strong>Kommode Elba 4 Schubladen</strong> verbindet Stauraum mit "
                "einem frischen, aber zurückhaltenden Farbton. Salbeigrün bringt Ruhe "
                "in den Raum und passt gut zu Holz, Weiß oder dunklen Akzenten.</p>"
                "<p>Vier Schubladen strukturieren den Inhalt übersichtlich. Die "
                "grifflose Front und die filigranen Metallfüße geben Elba eine klare "
                "Linie. Mit 100 x 85 x 40 cm eignet sich die Kommode auch für kleinere "
                "Bereiche.</p>"
            ),
            "html_en": (
                "<p><strong>Elba Chest of 4 Drawers</strong> combines storage with a "
                "fresh yet understated colour. Sage green brings calm to the room and "
                "works well with wood, white or darker accents.</p>"
                "<p>Four drawers keep contents clearly organised. The handleless front "
                "and slim metal feet give Elba a clean line. With dimensions of "
                "100 x 85 x 40 cm, the chest also fits smaller areas.</p>"
            ),
        },
    },
}


def normalize_furniture_demo_variant(variant):
    """Return a supported deterministic variant key."""
    if variant in FURNITURE_DEMO_VARIANTS:
        return variant

    return "variant_a"


def toggle_furniture_demo_variant(variant):
    """Switch between the two prepared offline content variants."""
    if normalize_furniture_demo_variant(variant) == "variant_a":
        return "variant_b"

    return "variant_a"


def get_furniture_demo_content(sku, variant="variant_a"):
    """Return prepared demo content for one SKU without calling any AI provider."""
    product_content = FURNITURE_DEMO_CONTENT.get(str(sku).strip())
    if product_content is None:
        return None

    return product_content[normalize_furniture_demo_variant(variant)]


def get_furniture_demo_skus():
    """Return all SKUs covered by the prepared furniture demo content."""
    return tuple(FURNITURE_DEMO_CONTENT.keys())


def normalize_furniture_demo_section_status(value):
    """Normalize one internal review section status."""
    if str(value).strip().lower() in ["approved", "freigegeben", "✓ freigegeben"]:
        return FURNITURE_DEMO_REVIEW_APPROVED

    return FURNITURE_DEMO_REVIEW_OPEN


def normalize_furniture_demo_review_decisions(value=None):
    """Return internal review decisions for the three demo content sections."""
    if isinstance(value, dict):
        return {
            section_key: normalize_furniture_demo_section_status(value.get(section_key))
            for section_key in FURNITURE_DEMO_REVIEW_SECTION_KEYS
        }

    normalized_status = normalize_furniture_demo_section_status(value)
    return {
        section_key: normalized_status
        for section_key in FURNITURE_DEMO_REVIEW_SECTION_KEYS
    }


def count_approved_furniture_demo_sections(review_decisions=None):
    """Count approved internal review sections for one product."""
    normalized_decisions = normalize_furniture_demo_review_decisions(review_decisions)

    return sum(
        1
        for section_key in FURNITURE_DEMO_REVIEW_SECTION_KEYS
        if normalized_decisions[section_key] == FURNITURE_DEMO_REVIEW_APPROVED
    )


def get_furniture_demo_final_review_status(review_decisions=None):
    """Return the single export-facing product review status."""
    if count_approved_furniture_demo_sections(review_decisions) == len(
        FURNITURE_DEMO_REVIEW_SECTION_KEYS
    ):
        return FURNITURE_DEMO_REVIEW_APPROVED

    return FURNITURE_DEMO_REVIEW_OPEN


def approve_furniture_demo_review_section(review_decisions, section_key):
    """Return updated internal decisions with one section approved."""
    normalized_decisions = normalize_furniture_demo_review_decisions(review_decisions)
    if section_key in FURNITURE_DEMO_REVIEW_SECTION_KEYS:
        normalized_decisions[section_key] = FURNITURE_DEMO_REVIEW_APPROVED

    return normalized_decisions


def reset_furniture_demo_review_decisions():
    """Return open internal review decisions for all demo content sections."""
    return normalize_furniture_demo_review_decisions()


def should_advance_furniture_demo_product(review_decisions=None):
    """Return True only when all internal review sections are approved."""
    return (
        get_furniture_demo_final_review_status(review_decisions)
        == FURNITURE_DEMO_REVIEW_APPROVED
    )


def get_next_furniture_demo_position(current_position, product_count):
    """Return the next product position without moving past the final product."""
    if product_count <= 0:
        return 0

    return min(current_position + 1, product_count - 1)
