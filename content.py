"""All website content (German + English).

To change text on the site, edit this file and run `python build.py`.
Every text that differs per language is a dict {"de": ..., "en": ...}.
"""

COMPANY = {
    "name": "CH engineering GmbH",
    "short": "CH engineering",
    "email": "info@che-weinbau.de",
    "phone": "+49 6541 8177611",
    "phone_display": "+49 (0)6541 8177611",
    "street": "Moselweinstraße 110",
    "zip_city": "54536 Kröv",
    "production": {
        "street": "Moselweinstraße 84a",
        "zip_city": "54487 Wintrich",
        "phone": "+49 6534 7994293",
        "phone_display": "+49 (0)6534 7994293",
    },
    "managing_directors": ["Peter Hoffmann", "Matthias Christ", "Roland Holbach"],
    "vat_id": "DE 299570324",
    "social": {
        "Facebook": "https://www.facebook.com/CH-engineering-244572932604753/",
        "Instagram": "https://www.instagram.com/ch_engineering/",
        "YouTube": "https://www.youtube.com/channel/UClRDJGX--0-gW1RtLfimI4A",
    },
}

SITE_URL = "https://che-weinbau.com"

# Visitor analytics: Plausible (cookieless, EU-hosted, no consent banner needed).
# Set to None to switch analytics off.
PLAUSIBLE_DOMAIN = "che-weinbau.com"
PLAUSIBLE_SCRIPT = "https://plausible.io/js/pa-fHH1l0u0f-Hv9c2HzHAAH.js"  # site-specific script from Plausible

# ---------------------------------------------------------------- navigation
# key -> path per language (paths end with "/"; "" is the German home page)
PAGES = {
    "home":    {"de": "",                           "en": "en/"},
    "msh":     {"de": "der-steillagen-vollernter/", "en": "en/the-steep-slope-harvester/"},
    "ut125":   {"de": "raupenfahrzeug-ut125/",      "en": "en/crawler-ut125/"},
    "keller":  {"de": "kellertechnik/",             "en": "en/cellar-technology/"},
    "news":    {"de": "news/",                      "en": "en/news/"},
    "contact": {"de": "kontakt/",                   "en": "en/contact/"},
    "imprint": {"de": "impressum/",                 "en": "en/imprint/"},
    "privacy": {"de": "datenschutz/",               "en": "en/privacy/"},
}

NAV = ["msh", "ut125", "keller", "news", "contact"]

NAV_LABELS = {
    "home":    {"de": "Startseite", "en": "Home"},
    "msh":     {"de": "Steillagen-Vollernter", "en": "Steep Slope Harvester"},
    "ut125":   {"de": "Raupe UT 125", "en": "Crawler UT 125"},
    "keller":  {"de": "Kellertechnik", "en": "Cellar technology"},
    "news":    {"de": "News", "en": "News"},
    "contact": {"de": "Kontakt", "en": "Contact"},
    "imprint": {"de": "Impressum", "en": "Imprint"},
    "privacy": {"de": "Datenschutz", "en": "Privacy"},
}

# Old WordPress URLs that should keep working (old path -> page key, language)
REDIRECTS = {
    "andreoli-ut-110/": ("ut125", "de"),
    "en/home/": ("home", "en"),
    "en/cms-system/": ("ut125", "en"),
    "rechtlicher-hinweis/": ("imprint", "de"),
    "en/meet-us-at-simei-2026-in-milan/": ("news", "en"),
    "en/ch-engineering-at-eima-2026/": ("news", "en"),
    "en/zuhause-an-der-mosel-vitis-live-2026-in-piesport-2/": ("news", "de"),
    "en/ch-engineering-gmbh-realises-compact-harvesting-vehicle-with-igus-energy-chains/": ("news", "en"),
    "en/weinlese-mit-vollernter-wie-winzer-den-personalmangel-bekaempfen/": ("news", "de"),
    "en/first-steep-slope-harvester-in-north-america/": ("news", "en"),
    "en/ch-engineering-viel-neues-beim-steillagen-vollernter/": ("news", "de"),
    "en/zu-gast-bei-einem-weltmarktfuehrer-aus-piesport-an-der-mosel/": ("news", "de"),
    "en/von-der-drohne-bis-zum-steillagen-vollernter/": ("news", "de"),
    "en/harvesting-in-douro-valley/": ("news", "en"),
}

# ---------------------------------------------------------------- UI strings
UI = {
    "skip": {"de": "Zum Inhalt springen", "en": "Skip to content"},
    "menu": {"de": "Menü", "en": "Menu"},
    "close": {"de": "Schließen", "en": "Close"},
    "lang_switch": {"de": "English", "en": "Deutsch"},
    "learn_more": {"de": "Mehr erfahren", "en": "Learn more"},
    "contact_cta": {"de": "Beratung anfragen", "en": "Get in touch"},
    "specs_note": {"de": "Die technischen Angaben sind unverbindlich.",
                   "en": "Technical specifications are non-binding."},
    "read_source": {"de": "Zum Artikel", "en": "Read article"},
    "source": {"de": "Quelle", "en": "Source"},
    "all_news": {"de": "Alle News", "en": "All news"},
    "footer_claim": {"de": "Innovation im Weinbau – entwickelt und gebaut an der Mosel.",
                     "en": "Innovation in viticulture – engineered and built on the Mosel."},
    "hours": {"de": "Öffnungszeiten", "en": "Opening hours"},
    "hours_text": {"de": ["Mo – Do: 8:00–12:00 & 13:00–16:15", "Fr: 8:00–12:00"],
                   "en": ["Mon – Thu: 8:00–12:00 & 13:00–16:15", "Fri: 8:00–12:00"]},
    "hq": {"de": "Firmensitz", "en": "Headquarters"},
    "production": {"de": "Produktionsstätte", "en": "Production facility"},
    "route": {"de": "Route planen", "en": "Get directions"},
    "follow": {"de": "Folgen Sie uns", "en": "Follow us"},
    "gallery": {"de": "Galerie", "en": "Gallery"},
    "event_label": {"de": "Messe", "en": "Trade fair"},
    "news_kicker": {"de": "Aktuelles", "en": "Latest"},
    "copyright": {"de": "Alle Rechte vorbehalten.", "en": "All rights reserved."},
}

