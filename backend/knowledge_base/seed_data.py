# ============================================================
# স্মার্ট কৃষি সহকারী — Bengali Agricultural Knowledge Base
# 30+ entries covering diseases, fertilizers, weather, crops
# ============================================================

KNOWLEDGE_ENTRIES = [

    # ===================== ধানের রোগ (Rice Diseases) =====================

    {
        "category": "রোগ",
        "crop": "ধান",
        "title_bn": "ধানের ব্লাস্ট রোগ",
        "title_en": "Rice Blast Disease",
        "content_bn": (
            "ধানের ব্লাস্ট রোগ Magnaporthe oryzae ছত্রাক দ্বারা হয়। পাতায় "
            "ধূসর কেন্দ্র ও বাদামী কিনারাসহ ডিম্বাকৃতি দাগ দেখা যায়। "
            "মাঝারি তাপমাত্রা (২৫-২৮°C) ও উচ্চ আর্দ্রতায় রোগ দ্রুত ছড়ায়। "
            "চিকিৎসা: ট্রাইসাইক্লাজোল ০.১% হারে স্প্রে করুন। "
            "প্রতিরোধ: ব্লাস্ট-প্রতিরোধী জাত (BR11, BRRI dhan29) ব্যবহার করুন। "
            "অতিরিক্ত নাইট্রোজেন সার পরিহার করুন।"
        ),
        "content_en": (
            "Rice blast caused by Magnaporthe oryzae fungus. Oval spots with "
            "gray center and brown border appear on leaves. Spreads rapidly at "
            "25-28°C with high humidity. Treatment: Spray Tricyclazole 0.1%. "
            "Prevention: Use blast-resistant varieties (BR11, BRRI dhan29). "
            "Avoid excess nitrogen fertilizer."
        ),
        "keywords": ["ব্লাস্ট", "blast", "ধান", "rice", "ছত্রাক", "দাগ", "ট্রাইসাইক্লাজোল"],
    },
    {
        "category": "রোগ",
        "crop": "ধান",
        "title_bn": "ধানের বাদামী দাগ রোগ",
        "title_en": "Rice Brown Spot Disease",
        "content_bn": (
            "Bipolaris oryzae ছত্রাক দ্বারা সৃষ্ট। পাতায় গোলাকার বাদামী দাগ, "
            "মাঝে সাদা কেন্দ্র। জমিতে পটাশিয়াম ও ফসফরাসের অভাবে রোগ বাড়ে। "
            "চিকিৎসা: ম্যানকোজেব ০.২% বা কার্বেন্ডাজিম স্প্রে করুন। "
            "প্রতিরোধ: সুষম সার ব্যবহার, বিশেষত পটাশ সার দিন।"
        ),
        "content_en": (
            "Caused by Bipolaris oryzae fungus. Round brown spots with white "
            "center on leaves. Worsens with potassium and phosphorus deficiency. "
            "Treatment: Spray Mancozeb 0.2% or Carbendazim. "
            "Prevention: Balanced fertilization, especially potash."
        ),
        "keywords": ["বাদামী দাগ", "brown spot", "ধান", "ম্যানকোজেব", "পটাশ"],
    },
    {
        "category": "রোগ",
        "crop": "ধান",
        "title_bn": "ধানের শীষ পচা / বাকানি রোগ",
        "title_en": "Rice Bakanae / Foot Rot Disease",
        "content_bn": (
            "Fusarium fujikuroi ছত্রাক দ্বারা হয়। আক্রান্ত চারা অস্বাভাবিক লম্বা, "
            "হলুদ ও দুর্বল হয়ে পড়ে। বীজের মাধ্যমে ছড়ায়। "
            "চিকিৎসা: থিরাম বা ক্যাপটান দিয়ে বীজ শোধন করুন (৩ গ্রাম/কেজি বীজ)। "
            "আক্রান্ত গাছ তুলে পুড়িয়ে ফেলুন।"
        ),
        "content_en": (
            "Caused by Fusarium fujikuroi. Infected seedlings grow abnormally tall, "
            "yellow and weak. Spreads through seeds. "
            "Treatment: Seed treatment with Thiram or Captan (3g/kg seed). "
            "Remove and burn infected plants."
        ),
        "keywords": ["বাকানি", "শীষ পচা", "bakanae", "foot rot", "ধান", "বীজ শোধন"],
    },
    {
        "category": "রোগ",
        "crop": "ধান",
        "title_bn": "ধানের টুংরো ভাইরাস রোগ",
        "title_en": "Rice Tungro Virus Disease",
        "content_bn": (
            "Rice Tungro Virus গ্রিন লিফহপার পোকার মাধ্যমে ছড়ায়। "
            "পাতা হলুদ-কমলা রঙ ধারণ করে, গাছ বামন হয়ে যায়। "
            "কোনো সরাসরি ওষুধ নেই। "
            "নিয়ন্ত্রণ: কার্বোফুরান বা ইমিডাক্লোপ্রিড দিয়ে পোকা মারুন। "
            "প্রতিরোধী জাত BRRI dhan27 ব্যবহার করুন।"
        ),
        "content_en": (
            "Rice Tungro Virus spread by green leafhopper insects. "
            "Leaves turn yellow-orange, plants become stunted. "
            "No direct cure. Control: Kill insects with Carbofuran or Imidacloprid. "
            "Use resistant variety BRRI dhan27."
        ),
        "keywords": ["টুংরো", "tungro", "ভাইরাস", "হলুদ", "গ্রিন লিফহপার", "ধান"],
    },
    {
        "category": "রোগ",
        "crop": "ধান",
        "title_bn": "ধানের মাজরা পোকা",
        "title_en": "Rice Stem Borer",
        "content_bn": (
            "মাজরা পোকার লার্ভা কাণ্ডের ভেতরে খায়। চারা অবস্থায় 'ডেড হার্ট' "
            "এবং থোড় অবস্থায় 'হোয়াইট ইয়ার' তৈরি করে। "
            "নিয়ন্ত্রণ: কার্বোফুরান ৩জি (১০ কেজি/বিঘা) জমিতে ছড়িয়ে দিন। "
            "ক্লোরপাইরিফস স্প্রে করুন। পোকার ডিমের গাদা সংগ্রহ করে নষ্ট করুন।"
        ),
        "content_en": (
            "Stem borer larvae feed inside the stem. Causes 'Dead Heart' at "
            "seedling stage and 'White Ear' at panicle stage. "
            "Control: Apply Carbofuran 3G (10kg/bigha). Spray Chlorpyrifos. "
            "Collect and destroy egg masses."
        ),
        "keywords": ["মাজরা", "stem borer", "ধান", "কার্বোফুরান", "ডেড হার্ট", "পোকা"],
    },

    # ===================== গমের রোগ (Wheat Diseases) =====================

    {
        "category": "রোগ",
        "crop": "গম",
        "title_bn": "গমের মরিচা রোগ",
        "title_en": "Wheat Rust Disease",
        "content_bn": (
            "Puccinia ছত্রাক দ্বারা হয়। পাতায় ও কাণ্ডে মরিচার মতো লাল-বাদামী "
            "গুঁড়ো দেখা যায়। ঠান্ডা ও আর্দ্র আবহাওয়ায় দ্রুত ছড়ায়। "
            "চিকিৎসা: প্রপিকোনাজোল ০.১% হারে স্প্রে করুন। "
            "প্রতিরোধী জাত BARI Gom-26, BARI Gom-28 ব্যবহার করুন।"
        ),
        "content_en": (
            "Caused by Puccinia fungus. Reddish-brown rust-like powder on leaves "
            "and stem. Spreads fast in cool humid weather. "
            "Treatment: Spray Propiconazole 0.1%. "
            "Use resistant varieties BARI Gom-26, BARI Gom-28."
        ),
        "keywords": ["মরিচা", "rust", "গম", "wheat", "প্রপিকোনাজোল", "ছত্রাক"],
    },
    {
        "category": "রোগ",
        "crop": "গম",
        "title_bn": "গমের ব্লাইট রোগ",
        "title_en": "Wheat Blight / Scab",
        "content_bn": (
            "Fusarium graminearum দ্বারা সৃষ্ট। শীষ সাদা হয়ে মারা যায়। "
            "উষ্ণ ও আর্দ্র আবহাওয়ায় ফুল ফোটার সময় আক্রমণ করে। "
            "চিকিৎসা: টেবুকোনাজোল বা প্রোথিওকোনাজোল স্প্রে করুন। "
            "দানায় বিষক্রিয়া (মাইকোটক্সিন) হতে পারে।"
        ),
        "content_en": (
            "Caused by Fusarium graminearum. Spikes turn white and die. "
            "Attacks during flowering in warm humid conditions. "
            "Treatment: Spray Tebuconazole or Prothioconazole. "
            "Grain may contain mycotoxins."
        ),
        "keywords": ["ব্লাইট", "scab", "গম", "শীষ", "Fusarium", "টেবুকোনাজোল"],
    },

    # ===================== সার পরামর্শ (Fertilizer Advice) =====================

    {
        "category": "সার",
        "crop": "ধান",
        "title_bn": "বোরো ধানের সার সুপারিশ",
        "title_en": "Boro Rice Fertilizer Recommendation",
        "content_bn": (
            "বোরো ধানে প্রতি বিঘায়: ইউরিয়া ২৫-৩০ কেজি (৩ ভাগে), "
            "টিএসপি ১৫-১৮ কেজি, এমওপি ১২-১৫ কেজি, জিপসাম ১০ কেজি। "
            "ইউরিয়া: রোপণের ১০ দিন পর (১/৩), কুশি মারার সময় (১/৩), "
            "থোড় আসার আগে (১/৩)। "
            "জমি তৈরির সময় টিএসপি, এমওপি, জিপসাম একসাথে দিন।"
        ),
        "content_en": (
            "Boro rice per bigha: Urea 25-30 kg (3 splits), TSP 15-18 kg, "
            "MOP 12-15 kg, Gypsum 10 kg. "
            "Urea: 10 days after planting (1/3), at tillering (1/3), "
            "before panicle initiation (1/3). "
            "Apply TSP, MOP, Gypsum at land preparation."
        ),
        "keywords": ["বোরো", "ধান", "সার", "ইউরিয়া", "টিএসপি", "এমওপি", "জিপসাম"],
    },
    {
        "category": "সার",
        "crop": "ধান",
        "title_bn": "আমন ধানের সার সুপারিশ",
        "title_en": "Aman Rice Fertilizer Recommendation",
        "content_bn": (
            "আমন ধানে প্রতি বিঘায়: ইউরিয়া ১৮-২২ কেজি, "
            "টিএসপি ১০-১২ কেজি, এমওপি ৮-১০ কেজি। "
            "বৃষ্টিপাত বেশি হলে ইউরিয়া দুই ভাগে দিন। "
            "জৈব সার (গোবর ১ টন/বিঘা) জমি তৈরিতে মেশালে রাসায়নিক কমানো যায়।"
        ),
        "content_en": (
            "Aman rice per bigha: Urea 18-22 kg, TSP 10-12 kg, MOP 8-10 kg. "
            "In heavy rain areas, split urea in two doses. "
            "Adding organic manure (1 ton compost/bigha) reduces chemical needs."
        ),
        "keywords": ["আমন", "ধান", "সার", "ইউরিয়া", "জৈব", "এমওপি"],
    },
    {
        "category": "সার",
        "crop": "গম",
        "title_bn": "গমের সার সুপারিশ",
        "title_en": "Wheat Fertilizer Recommendation",
        "content_bn": (
            "গমে প্রতি বিঘায়: ইউরিয়া ২০-২৫ কেজি, টিএসপি ১৫ কেজি, "
            "এমওপি ১০ কেজি, জিপসাম ৮ কেজি। "
            "বীজ বোনার আগে সব সার ছড়িয়ে মিশিয়ে দিন। "
            "ইউরিয়া অর্ধেক বপনের সময়, বাকি অর্ধেক ৩০-৩৫ দিন পর দিন।"
        ),
        "content_en": (
            "Wheat per bigha: Urea 20-25 kg, TSP 15 kg, MOP 10 kg, Gypsum 8 kg. "
            "Mix all basal fertilizers before sowing. "
            "Half urea at sowing, rest at 30-35 days."
        ),
        "keywords": ["গম", "wheat", "সার", "ইউরিয়া", "টিএসপি", "বপন"],
    },
    {
        "category": "সার",
        "crop": "পাট",
        "title_bn": "পাটের সার সুপারিশ",
        "title_en": "Jute Fertilizer Recommendation",
        "content_bn": (
            "পাটে প্রতি বিঘায়: ইউরিয়া ২০ কেজি, টিএসপি ১০ কেজি, "
            "এমওপি ৮ কেজি। বপনের আগে ভিত্তি সার দিন। "
            "ইউরিয়া দুই ভাগে: বপনের ১৫ দিন পর ও ৪৫ দিন পর। "
            "জমিতে সবুজ সার (ধইঞ্চা) আগে চাষ করলে ইউরিয়া কমানো যায়।"
        ),
        "content_en": (
            "Jute per bigha: Urea 20 kg, TSP 10 kg, MOP 8 kg. "
            "Apply basal dose before sowing. "
            "Urea in two splits: 15 days and 45 days after sowing. "
            "Green manure (Dhaincha) reduces urea requirement."
        ),
        "keywords": ["পাট", "jute", "সার", "ইউরিয়া", "ধইঞ্চা", "সবুজ সার"],
    },
    {
        "category": "সার",
        "crop": "সবজি",
        "title_bn": "সবজি চাষে সার ব্যবস্থাপনা",
        "title_en": "Vegetable Fertilizer Management",
        "content_bn": (
            "সাধারণ সবজিতে প্রতি শতকে: গোবর ৪০-৫০ কেজি, "
            "ইউরিয়া ৩০০-৪০০ গ্রাম, টিএসপি ২৫০-৩০০ গ্রাম, "
            "এমওপি ২০০-২৫০ গ্রাম। "
            "পচা গোবর সার মাটির স্বাস্থ্য ভালো রাখে। "
            "ফুলকপি, বাঁধাকপিতে বোরন সার (১০ গ্রাম/শতক) দিন।"
        ),
        "content_en": (
            "General vegetables per decimal: Compost 40-50 kg, "
            "Urea 300-400 g, TSP 250-300 g, MOP 200-250 g. "
            "Rotted compost improves soil health. "
            "Apply Boron (10g/decimal) for cauliflower and cabbage."
        ),
        "keywords": ["সবজি", "vegetable", "সার", "গোবর", "বোরন", "ফুলকপি"],
    },
    {
        "category": "সার",
        "crop": "ধান",
        "title_bn": "জিংক সারের প্রয়োজনীয়তা",
        "title_en": "Zinc Fertilizer for Rice",
        "content_bn": (
            "বাংলাদেশের অনেক জমিতে জিংকের অভাব আছে। "
            "ধানে জিংকের অভাবে পাতায় সাদা দাগ ও বাদামী ছোপ দেখা যায়। "
            "প্রতি বিঘায় জিংক সালফেট ১-২ কেজি বা ফলিয়ার স্প্রে হিসেবে "
            "০.৫% ZnSO4 দ্রবণ ব্যবহার করুন।"
        ),
        "content_en": (
            "Many Bangladesh soils are zinc deficient. "
            "Zinc deficiency in rice shows white streaks and brown spots. "
            "Apply Zinc Sulfate 1-2 kg/bigha or foliar spray 0.5% ZnSO4 solution."
        ),
        "keywords": ["জিংক", "zinc", "সালফেট", "ধান", "পুষ্টি", "অভাব"],
    },

    # ===================== আবহাওয়া পরামর্শ (Weather Advisory) =====================

    {
        "category": "আবহাওয়া",
        "crop": None,
        "title_bn": "বৃষ্টির সময় কৃষি পরামর্শ",
        "title_en": "Farming Advice During Rain",
        "content_bn": (
            "বৃষ্টির সম্ভাবনা থাকলে কীটনাশক ও ছত্রাকনাশক স্প্রে করবেন না — "
            "ওষুধ ধুয়ে যাবে। সেচ দেওয়ার দরকার নেই। "
            "মাঠে জলাবদ্ধতা হলে নালা কেটে পানি বের করুন। "
            "বৃষ্টির পর রোগের প্রকোপ বাড়তে পারে — গাছ পর্যবেক্ষণ করুন।"
        ),
        "content_en": (
            "Do not spray pesticides or fungicides if rain is expected — "
            "chemicals will wash off. No need for irrigation. "
            "If waterlogging occurs, cut drainage channels. "
            "Monitor crops after rain as disease risk increases."
        ),
        "keywords": ["বৃষ্টি", "rain", "স্প্রে", "জলাবদ্ধতা", "সেচ", "আবহাওয়া"],
    },
    {
        "category": "আবহাওয়া",
        "crop": None,
        "title_bn": "গরম ও খরায় কৃষি পরামর্শ",
        "title_en": "Farming in Hot & Dry Weather",
        "content_bn": (
            "তাপমাত্রা ৩৫°C এর বেশি হলে: সকালে বা সন্ধ্যায় সেচ দিন। "
            "মালচিং করুন (খড় বা কচুরিপানা) — মাটির আর্দ্রতা ধরে রাখবে। "
            "ইউরিয়া সার গরমে দেবেন না — বাষ্প হয়ে যাবে। "
            "খরা সহিষ্ণু জাত ব্যবহার করুন (BRRI dhan56, BINA dhan7)।"
        ),
        "content_en": (
            "When temperature above 35°C: irrigate in morning or evening. "
            "Mulch with straw or water hyacinth to retain soil moisture. "
            "Don't apply urea in extreme heat — it volatilizes. "
            "Use drought-tolerant varieties (BRRI dhan56, BINA dhan7)."
        ),
        "keywords": ["গরম", "খরা", "drought", "সেচ", "মালচিং", "তাপমাত্রা"],
    },
    {
        "category": "আবহাওয়া",
        "crop": None,
        "title_bn": "শীতকালীন কৃষি পরামর্শ",
        "title_en": "Winter Farming Advisory",
        "content_bn": (
            "শীতে ঘাস ও সবজির জন্য সকালের কুয়াশা উপকারী। "
            "তাপমাত্রা ১০°C এর নিচে গেলে চারার ক্ষতি হতে পারে — "
            "পলি শেড বা মাল্ট ব্যবহার করুন। "
            "গমের জন্য শীত আদর্শ (১৫-২০°C)। "
            "শীতকালীন সবজি: ফুলকপি, বাঁধাকপি, টমেটো চাষের উপযুক্ত সময়।"
        ),
        "content_en": (
            "Morning fog in winter benefits grass and vegetables. "
            "Below 10°C can damage seedlings — use poly shed or mulch. "
            "Winter is ideal for wheat (15-20°C). "
            "Best time for winter vegetables: cauliflower, cabbage, tomato."
        ),
        "keywords": ["শীত", "winter", "কুয়াশা", "গম", "সবজি", "তাপমাত্রা"],
    },
    {
        "category": "আবহাওয়া",
        "crop": "ধান",
        "title_bn": "বন্যার পর ধান চাষ",
        "title_en": "Rice Farming After Flood",
        "content_bn": (
            "বন্যার পানি সরে যাওয়ার পর মাটি পরীক্ষা করুন। "
            "পানি জমে ক্ষতিগ্রস্ত ধান তুলে ফেলুন। "
            "বন্যা-সহিষ্ণু জাত: BRRI dhan51, BRRI dhan52 (১৪ দিন পর্যন্ত ডুবে থাকতে পারে)। "
            "পানি নামার পর ১ সপ্তাহ অপেক্ষা করে ইউরিয়া দিন।"
        ),
        "content_en": (
            "Test soil after floodwater recedes. "
            "Remove flood-damaged rice plants. "
            "Flood-tolerant varieties: BRRI dhan51, BRRI dhan52 "
            "(can remain submerged up to 14 days). "
            "Wait 1 week after water recedes before applying urea."
        ),
        "keywords": ["বন্যা", "flood", "ধান", "সহিষ্ণু", "BRRI", "ডুবে"],
    },

    # ===================== ফসল ব্যবস্থাপনা (Crop Management) =====================

    {
        "category": "ফসল",
        "crop": "ধান",
        "title_bn": "ধানের জাত নির্বাচন",
        "title_en": "Rice Variety Selection",
        "content_bn": (
            "বোরো মৌসুম: BRRI dhan28, BRRI dhan29, BRRI dhan58 (উচ্চ ফলন)। "
            "আমন মৌসুম: BRRI dhan49, BRRI dhan52, বিনা ধান-7। "
            "লবণ সহিষ্ণু: BRRI dhan47, BRRI dhan61 (উপকূলীয় এলাকার জন্য)। "
            "সুগন্ধি: BRRI dhan34, BRRI dhan37 (বাজারে ভালো দাম)।"
        ),
        "content_en": (
            "Boro season: BRRI dhan28, dhan29, dhan58 (high yield). "
            "Aman season: BRRI dhan49, dhan52, BINA dhan7. "
            "Salt-tolerant: BRRI dhan47, dhan61 (for coastal areas). "
            "Aromatic: BRRI dhan34, dhan37 (premium market price)."
        ),
        "keywords": ["জাত", "variety", "BRRI", "বোরো", "আমন", "লবণ", "সুগন্ধি"],
    },
    {
        "category": "ফসল",
        "crop": "ধান",
        "title_bn": "ধান রোপণের সঠিক সময়",
        "title_en": "Rice Transplanting Schedule",
        "content_bn": (
            "বোরো: ডিসেম্বর-জানুয়ারিতে বীজতলা, জানুয়ারি-ফেব্রুয়ারিতে রোপণ। "
            "আউশ: এপ্রিল-মে তে বীজ বোনা। "
            "আমন: জুন-জুলাইতে বীজতলা, জুলাই-আগস্টে রোপণ। "
            "চারার বয়স ৩০-৩৫ দিনের মধ্যে রোপণ করুন।"
        ),
        "content_en": (
            "Boro: Seedbed in Dec-Jan, transplant Jan-Feb. "
            "Aus: Sow in April-May. "
            "Aman: Seedbed Jun-Jul, transplant Jul-Aug. "
            "Transplant seedlings within 30-35 days of age."
        ),
        "keywords": ["রোপণ", "বীজতলা", "বোরো", "আমন", "আউশ", "সময়", "মৌসুম"],
    },
    {
        "category": "ফসল",
        "crop": "সবজি",
        "title_bn": "টমেটো চাষ পদ্ধতি",
        "title_en": "Tomato Cultivation Method",
        "content_bn": (
            "অক্টোবর-নভেম্বরে বীজতলা তৈরি করুন। "
            "৩০ দিনের চারা জমিতে ৬০×৪৫ সেমি দূরত্বে লাগান। "
            "সার: গোবর ২ টন, ইউরিয়া ৪০০ গ্রাম, টিএসপি ৩০০ গ্রাম প্রতি শতকে। "
            "রোগ: আর্লি ব্লাইট, লেট ব্লাইট সাবধান — ম্যানকোজেব স্প্রে করুন।"
        ),
        "content_en": (
            "Prepare seedbed in Oct-Nov. "
            "Transplant 30-day seedlings at 60×45 cm spacing. "
            "Fertilizer per decimal: Compost 2 ton, Urea 400g, TSP 300g. "
            "Disease: Watch for early/late blight — spray Mancozeb."
        ),
        "keywords": ["টমেটো", "tomato", "সবজি", "চাষ", "বীজতলা", "ব্লাইট"],
    },
    {
        "category": "ফসল",
        "crop": "সবজি",
        "title_bn": "ফুলকপি ও বাঁধাকপি চাষ",
        "title_en": "Cauliflower and Cabbage Cultivation",
        "content_bn": (
            "সেপ্টেম্বর-অক্টোবরে বীজতলা। ৩০ দিনে চারা রোপণ। "
            "সারি থেকে সারি ৬০ সেমি, গাছ থেকে গাছ ৪৫ সেমি। "
            "বোরন অভাবে ফুলকপির কার্ড কালো হয় — বোরন স্প্রে করুন। "
            "ডায়মন্ডব্যাক মথ পোকায় সাইপারমেথ্রিন ব্যবহার করুন।"
        ),
        "content_en": (
            "Seedbed in Sep-Oct. Transplant at 30 days. "
            "Row spacing 60 cm, plant spacing 45 cm. "
            "Boron deficiency causes black curd — apply Boron spray. "
            "Use Cypermethrin against Diamondback Moth."
        ),
        "keywords": ["ফুলকপি", "বাঁধাকপি", "cauliflower", "cabbage", "বোরন", "সবজি"],
    },
    {
        "category": "ফসল",
        "crop": "পাট",
        "title_bn": "পাট চাষের পদ্ধতি",
        "title_en": "Jute Cultivation Method",
        "content_bn": (
            "মার্চ-এপ্রিলে বীজ বোনা। প্রতি শতকে ৫-৭ গ্রাম বীজ। "
            "দোআঁশ ও পলি মাটিতে ভালো হয়। "
            "৯০-১১০ দিনে ফুল আসার আগে কাটুন। "
            "জাগ দেওয়া: পরিষ্কার পানিতে ১৮-২৫ দিন জাগ দিন।"
        ),
        "content_en": (
            "Sow in March-April. 5-7g seed per decimal. "
            "Does well in loam and alluvial soil. "
            "Harvest before flowering at 90-110 days. "
            "Retting: steep in clean water for 18-25 days."
        ),
        "keywords": ["পাট", "jute", "চাষ", "বীজ", "জাগ", "রেটিং"],
    },
    {
        "category": "ফসল",
        "crop": "ফল",
        "title_bn": "আম গাছের পরিচর্যা",
        "title_en": "Mango Tree Care",
        "content_bn": (
            "ফেব্রুয়ারি-মার্চে মুকুল আসে — এ সময় সেচ দেবেন না। "
            "পাউডারি মিলডিউ হলে সালফার স্প্রে করুন। "
            "ম্যাঙ্গো হপার পোকায় ইমিডাক্লোপ্রিড ব্যবহার করুন। "
            "ফল ঝরা কমাতে NAA (ন্যাপথালিন অ্যাসিটিক অ্যাসিড) স্প্রে করুন।"
        ),
        "content_en": (
            "Mango blooms Feb-Mar — avoid irrigation during this time. "
            "Spray Sulphur for Powdery Mildew. "
            "Use Imidacloprid against Mango Hoppers. "
            "Spray NAA (Naphthalene Acetic Acid) to reduce fruit drop."
        ),
        "keywords": ["আম", "mango", "মুকুল", "পাউডারি মিলডিউ", "হপার", "ফল"],
    },

    # ===================== মাটি ও সেচ (Soil & Irrigation) =====================

    {
        "category": "মাটি",
        "crop": None,
        "title_bn": "মাটি পরীক্ষা ও pH ব্যবস্থাপনা",
        "title_en": "Soil Testing and pH Management",
        "content_bn": (
            "সুস্থ ফসলের জন্য মাটির pH ৬.০-৭.০ আদর্শ। "
            "অম্লীয় মাটিতে (pH < 5.5) চুন দিন — প্রতি বিঘায় ৪০-৫০ কেজি। "
            "ক্ষারীয় মাটিতে (pH > 7.5) জিপসাম বা সালফার দিন। "
            "উপজেলা কৃষি অফিস থেকে বিনামূল্যে মাটি পরীক্ষা করা যায়।"
        ),
        "content_en": (
            "Ideal soil pH for most crops: 6.0-7.0. "
            "For acidic soil (pH < 5.5): apply lime 40-50 kg/bigha. "
            "For alkaline soil (pH > 7.5): apply Gypsum or Sulphur. "
            "Free soil testing available at Upazila Agriculture Office."
        ),
        "keywords": ["মাটি", "soil", "pH", "চুন", "lime", "অম্লীয়", "পরীক্ষা"],
    },
    {
        "category": "সেচ",
        "crop": "ধান",
        "title_bn": "ধানে সঠিক সেচ ব্যবস্থাপনা",
        "title_en": "Irrigation Management for Rice",
        "content_bn": (
            "ধানে ক্রমাগত পানি রাখার দরকার নেই। "
            "AWD (Alternate Wetting and Drying) পদ্ধতি: ৫ সেমি পানি দিন, "
            "মাটি ফেটে গেলে আবার সেচ দিন — ৩০% পানি সাশ্রয়। "
            "ফুল ফোটার সময় (১৫-২০ দিন) জমিতে পানি থাকা জরুরি। "
            "কাটার ১৫ দিন আগে সেচ বন্ধ করুন।"
        ),
        "content_en": (
            "Rice doesn't need continuous flooding. "
            "AWD method: add 5cm water, re-irrigate when soil cracks — saves 30% water. "
            "Water essential during flowering (15-20 days). "
            "Stop irrigation 15 days before harvest."
        ),
        "keywords": ["সেচ", "irrigation", "AWD", "ধান", "পানি", "সাশ্রয়"],
    },
    {
        "category": "সেচ",
        "crop": "সবজি",
        "title_bn": "সবজি বাগানে ড্রিপ সেচ",
        "title_en": "Drip Irrigation for Vegetables",
        "content_bn": (
            "ড্রিপ সেচে ৬০-৭০% পানি সাশ্রয় হয়। "
            "গোড়ায় সরাসরি পানি পড়ায় রোগ কম হয়। "
            "টমেটো, মরিচ, বেগুনে বিশেষ উপকারী। "
            "বাংলাদেশ সরকার ক্ষুদ্র কৃষকদের ভর্তুকিতে ড্রিপ সেচ দিচ্ছে।"
        ),
        "content_en": (
            "Drip irrigation saves 60-70% water. "
            "Direct root watering reduces disease. "
            "Especially beneficial for tomato, chili, brinjal. "
            "Bangladesh government provides subsidized drip irrigation to small farmers."
        ),
        "keywords": ["ড্রিপ", "drip", "সেচ", "পানি", "সবজি", "সাশ্রয়", "ভর্তুকি"],
    },

    # ===================== কীটনাশক ও পোকামাকড় (Pest Management) =====================

    {
        "category": "পোকা",
        "crop": "সবজি",
        "title_bn": "সবজির সাদা মাছি ও থ্রিপস নিয়ন্ত্রণ",
        "title_en": "Whitefly and Thrips Control in Vegetables",
        "content_bn": (
            "সাদা মাছি ভাইরাস রোগ ছড়ায়। নিম তেল (২%) স্প্রে কার্যকর। "
            "হলুদ আঠালো ফাঁদ ব্যবহার করুন। "
            "রাসায়নিক: ইমিডাক্লোপ্রিড বা থায়ামেথোক্সাম স্প্রে করুন। "
            "থ্রিপসে স্পিনোসাড বা ফিপ্রোনিল ব্যবহার করুন।"
        ),
        "content_en": (
            "Whitefly spreads viral diseases. Neem oil (2%) spray is effective. "
            "Use yellow sticky traps. "
            "Chemical: Spray Imidacloprid or Thiamethoxam. "
            "For thrips: use Spinosad or Fipronil."
        ),
        "keywords": ["সাদা মাছি", "whitefly", "থ্রিপস", "thrips", "নিম", "সবজি"],
    },
    {
        "category": "পোকা",
        "crop": None,
        "title_bn": "জৈব বালাই দমন পদ্ধতি",
        "title_en": "Organic Pest Control Methods",
        "content_bn": (
            "নিম তেল ২% স্প্রে: বেশিরভাগ পোকায় কার্যকর, পরিবেশবান্ধব। "
            "ফেরোমন ফাঁদ: মথ ও লেদা পোকা ধরতে ব্যবহার করুন। "
            "আলোর ফাঁদ: রাতে পোকা আকৃষ্ট করে মারা যায়। "
            "উপকারী পোকা (লেডিবার্ড, মাকড়সা) রক্ষা করুন।"
        ),
        "content_en": (
            "Neem oil 2% spray: effective for most pests, eco-friendly. "
            "Pheromone traps: use to catch moths and armyworms. "
            "Light traps: attract and kill nocturnal pests. "
            "Protect beneficial insects (ladybirds, spiders)."
        ),
        "keywords": ["জৈব", "organic", "নিম", "ফেরোমন", "আলো ফাঁদ", "পরিবেশ"],
    },
    {
        "category": "পোকা",
        "crop": "ধান",
        "title_bn": "ধানের বাদামী গাছফড়িং (BPH)",
        "title_en": "Brown Planthopper (BPH) in Rice",
        "content_bn": (
            "BPH ধানের সবচেয়ে বিপজ্জনক পোকা। গাছের গোড়ায় থাকে। "
            "হপারবার্ন: আক্রান্ত অংশ পুড়ে যাওয়ার মতো বাদামী হয়। "
            "নিয়ন্ত্রণ: ইমিডাক্লোপ্রিড বা বুপ্রোফেজিন স্প্রে করুন গোড়ায়। "
            "পানি সরিয়ে ৩-৪ দিন জমি শুকান।"
        ),
        "content_en": (
            "BPH is the most dangerous rice pest. Found at plant base. "
            "Hopperburn: affected area turns brown as if burnt. "
            "Control: Spray Imidacloprid or Buprofezin at base. "
            "Drain water and dry field for 3-4 days."
        ),
        "keywords": ["বাদামী গাছফড়িং", "BPH", "planthopper", "ধান", "হপারবার্ন"],
    },

    # ===================== সংগ্রহোত্তর ব্যবস্থাপনা (Post-harvest) =====================

    {
        "category": "সংগ্রহ",
        "crop": "ধান",
        "title_bn": "ধান কাটা ও মাড়াই",
        "title_en": "Rice Harvesting and Threshing",
        "content_bn": (
            "৮০% শীষ পাকলে কাটুন। আর্দ্রতা ২০-২২% এ কাটা ভালো। "
            "কাটার পর দ্রুত মাড়াই করুন — দেরি করলে অঙ্কুর গজাতে পারে। "
            "রোদে শুকিয়ে আর্দ্রতা ১৪% এ নামান (সংরক্ষণের জন্য)। "
            "যন্ত্র দিয়ে কাটলে শস্যক্ষতি ৫% এর নিচে রাখুন।"
        ),
        "content_en": (
            "Harvest when 80% panicles are ripe. Best at 20-22% moisture. "
            "Thresh quickly after cutting — delays cause sprouting. "
            "Sun-dry to 14% moisture for safe storage. "
            "Mechanical harvesting should keep grain loss below 5%."
        ),
        "keywords": ["কাটা", "harvest", "মাড়াই", "threshing", "আর্দ্রতা", "সংরক্ষণ"],
    },
    {
        "category": "সংগ্রহ",
        "crop": None,
        "title_bn": "ফসল সংরক্ষণ ও গুদামজাত",
        "title_en": "Crop Storage and Warehousing",
        "content_bn": (
            "ধান-গম ১৪% আর্দ্রতার নিচে সংরক্ষণ করুন। "
            "বায়ুরোধী ড্রাম বা হার্মেটিক ব্যাগে রাখুন। "
            "গুদামে ৩ ধরনের পোকা থেকে সাবধান: ধানের ঘুণ, ছাতুপোকা, শুঁটকিপোকা। "
            "ফসফিন ট্যাবলেট দিয়ে গুদাম ফিউমিগেশন করুন।"
        ),
        "content_en": (
            "Store rice/wheat below 14% moisture. "
            "Use airtight drums or hermetic bags. "
            "Watch for 3 storage pests: rice weevil, grain moth, flour beetle. "
            "Fumigate warehouse with Phosphine tablets."
        ),
        "keywords": ["সংরক্ষণ", "storage", "গুদাম", "আর্দ্রতা", "ফিউমিগেশন", "পোকা"],
    },

    # ===================== বিশেষ পরামর্শ (Special Advice) =====================

    {
        "category": "সাধারণ",
        "crop": None,
        "title_bn": "কৃষি ঋণ ও সরকারি সহায়তা",
        "title_en": "Agricultural Loan and Government Support",
        "content_bn": (
            "কৃষি ব্যাংক থেকে ৪% সুদে কৃষি ঋণ পাওয়া যায়। "
            "উপজেলা কৃষি অফিস থেকে বিনামূল্যে বীজ ও সার পাওয়া সম্ভব। "
            "কৃষি কার্ড তৈরি করুন — অনেক সুবিধা পাবেন। "
            "হটলাইন: কৃষি তথ্য সার্ভিস — ১৬১২৩ নম্বরে ফোন করুন।"
        ),
        "content_en": (
            "Agricultural loans available at 4% interest from Krishi Bank. "
            "Free seeds and fertilizer from Upazila Agriculture Office. "
            "Get an Agriculture Card for various benefits. "
            "Hotline: Agriculture Information Service — call 16123."
        ),
        "keywords": ["ঋণ", "loan", "সরকার", "কৃষি ব্যাংক", "বীজ", "সহায়তা", "16123"],
    },
    {
        "category": "সাধারণ",
        "crop": None,
        "title_bn": "কৃষি বীমা",
        "title_en": "Crop Insurance",
        "content_bn": (
            "প্রাকৃতিক দুর্যোগে ফসল নষ্ট হলে কৃষি বীমা থেকে ক্ষতিপূরণ পাবেন। "
            "সদাকত উপজেলা অফিসে বা Sadharan Bima Corporation এ আবেদন করুন। "
            "প্রিমিয়াম কম — সরকার ভর্তুকি দেয়। "
            "আবেদনে জমির পর্চা, খতিয়ান ও জাতীয় পরিচয়পত্র লাগবে।"
        ),
        "content_en": (
            "Get compensation from crop insurance for natural disaster losses. "
            "Apply at Upazila office or Sadharan Bima Corporation. "
            "Low premium — government subsidizes it. "
            "Documents needed: land deed, khatian, and NID."
        ),
        "keywords": ["বীমা", "insurance", "ক্ষতিপূরণ", "দুর্যোগ", "ভর্তুকি"],
    },
    {
        "category": "রোগ",
        "crop": "সবজি",
        "title_bn": "বেগুনের ডগা ও ফল ছিদ্রকারী পোকা",
        "title_en": "Brinjal Shoot and Fruit Borer",
        "content_bn": (
            "Leucinodes orbonalis লার্ভা ডগা ও ফল ছিদ্র করে খায়। "
            "আক্রান্ত ডগা ঝরে পড়ে ও ফল খাওয়ার অযোগ্য হয়। "
            "নিয়ন্ত্রণ: সাইপারমেথ্রিন বা কার্বারিল স্প্রে সন্ধ্যায় করুন। "
            "ফেরোমন ফাঁদ ব্যবহার করুন। আক্রান্ত ডগা কেটে পোড়ান।"
        ),
        "content_en": (
            "Leucinodes orbonalis larvae bore into shoots and fruits. "
            "Infected shoots wilt and fruits become inedible. "
            "Control: Spray Cypermethrin or Carbaryl in evening. "
            "Use pheromone traps. Cut and burn infected shoots."
        ),
        "keywords": ["বেগুন", "brinjal", "ডগা ছিদ্রকারী", "shoot borer", "ফেরোমন"],
    },
    {
        "category": "রোগ",
        "crop": "ফল",
        "title_bn": "পেঁপের মোজাইক ভাইরাস",
        "title_en": "Papaya Mosaic Virus",
        "content_bn": (
            "এফিড পোকার মাধ্যমে ছড়ায়। পাতায় হলুদ-সবুজ মোজাইক দাগ। "
            "ফল ছোট ও বিকৃত হয়। কোনো ওষুধ নেই। "
            "নিয়ন্ত্রণ: আক্রান্ত গাছ তুলে নষ্ট করুন। "
            "এফিড মারতে ইমিডাক্লোপ্রিড স্প্রে করুন। "
            "রোগমুক্ত চারা রোপণ করুন।"
        ),
        "content_en": (
            "Spread by aphids. Yellow-green mosaic patterns on leaves. "
            "Fruits become small and deformed. No cure available. "
            "Control: Uproot and destroy infected plants. "
            "Spray Imidacloprid to kill aphids. "
            "Plant disease-free seedlings."
        ),
        "keywords": ["পেঁপে", "papaya", "মোজাইক", "mosaic", "ভাইরাস", "এফিড"],
    },
]


def get_all_entries():
    """সব knowledge base এন্ট্রি রিটার্ন করে"""
    return KNOWLEDGE_ENTRIES


def get_entries_by_crop(crop: str):
    """নির্দিষ্ট ফসলের এন্ট্রি রিটার্ন করে"""
    return [e for e in KNOWLEDGE_ENTRIES if e.get("crop") == crop or e.get("crop") is None]


def get_entries_by_category(category: str):
    """নির্দিষ্ট ক্যাটাগরির এন্ট্রি রিটার্ন করে"""
    return [e for e in KNOWLEDGE_ENTRIES if e.get("category") == category]


if __name__ == "__main__":
    print(f"✅ মোট এন্ট্রি: {len(KNOWLEDGE_ENTRIES)}")
    cats = {}
    for e in KNOWLEDGE_ENTRIES:
        cats[e["category"]] = cats.get(e["category"], 0) + 1
    for cat, count in cats.items():
        print(f"   {cat}: {count}টি")
