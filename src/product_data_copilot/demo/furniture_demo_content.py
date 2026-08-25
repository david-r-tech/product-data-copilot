"""Prepared offline content variants for the German furniture demo.

The demo content is deterministic and does not call an AI provider. Each text
uses only facts from the demo furniture spreadsheet so the presentation can show
a safe human-in-the-loop content workflow without invented product claims.
"""

FURNITURE_DEMO_DEFAULT_SKU = "PDC-MOB-001"
FURNITURE_DEMO_VARIANTS = ("variant_a", "variant_b")
FURNITURE_DEMO_REVIEW_OPEN = "Noch nicht freigegeben"
FURNITURE_DEMO_REVIEW_APPROVED = "Freigegeben"


FURNITURE_DEMO_CONTENT = {
    "PDC-MOB-001": {
        "variant_a": {
            "bulletpoints_de": [
                "3-Sitzer-Sofa in Hellgrau mit Webstoffbezug",
                "Massivholz aus Eiche und konische Holzfüße",
                "Abnehmbare Sitzkissen laut Produktdaten",
                "Maße: 220 x 84 x 92 cm",
                "Pflegeleichter Webstoff ist in den Produktdaten angegeben",
            ],
            "html_de": (
                "<p><strong>Nordic Lounge Sofa 3-Sitzer</strong> kombiniert einen "
                "hellgrauen Webstoffbezug mit Massivholz aus Eiche. Die konischen "
                "Holzfüße und die abnehmbaren Sitzkissen sind als zentrale Merkmale "
                "in den Produktdaten angegeben.</p>"
                "<p>Mit Maßen von 220 x 84 x 92 cm ist das Sofa klar beschrieben. "
                "Der Datensatz nennt außerdem pflegeleichten Webstoff als "
                "Produkteigenschaft.</p>"
            ),
            "html_en": (
                "<p><strong>Nordic Lounge 3-Seater Sofa</strong> combines light "
                "grey woven fabric with solid oak wood. The product data lists "
                "tapered wooden legs and removable seat cushions as key features.</p>"
                "<p>The sofa is specified with dimensions of 220 x 84 x 92 cm. "
                "Easy-care woven fabric is also included in the provided product "
                "information.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Hellgraues 3-Sitzer-Sofa mit abnehmbaren Sitzkissen",
                "Materialmix aus Webstoff und Massivholz (Eiche)",
                "Konische Holzfüße als sichtbares Produktmerkmal",
                "Angegebene Maße: 220 x 84 x 92 cm",
                "Produktdaten nennen einen pflegeleichten Webstoff",
            ],
            "html_de": (
                "<p><strong>Nordic Lounge Sofa 3-Sitzer</strong> wird in Hellgrau "
                "geführt und besteht laut Datensatz aus Webstoff und Massivholz "
                "(Eiche). Die abnehmbaren Sitzkissen und konischen Holzfüße geben "
                "dem Produkt seine wichtigsten beschriebenen Merkmale.</p>"
                "<p>Die Maße sind mit 220 x 84 x 92 cm angegeben. Zusätzlich nennt "
                "der Datensatz einen pflegeleichten Webstoff.</p>"
            ),
            "html_en": (
                "<p><strong>Nordic Lounge 3-Seater Sofa</strong> is listed in light "
                "grey and, according to the source data, uses woven fabric and solid "
                "oak wood. Removable seat cushions and tapered wooden legs are the "
                "main described features.</p>"
                "<p>The stated dimensions are 220 x 84 x 92 cm. The data also lists "
                "easy-care woven fabric.</p>"
            ),
        },
    },
    "PDC-MOB-002": {
        "variant_a": {
            "bulletpoints_de": [
                "Esstisch Arvid aus geöltem Massivholz (Eiche)",
                "Ausziehbar auf 230 cm laut Produktdaten",
                "Natürliche Farbgebung mit geölter Oberfläche",
                "Abgerundete Kanten sind angegeben",
                "Maße: 180 x 75 x 90 cm",
            ],
            "html_de": (
                "<p><strong>Eichenholz Esstisch Arvid</strong> besteht laut "
                "Produktdaten aus geöltem Massivholz (Eiche) und wird in der Farbe "
                "Natur geführt. Der Tisch ist auf 230 cm ausziehbar.</p>"
                "<p>Die Produktdaten nennen eine geölte Oberfläche und abgerundete "
                "Kanten. Die Maße sind mit 180 x 75 x 90 cm angegeben.</p>"
            ),
            "html_en": (
                "<p><strong>Arvid Oak Dining Table</strong> is listed as oiled solid "
                "oak wood in a natural colour. The table can be extended to 230 cm "
                "according to the product data.</p>"
                "<p>The source data also mentions an oiled surface and rounded "
                "edges. The stated dimensions are 180 x 75 x 90 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Geölter Esstisch aus Massivholz (Eiche)",
                "Ausziehfunktion bis 230 cm",
                "Farbton Natur laut Datensatz",
                "Mit abgerundeten Kanten beschrieben",
                "Format: 180 x 75 x 90 cm",
            ],
            "html_de": (
                "<p><strong>Eichenholz Esstisch Arvid</strong> wird mit geöltem "
                "Massivholz aus Eiche und dem Farbton Natur beschrieben. Die "
                "Ausziehfunktion auf 230 cm ist als Merkmal hinterlegt.</p>"
                "<p>Zusätzlich enthält der Datensatz eine geölte Oberfläche, "
                "abgerundete Kanten und Maße von 180 x 75 x 90 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Arvid Oak Dining Table</strong> is described with oiled "
                "solid oak wood and a natural finish. The extension to 230 cm is "
                "included as a product feature.</p>"
                "<p>The data also lists an oiled surface, rounded edges and "
                "dimensions of 180 x 75 x 90 cm.</p>"
            ),
        },
    },
    "PDC-MOB-003": {
        "variant_a": {
            "bulletpoints_de": [
                "2er-Set Polsterstühle in Smaragdgrün",
                "Samtbezug mit gepolsterter Sitzfläche",
                "Materialien: Metall, Samtstoff und Schaumstoff",
                "Pulverbeschichtetes Metallgestell laut Produktdaten",
                "Maße je Stuhl: 52 x 84 x 58 cm",
            ],
            "html_de": (
                "<p><strong>Polsterstuhl Maja 2er-Set</strong> wird als Set aus zwei "
                "Stühlen in Smaragdgrün geführt. Die Produktdaten nennen Samtbezug, "
                "gepolsterte Sitzfläche und ein pulverbeschichtetes Metallgestell.</p>"
                "<p>Als Materialien sind Metall, Samtstoff und Schaumstoff angegeben. "
                "Die Maße betragen 52 x 84 x 58 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Maja Upholstered Chair Set of 2</strong> is listed as a "
                "two-chair set in emerald green. The product data includes velvet "
                "upholstery, a padded seat and a powder-coated metal frame.</p>"
                "<p>The listed materials are metal, velvet fabric and foam. The "
                "dimensions are 52 x 84 x 58 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Zwei Stühle im Set, Farbe Smaragdgrün",
                "Gepolsterte Sitzfläche mit Samtbezug",
                "Metallgestell mit Pulverbeschichtung",
                "Materialangaben: Metall, Samtstoff, Schaumstoff",
                "Angegebenes Maß: 52 x 84 x 58 cm",
            ],
            "html_de": (
                "<p><strong>Polsterstuhl Maja 2er-Set</strong> fasst zwei Stühle in "
                "Smaragdgrün zusammen. Laut Datensatz gehören die gepolsterte "
                "Sitzfläche und der Samtbezug zu den zentralen Merkmalen.</p>"
                "<p>Das Metallgestell ist als pulverbeschichtet angegeben. Die "
                "Produktdaten nennen außerdem Maße von 52 x 84 x 58 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Maja Upholstered Chair Set of 2</strong> includes two "
                "chairs in emerald green. According to the source data, the padded "
                "seat and velvet upholstery are key features.</p>"
                "<p>The metal frame is listed as powder-coated. The product data also "
                "states dimensions of 52 x 84 x 58 cm.</p>"
            ),
        },
    },
    "PDC-MOB-004": {
        "variant_a": {
            "bulletpoints_de": [
                "Sideboard in Eiche / Schwarz mit drei Türen",
                "Materialien: MDF, Eichenfurnier und Metall",
                "Zwei höhenverstellbare Einlegeböden",
                "Kabelführung und schwarze Metallgriffe",
                "Maße: 160 x 78 x 42 cm",
            ],
            "html_de": (
                "<p><strong>Sideboard Lino mit 3 Türen</strong> kombiniert Eiche / "
                "Schwarz mit MDF, Eichenfurnier und Metall. Der Datensatz nennt drei "
                "Türen und schwarze Metallgriffe.</p>"
                "<p>Zwei höhenverstellbare Einlegeböden und eine Kabelführung sind "
                "als Merkmale angegeben. Die Maße betragen 160 x 78 x 42 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Lino Sideboard with 3 Doors</strong> combines oak / black "
                "colouring with MDF, oak veneer and metal. The data lists three doors "
                "and black metal handles.</p>"
                "<p>Two height-adjustable shelves and cable management are included "
                "as features. The stated dimensions are 160 x 78 x 42 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Dreitüriges Sideboard in Eiche / Schwarz",
                "MDF, Eichenfurnier und Metall laut Materialangabe",
                "Mit zwei höhenverstellbaren Einlegeböden",
                "Kabelführung als praktisches Ausstattungsmerkmal",
                "Format: 160 x 78 x 42 cm",
            ],
            "html_de": (
                "<p><strong>Sideboard Lino mit 3 Türen</strong> ist mit Eiche / "
                "Schwarz, MDF, Eichenfurnier und Metall beschrieben. Die drei Türen "
                "und schwarzen Metallgriffe sind in den Produktdaten enthalten.</p>"
                "<p>Der Datensatz führt außerdem zwei höhenverstellbare Einlegeböden "
                "sowie eine Kabelführung auf. Die Maße sind 160 x 78 x 42 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Lino Sideboard with 3 Doors</strong> is described with "
                "oak / black colouring, MDF, oak veneer and metal. Three doors and "
                "black metal handles are included in the product data.</p>"
                "<p>The source also lists two height-adjustable shelves and cable "
                "management. The dimensions are 160 x 78 x 42 cm.</p>"
            ),
        },
    },
    "PDC-MOB-005": {
        "variant_a": {
            "bulletpoints_de": [
                "Polsterbett Haven mit Liegefläche 160 x 200 cm",
                "Materialien: Holzwerkstoff, Bouclé-Stoff und Metall",
                "Cremefarbene Ausführung laut Produktdaten",
                "Gepolstertes Kopfteil und Stauraum angegeben",
                "Maße: 178 x 108 x 218 cm",
            ],
            "html_de": (
                "<p><strong>Polsterbett Haven 160 x 200 cm</strong> wird in Creme "
                "geführt und nutzt Holzwerkstoff, Bouclé-Stoff und Metall. Die "
                "Liegefläche ist mit 160 x 200 cm angegeben.</p>"
                "<p>Als Merkmale nennt der Datensatz ein gepolstertes Kopfteil, "
                "einen enthaltenen Lattenrost und Stauraum. Die Gesamtmaße sind "
                "178 x 108 x 218 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Haven Upholstered Bed 160 x 200 cm</strong> is listed in "
                "cream and uses engineered wood, bouclé fabric and metal. The lying "
                "surface is specified as 160 x 200 cm.</p>"
                "<p>The data lists an upholstered headboard, an included slatted "
                "frame and storage space. Overall dimensions are 178 x 108 x 218 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Bett in Creme mit Liegefläche 160 x 200 cm",
                "Bouclé-Stoff, Holzwerkstoff und Metall",
                "Gepolstertes Kopfteil laut Datensatz",
                "Lattenrost inklusive und Stauraum angegeben",
                "Gesamtmaß: 178 x 108 x 218 cm",
            ],
            "html_de": (
                "<p><strong>Polsterbett Haven 160 x 200 cm</strong> verbindet laut "
                "Datensatz Holzwerkstoff, Bouclé-Stoff und Metall in der Farbe "
                "Creme. Die Liegefläche beträgt 160 x 200 cm.</p>"
                "<p>Hinterlegt sind ein gepolstertes Kopfteil, ein inklusiver "
                "Lattenrost und Stauraum. Die angegebenen Gesamtmaße lauten "
                "178 x 108 x 218 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Haven Upholstered Bed 160 x 200 cm</strong> combines "
                "engineered wood, bouclé fabric and metal in cream according to the "
                "source data. The lying surface is 160 x 200 cm.</p>"
                "<p>The listed features include an upholstered headboard, an included "
                "slatted frame and storage space. Overall dimensions are "
                "178 x 108 x 218 cm.</p>"
            ),
        },
    },
    "PDC-MOB-006": {
        "variant_a": {
            "bulletpoints_de": [
                "Schreibtisch in Weiß / Eiche",
                "Holzwerkstoff und Stahl laut Materialangabe",
                "Kompakte Arbeitsfläche mit Kabelöffnung",
                "Seitliches Ablagefach und stabile Stahlbeine",
                "Maße: 120 x 76 x 60 cm",
            ],
            "html_de": (
                "<p><strong>Schreibtisch Nova Compact</strong> wird in Weiß / Eiche "
                "geführt und besteht laut Datensatz aus Holzwerkstoff und Stahl. "
                "Die Produktdaten nennen eine kompakte Arbeitsfläche.</p>"
                "<p>Als weitere Merkmale sind Kabelöffnung, seitliches Ablagefach "
                "und stabile Stahlbeine angegeben. Die Maße betragen 120 x 76 x 60 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Nova Compact Desk</strong> is listed in white / oak and "
                "uses engineered wood and steel according to the data. The product "
                "information includes a compact work surface.</p>"
                "<p>Additional listed features are a cable opening, side storage "
                "compartment and stable steel legs. The dimensions are 120 x 76 x 60 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Kompakter Schreibtisch mit Arbeitsfläche",
                "Farbe Weiß / Eiche im Datensatz",
                "Mit Kabelöffnung und seitlichem Ablagefach",
                "Holzwerkstoff und Stahl als Materialien",
                "Angegebenes Maß: 120 x 76 x 60 cm",
            ],
            "html_de": (
                "<p><strong>Schreibtisch Nova Compact</strong> ist mit einer kompakten "
                "Arbeitsfläche, Kabelöffnung und seitlichem Ablagefach beschrieben. "
                "Die Farbgebung ist Weiß / Eiche.</p>"
                "<p>Der Datensatz nennt Holzwerkstoff und Stahl als Materialien sowie "
                "stabile Stahlbeine. Die Maße sind 120 x 76 x 60 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Nova Compact Desk</strong> is described with a compact "
                "work surface, cable opening and side storage compartment. The colour "
                "combination is white / oak.</p>"
                "<p>The source data lists engineered wood and steel as materials, "
                "along with stable steel legs. The dimensions are 120 x 76 x 60 cm.</p>"
            ),
        },
    },
    "PDC-MOB-007": {
        "variant_a": {
            "bulletpoints_de": [
                "2-türiger Kleiderschrank in Weiß",
                "Holzwerkstoff und Spiegelglas laut Materialangabe",
                "Mit Spiegeltür und Kleiderstange",
                "Drei Einlegeböden und Soft-Close-Scharniere",
                "Maße: 120 x 200 x 58 cm",
            ],
            "html_de": (
                "<p><strong>Kleiderschrank Vela 2-türig</strong> wird in Weiß geführt "
                "und besteht laut Datensatz aus Holzwerkstoff und Spiegelglas. Die "
                "Produktdaten nennen zwei Türen und eine Spiegeltür.</p>"
                "<p>Zusätzlich sind Kleiderstange, drei Einlegeböden und "
                "Soft-Close-Scharniere aufgeführt. Die Maße betragen 120 x 200 x 58 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Vela 2-Door Wardrobe</strong> is listed in white and uses "
                "engineered wood and mirror glass according to the data. The product "
                "information includes two doors and a mirrored door.</p>"
                "<p>A clothes rail, three shelves and soft-close hinges are also "
                "listed. The dimensions are 120 x 200 x 58 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Kleiderschrank mit zwei Türen",
                "Weiße Ausführung mit Spiegelglas",
                "Kleiderstange und drei Einlegeböden",
                "Soft-Close-Scharniere laut Produktdaten",
                "Format: 120 x 200 x 58 cm",
            ],
            "html_de": (
                "<p><strong>Kleiderschrank Vela 2-türig</strong> fasst die "
                "hinterlegten Merkmale kompakt zusammen: zwei Türen, Spiegeltür, "
                "Kleiderstange und drei Einlegeböden.</p>"
                "<p>Als Materialien sind Holzwerkstoff und Spiegelglas angegeben. "
                "Der Datensatz nennt außerdem Soft-Close-Scharniere und Maße von "
                "120 x 200 x 58 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Vela 2-Door Wardrobe</strong> summarises the listed "
                "features as two doors, mirrored door, clothes rail and three shelves.</p>"
                "<p>The materials are engineered wood and mirror glass. The source "
                "also lists soft-close hinges and dimensions of 120 x 200 x 58 cm.</p>"
            ),
        },
    },
    "PDC-MOB-008": {
        "variant_a": {
            "bulletpoints_de": [
                "Runder Couchtisch in Dunkelbraun / Schwarz",
                "Materialien: Mangoholz und Metall",
                "Runde Tischplatte laut Produktdaten",
                "Offenes Metallgestell und Ablagefläche",
                "Maße: 80 x 42 x 80 cm",
            ],
            "html_de": (
                "<p><strong>Couchtisch Rune rund</strong> kombiniert Dunkelbraun / "
                "Schwarz mit Mangoholz und Metall. Die Produktdaten nennen eine "
                "runde Tischplatte und ein offenes Metallgestell.</p>"
                "<p>Eine handbearbeitete Holzmaserung und eine Ablagefläche sind "
                "ebenfalls aufgeführt. Die Maße betragen 80 x 42 x 80 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Rune Round Coffee Table</strong> combines dark brown / "
                "black colouring with mango wood and metal. The product data lists "
                "a round tabletop and an open metal frame.</p>"
                "<p>A hand-finished wood grain and a shelf area are also listed. "
                "The dimensions are 80 x 42 x 80 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Couchtisch mit runder Tischplatte",
                "Dunkelbraun / Schwarz als Farbangabe",
                "Mangoholz und Metall laut Datensatz",
                "Offenes Metallgestell mit Ablagefläche",
                "Angegebenes Maß: 80 x 42 x 80 cm",
            ],
            "html_de": (
                "<p><strong>Couchtisch Rune rund</strong> wird mit runder Tischplatte, "
                "offenem Metallgestell und Ablagefläche beschrieben. Die Farbangabe "
                "lautet Dunkelbraun / Schwarz.</p>"
                "<p>Als Materialien sind Mangoholz und Metall hinterlegt. Zusätzlich "
                "nennt der Datensatz eine handbearbeitete Holzmaserung und Maße von "
                "80 x 42 x 80 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Rune Round Coffee Table</strong> is described with a "
                "round tabletop, open metal frame and shelf area. The listed colour "
                "is dark brown / black.</p>"
                "<p>The materials are mango wood and metal. The source also mentions "
                "a hand-finished wood grain and dimensions of 80 x 42 x 80 cm.</p>"
            ),
        },
    },
    "PDC-MOB-009": {
        "variant_a": {
            "bulletpoints_de": [
                "TV-Lowboard Sora 180 in Anthrazit",
                "Holzwerkstoff und Metall laut Materialangabe",
                "Zwei Schubladen sind angegeben",
                "Offene Gerätefächer und Kabeldurchlass",
                "Maße: 180 x 50 x 40 cm",
            ],
            "html_de": (
                "<p><strong>TV-Lowboard Sora 180</strong> wird in Anthrazit geführt "
                "und nutzt laut Datensatz Holzwerkstoff und Metall. Die Produktdaten "
                "nennen zwei Schubladen und offene Gerätefächer.</p>"
                "<p>Ein Kabeldurchlass und matte Fronten sind ebenfalls angegeben. "
                "Die Maße betragen 180 x 50 x 40 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Sora 180 TV Lowboard</strong> is listed in anthracite and "
                "uses engineered wood and metal according to the data. The product "
                "information includes two drawers and open device compartments.</p>"
                "<p>A cable opening and matt fronts are also listed. The dimensions "
                "are 180 x 50 x 40 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Lowboard für TV-Möbel mit 180 cm Breite",
                "Farbe Anthrazit laut Produktdaten",
                "Mit zwei Schubladen und offenen Gerätefächern",
                "Kabeldurchlass und matte Fronten angegeben",
                "Format: 180 x 50 x 40 cm",
            ],
            "html_de": (
                "<p><strong>TV-Lowboard Sora 180</strong> enthält laut Datensatz zwei "
                "Schubladen, offene Gerätefächer und einen Kabeldurchlass. Die "
                "Farbe ist Anthrazit.</p>"
                "<p>Als Materialien sind Holzwerkstoff und Metall angegeben. Die "
                "Produktdaten nennen zudem matte Fronten und Maße von 180 x 50 x 40 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Sora 180 TV Lowboard</strong> includes two drawers, open "
                "device compartments and a cable opening according to the source "
                "data. The colour is anthracite.</p>"
                "<p>The materials are engineered wood and metal. The product data "
                "also lists matt fronts and dimensions of 180 x 50 x 40 cm.</p>"
            ),
        },
    },
    "PDC-MOB-010": {
        "variant_a": {
            "bulletpoints_de": [
                "Kommode Elba mit vier Schubladen",
                "Farbe Salbeigrün laut Datensatz",
                "MDF und Metall als Materialien",
                "Griffloses Design und filigrane Metallfüße",
                "Maße: 100 x 85 x 40 cm",
            ],
            "html_de": (
                "<p><strong>Kommode Elba 4 Schubladen</strong> wird in Salbeigrün "
                "geführt und besteht laut Datensatz aus MDF und Metall. Die vier "
                "Schubladen sind als zentrales Merkmal angegeben.</p>"
                "<p>Der Datensatz nennt außerdem griffloses Design, pflegeleichte "
                "Oberfläche und filigrane Metallfüße. Die Maße betragen 100 x 85 x 40 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Elba Chest of 4 Drawers</strong> is listed in sage green "
                "and uses MDF and metal according to the data. The four drawers are "
                "the main listed feature.</p>"
                "<p>The source data also mentions a handleless design, easy-care "
                "surface and slim metal feet. The dimensions are 100 x 85 x 40 cm.</p>"
            ),
        },
        "variant_b": {
            "bulletpoints_de": [
                "Vier Schubladen laut Produktdaten",
                "Kommode in Salbeigrün",
                "Materialangabe: MDF und Metall",
                "Griffloses Design mit filigranen Metallfüßen",
                "Angegebenes Maß: 100 x 85 x 40 cm",
            ],
            "html_de": (
                "<p><strong>Kommode Elba 4 Schubladen</strong> fasst vier Schubladen, "
                "griffloses Design und filigrane Metallfüße in einem Produktdatensatz "
                "zusammen. Die Farbe ist Salbeigrün.</p>"
                "<p>Als Materialien sind MDF und Metall hinterlegt. Zusätzlich nennt "
                "der Datensatz eine pflegeleichte Oberfläche und Maße von "
                "100 x 85 x 40 cm.</p>"
            ),
            "html_en": (
                "<p><strong>Elba Chest of 4 Drawers</strong> combines four drawers, "
                "a handleless design and slim metal feet in the product data. The "
                "colour is sage green.</p>"
                "<p>The listed materials are MDF and metal. The data also includes "
                "an easy-care surface and dimensions of 100 x 85 x 40 cm.</p>"
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
    return "variant_b" if normalize_furniture_demo_variant(variant) == "variant_a" else "variant_a"


def get_furniture_demo_content(sku, variant="variant_a"):
    """Return prepared demo content for one SKU without calling any AI provider."""
    product_content = FURNITURE_DEMO_CONTENT.get(str(sku).strip())
    if product_content is None:
        return None

    return product_content[normalize_furniture_demo_variant(variant)]


def get_furniture_demo_skus():
    """Return all SKUs covered by the prepared furniture demo content."""
    return tuple(FURNITURE_DEMO_CONTENT.keys())
