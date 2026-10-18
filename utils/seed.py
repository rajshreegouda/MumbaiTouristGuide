"""Starter data. Everything can be edited / deleted from the Admin panel.
Coordinates are approximate. Hotel / cafe prices are indicative only - verify before travelling."""

WL, CL, NM = "Western Line", "Central Line", "Navi Mumbai"
REGIONS = [WL, CL, NM]
CATEGORIES = ["Heritage", "Beach", "Religious", "Nature", "Museum", "Park", "Viewpoint", "Landmark"]


def yt(q):
    return "https://www.youtube.com/results?search_query=" + q.replace(" ", "+")


def P(name, region, area, station, cat, desc, dos, donts, best, fee, lat, lon, wiki):
    return dict(name=name, region=region, area=area, station=station, category=cat, description=desc,
                dos="\n".join(dos), donts="\n".join(donts), best_time=best, entry_fee=fee, lat=lat, lon=lon,
                wiki_title=wiki, image="", youtube=yt(name + " Mumbai vlog"))


PLACES = [
    # ---------------- WESTERN LINE ----------------
    P("Marine Drive", WL, "Churchgate / Nariman Point", "Churchgate", "Viewpoint",
      "A 3.6 km curved boulevard along the Arabian Sea, nicknamed the Queen's Necklace for its glittering streetlights at night. Locals come for sunsets, chai and sea breeze.",
      ["Visit around sunset and stay for the night lights", "Walk on the promenade and try roadside chai or bhel", "Keep valuables in a zipped bag"],
      ["Don't sit on the sea-facing rocks at high tide or during monsoon", "Don't litter on the promenade", "Don't swim - the water is rough and unsafe"],
      "October to March, evenings", "Free", 18.9440, 72.8230, "Marine Drive, Mumbai"),
    P("Gateway of India", WL, "Colaba", "Churchgate (taxi 10 min)", "Heritage",
      "An arch-monument on the Mumbai waterfront built in the early 20th century. It is the departure point for ferries to Elephanta Caves and sits opposite the Taj Mahal Palace hotel.",
      ["Go early morning for fewer crowds and better photos", "Book Elephanta ferry tickets only from official counters", "Explore nearby Colaba Causeway for shopping"],
      ["Don't trust unofficial photographers or touts who quote high prices", "Don't feed the pigeons in large amounts", "Don't leave bags unattended"],
      "November to February", "Free", 18.9220, 72.8347, "Gateway of India"),
    P("Haji Ali Dargah", WL, "Worli / Mahalaxmi", "Mahalaxmi", "Religious",
      "A mosque and tomb of Sufi saint Pir Haji Ali Shah Bukhari, set on an islet about 500 m off the coast and reached by a causeway that is submerged at high tide.",
      ["Check tide timings before walking the causeway", "Dress modestly and cover your head inside", "Remove footwear before entering"],
      ["Don't walk the causeway at high tide", "Don't photograph inside the prayer areas", "Don't wear shorts or sleeveless clothing"],
      "Early morning or evening; Thursdays and Fridays are very crowded", "Free", 18.9827, 72.8089, "Haji Ali Dargah"),
    P("Siddhivinayak Temple", WL, "Prabhadevi", "Dadar / Prabhadevi", "Religious",
      "One of Mumbai's best-known temples, dedicated to Lord Ganesha. It is especially busy on Tuesdays and during Ganesh Chaturthi.",
      ["Book darshan slots online if available", "Dress modestly", "Carry only a small bag"],
      ["Don't carry large bags, they may not be allowed in", "Don't take photos inside the sanctum", "Avoid Tuesdays if you dislike long queues"],
      "Weekdays, early morning", "Free", 19.0169, 72.8300, "Siddhivinayak Temple, Mumbai"),
    P("Bandra Fort (Castella de Aguada)", WL, "Bandstand, Bandra West", "Bandra", "Heritage",
      "A small Portuguese fort from 1640 overlooking Mahim Bay and the Bandra-Worli Sea Link. Popular for sunset views, film shoots and quiet seaside walks.",
      ["Come at sunset for the Sea Link view", "Wear comfortable shoes for the stone steps", "Combine with a Bandstand promenade walk"],
      ["Don't climb on crumbling walls", "Don't leave litter", "Don't visit alone after dark"],
      "Evenings, October to February", "Free", 19.0426, 72.8186, "Bandra Fort"),
    P("Juhu Beach", WL, "Juhu", "Vile Parle / Andheri (auto 15 min)", "Beach",
      "Mumbai's most famous beach, known for street food such as pav bhaji, bhel and golas, and for celebrity-spotting in the neighbourhood.",
      ["Try street food from busy, clean-looking stalls", "Visit at sunset", "Keep phone and wallet secure"],
      ["Don't swim - strong currents and pollution", "Don't drink untreated water or ice", "Don't leave belongings unattended"],
      "Evenings, November to February", "Free", 19.0988, 72.8265, "Juhu Beach"),
    P("Sanjay Gandhi National Park", WL, "Borivali East", "Borivali", "Nature",
      "A large forest national park inside the city with leopards, deer, butterflies, nature trails, a lion safari and a lake. A rare green lung for a metropolis.",
      ["Wear trekking shoes and carry water", "Go early morning for birds and cooler weather", "Follow forest-department safari rules"],
      ["Don't feed or tease animals", "Don't carry plastic bags or loud speakers", "Don't wander off marked trails"],
      "June to September (green) or October to February (pleasant)", "Ticketed - check at the gate", 19.2147, 72.9106, "Sanjay Gandhi National Park"),
    P("Kanheri Caves", WL, "Inside Sanjay Gandhi National Park", "Borivali", "Heritage",
      "More than 100 rock-cut Buddhist caves dating from about the 1st century BCE to the 10th century CE, set in forest within the national park.",
      ["Start early - it is a walk/hike between caves", "Carry water and snacks", "Hire an official guide for context"],
      ["Don't carve or write on the cave walls", "Don't litter", "Don't visit during heavy rain - paths are slippery"],
      "July to February", "Ticketed - check at the gate", 19.2058, 72.9066, "Kanheri Caves"),
    P("Global Vipassana Pagoda", WL, "Gorai", "Borivali (then ferry / bus)", "Religious",
      "A huge meditation hall with a golden dome near Gorai Creek, built to promote Vipassana meditation. Visitors can walk around the exterior and the peaceful grounds.",
      ["Keep silence in the meditation area", "Combine with a Gorai beach visit", "Check ferry timings in advance"],
      ["Don't speak loudly or play music", "Don't enter meditation cells without permission", "Don't wear revealing clothes"],
      "Morning, October to March", "Free to visit exterior", 19.2310, 72.8060, "Global Vipassana Pagoda"),

    # ---------------- CENTRAL LINE ----------------
    P("Chhatrapati Shivaji Maharaj Terminus (CSMT)", CL, "Fort", "CSMT", "Heritage",
      "A UNESCO World Heritage railway station in Victorian Gothic Revival style, completed in 1888 and still one of the busiest stations in the world.",
      ["Look up at the central dome and facade from across the road", "Visit early morning or late evening for photos", "Walk to nearby Fort heritage buildings"],
      ["Don't photograph railway staff or restricted areas", "Don't visit in peak rush hour with heavy luggage", "Don't buy tickets from touts"],
      "Morning or night", "Free (exterior)", 18.9398, 72.8355, "Chhatrapati Shivaji Maharaj Terminus"),
    P("Elephanta Caves", CL, "Elephanta Island", "CSMT (then Gateway ferry)", "Heritage",
      "A UNESCO World Heritage cave complex on an island in Mumbai Harbour with 6th-century rock-cut Shiva temples, including the famous Trimurti sculpture.",
      ["Take the first ferries of the day", "Carry water and a hat", "Check the ferry is not closed in monsoon"],
      ["Don't feed the monkeys", "Don't touch the carvings", "Don't miss the last return ferry"],
      "October to March (ferries pause in monsoon)", "Ferry + ticket - check on site", 18.9633, 72.9315, "Elephanta Caves"),
    P("Dr. Bhau Daji Lad Museum", CL, "Byculla", "Byculla", "Museum",
      "Mumbai's oldest museum, restored to its Victorian glory, showing the city's history, decorative arts, models and rare prints.",
      ["Allow 1.5 to 2 hours", "Check for special exhibitions", "Pair with a visit to the zoo next door"],
      ["Don't use flash photography", "Don't touch the exhibits", "Don't visit on days it is closed - check timings"],
      "Weekday mornings", "Ticketed - check at counter", 18.9792, 72.8328, "Bhau Daji Lad Museum"),
    P("Byculla Zoo (Rani Baug)", CL, "Byculla", "Byculla", "Park",
      "A heritage botanical garden and zoo with penguins, birds, big cats and old trees, popular with families.",
      ["Go early to see animals active", "Carry water and sun protection", "Visit with children - it's family friendly"],
      ["Don't feed the animals", "Don't tap on enclosures", "Don't litter"],
      "October to February, mornings", "Ticketed - check at gate", 18.9790, 72.8354, "Veermata Jijabai Bhosale Udyan"),
    P("Shivaji Park", CL, "Dadar", "Dadar", "Park",
      "A huge open ground in Dadar famous for cricket, with the sea-facing Shivaji Park beach (Dadar Chowpatty) nearby and plenty of Mumbai street food nearby.",
      ["Visit in the morning to watch cricket practice", "Try vada pav nearby", "Walk to Dadar Chowpatty"],
      ["Don't wander into practice nets", "Don't litter", "Don't swim at the nearby beach"],
      "Mornings and evenings", "Free", 19.0270, 72.8379, "Shivaji Park"),
    P("Powai Lake", CL, "Powai", "Kanjurmarg / Vikhroli (auto 15 min)", "Nature",
      "A scenic artificial lake surrounded by hills and towers, popular for sunsets and as a quiet spot in the city. Crocodiles are present - keep your distance.",
      ["Go for the sunset walk on the promenade", "Carry a camera or binoculars for birds", "Respect rules for the Hiranandani area"],
      ["Don't enter the water", "Don't feed wildlife", "Don't litter"],
      "Late afternoon to evening", "Free", 19.1273, 72.9060, "Powai Lake"),
    P("Upvan Lake", CL, "Thane", "Thane (auto 15 min)", "Nature",
      "A lakeside park at the foot of Yeoor Hills in Thane, known for its evening promenade, ponies and scenic backdrop. A local favourite for quick weekend breaks.",
      ["Visit in the evening", "Combine with Yeoor Hills for a short trek", "Carry water"],
      ["Don't litter or throw things into the lake", "Don't swim", "Don't stay after closing time"],
      "Evenings, October to February", "Free / check local rules", 19.2143, 72.9783, "Upvan Lake"),

    # ---------------- NAVI MUMBAI ----------------
    P("Karnala Bird Sanctuary", NM, "Panvel", "Panvel (taxi 30 min)", "Nature",
      "A forest sanctuary with 150+ bird species and the historic Karnala Fort perched on a pinnacle. Good for birders and light trekkers.",
      ["Start early, carry water and snacks", "Wear trekking shoes and use binoculars", "Hire a guide for bird spotting"],
      ["Don't feed or disturb birds", "Don't make loud noise", "Don't litter"],
      "October to March", "Ticketed - check at gate", 18.8886, 73.1193, "Karnala Bird Sanctuary"),
    P("Pandavkada Waterfalls", NM, "Kharghar", "Kharghar", "Nature",
      "A seasonal waterfall in the Kharghar hills, a popular monsoon picnic spot with a trek through greenery.",
      ["Go on weekdays - weekends are crowded", "Wear shoes with grip", "Carry a waterproof bag"],
      ["Don't enter during heavy rain or flood warnings", "Don't litter", "Don't carry alcohol"],
      "July to September", "Free (check local entry rules)", 19.0453, 73.0795, "Pandavkada Falls"),
    P("Belapur Fort", NM, "CBD Belapur", "CBD Belapur", "Heritage",
      "A small Portuguese-era fort with views of Thane Creek and the Palm Beach Road skyline, a quiet heritage stop in Navi Mumbai.",
      ["Visit in the evening for views", "Carry water", "Explore the nearby CBD Belapur promenade"],
      ["Don't climb on loose walls", "Don't litter", "Don't visit alone after dark"],
      "Evenings, October to February", "Free", 19.0207, 73.0390, "Belapur Fort"),
    P("Central Park, Kharghar", NM, "Kharghar", "Kharghar", "Park",
      "A large landscaped park near the Kharghar golf course and hills, ideal for walks, cycling and picnics.",
      ["Come early morning or evening", "Carry water", "Walk or cycle on the designated paths"],
      ["Don't litter", "Don't pluck flowers or plants", "Don't bring pets where banned"],
      "Mornings and evenings", "Free", 19.0434, 73.0668, "Central Park, Kharghar"),
    P("Wonders Park", NM, "Nerul", "Nerul", "Park",
      "A themed park in Nerul with miniature models of the Seven Wonders of the World, a children's play area and gardens.",
      ["Visit in the evening", "Take kids for the play area", "Check timings before going"],
      ["Don't touch the models", "Don't litter", "Don't bring outside food if disallowed"],
      "Evenings, October to February", "Ticketed - check at counter", 19.0166, 73.0145, "Wonders Park"),
]