# ---------------------------------------------------------------- events banner
# Shown on the home page until `end` (YYYY-MM-DD). Hidden automatically afterwards.
EVENTS = [
    {
        "start": "2026-11-17", "end": "2026-11-20",
        "title": {"de": "SIMEI 2026 · Mailand", "en": "SIMEI 2026 · Milan"},
        "text": {"de": "Besuchen Sie uns vom 17. bis 20. November auf der SIMEI in Mailand und erleben Sie den Steillagen-Vollernter MSH.",
                 "en": "Visit us at SIMEI in Milan, 17–20 November, and see the Steep Slope Harvester MSH up close."},
        "url": "https://www.simei.it/en",
    },
]

# ---------------------------------------------------------------- home
HOME = {
    "title": {"de": "CH engineering – Innovation im Weinbau",
              "en": "CH engineering – Innovation in Viticulture"},
    "description": {
        "de": "CH engineering aus Kröv an der Mosel baut den Steillagen-Vollernter MSH: maschinelle Traubenlese bis 75 % Steigung, in Terrassen und in der Ebene – mit Traubenqualität auf Handlese-Niveau.",
        "en": "CH engineering from Kröv on the Mosel builds the Steep Slope Harvester MSH: mechanical grape harvesting on slopes up to 75 %, on terraces and on flat ground – with hand-picked grape quality.",
    },
    "hero_kicker": {"de": "Innovation im Weinbau", "en": "Innovation in viticulture"},
    "hero_title": {"de": "Der Steillagen-Vollernter MSH", "en": "The Steep Slope Harvester MSH"},
    "hero_text": {
        "de": "Eine Revolution im Weinbau: maschinelle Traubenlese bis 75 % Steigung, in Terrassen und in der Ebene – mit nur einer Maschine.",
        "en": "A revolution in viticulture: mechanical grape harvesting on slopes up to 75 %, on terraces and on flat ground – with a single machine.",
    },
    "stats": [
        {"value": "75 %", "label": {"de": "max. Steigung", "en": "max. gradient"}},
        {"value": "1", "label": {"de": "Fahrgasse genügt", "en": "single driving lane"}},
        {"value": "4 km/h", "label": {"de": "Erntegeschwindigkeit", "en": "harvesting speed"}},
        {"value": "2014", "label": {"de": "gegründet an der Mosel", "en": "founded on the Mosel"}},
    ],
    "intro_kicker": {"de": "Weltneuheit im Weinbau", "en": "A world first in viticulture"},
    "intro_title": {"de": "Der nächste Entwicklungsschritt der Steillagen-Lese.",
                    "en": "The next step in steep-slope harvesting."},
    "intro": {
        "de": [
            "Der CH engineering Multi Slope Harvester (MSH) markiert den nächsten Entwicklungsschritt im modernen Weinbau. Nach über einem Jahrzehnt erfolgreicher Marktpraxis ist er das Ergebnis konsequenter Weiterentwicklung auf Basis umfangreicher Praxiserfahrung.",
            "Bereits der erste serienreife Steillagen-Vollernter revolutionierte die mechanisierte Traubenernte in extremen Hanglagen bis zu 75 % Steigung. Der MSH erweitert diese bewährten Leistungsmerkmale entscheidend: Er ermöglicht erstmals eine wirtschaftliche und effiziente Traubenernte in Steillagen, terrassierten Weinbergen und ebenen Flächen – mit nur einer universell einsetzbaren Maschine.",
        ],
        "en": [
            "The CH engineering Multi Slope Harvester (MSH) marks the next stage of development in modern viticulture. After more than a decade of successful market application, it is the result of continuous advancement based on extensive practical experience.",
            "The first series-produced steep-slope harvester already revolutionized mechanized grape harvesting on extreme terrain with gradients of up to 75 %. The MSH significantly expands these proven capabilities: for the first time, it enables efficient, economical harvesting on steep slopes, terraced vineyards and flat terrain – all with a single, universally applicable machine.",
        ],
    },
    "features": [
        {"icon": "grape", "title": {"de": "Perfektes Erntegut", "en": "Excellent grape quality"},
         "text": {"de": "Schonende Traubenbehandlung ohne Quetschen und eine dreifache Blatt-Trennung.",
                  "en": "Gentle grape handling without crushing, plus triple leaf separation."}},
        {"icon": "shield", "title": {"de": "Niedrige Verlustraten", "en": "Low loss rates"},
         "text": {"de": "Fangtaschen und eine intelligente Luftführung im Erntekopf halten die Trauben in der Maschine.",
                  "en": "Catch pockets and intelligent airflow in the harvesting head keep the grapes in the machine."}},
        {"icon": "leaf", "title": {"de": "Schonend zur Pflanze", "en": "Gentle to the vine"},
         "text": {"de": "Raupenfahrwerk mit 1,3 m² Auflagefläche für geringen Bodendruck.",
                  "en": "Crawler tracks with 1.3 m² contact area for low ground pressure."}},
        {"icon": "speed", "title": {"de": "Hohe Erntegeschwindigkeit", "en": "High picking speed"},
         "text": {"de": "Bis zu 4 km/h im Hang – bei konstant hoher Erntequalität.",
                  "en": "Up to 4 km/h on the slope – with consistently high harvest quality."}},
    ],
    "split1": {
        "kicker": {"de": "Eine Fahrgasse. Jede Lage.", "en": "One lane. Every site."},
        "title": {"de": "Steillage, Terrasse, Ebene.", "en": "Steep slope, terrace, flat."},
        "text": {
            "de": [
                "Als Anbaugerät benötigt der Traubenvollernter nur eine Fahrgasse zum Bearbeiten des Weinbergs. Damit ist erstmals auch die maschinelle Lese in Terrassen-Weinbergen möglich.",
                "Der große Behälter erlaubt das Durchfahren langer Reihen ohne Unterbrechung. Eine intelligente Luftführung im Erntekopf passt die Maschine von Steillagen auf Terrassen an, Kurvenradien ab 12 m sind kein Problem.",
                "Auch dort, wo herkömmliche Maschinen wegen ihrer Abmessungen nicht mehr fahren können – etwa bei engen Zuwegungen –, findet der Steillagen-Vollernter seinen Einsatz.",
            ],
            "en": [
                "As an implement-mounted harvester, it needs just a single driving lane to work the vineyard. This makes mechanical harvesting in terraced vineyards possible for the first time.",
                "The large-capacity bin allows long rows to be harvested without interruption. Intelligent airflow in the harvesting head adapts the machine from steep slopes to terraces, and turning radii from 12 m pose no challenge.",
                "It is also the answer wherever conventional machines reach their limits due to their size – for example, where access routes into the vineyard are narrow.",
            ],
        },
    },
    "split2": {
        "kicker": {"de": "Traubenqualität auf Handlese-Niveau", "en": "Hand-picked quality"},
        "title": {"de": "Steillagenweinbau ist Qualitätsweinbau.", "en": "Steep-slope viticulture is quality viticulture."},
        "text": {
            "de": [
                "Diese Überzeugung prägt die Konstruktion des MSH: besonders schonende Traubenbehandlung, intelligente Mechanisierung und konstant hohe Erntequalität – bei einer Erntegeschwindigkeit von bis zu 4 km/h.",
                "CH engineering betreut zufriedene Kunden weltweit. Kontinuierliche Weiterentwicklung, praxisorientierte Innovation und höchste Qualitätsansprüche stehen dabei im Mittelpunkt.",
            ],
            "en": [
                "This conviction shapes the design of the MSH: exceptionally gentle grape handling, intelligent mechanization and consistently high harvest quality – at harvesting speeds of up to 4 km/h.",
                "CH engineering serves happy customers worldwide. Continuous development, practical innovation and the highest quality standards are at the heart of everything we do.",
            ],
        },
    },
    "products_title": {"de": "Unsere Lösungen", "en": "Our solutions"},
    "products": [
        {"page": "msh", "img": "msh-mechanical.jpg",
         "title": {"de": "Steillagen-Vollernter MSH", "en": "Steep Slope Harvester MSH"},
         "text": {"de": "Der erste Steillagen-Vollernter der Welt – bis 75 % Steigung, in Terrassen und in der Ebene.",
                  "en": "The world's first steep-slope harvester – up to 75 % gradient, on terraces and on flat ground."}},
        {"page": "ut125", "img": "ut125-side.jpg",
         "title": {"de": "Raupenfahrzeug Andreoli UT 125", "en": "Crawler Andreoli UT 125"},
         "text": {"de": "Das Trägerfahrzeug für den Vollernter – und vielseitige Raupe für das ganze Weinbaujahr.",
                  "en": "The carrier for the harvester – and a versatile crawler for the whole viticultural year."}},
        {"page": "keller", "img": "keller-1.jpg",
         "title": {"de": "Kellertechnik", "en": "Cellar technology"},
         "text": {"de": "Individuell geplante Traubenannahme im Baukastensystem – mit Traubenmühle bis ca. 18 t/h.",
                  "en": "Custom-planned modular grape reception systems – with a grape mill up to approx. 18 t/h."}},
    ],
    "story_kicker": {"de": "Unsere Geschichte", "en": "Our story"},
    "story_title": {"de": "Aus der Mosel, für die steilsten Weinberge der Welt.",
                    "en": "From the Mosel, for the world's steepest vineyards."},
    "story": {
        "de": "Seit 2014 produziert CH engineering Maschinen für den landwirtschaftlichen Einsatz. Wirtschaftlichkeit, Zuverlässigkeit und Schlagkraft zeichnen unsere Entwicklungen aus. So ist unser Steillagen-Vollernter kleiner, leichter und kompakter als jeder herkömmliche Ernter. Zugleich steht Qualität im Vordergrund – denn Steillagen-Weinbau bedeutet immer auch Qualitätsweinbau.",
        "en": "Since 2014, CH engineering has been building machines for agricultural use. Our developments stand for profitability, reliability and performance. Our steep-slope harvester is smaller, lighter and more compact than any conventional harvester. At the same time, quality comes first – because steep-slope viticulture always means quality viticulture.",
    },
    "cta_title": {"de": "Interesse am MSH?", "en": "Interested in the MSH?"},
    "cta_text": {"de": "Wir beraten Sie gerne – persönlich, telefonisch oder bei einer Vorführung in Ihrem Weinberg.",
                 "en": "We're happy to advise you – in person, by phone or with a demonstration in your vineyard."},
}

