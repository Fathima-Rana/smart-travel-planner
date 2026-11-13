import math
from budget_benchmarks import (
    calculate_real_trip_budget,
    analyze_budget_feasibility,
    get_country_benchmark,
)


# ============================================================
# DETAILED DESTINATION-SPECIFIC ITINERARIES
# Each destination has a list of day-plans.
# Each day-plan is a dict:
#   morning, afternoon, evening, food_tip, entry_fee_est, distance_from_centre
# The itinerary engine cycles / trims these to match the trip duration.
# ============================================================

DETAILED_ITINERARIES = {
    # ────────────── KERALA ──────────────
    "Wayanad": [
        {
            "theme": "Arrival & Kalpetta Town",
            "morning":   "Arrive in Kalpetta. Check in and freshen up. Walk around Kalpetta town market — browse fresh spices, banana chips, and Wayanad coffee.",
            "afternoon": "🏞️ Pookode Lake (9 AM–5 PM) — rent a paddleboat on this pristine freshwater lake surrounded by forest. ₹30–50/person entry. 7 km from Kalpetta.",
            "evening":   "🌅 Lakkidi View Point — breathtaking panoramic view of the Thamarassery pass from 700 m altitude. Best at sunset. Free entry.",
            "food_tip":  "Try Wayanad-style fish curry and puttu at Hotel Regency, Kalpetta.",
            "entry_fee_est": "₹80–120 total",
            "distance_from_centre": "7–14 km",
        },
        {
            "theme": "Dams, Caves & Wilderness",
            "morning":   "🏛️ Edakkal Caves (9 AM–4:30 PM) — 1 km steep trek to 3,000-year-old neolithic petroglyphs carved into rock. ₹30/person + ₹20 camera. Arrive early to avoid weekend queues. 12 km from Kalpetta.",
            "afternoon": "🌊 Banasura Sagar Dam — largest earthen dam in India, 21 km from Kalpetta. Boating available (₹50/person). Stunning backdrop of Brahmagiri hills.",
            "evening":   "🌿 Soochipara (Sentinel Rock) Waterfalls — 2 km trek through coffee estate. Refreshing natural pool at the falls base. ₹50 entry. Check water levels before visiting.",
            "food_tip":  "Lunch at Vythiri Village Resort restaurant or local bamboo hut eateries near Banasura.",
            "entry_fee_est": "₹100–150 total",
            "distance_from_centre": "12–25 km",
        },
        {
            "theme": "Wildlife, Tea & Tribal Culture",
            "morning":   "🐘 Muthanga Wildlife Sanctuary (6 AM–5 PM) — guided safari jeep to spot wild elephants, gaur, and deer inside the Nilgiri Biosphere. ₹300–500/person.",
            "afternoon": "🍃 Wayanad Tea & Coffee Plantations — guided plantation tour at Vythiri Estate or Green Magic Nature Resort. Learn the process from leaf to cup.",
            "evening":   "🎭 Tribal Cultural Centre, Ambalavayal — exhibits on Kurichiyas, Paniyas, and other indigenous Wayanad tribes. Artefacts and traditional tools on display. Free or minimal entry.",
            "food_tip":  "Dinner at Green Gate Restaurant, Kalpetta — try bamboo biryani and pandi curry.",
            "entry_fee_est": "₹350–550 total",
            "distance_from_centre": "18–28 km",
        },
        {
            "theme": "Chembra Peak & Waterfalls",
            "morning":   "🏔️ Chembra Peak Trek (7 AM start) — highest peak in Wayanad at 2,100 m. Stunning heart-shaped lake at midpoint. ₹200 trekking permit + mandatory guide (₹400). 8 km from Kalpetta.",
            "afternoon": "💧 Meenmutty Waterfalls — tallest waterfall in Wayanad at 300 m height. 2 km moderately difficult forest trek. ₹50 entry. 29 km from Kalpetta.",
            "evening":   "Relax at accommodation, buy local honey, pepper, and cardamom from Sulthan Bathery market.",
            "food_tip":  "Post-trek meal at Sulthan Bathery town — try Kerala-style meals at Ariya Bhavan.",
            "entry_fee_est": "₹650–750 total (heavy trekking day)",
            "distance_from_centre": "8–29 km",
        },
    ],

    "Munnar": [
        {
            "theme": "Arrival & Tea Valleys",
            "morning":   "Scenic drive from base; stop at Cheeyappara Waterfalls (NH85, 40 km before Munnar) and Valara Waterfalls (2 km ahead). Free entry.",
            "afternoon": "🍃 Tata Tea Museum (9 AM–4 PM) — Kerala's only tea museum. Exhibits on 150 years of hill tea heritage, live machinery, and tasting session. ₹120/person. Book ahead.",
            "evening":   "🌄 Top Station Viewpoint — 32 km from Munnar town, highest point at 1,700 m. Panoramic view over Tamil Nadu plains. Free. Go before 5 PM.",
            "food_tip":  "Dinner at Saravana Bhavan, Munnar town — hearty South Indian thali.",
            "entry_fee_est": "₹120–200 total",
            "distance_from_centre": "7–32 km",
        },
        {
            "theme": "Lakes, Dams & Wildlife",
            "morning":   "🐘 Mattupetty Dam & Indo-Swiss Dairy Farm (9 AM–5 PM) — beautiful shola-rimmed reservoir, 13 km from Munnar. Speed boating ₹200/person. High-altitude dairy with prize Holstein cattle.",
            "afternoon": "🦬 Eravikulam National Park (8 AM–4 PM, closed Feb–Mar for calving) — home to the endangered Nilgiri Tahr mountain goat. Guided bus safari. ₹125/person Indian. Arrive by 8 AM to beat the queue.",
            "evening":   "🌿 Echo Point — shout and hear your voice echo across the Mattupetty reservoir. Beautiful evening light on surrounding hills. ₹30/person.",
            "food_tip":  "Local street-side corn, sweet bonda, and cardamom tea at the Echo Point stalls.",
            "entry_fee_est": "₹355–500 total",
            "distance_from_centre": "13–15 km",
        },
        {
            "theme": "Plantation Walks & Waterfalls",
            "morning":   "🏞️ Attukal Waterfalls — spectacular 30 m cascade through dense shola forest, 8 km from Munnar. Short 500 m walk from road. Free.",
            "afternoon": "🌿 Lockhart Gap View Point — breathtaking valley view at 1,800 m, 10 km from town. Free entry.",
            "evening":   "🌺 Rajamala / Eravikulam grasslands evening walk (if not visited yesterday). Rare Neelakurinji blooms every 12 years (next: 2030). Check seasonal bloom status.",
            "food_tip":  "Lunch at The Tall Trees Resort café or Zest restaurant, Munnar — Kerala fish curry and appam.",
            "entry_fee_est": "₹30–125 total",
            "distance_from_centre": "8–15 km",
        },
        {
            "theme": "Suryanelli, Kundala & Explore",
            "morning":   "🌊 Kundala Lake & Arch Dam — 20 km from Munnar. Kashmir shikara-style boat ride on a stunning high-altitude reservoir. ₹30–50/person.",
            "afternoon": "🚶 Suryanelli meadows hike — golden grasslands and cloud-forest, ideal for bird-watching (Nilgiri flycatcher, sunbirds). Self-guided walk.",
            "evening":   "Munnar bazaar — buy fresh cardamom powder, organic tea blends, eucalyptus oil, and homemade chocolate.",
            "food_tip":  "Dinner at Rapsy Restaurant, Munnar — Munnar-style mutton curry and porotta.",
            "entry_fee_est": "₹80–150 total",
            "distance_from_centre": "10–20 km",
        },
    ],

    "Alleppey": [
        {
            "theme": "Arrival & Houseboat Check-in",
            "morning":   "Arrive at Alleppey (Alappuzha). Drop luggage at hotel and head to the Boat Jetty (Finishing Point).",
            "afternoon": "🚢 Check in to overnight houseboat (kettuvallam) by 12 PM. Cruise through Vembanad Lake and the narrow village canals. Watch toddy tappers, coir weaving, and paddy cultivation from your deck.",
            "evening":   "🌅 Sunset on Vembanad Lake from the houseboat upper deck. Kerala sadya dinner served on board — full-course banana leaf rice meal.",
            "food_tip":  "All meals included on houseboat. Ask the cook to prepare karimeen pollichathu (pearl-spot fish in banana leaf).",
            "entry_fee_est": "₹4,000–10,000 for full houseboat/night",
            "distance_from_centre": "On-water cruise",
        },
        {
            "theme": "Backwater Villages & Kuttanad",
            "morning":   "🛶 Morning canoe ride through narrow shikara-width village canals into Kuttanad 'Venice of the East' — fields cultivated below sea level. ₹300–500/hour.",
            "afternoon": "🏖️ Marari Beach (12 km north) — quieter, cleaner alternative to Alleppey Beach. Casuarina trees and fishing hamlets. No entry fee.",
            "evening":   "🌊 Alleppey Beach promenade and old lighthouse (established 1862). Coconut water and fresh seafood shacks.",
            "food_tip":  "Dinner at Chakara Restaurant or Harbour Restaurant — prawn moilee and fish mappas.",
            "entry_fee_est": "₹300–500 canoe ride",
            "distance_from_centre": "0–12 km",
        },
        {
            "theme": "Krishnapuram & Village Life",
            "morning":   "🏰 Krishnapuram Palace (10 AM–5 PM, closed Mon) — 18th-century Kerala-style palace with Gajendra Moksham mural (largest in Kerala), antiques, and palanquins. ₹20/person. 47 km south.",
            "afternoon": "🌿 Coir Village or Kerala Tourism snake boat village — watch traditional coir mat weaving. Free.",
            "evening":   "Pathiramanal Island — tiny migratory bird island in Vembanad Lake, accessible by boat. Bird-watching haven.",
            "food_tip":  "Try Alleppey-style fish curry at Tharavad Restaurant.",
            "entry_fee_est": "₹20–200 total",
            "distance_from_centre": "0–47 km",
        },
    ],

    "Kochi": [
        {
            "theme": "Fort Kochi Heritage Walk",
            "morning":   "⛵ Chinese Fishing Nets (cantilever nets) — best viewed at 6:30 AM during sunrise catch. Buy freshly caught fish and get it cooked at a nearby stall for ₹100.",
            "afternoon": "🏛️ St. Francis Church (Asia's oldest European church, 1503) → Dutch Cemetery → Mattancherry Palace / Dutch Palace (₹10/person, closed Fri) with the famous Ramayana murals → Paradesi Synagogue (oldest active synagogue in India, ₹5/person).",
            "evening":   "🎭 Kerala Kathakali Centre show at 5 PM (₹350/person) — elaborate classical dance performance with make-up demonstration beforehand.",
            "food_tip":  "Dinner at Kashi Art Café or The Malabar Junction — Syrian Christian duck roast.",
            "entry_fee_est": "₹365–500 total",
            "distance_from_centre": "0–5 km Fort Kochi area",
        },
        {
            "theme": "Ernakulam & Spice Market",
            "morning":   "🌿 Mattancherry Spice Market (Jewtown) — Asia's largest spice trading hub. Buy cardamom, pepper, cinnamon and kokum at wholesale prices.",
            "afternoon": "🏛️ Kerala Folklore Museum (10 AM–7 PM) — 4,000+ artefacts across three floors of architecture replicas, tribal masks, temple art. ₹100/person.",
            "evening":   "🚢 Marine Drive promenade and Infopark backwater cruise (₹25/person on public ferry between Ernakulam and Fort Kochi islands).",
            "food_tip":  "Lunch at Pai Dosa, Broadway — Kerala-style meals. Dinner at Fusion Bay.",
            "entry_fee_est": "₹125–200 total",
            "distance_from_centre": "3–8 km",
        },
        {
            "theme": "Cherai Beach & Hill Palace",
            "morning":   "🏖️ Cherai Beach, Vypeen Island (25 km from Fort Kochi) — pristine backwater-meets-sea beach. Dolphins are occasionally spotted offshore. Free.",
            "afternoon": "🏰 Hill Palace Museum, Tripunithura (₹20 adults) — largest archaeological museum in Kerala, former Cochin royal family residence.",
            "evening":   "Lulu Mall or Grand Bazaar for shopping, or Kerala cultural village show.",
            "food_tip":  "Seafood dinner at Ocean Restaurant, Marine Drive.",
            "entry_fee_est": "₹40–100 total",
            "distance_from_centre": "10–25 km",
        },
    ],

    "Varkala": [
        {
            "theme": "Cliff Walk & Temple",
            "morning":   "🌊 Papanasam Beach — sacred Ayurvedic spring meets sea. Morning dip in the mineral-spring water, believed to wash away sins. Free.",
            "afternoon": "🛕 Janardanaswamy Temple (500+ years old) — active Vishnu temple perched directly above the cliff. One of the few temples in Kerala welcoming non-Hindus at the periphery.",
            "evening":   "🌅 North Cliff promenade — yoga studios, Ayurveda shops, and breezy rooftop restaurants overlooking the Arabian Sea.",
            "food_tip":  "Dinner at Clafouti Restaurant on the cliff — wood-fired pizza and coconut fish curry.",
            "entry_fee_est": "Mostly free",
            "distance_from_centre": "0–3 km",
        },
        {
            "theme": "Yoga, Ayurveda & Coves",
            "morning":   "🧘 Sunrise yoga session at a cliff-top yoga centre (many offer drop-in ₹500–800/session). Ayurvedic massage at reputed centres.",
            "afternoon": "🏖️ Black Beach & Edava Beach — less crowded southern coves with dramatic laterite cliffs. 5 km south of main cliff.",
            "evening":   "Kathakali or Mohiniyattam cultural show at cliff-side cultural space.",
            "food_tip":  "Try Varkala-style prawn masala at Café del Mar or The Coffee Temple.",
            "entry_fee_est": "₹500–800 yoga/massage",
            "distance_from_centre": "0–5 km",
        },
    ],

    "Goa": [
        {
            "theme": "North Goa Beaches & Forts",
            "morning":   "🏖️ Calangute Beach — Goa's most popular beach. Walk south along the 7 km shoreline. Rent a sun bed or join a water-sports booth.",
            "afternoon": "🏰 Fort Aguada (9 AM–6 PM) — 17th-century Portuguese fortress commanding the Mandovi River mouth. Lighthouse, prison ruins, and sea bastions. ₹25/person. 6 km south.",
            "evening":   "🌅 Anjuna Flea Market (Wednesday only) or Baga Nightlife Strip — Tito's Lane, Café Mambo, and Britto's.",
            "food_tip":  "Fish thali at A Reverie or Souza Lobo, Calangute — Goan prawn curry rice.",
            "entry_fee_est": "₹25–200 total",
            "distance_from_centre": "0–15 km",
        },
        {
            "theme": "Old Goa Heritage & Spice Farms",
            "morning":   "⛪ Old Goa (UNESCO Heritage Site) — Basilica of Bom Jesus (St. Francis Xavier's relics, 1605), Se Cathedral (largest church in Asia), Church of St. Francis of Assisi. All free entry. 10 km from Panaji.",
            "afternoon": "🌿 Savoi Spice Plantation (11 AM or 3 PM sessions) — 60 min guided walk through organic spice groves. Traditional Goan lunch included. ₹600/person. 28 km east.",
            "evening":   "🚢 Mandovi River sunset cruise (₹300/person) departing Panaji Jetty — live Goan folk music and dance on board.",
            "food_tip":  "Pork vindaloo and bebinca dessert at Ritz Classic, Panaji.",
            "entry_fee_est": "₹900–1,100 total",
            "distance_from_centre": "10–28 km",
        },
        {
            "theme": "South Goa Beaches & Cabo de Rama",
            "morning":   "🏖️ Palolem Beach (South Goa) — crescent-shaped paradise beach. Kayak to Honeymoon Island (₹200). 65 km from Panaji — travel by scooter or taxi.",
            "afternoon": "🏰 Cabo de Rama Fort — ruined Portuguese fortification on a dramatic cliff 80 m above the Arabian Sea. Sunset views. ₹25/person.",
            "evening":   "🐬 Butterfly Beach boat trip from Agonda (₹300/person for shared boat) — secluded beach only accessible by sea, with dolphins en route.",
            "food_tip":  "Seafood shack dinner at Magic Italy or Dropadi, Palolem.",
            "entry_fee_est": "₹525–700 total",
            "distance_from_centre": "55–70 km",
        },
        {
            "theme": "Dudhsagar Falls & Wildlife",
            "morning":   "💦 Dudhsagar Falls (4 WD jeep safari + 2 km hike) — India's 5th tallest waterfall at 310 m, on the Goa–Karnataka border. Seasonal (Oct–Jun). ₹400–600/person including jeep. 60 km from Panaji. Must depart by 7 AM.",
            "afternoon": "🐘 Bhagwan Mahaveer Wildlife Sanctuary & Molem National Park — guided forest walk. Occasional gaur, barking deer, and giant squirrel sightings.",
            "evening":   "Return to North Goa. Relax at Candolim or Sinquerim Beach.",
            "food_tip":  "Goan fish curry at Gunpowder or Fisherman's Wharf.",
            "entry_fee_est": "₹400–700 total",
            "distance_from_centre": "55–65 km",
        },
    ],

    "Ooty": [
        {
            "theme": "Botanical Garden & Lake",
            "morning":   "🌺 Ooty Botanical Garden (7 AM–6:30 PM) — 22 hectares, 650+ plant species including a 20 million-year-old fossilised tree trunk. ₹50/person Indian.",
            "afternoon": "🚂 Nilgiri Mountain Railway (UNESCO Heritage) — 1908 steam-era rack-and-pinion train from Ooty to Coonoor (45 min). Tickets from ₹40. Book on IRCTC well in advance.",
            "evening":   "⛵ Ooty Lake — paddleboat and motor boat rides. ₹40–80/person. Pleasant lakeside walk.",
            "food_tip":  "Ooty homemade chocolate from King Star or JS Chocolates shop on Commercial Road.",
            "entry_fee_est": "₹130–200 total",
            "distance_from_centre": "0–5 km",
        },
        {
            "theme": "Tea Factory & Viewpoints",
            "morning":   "🍃 Doddabetta Peak — Nilgiris highest point at 2,637 m. Telescope House and stunning 360° views. ₹50/person. 10 km from Ooty.",
            "afternoon": "🏭 Dodabetta Tea Factory tour — watch the full process from green leaf to packaged tea with a guided explanation. Free or ₹30 donation.",
            "evening":   "🌅 Wenlock Downs / Golf Course — rolling emerald-green meadows at high altitude. Scenic evening walk.",
            "food_tip":  "Hot Nilgiri tea with cream biscuits from wayside stalls. Dinner at Hotel Nahar.",
            "entry_fee_est": "₹80–150 total",
            "distance_from_centre": "10 km",
        },
        {
            "theme": "Coonoor & Avalanche",
            "morning":   "🌿 Coonoor (18 km from Ooty) — Sim's Park Botanical Garden (₹30), Lamb's Rock viewpoint, and tea estate walks.",
            "afternoon": "❄️ Avalanche Lake — pristine shola-grass ecosystem at 2,400 m altitude. Entry permit from Forest Dept (₹50). 28 km from Ooty. Trout fishing permitted.",
            "evening":   "Return to Ooty. Pykara Lake evening visit or stay in Coonoor.",
            "food_tip":  "Lunch at The Balmoral Hotel, Coonoor — colonial-era bungalow restaurant.",
            "entry_fee_est": "₹80–150 total",
            "distance_from_centre": "18–28 km",
        },
    ],

    "Coorg": [
        {
            "theme": "Abbey Falls & Coffee Estates",
            "morning":   "☕ Coffee plantation walk — Coorg (Kodagu) produces 30% of India's coffee. Join a guided estate tour at Rainforest Retreat or Honey Valley. Walk among Arabica and Robusta plants.",
            "afternoon": "💦 Abbey Falls (9 AM–6 PM) — 70 ft double waterfall framed by coffee and spice estates. 10 min walk from parking. ₹20/person. 9 km from Madikeri.",
            "evening":   "🏰 Madikeri Fort & Raja's Seat (sunset point) — 17th-century Kodagu fort and the famous royal bench overlooking mist-covered valleys at dusk.",
            "food_tip":  "Kodagu-style pandi curry (pork) and kadumbuttu (rice dumplings) at Coorg Cuisine Restaurant.",
            "entry_fee_est": "₹20–100 total",
            "distance_from_centre": "0–15 km",
        },
        {
            "theme": "Nagarhole & Dubare",
            "morning":   "🐘 Dubare Elephant Camp (9 AM–11 AM, bath time) — official Karnataka Forest Dept camp. Interact with semi-wild elephants, assist mahouts in bathing them in Cauvery River. ₹200/person + boat crossing ₹20. 34 km from Madikeri.",
            "afternoon": "🌿 Nagarhole National Park safari (3 PM–6 PM jeep safari) — spot elephants, leopards, tigers (rare), gaur, and sambar deer. ₹650–900/person.",
            "evening":   "Bhagamandala & Talacauvery — sacred Triveni Sangam (confluence of 3 rivers) and the origin spring of Cauvery River at 1,276 m. 51 km from Madikeri.",
            "food_tip":  "Lunch at Padi Iguthappa near Bhagamandala — Kodava-style meals.",
            "entry_fee_est": "₹870–1,120 total",
            "distance_from_centre": "34–51 km",
        },
    ],

    "Mysuru": [
        {
            "theme": "Mysore Palace & Market",
            "morning":   "🏰 Mysore Palace (10 AM–5:30 PM, illuminated on Sun & holidays 7–7:45 PM) — one of India's most visited monuments. 145 rooms of Indo-Saracenic opulence. ₹100/person (₹200 with audio guide).",
            "afternoon": "🛍️ Devaraja Market — sprawling fragrant market of jasmine garlands, incense sticks, silk, and spices dating to 1900. Free.",
            "evening":   "🌅 Chamundi Hill & Sri Chamundeshwari Temple — 1,000-step climb or drive up the sacred hilltop. Panoramic view over Mysuru city and Nandi bull statue.",
            "food_tip":  "Mysore pak (iconic sweet) from Guru Sweets and Mylari dosas for breakfast.",
            "entry_fee_est": "₹100–200 total",
            "distance_from_centre": "0–13 km",
        },
        {
            "theme": "Brindavan Gardens & Srirangapatna",
            "morning":   "🕌 Srirangapatna (15 km) — Tipu Sultan's island fort capital. Sri Ranganathaswamy Temple (one of Vaishnava 108 Divya Desams), Tipu's Summer Palace (Daria Daulat Bagh, ₹15), Gumbaz mausoleum.",
            "afternoon": "🌹 Brindavan Gardens (₹30 entry, musical fountain 6:30–7:30 PM on Sat/Sun) — KRS Dam garden terraced along the Cauvery. Illuminated fountain show is spectacular.",
            "evening":   "Silk weaving demonstration at KSIC Silk Factory showroom, Mananthody Road.",
            "food_tip":  "Lunch at Hotel RRR, Mysore — authentic Mysore thali. Evening coffee at Infosys Circle.",
            "entry_fee_est": "₹45–100 total",
            "distance_from_centre": "15–20 km",
        },
    ],

    "Gokarna": [
        {
            "theme": "Mahabaleshwar Temple & Om Beach",
            "morning":   "🛕 Sri Mahabaleshwar Temple — ancient Shaivite temple housing the self-manifested Atmalinga, one of the 7 sacred Mukti-Sthalas. Dress modestly.",
            "afternoon": "🏖️ Om Beach — so named because the shoreline traces the OM (ॐ) symbol from the air. Pristine beach surrounded by rocky headlands. Boat ride to Half Moon Beach (₹300–400/person).",
            "evening":   "🌅 Sunset at Kudle Beach — less crowded, hippy-vibe beach with shacks and hammocks.",
            "food_tip":  "Dinner at Namaste Cafe, Om Beach — fresh catch grilled seafood and Israeli hummus.",
            "entry_fee_est": "₹300–400 boat ride",
            "distance_from_centre": "0–5 km",
        },
        {
            "theme": "Secret Beaches & Cliff Walk",
            "morning":   "🌊 Paradise Beach & Half Moon Beach — accessible only by a 1.5 km forest cliff trail or boat. Pack water and snacks. Pristine and semi-deserted.",
            "afternoon": "🗿 Mirjan Fort (15 km, ruins of 16th-century Keladi Nayaka fort) — surrounded by tropical jungle, seasonal stream moat, and bird life. ₹25/person.",
            "evening":   "Beachside bonfire at Om Beach or Kudle Beach shack.",
            "food_tip":  "Try Mangalorean-style fish curry at La Pizzeria or Shree Shakti Hotel.",
            "entry_fee_est": "₹25–100 total",
            "distance_from_centre": "0–15 km",
        },
    ],

    # ────────────── INTERNATIONAL ──────────────
    "Tokyo": [
        {
            "theme": "Arrival & Shinjuku",
            "morning":   "✈️ Arrive at Narita / Haneda. Take Narita Express (¥3,070) or Limousine Bus (¥3,100) to city. Get IC card (Suica/Pasmo) for all transit.",
            "afternoon": "🗼 Tokyo Metropolitan Government Building (free observatory, 5:30 PM–10:30 PM Tue–Sun) — panoramic 360° skyline views. Shinjuku Gyoen National Garden (¥500, closes 4:30 PM).",
            "evening":   "🌃 Kabukicho entertainment district, Memory Lane (Omoide Yokocho) — tiny yakitori alley. Dinner at standing sushi bar.",
            "food_tip":  "Ichiran Ramen solo-booth ramen experience — 100% tonkotsu broth, ¥1,000.",
            "entry_fee_est": "¥500–1,000 (₹300–600)",
            "distance_from_centre": "0–8 km",
        },
        {
            "theme": "Senso-ji & Akihabara",
            "morning":   "⛩️ Senso-ji Temple, Asakusa — Tokyo's oldest temple (645 AD). Arrive by 7 AM to beat crowds. Nakamise shopping arcade: matcha KitKats, ningyo-yaki, and samurai souvenirs.",
            "afternoon": "🎮 Akihabara Electric Town — 10 floors of electronics, anime figures, retro game cartridges, and maid cafés. Budget ¥3,000–5,000 for shopping.",
            "evening":   "🌸 Sumida River evening walk near Asakusa. Tokyo Skytree observation deck (¥2,100) with evening city glow.",
            "food_tip":  "Tendon Tenya near Asakusa — delicious tempura bowl, ¥700.",
            "entry_fee_est": "¥4,200–7,100 (₹2,500–4,200)",
            "distance_from_centre": "5–12 km",
        },
        {
            "theme": "Harajuku, Shibuya & Meiji",
            "morning":   "🌿 Meiji Jingu Shrine — forested 70 ha Shinto sanctuary. Serene morning stroll on gravel paths under 100-year-old camphor trees. Free.",
            "afternoon": "👗 Takeshita Street, Harajuku — youth fashion Mecca: crepe stands, cosplay stores, kawaii culture. → Shibuya Sky observatory (¥2,000) or Shibuya Crossing — the world's busiest pedestrian crossing.",
            "evening":   "🛍️ Omotesando Hills — Tokyo's Champs-Élysées. Window shop Japanese luxury brands and street fashion.",
            "food_tip":  "Shibuya: dinner at Uoriki seafood izakaya. Harajuku: legendary rainbow-layer crêpes at Marion Crêpes.",
            "entry_fee_est": "¥2,000–4,000 (₹1,200–2,400)",
            "distance_from_centre": "8–12 km",
        },
        {
            "theme": "Nikko Day Trip",
            "morning":   "🚄 Day trip to Nikko (2 hrs by Tobu Express, ¥1,360). Toshogu Shrine — UNESCO World Heritage, elaborate mausoleum of Tokugawa Ieyasu. ¥1,300/person.",
            "afternoon": "💦 Kegon Falls — 97 m waterfall in volcanic Nikko. Elevator to viewing platform ¥570. Chuzenji Lake shore walk.",
            "evening":   "Return to Tokyo. Akihabara evening electronics shopping.",
            "food_tip":  "Nikko: yuba (tofu skin) cuisine at Suzuya Restaurant — local specialty.",
            "entry_fee_est": "¥3,230–5,000 (₹2,000–3,000)",
            "distance_from_centre": "150 km day trip",
        },
        {
            "theme": "teamLab & Odaiba",
            "morning":   "🎨 teamLab Planets, Toyosu (9 AM) — immersive digital art walk-through in water, light tunnels, and flower rooms. ¥3,200/person. Book online well in advance.",
            "afternoon": "🌁 Odaiba artificial island — Gundam Statue (free), DiverCity mall, TeamLab Borderless (¥2,800), and a clear view of Rainbow Bridge and Mount Fuji on clear days.",
            "evening":   "Onsen spa at Odaiba Oedo Onsen Monogatari (¥2,980) — Edo-period themed hot spring resort with yukata dress-up.",
            "food_tip":  "DiverCity food court: try tamagoyaki (rolled omelette) and chirashi-zushi bowls.",
            "entry_fee_est": "¥6,000–9,000 (₹3,600–5,400)",
            "distance_from_centre": "10–18 km",
        },
    ],

    "Phuket": [
        {
            "theme": "Arrival, Patong & Sunset View",
            "morning": "Arrive at Phuket International Airport (HKT). Transfer to hotel (Patong, Kata, or Karon beach). Check in and freshen up.",
            "afternoon": "🏖️ Patong Beach or Kata Beach — walk along the crescent bay, swim in warm Andaman waters, or try parasailing/jet-skiing.",
            "evening": "🌅 Promthep Cape (Phromthep Cape) — Phuket's southernmost viewpoint. World-famous panoramic Andaman sunset. Free entry.",
            "food_tip": "Tom Yum Goong and fresh grilled red snapper at Savoey Seafood or Malin Plaza street food market, Patong.",
            "entry_fee_est": "฿50–150 (₹120–350)",
            "distance_from_centre": "5–18 km",
        },
        {
            "theme": "Phi Phi Islands & Maya Bay Island Hopping",
            "morning": "🚤 Full-day speedboat tour to Phi Phi Islands (departing Rassada Pier 7:30 AM). Cruise past Viking Cave and Monkey Beach.",
            "afternoon": "🏝️ Maya Bay (The Beach movie setting) & Pileh Lagoon emerald natural swimming pool. Snorkelling with sea turtles and parrotfish.",
            "evening": "Return to Phuket pier by 5 PM. Night stroll along Bangla Road — neon walking street with live music, street performers, and food carts.",
            "food_tip": "Pad Thai with tiger prawns and banana Nutella roti pancake from street stalls.",
            "entry_fee_est": "฿1,500–2,200 speed boat tour (₹3,500–5,000) incl. national park fee",
            "distance_from_centre": "Full-day offshore tour",
        },
        {
            "theme": "Big Buddha & Old Phuket Town",
            "morning": "🛕 The Big Buddha (Phra Phutta Ming Mongkol Akenakakhiri) — 45 m tall white Burmese marble Buddha on Nakkerd Hill with 360° views. Free entry. Dress respectfully.",
            "afternoon": "🏛️ Old Phuket Town (Thalang Road & Soi Rommanee) — Sino-Portuguese heritage architecture, pastel shophouses, street murals, and boutique cafés.",
            "evening": "Wat Chalong — Phuket's largest, most ornate Buddhist temple. Evening chilled coconut at Rawai Seafood Market.",
            "food_tip": "Moo Hong (braised pork belly) and Phuket Hokkien noodles at Raya Restaurant or Tu Kab Khao in Old Town.",
            "entry_fee_est": "฿50–200 (₹120–480)",
            "distance_from_centre": "8–15 km",
        },
    ],

    "Chiang Mai": [
        {
            "theme": "Old City Temples & Night Bazaar",
            "morning": "Arrive in Chiang Mai. Explore the moat-surrounded Old City. Wat Phra Singh (14th century, Lion Buddha) and Wat Chedi Luang ancient ruined pagoda.",
            "afternoon": "☕ Nimmanhaemin Road — trendy art district, modern Thai boutiques, world-class artisanal coffee shops, and Maya Lifestyle mall.",
            "evening": "Night Bazaar on Chang Klan Road or Sunday Walking Street (Rachadamnoen Rd) — handcrafted hill-tribe silver, silk scarves, and lantern-lit stalls.",
            "food_tip": "Khao Soi (creamy coconut curry noodle soup with crispy noodles) at Khao Soi Islam or Huen Phen.",
            "entry_fee_est": "฿100–200 (₹240–480)",
            "distance_from_centre": "0–4 km",
        },
        {
            "theme": "Doi Suthep & Ethical Elephant Sanctuary",
            "morning": "🐘 Morning half-day at an ethical Elephant Nature Park or Elephant Jungle Sanctuary — feed, bathe, and walk alongside rescued Asian elephants (no riding).",
            "afternoon": "🛕 Wat Phra That Doi Suthep — sacred golden mountain temple at 1,060 m altitude. Climb the 306-step Naga dragon staircase or take funicular elevator (฿30). Spectacular city view.",
            "evening": "Bhubing Palace royal winter flower gardens or sunset drink at a riverside bar along Ping River.",
            "food_tip": "Sai Oua (spicy northern Thai herbal sausage) and sticky rice at Ton Payom Market.",
            "entry_fee_est": "฿1,800–2,500 sanctuary + ฿50 Doi Suthep (₹4,500–6,000 total)",
            "distance_from_centre": "15–40 km",
        },
    ],

    "Pattaya": [
        {
            "theme": "Coral Island & Beach Adventure",
            "morning": "Arrive in Pattaya. Take 20 min speedboat from Bali Hai Pier to Koh Larn (Coral Island).",
            "afternoon": "🏖️ Tawaen Beach / Tien Beach — crystal clear waters, banana boat rides, parasailing, and underwater sea-walking amongst coral.",
            "evening": "Return to Pattaya. Visit Pattaya Viewpoint (Khao Pattaya) for sweeping crescent bay view. Night walk at Walking Street.",
            "food_tip": "Fresh grilled jumbo prawns and spicy green papaya salad (Som Tum) at Jomtien Beach shacks.",
            "entry_fee_est": "฿300–800 boat & beach activities (₹700–1,900)",
            "distance_from_centre": "Island crossing",
        },
        {
            "theme": "Sanctuary of Truth & Floating Market",
            "morning": "🏛️ The Sanctuary of Truth (Prasat Sut Ja-Tum) — colossal 105 m hand-carved all-wood seaside temple/museum. An awe-inspiring architectural wonder. ฿500 entry.",
            "afternoon": "🚣 Pattaya Floating Market (Four Regions Floating Market) — explore traditional wooden boats selling snacks, wood crafts, and silk across 4 Thai cultural zones.",
            "evening": "Tiffany's Show or Alcazar Cabaret Show — world-famous glamorous musical theatre.",
            "food_tip": "Mango sticky rice and coconut ice cream served in real coconut shell inside the floating market.",
            "entry_fee_est": "฿800–1,200 (₹1,900–2,800)",
            "distance_from_centre": "5–12 km",
        },
    ],

    "Krabi": [
        {
            "theme": "Railay Beach & Limestone Cliffs",
            "morning": "Arrive in Krabi. Long-tail boat from Ao Nang beach to Railay Beach (accessible only by boat due to limestone cliffs, ฿100 one-way).",
            "afternoon": "🧗 Phra Nang Cave Beach — legendary Princess Cave, emerald water swimming, and watching rock climbers scale sheer limestone karst bluffs.",
            "evening": "Sunset at Railay West Beach. Evening walk through Ao Nang Night Market.",
            "food_tip": "Massaman curry and roti pancakes at Ao Nang beachfront restaurants.",
            "entry_fee_est": "฿200 boat rides (₹480)",
            "distance_from_centre": "Boat transfer",
        },
        {
            "theme": "Emerald Pool & Tiger Cave Temple",
            "morning": "🌿 Emerald Pool (Sa Morakot) & Hot Springs Waterfall (Klong Thom) — crystal natural freshwater pool in Khao Phra Bang Khram Nature Reserve. ฿200 entry.",
            "afternoon": "🛕 Wat Tham Suea (Tiger Cave Temple) — climb 1,237 steep steps to the summit golden Buddha. Stunning 360° jungle and limestone karst panorama.",
            "evening": "Krabi Town night market (Friday–Sunday) — local Southern Thai food, live musicians, and crafts.",
            "food_tip": "Gaeng Som (Southern Thai spicy sour fish curry) with jasmine rice.",
            "entry_fee_est": "฿300–400 (₹700–950)",
            "distance_from_centre": "25–45 km",
        },
    ],

    "Dubai": [
        {
            "theme": "Burj Khalifa, Dubai Mall & Fountain",
            "morning": "Arrive in Dubai. Check in. Take Dubai Metro Red Line to Burj Khalifa / Dubai Mall station.",
            "afternoon": "🏙️ Burj Khalifa At The Top (Levels 124+125, ~AED 179) — look out from the world's tallest building. Explore Dubai Mall and Dubai Aquarium underwater zoo.",
            "evening": "⛲ Dubai Fountain Show (every 30 mins from 6 PM, free) — synchronized music, light and water dance at the foot of Burj Khalifa.",
            "food_tip": "Shawarma and freshly squeezed pomegranate juice at Al Mallah, Dhiyafah Road, or Time Out Market Dubai Mall.",
            "entry_fee_est": "AED 180–250 (₹4,000–5,600)",
            "distance_from_centre": "0–8 km",
        },
        {
            "theme": "Desert Safari & Bedouin Camp",
            "morning": "Heritage Dubai: visit Al Fahidi Historical Neighbourhood, ride a traditional abra water taxi across Dubai Creek (AED 1), and explore the Gold & Spice Souks.",
            "afternoon": "🚙 Red Dunes Desert Safari (3 PM pickup) — thrilling 4x4 dune bashing across golden Lahbab sand dunes, sandboarding, and camel rides.",
            "evening": "Desert campsite: BBQ buffet dinner under the stars with Tanoura dance, fire show, and belly dancing.",
            "food_tip": "Authentic Emirati chicken machboos and luqaimat (sweet honey dumplings) at Al Fanar Restaurant.",
            "entry_fee_est": "AED 150–220 safari (₹3,400–5,000)",
            "distance_from_centre": "45 km into desert",
        },
    ],

    "Bangkok": [
        {
            "theme": "Grand Palace & Chao Phraya",
            "morning":   "🏛️ Grand Palace + Wat Phra Kaew (Temple of the Emerald Buddha) — Thailand's most sacred site. Open 8:30 AM–3:30 PM. ฿500/person. Dress code strictly enforced: cover knees and shoulders.",
            "afternoon": "⛩️ Wat Pho — Reclining Buddha (46 m long, gold-plated). Oldest temple in Bangkok, famous Thai massage school. ฿200. Then take river ferry to Wat Arun (Temple of Dawn), ฿100.",
            "evening":   "🌃 Asiatique The Riverfront — open-air riverside night bazaar with Ferris wheel, street food, and live shows. Ferris wheel ฿250.",
            "food_tip":  "Pad kra pao (stir-fried holy basil with pork/chicken) at any street stall — authentic Bangkok meal for ฿60.",
            "entry_fee_est": "฿800–1,100 (₹1,900–2,600)",
            "distance_from_centre": "0–6 km",
        },
        {
            "theme": "Chatuchak & Thai Culture",
            "morning":   "🛍️ Chatuchak Weekend Market (open Sat–Sun, 6 AM–6 PM) — 8,000+ stalls across 27 sections. Antiques, street fashion, live plants, vintage vinyl, and exotic pets.",
            "afternoon": "🏛️ Jim Thompson House — silk tycoon's Thai traditional house-museum (9 AM–6 PM). ฿200.",
            "evening":   "Lumphini Park evening jog, monitor lizard spotting. Sukhumvit Soi 38 night food market.",
            "food_tip":  "Mango sticky rice (₹200 equivalent) from Or Tor Kor Market near Chatuchak.",
            "entry_fee_est": "฿200–450 (₹500–1,100)",
            "distance_from_centre": "10–15 km",
        },
    ],

    "Singapore": [
        {
            "theme": "Marina Bay & Gardens",
            "morning":   "🌿 Gardens by the Bay (Supertree Grove — free, outdoor) — iconic steel-clad trees up to 16 storeys. Cloud Forest dome S$28/person.",
            "afternoon": "🏙️ Marina Bay Sands SkyPark Observation Deck (S$32) — 57th-floor view of city skyline and Strait of Malacca.",
            "evening":   "💡 Spectra Light & Water Show at Event Plaza, Marina Bay — free 15 min show at 8 PM & 9 PM daily.",
            "food_tip":  "Hawker Centre dinner at Lau Pa Sat — chilli crab, satay, and char kway teow from ₹400 per person.",
            "entry_fee_est": "S$60 (₹3,800)",
            "distance_from_centre": "0–3 km",
        },
        {
            "theme": "Sentosa & Universal Studios",
            "morning":   "🎢 Universal Studios Singapore — full-day park. S$83/adult. Rides across Hollywood, New York, Sci-Fi City, Ancient Egypt, and The Lost World zones.",
            "afternoon": "🏖️ Sentosa Island beaches — Siloso Beach, Palawan Beach, and Tanjong Beach are free. Luge & Skyride ₹800 equivalent.",
            "evening":   "🔥 Wings of Time show on Siloso Beach — nightly pyrotechnic water projection show (S$18).",
            "food_tip":  "Chirashi sushi bowl at Sakura International Buffet, or hawker crab at Mellben Seafood.",
            "entry_fee_est": "S$100+ (₹6,300+)",
            "distance_from_centre": "6–8 km",
        },
    ],
}