def H(name, region, area, stars, price, lat, lon, phone, desc):
    return dict(name=name, region=region, area=area, stars=stars, price_per_night=price, lat=lat, lon=lon,
                phone=phone, description=desc)


HOTELS = [
    H("The Taj Mahal Palace", WL, "Colaba", 5, "Luxury (Rs 25,000+)", 18.9217, 72.8332, "", "Iconic heritage hotel facing the Gateway of India."),
    H("The Oberoi, Mumbai", WL, "Nariman Point", 5, "Luxury (Rs 20,000+)", 18.9272, 72.8209, "", "Sea-facing luxury hotel near Marine Drive."),
    H("Trident Nariman Point", WL, "Nariman Point", 5, "Premium (Rs 12,000+)", 18.9266, 72.8218, "", "Business and leisure hotel on the Marine Drive curve."),
    H("Sofitel Mumbai BKC", WL, "Bandra Kurla Complex", 5, "Premium (Rs 12,000+)", 19.0664, 72.8686, "", "Modern hotel in the business district."),
    H("JW Marriott Mumbai Juhu", WL, "Juhu", 5, "Premium (Rs 12,000+)", 19.1001, 72.8266, "", "Beachside hotel near Juhu Beach."),
    H("Lemon Tree Premier, Andheri", WL, "Andheri East", 4, "Mid-range (Rs 6,000+)", 19.1136, 72.8697, "", "Reliable mid-range stay near the airport and metro."),
    H("ITC Grand Central", CL, "Parel", 5, "Premium (Rs 12,000+)", 19.0010, 72.8409, "", "Luxury hotel in central Mumbai near Parel station."),
    H("Renaissance Mumbai Convention Centre", CL, "Powai", 5, "Premium (Rs 10,000+)", 19.1269, 72.9049, "", "Lakeside hotel overlooking Powai Lake."),
    H("Hotel Fariyas, Colaba", CL, "Colaba / Fort", 3, "Budget (Rs 4,000+)", 18.9225, 72.8315, "", "Budget stay close to South Mumbai sights."),
    H("Four Points by Sheraton, Vashi", NM, "Vashi", 4, "Mid-range (Rs 6,000+)", 19.0771, 72.9988, "", "Comfortable hotel near Vashi station."),
    H("Radisson Blu, Belapur", NM, "CBD Belapur", 4, "Mid-range (Rs 6,000+)", 19.0211, 73.0384, "", "Mid-range hotel convenient for Belapur and Kharghar."),
    H("Ramada Navi Mumbai", NM, "Vashi", 4, "Mid-range (Rs 5,000+)", 19.0746, 73.0001, "", "Hotel near Vashi and the Palm Beach Road corridor."),
]