# ---------------------------------------------------------------- MSH page
MSH = {
    "title": {"de": "Der Steillagen-Vollernter MSH", "en": "The Steep Slope Harvester MSH"},
    "description": {
        "de": "Der Steillagen-Vollernter MSH erntet bis 75 % Hangneigung mit nur einer Fahrgasse. Technische Daten, Leseergebnisse und Galerie.",
        "en": "The Steep Slope Harvester MSH harvests on slopes up to 75 % using a single lane. Specifications, harvest results and gallery.",
    },
    "hero_img": "msh-slope.jpg",
    "kicker": {"de": "Innovation im Weinbau", "en": "Innovation in viticulture"},
    "lead": {"de": "Der erste Steillagen-Vollernter der Welt begeistert unsere Kunden weltweit.",
             "en": "The world's first steep-slope harvester impresses our customers around the globe."},
    "sections": [
        {"img": "msh-studio-detail.jpg",
         "title": {"de": "Sicher im Hang.", "en": "Secure on the slope."},
         "text": {
             "de": ["Der Steillagen-Vollernter erntet bergab bei bis zu 75 % Hangneigung und benötigt dabei nur eine Fahrgasse. Das Raupenfahrwerk verteilt das Gewicht mit einer Auflagefläche von 1,3 m² und sorgt so für geringen Bodendruck.",
                    "Gesichert wird die Maschine mit einer elektronischen Hangelwinde mit 1.300 kg Zugkraft an einem Anhänger am oberen Ende des Weinbergs. Bei der Rückfahrt wird der Erntekopf geöffnet und die Maschine fährt über die Zeile hinweg. Außerdem kann das Fahrzeug im Steilhang wenden."],
             "en": ["The harvester works downhill on slopes of up to 75 % and needs just a single lane. Its crawler tracks spread the weight over a 1.3 m² contact area, keeping ground pressure low.",
                    "The machine is secured by an electronically controlled winch with 1,300 kg pulling force, anchored to a trailer at the top of the vineyard. On the way back up, the harvesting head opens and the machine drives over the row. It can even turn on the steep slope."],
         }},
        {"img": "msh-studio-front.jpg",
         "title": {"de": "Digital gesteuert.", "en": "Digitally controlled."},
         "text": {
             "de": ["Eine moderne Digitalsteuerung sichert die gleichbleibende Erntequalität während der Fahrt. Sie enthält Programme für unterschiedliche Rebsorten, ein Verrechnungssystem für Lohnunternehmer und ein Reinigungsprogramm. Individuelle Einstellungen lassen sich speichern und bearbeiten."],
             "en": ["A modern digital control system ensures consistent harvest quality on the move. It includes programs for different grape varieties, a billing system for contractors and a cleaning program. Individual settings can be saved and edited."],
         }},
    ],
    "quality_title": {"de": "Qualität, die überzeugt.", "en": "Superior harvest quality."},
    "quality_text": {
        "de": "Die ausgeklügelte Bandführung vermeidet das Quetschen der Trauben. Eine dreifache Blatt-Trennung reduziert unerwünschte Rückstände im Leseergebnis, während Fangtaschen und eine intelligente Luftführung für geringe Verlustraten sorgen. Die Leseergebnisse begeistern unsere Kunden auf der ganzen Welt.",
        "en": "A well-designed belt guide prevents the grapes from being crushed. Triple leaf separation reduces unwanted residue in the harvest, while catch pockets and intelligent airflow keep losses low. The results impress our customers around the world.",
    },
    "quality_imgs": ["grapes-1.jpg", "grapes-2.jpg", "grapes-3.jpg", "grapes-4.jpg", "grapes-5.jpg", "grapes-6.jpg"],
    "specs_title": {"de": "Der MSH in Zahlen.", "en": "The MSH in numbers."},
    "specs": [
        ({"de": "Sammelbehälter (je nach Ausstattung)", "en": "Bin capacity (depending on equipment)"}, "1.030 l"),
        ({"de": "Kipphöhe Behälterkante", "en": "Tipping height, bin edge"}, "1.800 mm"),
        ({"de": "Anzahl Schüttelstäbe", "en": "Shaker rods"}, {"de": "2 × 5 (optional 2 × 6)", "en": "2 × 5 (optional 2 × 6)"}),
        ({"de": "Arbeitsgeschwindigkeit Ernte", "en": "Working speed, harvesting"}, "3–5 km/h"),
        ({"de": "Arbeitsgeschwindigkeit Rückfahrt", "en": "Working speed, return"}, {"de": "bis 9 km/h", "en": "up to 9 km/h"}),
        ({"de": "Min. Zeilenbreite, Erntebetrieb", "en": "Min. row width, harvesting"}, "1.600 mm"),
        ({"de": "Max. Steigleistung", "en": "Max. climbing ability"}, "75 %*"),
        ({"de": "Max. seitliche Hangneigung", "en": "Max. lateral slope"}, {"de": "30 %* (je nach Ausführung)", "en": "30 %* (depending on version)"}),
        ({"de": "Abmessungen (L × B × H)", "en": "Dimensions (L × W × H)"}, "4.900 × 1.330 × 2.700 mm"),
        ({"de": "Gewicht Ernte-Aggregat", "en": "Weight, harvesting unit"}, "1.650 kg"),
        ({"de": "Digitalsteuerung", "en": "Digital control"},
         {"de": "Ernteprogramme · Verrechnungssystem für Lohnunternehmer · Waschprogramm · Kontroll- und Alarmfunktion",
          "en": "Harvesting programs · billing system for contractors · washing program · monitoring and alarm function"}),
        ({"de": "Kamerasystem", "en": "Camera system"}, {"de": "bis zu 4 Kameras (optional)", "en": "up to 4 cameras (optional)"}),
        ({"de": "Abstellvorrichtung", "en": "Parking stand"}, "✓"),
    ],
    "specs_foot": {"de": "* abhängig von Boden- und Wetterverhältnissen", "en": "* depending on ground and weather conditions"},
    "gallery": ["msh-mosel.jpg", "msh-row.jpg", "msh-g01.jpg", "msh-g02.jpg", "msh-g03.jpg", "msh-g04.jpg",
                "msh-g05.jpg", "msh-g06.jpg", "msh-g07.jpg", "msh-g08.jpg", "msh-g09.jpg", "msh-g10.jpg"],
}