def create_detailed_itinerary(destination: str, days: int, preference: str = "Any") -> list:
    """
    Generate a detailed day-by-day itinerary for the given destination.
    Returns a list of dicts (one per day) with morning/afternoon/evening/food_tip/entry_fee.
    Falls back to generic preference-based plan if destination is not in DETAILED_ITINERARIES.
    """
    dest_key = destination.strip().title()
    days = max(1, int(days))

    if dest_key in DETAILED_ITINERARIES:
        day_plans = DETAILED_ITINERARIES[dest_key]
    else:
        # Generic plans based on travel preference
        generic = {
            "Beach": [
                {
                    "theme": "Beach Arrival & First Dip",
                    "morning": "Arrive at destination. Check in and head to the main beach for orientation.",
                    "afternoon": f"🏖️ Explore the most popular beach at {dest_key}. Swim, sunbathe, and rent equipment for water sports.",
                    "evening": "🌅 Sunset walk along the shore. Explore beachside shacks and fresh seafood stalls.",
                    "food_tip": "Try the local catch-of-the-day prepared in coastal style.",
                    "entry_fee_est": "Mostly free",
                    "distance_from_centre": "0–5 km",
                },
                {
                    "theme": "Hidden Coves & Sea Activities",
                    "morning": "🚤 Boat trip to lesser-known beaches or nearby islands. Look for snorkelling spots.",
                    "afternoon": "Water sports: kayaking, parasailing, or jet-skiing depending on availability.",
                    "evening": "Visit a local fish market or village, learn about the fishing community.",
                    "food_tip": "Grilled prawns or lobster at a beachside shack.",
                    "entry_fee_est": "₹200–500 activities",
                    "distance_from_centre": "5–20 km",
                },
                {
                    "theme": "Local Culture & Markets",
                    "morning": "Visit a historic temple, fort, or lighthouse near the coast.",
                    "afternoon": "Browse the local market for spices, handicrafts, and souvenirs.",
                    "evening": "Beachside bonfire or cultural show.",
                    "food_tip": "Local coastal cuisine at a family-run restaurant.",
                    "entry_fee_est": "₹50–200",
                    "distance_from_centre": "5–15 km",
                },
            ],
            "Hills and Nature": [
                {
                    "theme": "Arrival & First Trek",
                    "morning": f"Arrive in {dest_key}. Acclimatise to altitude. Morning walk through the town centre.",
                    "afternoon": "🏞️ Visit the nearest well-known viewpoint or nature reserve for panoramic vistas.",
                    "evening": "🌅 Sunset from a prominent hilltop or lake shore.",
                    "food_tip": "Try local mountain cuisine — corn, millets, or regional stew.",
                    "entry_fee_est": "₹50–150",
                    "distance_from_centre": "5–20 km",
                },
                {
                    "theme": "Waterfalls & Wildlife",
                    "morning": "🌊 Trek to a popular waterfall. Carry water and wear non-slip shoes.",
                    "afternoon": "🐘 Visit a wildlife sanctuary or national park for a safari/nature walk.",
                    "evening": "Plantation tour (tea, coffee, or spice) at a nearby estate.",
                    "food_tip": "Freshly brewed local tea with hot bhajis from a roadside stall.",
                    "entry_fee_est": "₹200–600",
                    "distance_from_centre": "10–30 km",
                },
                {
                    "theme": "Heritage & Local Villages",
                    "morning": "Visit a tribal cultural centre or local museum.",
                    "afternoon": "Village walk and interaction with local farming/weaving community.",
                    "evening": "Market visit for hill spices, honey, and handicrafts.",
                    "food_tip": "Traditional home-cooked meal at a village homestay.",
                    "entry_fee_est": "₹0–100",
                    "distance_from_centre": "0–20 km",
                },
            ],
            "Historical": [
                {
                    "theme": "Monuments & Heritage Walk",
                    "morning": f"🏰 Visit the most iconic monument or fort in {dest_key}. Hire an official guide for context.",
                    "afternoon": "🏛️ Explore a museum or heritage neighbourhood with colonial or ancient architecture.",
                    "evening": "Guided heritage walk through old quarters. Street food trail.",
                    "food_tip": "Try a heritage recipe restaurant serving regional thali or royal cuisine.",
                    "entry_fee_est": "₹100–300",
                    "distance_from_centre": "0–10 km",
                },
                {
                    "theme": "Temples, Palaces & Culture",
                    "morning": "Visit a major religious site or palace — morning is ideal for peaceful exploration.",
                    "afternoon": "Craft or textile museum. Kathakali, Bharat Natyam, or regional dance show.",
                    "evening": "Attend a light-and-sound show or cultural evening at the fort.",
                    "food_tip": "Heritage restaurant or century-old sweet shop nearby.",
                    "entry_fee_est": "₹150–400",
                    "distance_from_centre": "5–15 km",
                },
            ],
            "City and Culture": [
                {
                    "theme": "City Highlights",
                    "morning": f"Explore the main city centre of {dest_key} — landmark square, central market.",
                    "afternoon": "City museum, art gallery, or cultural centre.",
                    "evening": "Evening promenade, local street food, and night market.",
                    "food_tip": "Regional cuisine at a well-reviewed local restaurant.",
                    "entry_fee_est": "₹50–200",
                    "distance_from_centre": "0–8 km",
                },
                {
                    "theme": "Neighbourhoods & Local Life",
                    "morning": "Heritage neighbourhood walk: traditional architecture, old bazaars.",
                    "afternoon": "Handicraft and textile workshops. Visit artisan quarters.",
                    "evening": "Cultural show, classical music performance, or cinema.",
                    "food_tip": "Street food sampling across 3–4 local eateries.",
                    "entry_fee_est": "₹100–300",
                    "distance_from_centre": "2–15 km",
                },
            ],
        }
        day_plans = generic.get(preference, generic.get("City and Culture", []))
        if not day_plans:
            day_plans = [
                {
                    "theme": f"Explore {dest_key}",
                    "morning": f"Morning sightseeing in {dest_key}.",
                    "afternoon": "Afternoon cultural and heritage sites.",
                    "evening": "Evening local food and market exploration.",
                    "food_tip": "Try the local cuisine at a popular nearby restaurant.",
                    "entry_fee_est": "₹100–300",
                    "distance_from_centre": "0–15 km",
                }
            ]

    itinerary = []
    for day_num in range(1, days + 1):
        plan = day_plans[(day_num - 1) % len(day_plans)]
        itinerary.append({
            "day": day_num,
            "theme": plan.get("theme", f"Day {day_num}"),
            "morning": plan.get("morning", "Morning activities"),
            "afternoon": plan.get("afternoon", "Afternoon activities"),
            "evening": plan.get("evening", "Evening activities"),
            "food_tip": plan.get("food_tip", "Try local cuisine"),
            "entry_fee_est": plan.get("entry_fee_est", "Varies"),
            "distance_from_centre": plan.get("distance_from_centre", "Varies"),
        })
    return itinerary