def C(name, region, area, spec, price, lat, lon, desc):
    return dict(name=name, region=region, area=area, speciality=spec, price_for_two=price, lat=lat, lon=lon,
                description=desc)


CAFES = [
    C("Leopold Cafe", WL, "Colaba", "Continental, beer, desserts", "Rs 1,200", 18.9226, 72.8319, "A Colaba institution since 1871."),
    C("Cafe Mondegar", WL, "Colaba", "Jukebox, burgers, beer", "Rs 1,000", 18.9234, 72.8317, "Quirky cafe famous for its jukebox and murals."),
    C("Kyani & Co.", WL, "Marine Lines", "Irani chai, bun maska, mawa cake", "Rs 300", 18.9448, 72.8283, "Old Irani cafe with chai and bun maska."),
    C("Candies", WL, "Bandra West", "Sandwiches, cakes, coffee", "Rs 700", 19.0572, 72.8283, "Casual Bandra hangout near Pali Hill."),
    C("Prithvi Cafe", WL, "Juhu", "Irani chai, snacks", "Rs 500", 19.1067, 72.8268, "Theatre cafe beside Prithvi Theatre."),
    C("Britannia & Co.", CL, "Ballard Estate", "Berry pulao, caramel custard", "Rs 800", 18.9371, 72.8398, "Historic Parsi restaurant in Fort."),
    C("Cafe Madras", CL, "Matunga", "South Indian breakfast, filter coffee", "Rs 250", 19.0272, 72.8567, "Classic Matunga idli-dosa cafe."),
    C("Cafe Good Luck", CL, "Powai / Hiranandani", "Coffee and breakfast", "Rs 600", 19.1176, 72.9060, "Casual cafe near Powai."),
    C("Theobroma, Vashi", NM, "Vashi", "Bakery, brownies, cakes", "Rs 500", 19.0769, 72.9985, "Popular dessert cafe."),
    C("Cafe Coffee Day, Kharghar", NM, "Kharghar", "Coffee, snacks", "Rs 400", 19.0435, 73.0670, "A convenient stop near Central Park."),
]