# ---------------------------------------------------------------- UT 125 page
UT125 = {
    "title": {"de": "Raupenfahrzeug Andreoli UT 125", "en": "Crawler Andreoli UT 125"},
    "description": {
        "de": "Die Andreoli Raupe UT 125: Trägerfahrzeug für den Steillagen-Vollernter und vielseitige Raupe für den Weinbau. Ausstattung und technische Daten.",
        "en": "The Andreoli UT 125 crawler: carrier vehicle for the Steep Slope Harvester and a versatile crawler for viticulture. Equipment and specifications.",
    },
    "hero_img": "ut125-field.jpg",
    "kicker": {"de": "Trägerfahrzeug", "en": "Carrier vehicle"},
    "lead": {
        "de": "Die ANDREOLI Raupe UT 125 wurde speziell für den Einsatz eines Traubenvollernters ausgelegt. Pumpen, Radgetriebe, Zapfwellengetriebe und Fahrwerkskomponenten halten viele tausend Betriebsstunden stand.",
        "en": "The ANDREOLI UT 125 crawler was designed specifically for operating a grape harvester. Its pumps, wheel drives, PTO gearbox and chassis components withstand many thousands of operating hours.",
    },
    "intro": {
        "de": "Hergestellt von Andreoli in Italien, ist die Raupe die perfekte Ergänzung für unseren Vollernter – und überzeugt auch bei vielen anderen Arbeiten im Weinberg.",
        "en": "Built by Andreoli in Italy, the crawler is the perfect partner for our harvester – and excels at many other jobs in the vineyard, too.",
    },
    "features": [
        {"img": "ut125-joystick.jpg",
         "kicker": {"de": "Intuitive Steuerung", "en": "Intuitive controls"},
         "title": {"de": "Höchste Fahrpräzision", "en": "Highest driving precision"},
         "text": {"de": "Die Raupe wird im Wesentlichen über zwei Joysticks bedient – einer für den Fahrantrieb, einer für die hydraulischen Zusatzgeräte. Dank Tempomat lassen sich Vorwärts- und Rückwärtsgeschwindigkeit individuell speichern. Zusätzlichen Komfort bietet ein Motordrehzahlspeicher.",
                  "en": "The crawler is operated mainly with two joysticks – one for travel and one for hydraulic implements. Thanks to cruise control, forward and reverse speeds can be stored individually. An engine speed memory adds further comfort."}},
        {"img": "ut125-camera.jpg",
         "kicker": {"de": "Überwachungssystem", "en": "Monitoring system"},
         "title": {"de": "Immer alles im Blick", "en": "Always everything in sight"},
         "text": {"de": "Ein Überwachungssystem gibt dem Fahrer Überblick und Kontrolle über alle maschinellen Vorgänge. Auf einem Bildschirm in der Kabine erscheinen die Bilder der bis zu vier optionalen Außenkameras.",
                  "en": "A monitoring system gives the driver an overview and control of all machine processes. A screen in the cab shows the views from up to four optional external cameras."}},
        {"img": "ut125-cab.jpg",
         "kicker": {"de": "Aktivkohle-Filtersystem", "en": "Activated carbon filter"},
         "title": {"de": "Schutz vor Wind und Wetter", "en": "Protection from wind and weather"},
         "text": {"de": "Die ROPS-geprüfte Fahrerkabine schützt mit Klimaanlage und Heizung vor Wetter- und Klimaeinflüssen. Ein Aktivkohle-Filtersystem hält Staub und Pflanzenschutzmittel aus der Kabine fern. Der Grammer-Sitz ist elektrisch neigungsverstellbar und luftgefedert.",
                  "en": "The ROPS-tested cab protects the driver from the elements with air conditioning and heating. An activated carbon filter keeps dust and crop protection products out of the cab. The Grammer seat offers electric tilt adjustment and air suspension."}},
        {"img": "ut125-hof.jpg",
         "kicker": {"de": "Dreipunkt-Kraftheber", "en": "Three-point linkage"},
         "title": {"de": "Vielseitig einsetzbar", "en": "Wide range of applications"},
         "text": {"de": "Da der Vollernter ein Anbaugerät ist, lässt er sich in etwa 30 Minuten demontieren und gegen den Dreipunkt-Kraftheber tauschen. So wird die Raupe zum Allrounder im Weinbau: Vorschneiden, Mulchen, Grubbern, Laubschneiden, Pflanzenschutz, Pflanzfeldvorbereitung und Pflanzen.",
                  "en": "Because the harvester is an implement, it can be removed in about 30 minutes and swapped for the three-point linkage. That makes the crawler an all-rounder in the vineyard: pre-pruning, mulching, cultivating, leaf trimming, crop protection, field preparation and planting."}},
    ],
    "specs_title": {"de": "Die Raupe in Zahlen.", "en": "The crawler in numbers."},
    "spec_groups": [
        ({"de": "Motor", "en": "Engine"}, [
            ({"de": "Motor", "en": "Engine"}, "FPT F36 Stage V"),
            ({"de": "Zylinder / Hubraum", "en": "Cylinders / displacement"}, "4 / 3.600 cm³"),
            ({"de": "Nennleistung", "en": "Rated output"}, {"de": "90 kW (125 PS)", "en": "90 kW (125 hp)"}),
            ({"de": "Max. Drehzahl", "en": "Max. engine speed"}, {"de": "2.300 U/min", "en": "2,300 rpm"}),
            ({"de": "Max. Drehmoment", "en": "Max. torque"}, {"de": "490 Nm bei 1.400 U/min", "en": "490 Nm at 1,400 rpm"}),
            ({"de": "Abgasreinigung", "en": "Exhaust aftertreatment"}, "Stage V / DOC + DPF"),
        ]),
        ({"de": "Leistung", "en": "Performance"}, [
            ({"de": "Arbeitsgeschwindigkeit", "en": "Working speed"}, "0–7,0 km/h"),
            ({"de": "Max. Steigleistung", "en": "Max. climbing ability"}, "75 %*"),
            ({"de": "Max. seitliche Neigung", "en": "Max. lateral slope"}, "30 %*"),
        ]),
        ({"de": "Hydraulik", "en": "Hydraulics"}, [
            ({"de": "Fahrantrieb", "en": "Drive"}, {"de": "Einstufiger Hydrostatantrieb", "en": "Single-stage hydrostatic drive"}),
            ({"de": "Hydraulikmotor", "en": "Hydraulic motor"}, "Bosch Rexroth"),
            ({"de": "Ölsystem", "en": "Oil system"}, {"de": "2-Kreis (1× Fahrantrieb, 1× Verbraucher)", "en": "2-circuit (1× drive, 1× implements)"}),
            ({"de": "Kraftheber", "en": "Power lift"}, {"de": "Kat. I mit Schnellkuppler", "en": "Cat. I with quick coupler"}),
            ({"de": "Steuergeräte", "en": "Control valves"}, {"de": "6× doppelt-, 1× einfachwirkend, elektronischer Mengenteiler, Joystickbedienung", "en": "6× double-acting, 1× single-acting, electronic flow divider, joystick control"}),
        ]),
        ({"de": "Abmessungen & Gewicht", "en": "Dimensions & weight"}, [
            ({"de": "Breite / Länge", "en": "Width / length"}, "1.330 / 3.500 mm"),
            ({"de": "Höhe (mit Klimaanlage)", "en": "Height (with A/C)"}, "2.700 mm"),
            ({"de": "Kettenbreite / Kontaktfläche", "en": "Track width / contact area"}, "320 mm / 1,3 m²"),
            ({"de": "Dieseltank", "en": "Diesel tank"}, "65 l"),
            ({"de": "Gewicht", "en": "Weight"}, {"de": "ab 3.600 kg (je nach Ausstattung)", "en": "from 3,600 kg (depending on equipment)"}),
        ]),
        ({"de": "Ausstattung", "en": "Equipment"}, [
            ({"de": "Zapfwelle", "en": "PTO"}, {"de": "mechanisch, 540 U/min, elektrische Einschaltung", "en": "mechanical, 540 rpm, electric engagement"}),
            ({"de": "Seilwinde (Option)", "en": "Winch (optional)"}, {"de": "Hangelwinde, hydraulisch, 300–1.300 kg elektronisch regelbar, 200 m Seil", "en": "Hydraulic winch, 300–1,300 kg electronically adjustable, 200 m cable"}),
            ({"de": "Fahrersitz", "en": "Driver's seat"}, {"de": "Grammer MSG 93, Luftfederung, Neigungsverstellung, integrierte Joysticks", "en": "Grammer MSG 93, air suspension, tilt adjustment, integrated joysticks"}),
            ({"de": "Tempomat", "en": "Cruise control"}, {"de": "mit elektronischer Pumpensteuerung", "en": "with electronic pump control"}),
            ({"de": "Kabine", "en": "Cab"}, {"de": "Teilkabine; optional Vollkabine mit Heizung und Klimaanlage", "en": "Partial cab; optional full cab with heating and A/C"}),
        ]),
    ],
    "specs_foot": {"de": "* abhängig von Boden- und Wetterverhältnissen sowie Anbaugeräten",
                   "en": "* depending on ground and weather conditions and attachments"},
    "gallery": ["ut125-side.jpg", "ut125-tracks.jpg", "ut125-terminal.jpg", "ut125-display.jpg",
                "ut125-controls.jpg", "ut125-armrest.jpg", "msh-studio-ut125.jpg", "ut125-hof.jpg"],
}