def create_budget_breakdown(
    budget,
    days,
    travellers,
    destination="Goa",
    country="India",
    starting_location="Malappuram, Kerala"
):
    if budget <= 0 or days <= 0 or travellers <= 0:
        print("Budget, days, and travellers must be greater than zero.")
        return

    real_plan = calculate_real_trip_budget(
        destination=destination,
        country=country,
        days=days,
        travellers=travellers,
        starting_location=starting_location,
    )

    feasibility = analyze_budget_feasibility(budget, real_plan)

    print("\nDETAILED TRIP BUDGET & FEASIBILITY REPORT")
    print("=" * 50)
    print(f"Destination: {destination}, {country}")
    print(f"Trip Duration: {days} day(s) ({real_plan['nights']} night(s))")
    print(f"Travellers: {travellers} | Rooms: {real_plan['rooms']}")
    print(f"User Budget: Rs{budget:,.0f} (Rs{budget / travellers:,.0f}/person)")
    print(f"Realistic Market Cost: Rs{real_plan['estimated_total_cost']:,.0f}")
    print("-" * 50)
    print(f"Feasibility Status: {feasibility['badge_label']}")
    print(f"Diagnosis: {feasibility['headline']}")
    print(f"{feasibility['summary']}")
    print("-" * 50)
    print("REALISTIC ITEM-BY-ITEM EXPENSE BREAKDOWN:")
    for item in real_plan["items"]:
        print(
            f" - {item['Expense']}: Rs{item['Estimated amount (INR)']:,.0f} "
            f"({item['Share']}) [{item['Rate / Unit']}]"
        )
    print("=" * 50)
    calculate_rooms(travellers)
    return real_plan