# ---------------------------------------------------------------- Kellertechnik
KELLER = {
    "title": {"de": "Kellertechnik – Traubenannahme", "en": "Cellar technology – grape reception"},
    "description": {
        "de": "CH engineering plant und baut Ihre Traubenannahme: Schwerlastregal, Großtrichter und Traubenmühle im Baukastensystem.",
        "en": "CH engineering plans and builds your grape reception: heavy-duty rack, large hopper and grape mill in a modular system.",
    },
    "hero_img": "keller-1.jpg",
    "kicker": {"de": "Kellertechnik", "en": "Cellar technology"},
    "lead": {"de": "Wir planen und bauen Ihre Traubenannahme – nach Ihren Vorstellungen.",
             "en": "We plan and build your grape reception system – to your specifications."},
    "intro": {
        "de": "Die Traubenannahme ist im Baukastensystem aufgebaut und besteht aus einem Schwerlastregal, einem Großtrichter und einer Traubenmühle.",
        "en": "Our grape reception is a modular system made up of a heavy-duty rack, a large hopper and a grape mill.",
    },
    "modules": [
        {"num": "01", "title": {"de": "Schwerlastregal", "en": "Heavy-duty rack"},
         "text": {"de": "Individuell an Pressen und Größen anpassbar. 4 m hoher Stützrahmen mit Sondertraversen für Stabilität. Auf Rollen gelagert und dadurch einfach umzupositionieren.",
                  "en": "Adaptable to your press and size requirements. 4 m support frame with special cross-members for stability. Mounted on rollers for easy repositioning."}},
        {"num": "02", "title": {"de": "Großtrichter", "en": "Large hopper"},
         "text": {"de": "Für Euroboxen (500/600 l) oder Speidel-Transportboxen (1.300 × 1.500 mm). WIG-verschweißt, sauber verschliffen und gebeizt, mit Haltern zur Montage am Regal.",
                  "en": "Takes Euro boxes (500/600 l) or Speidel transport boxes (1,300 × 1,500 mm). TIG-welded, ground and pickled, with brackets for mounting on the rack."}},
        {"num": "03", "title": {"de": "Traubenmühle", "en": "Grape mill"},
         "text": {"de": "Komplett aus V2A, angetrieben von einem Getriebemotor. Sternwalzen (70 cm) aus lebensmittelechtem Gummi, gefederte Steinsicherung, Leistung ca. 18 t/h.",
                  "en": "Fully stainless steel (V2A), driven by a geared motor. 70 cm star rollers made of food-grade rubber, spring-loaded stone guard, capacity approx. 18 t/h."}},
        {"num": "04", "title": {"de": "Schnellwechselsystem", "en": "Quick-change system"},
         "text": {"de": "Sollen Trauben ganz gepresst werden, wird die Mühle über vier Schnellverschlüsse ohne Werkzeug gegen einen Leerkasten getauscht.",
                  "en": "For whole-bunch pressing, the mill is swapped for an empty box via four quick-release fasteners – no tools needed."}},
    ],
    "gallery": ["keller-1.jpg", "keller-2.jpg", "keller-3.jpg"],
    "cta": {"de": "Auf Wunsch planen und bauen wir Ihre Traubenannahme nach Ihren Vorstellungen.",
            "en": "On request, we plan and build your grape reception exactly to your requirements."},
}

# ---------------------------------------------------------------- news
# newest first. "body" = full text for our own posts; "summary" for press coverage.
NEWS = [
    {"date": "2026-03-26", "img": "news-simei.jpg", "lang": "en",
     "title": {"de": "Besuchen Sie uns auf der SIMEI 2026 in Mailand", "en": "Meet us at SIMEI 2026 in Milan"},
     "body": {"de": "Vom 17. bis 20. November sind wir auf der SIMEI in Mailand, der internationalen Leitmesse für Wein- und Getränketechnik. Wir zeigen unsere Lösungen für die moderne mechanisierte Traubenlese – und wie Effizienz und höchste Qualität im Steillagenweinbau zusammenkommen. Erleben Sie vor Ort den Steillagen-Vollernter MSH für Steillagen, Terrassen und ebene Flächen.",
              "en": "We will be at SIMEI in Milan from 17 to 20 November – the leading international trade fair for wine and beverage technology. We'll show our solutions for modern mechanized grape harvesting and how efficiency and premium quality come together in steep-slope viticulture. Discover the Steep Slope Harvester MSH, designed for steep slopes, terraced vineyards and flat terrain."},
     "link": "https://www.simei.it/en", "source": "simei.it"},
    {"date": "2026-03-26", "img": "news-eima.jpg", "lang": "en",
     "title": {"de": "CH engineering auf der EIMA 2026", "en": "CH engineering at EIMA 2026"},
     "body": {"de": "Vom 10. bis 14. November präsentieren wir auf der EIMA International in Bologna unsere Lösungen für den modernen Weinbau – mit dem neuen Steillagen-Vollernter MSH.",
              "en": "From 10 to 14 November we present our solutions for modern viticulture at EIMA International in Bologna, Italy – including the new Steep Slope Harvester MSH."},
     "link": "https://www.eima.it/", "source": "eima.it"},
    {"date": "2026-02-26", "img": "news-vitis.jpg", "lang": "de",
     "title": {"de": "Zuhause an der Mosel: VITIS LIVE 2026 in Piesport", "en": "At home on the Mosel: VITIS LIVE 2026 in Piesport"},
     "body": {"de": "Heimspiel für uns: Die VITIS LIVE findet am 1. und 2. Juli 2026 genau dort statt, wo unsere Technik zuhause ist – am Sportplatz in Piesport an der Mosel. Wir zeigen den Steillagen-Vollernter MSH und unser Traubenübergabesystem für effiziente und schonende Traubenernte in jeder Lage.",
              "en": "A home game for us: VITIS LIVE takes place on 1–2 July 2026 right where our technology is at home – at the sports ground in Piesport on the Mosel. We'll show the Steep Slope Harvester MSH and our grape transfer system for efficient, gentle harvesting on any site."},
     "link": "https://vitis-live.de/", "source": "vitis-live.de"},
    {"date": "2024-12-12", "img": "news-igus.jpg", "lang": "en",
     "title": {"de": "Kompaktes Erntefahrzeug mit igus-Energieketten", "en": "Compact harvesting vehicle with igus energy chains"},
     "summary": {"de": "igus berichtet, wie unser Vollernter mit robusten Energieketten aus Hochleistungskunststoff auch unter schwierigen Bedingungen zuverlässig und wartungsarm arbeitet – in Hängen bis 75 % Steigung.",
                 "en": "igus reports on how our harvester uses robust high-performance plastic energy chains to work reliably and with little maintenance, even on slopes of up to 75 %."},
     "link": "https://press.igus.eu/robots-take-care-of-harvesting-grapes/", "source": "igus"},
    {"date": "2024-10-11", "img": "news-br.jpg", "lang": "de",
     "title": {"de": "Weinlese mit Vollernter: Wie Winzer den Personalmangel bekämpfen", "en": "Harvesting with machines: how winegrowers tackle the labour shortage"},
     "summary": {"de": "Der Bayerische Rundfunk (Unser Land) begleitet einen fränkischen Winzer beim Test unseres Steillagen-Vollernters – mit dem Ziel, die Lese künftig ohne Saisonarbeitskräfte zu schaffen.",
                 "en": "Bavarian broadcaster BR (Unser Land) follows a Franconian winegrower testing our steep-slope harvester, aiming to manage future harvests without seasonal workers."},
     "link": "https://www.br.de/nachrichten/", "source": "BR24"},
    {"date": "2022-11-08", "img": None, "lang": "en",
     "title": {"de": "Erster Steillagen-Vollernter in Nordamerika", "en": "First steep slope harvester in North America"},
     "summary": {"de": "Wine Business berichtet über den ersten Einsatz unseres Vollernters in den USA beim Weingut Gundlach Bundschu im Sonoma Valley.",
                 "en": "Wine Business reports on the US debut of our harvester at Gundlach Bundschu winery in Sonoma Valley – “a game changer” for hillside vineyards."},
     "link": "https://www.winebusiness.com/news/article/264252", "source": "Wine Business"},
    {"date": "2022-07-30", "img": "news-dwm-2022.jpg", "lang": "de",
     "title": {"de": "Viel Neues beim Steillagen-Vollernter", "en": "Lots of news on the steep slope harvester"},
     "summary": {"de": "Das Deutsche Weinbaujahrbuch-Magazin über Neuerungen am Vollernter und an der überarbeiteten Andreoli-Raupe.",
                 "en": "German wine trade magazine DWM on the latest improvements to the harvester and the redesigned Andreoli crawler."},
     "link": "https://www.dwm-aktuell.de/ch-engineering-viel-neues-beim-steillagen-vollernter", "source": "dwm-aktuell.de"},
    {"date": "2021-08-03", "img": "news-sdblech.jpg", "lang": "de",
     "title": {"de": "Zu Gast bei einem Weltmarktführer aus Piesport", "en": "Visiting a world market leader from Piesport"},
     "summary": {"de": "Ein Porträt über die Entstehung von CH engineering aus der Carl Hoffmann Landmaschinen GmbH und den Weg zum ersten serienreifen Steillagen-Vollernter.",
                 "en": "A portrait of how CH engineering grew out of Carl Hoffmann Landmaschinen GmbH and developed the first series-production steep-slope harvester."},
     "link": "https://sd-blech.de/2021/08/03/zu-gast-bei-einem-weltmarktfuehrer-aus-piesport-an-der-mosel/", "source": "SD Blech"},
    {"date": "2020-09-09", "img": "news-eu.jpg", "lang": "de",
     "title": {"de": "Von der Drohne bis zum Steillagen-Vollernter", "en": "From drones to the steep slope harvester"},
     "summary": {"de": "Beim informellen EU-Agrarrat in Koblenz wurde den EU-Agrarministern in den Winninger Steillagen digitale Weinbautechnik vorgeführt – darunter unser Vollernter.",
                 "en": "At the informal EU Agriculture Council in Koblenz, EU agriculture ministers saw digital viticulture technology in the steep vineyards of Winningen – including our harvester."},
     "link": "https://www.dwm-aktuell.de/-drohne-steillagen-vollernter", "source": "dwm-aktuell.de"},
    {"date": "2019-10-31", "img": "news-douro.jpg", "lang": "en",
     "title": {"de": "Lese im Douro-Tal", "en": "Harvesting in the Douro Valley"},
     "summary": {"de": "Ein Bericht über den Wandel im Douro-Tal – und den Einsatz unseres Steillagen-Vollernters in den steilen Terrassen Portugals.",
                 "en": "A report on the changing Douro region – and our steep-slope harvester at work on Portugal's steep terraces."},
     "link": None, "source": None},
]