def create_itinerary(destination, days):
    """Generate a destination-specific itinerary."""
    dest = (destination or "").strip().title()
    detailed = create_detailed_itinerary(dest, days)
    print(f"\n{days}-DAY ITINERARY FOR {dest.upper()}")
    print("-" * 45)
    for day in detailed:
        print(f"Day {day['day']} ({day['theme']}): {day['morning']} | {day['afternoon']} | {day['evening']}")
    return detailed


def calculate_rooms(travellers, people_per_room=2):
    if travellers <= 0 or people_per_room <= 0:
        raise ValueError("Travellers and people per room must be positive.")
    rooms = math.ceil(travellers / people_per_room)
    print("\nACCOMMODATION PLANNER")
    print("-" * 30)
    print(f"Number of travellers: {travellers}")
    print(f"People per room: {people_per_room}")
    print(f"Rooms required: {rooms}")
    return rooms


def estimate_trip_expenses(
    destination,
    days,
    travellers,
    people_per_room=2,
    country="India",
    user_budget=None,
    starting_location="Malappuram, Kerala"
):
    if days <= 0 or travellers <= 0 or people_per_room <= 0:
        raise ValueError("Days, travellers, and room capacity must be positive.")
    real_plan = calculate_real_trip_budget(
        destination=destination,
        country=country,
        days=days,
        travellers=travellers,
        starting_location=starting_location,
    )
    estimated_total = real_plan["estimated_total_cost"]
    print(f"\nREALISTIC ESTIMATED TRIP COST FOR {destination.upper()}, {country.upper()}")
    print("=" * 55)
    for item in real_plan["items"]:
        print(f"{item['Category']} ({item['Expense']}): Rs{item['Estimated amount (INR)']:,.0f}")
    print("-" * 55)
    print(f"Estimated Total: Rs{estimated_total:,.0f}")
    print(f"Per Person: Rs{real_plan['cost_per_person']:,.0f}")
    print(f"Per Person Per Day: Rs{real_plan['cost_per_person_day']:,.0f}")
    print("=" * 55)
    if user_budget is not None and user_budget > 0:
        feasibility = analyze_budget_feasibility(user_budget, real_plan)
        print(f"\nBUDGET FEASIBILITY ANALYSIS:")
        print(f"Status: {feasibility['badge_label']}")
        print(f"{feasibility['headline']}")
        print(f"{feasibility['summary']}")
        print("=" * 55)
    return estimated_total


def main():
    print("SMART TRAVEL PLANNER")
    destination = input("Enter your destination (e.g. Tokyo, Goa): ").strip()
    country = input("Enter country (e.g. Japan, India): ").strip() or "India"
    try:
        budget = float(input("Enter your total budget (INR): "))
        days = int(input("Enter the number of travel days: "))
        travellers = int(input("Enter the number of travellers: "))
    except ValueError:
        print("Please enter valid numbers.")
        return
    if not destination or budget <= 0 or days <= 0 or travellers <= 0:
        print("Please enter valid trip details.")
        return
    create_budget_breakdown(budget, days, travellers, destination=destination, country=country)
    itinerary = create_detailed_itinerary(destination, days)
    print(f"\n{days}-DAY ITINERARY FOR {destination.upper()}")
    for day in itinerary:
        print(f"\nDay {day['day']} — {day['theme']}")
        print(f"  Morning:   {day['morning']}")
        print(f"  Afternoon: {day['afternoon']}")
        print(f"  Evening:   {day['evening']}")
        print(f"  Food Tip:  {day['food_tip']}")


if __name__ == "__main__":
    main()