NEWS_PAGE = {
    "title": {"de": "News", "en": "News"},
    "description": {"de": "Aktuelles von CH engineering: Messen, Presseberichte und Neuigkeiten rund um den Steillagen-Vollernter.",
                    "en": "News from CH engineering: trade fairs, press coverage and updates on the Steep Slope Harvester."},
    "hero_img": "news-header.jpg",
    "kicker": {"de": "Aktuelles", "en": "Latest"},
    "lead": {"de": "Messen, Presseberichte und Neuigkeiten rund um den Steillagen-Vollernter.",
             "en": "Trade fairs, press coverage and updates on the Steep Slope Harvester."},
}

CONTACT_PAGE = {
    "title": {"de": "Kontakt", "en": "Contact"},
    "description": {"de": "Kontakt zu CH engineering GmbH in Kröv an der Mosel: Telefon, E-Mail, Öffnungszeiten und Anfahrt.",
                    "en": "Contact CH engineering GmbH in Kröv on the Mosel: phone, email, opening hours and directions."},
    "hero_img": "msh-mosel.jpg",
    "kicker": {"de": "Kontakt", "en": "Contact"},
    "lead": {"de": "Interesse? Wir freuen uns auf Ihre Anfrage.", "en": "Interested? We look forward to hearing from you."},
}
