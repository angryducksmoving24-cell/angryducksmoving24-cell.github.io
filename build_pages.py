#!/usr/bin/env python3
"""Build dedicated service + city SEO pages for Angry Ducks Moving."""
import json, os

BASE = "https://angryducksmovingknox.netlify.app"
PHONE = "(865) 936-3891"
PHONE_HREF = "tel:8659363891"

HEAD_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-4EYSTVLZ99"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-4EYSTVLZ99');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#129414;</text></svg>">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{ theme: {{ extend: {{ colors: {{ tactical: {{
            bg: '#0F172A', card: '#1E293B', accent: '#22C55E', accentHover: '#16A34A',
            text: '#F8FAFC', muted: '#94A3B8' }} }} }} }} }};
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script type="application/ld+json">
    {schema}
    </script>
</head>
<body class="bg-tactical-bg text-tactical-text font-sans antialiased">
    <header class="sticky top-0 z-40 bg-tactical-card/90 backdrop-blur-md border-b border-tactical-accent/30 px-4 lg:px-8 py-3">
        <div class="max-w-6xl mx-auto flex items-center justify-between">
            <a href="/" class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-slate-900 border border-tactical-accent/50 flex items-center justify-center text-2xl">&#129414;</div>
                <span class="text-lg font-black tracking-tight uppercase text-white">Angry Ducks <span class="text-tactical-accent">Moving</span></span>
            </a>
            <div class="flex items-center gap-3">
                <a href="/" class="hidden md:inline text-xs font-bold uppercase tracking-wider text-tactical-muted hover:text-tactical-accent">Home</a>
                <a href="{phone_href}" class="bg-tactical-accent hover:bg-tactical-accentHover text-slate-950 font-extrabold px-4 py-2 rounded-xl text-xs uppercase tracking-wider"><i class="fa-solid fa-phone mr-1"></i> {phone}</a>
            </div>
        </div>
    </header>
    <nav class="max-w-6xl mx-auto px-4 lg:px-8 pt-6 text-xs text-tactical-muted" aria-label="Breadcrumb">
        <a href="/" class="hover:text-tactical-accent">Home</a> <span class="mx-1">/</span> <span class="text-white">{crumb}</span>
    </nav>
    <main class="max-w-6xl mx-auto px-4 lg:px-8 py-8 space-y-10">
        <section class="bg-tactical-card border border-tactical-accent/40 rounded-2xl p-6 md:p-10">
            <h1 class="text-3xl md:text-4xl font-black uppercase tracking-tight text-white">{h1}</h1>
            <p class="text-tactical-muted mt-4 leading-relaxed max-w-3xl">{intro}</p>
            <div class="flex flex-wrap gap-3 mt-6">
                <a href="{phone_href}" class="bg-tactical-accent hover:bg-tactical-accentHover text-slate-950 font-extrabold px-6 py-3 rounded-xl text-sm uppercase tracking-wider"><i class="fa-solid fa-phone mr-2"></i>Call {phone}</a>
                <a href="/#sarge-chat" class="border border-tactical-accent/50 text-tactical-accent hover:bg-tactical-accent hover:text-slate-950 font-bold px-6 py-3 rounded-xl text-sm uppercase tracking-wider transition-colors">Get a Quote Online</a>
            </div>
        </section>
"""

SECTION_TMPL = """        <section class="bg-slate-900/60 border border-slate-800 p-6 md:p-8 rounded-2xl space-y-4">
            <h2 class="text-xl md:text-2xl font-black uppercase tracking-tight text-white">{h2}</h2>
{paras}
        </section>
"""

FAQ_TMPL = """        <section class="bg-slate-900/60 border border-slate-800 p-6 md:p-8 rounded-2xl space-y-4">
            <h2 class="text-xl md:text-2xl font-black uppercase tracking-tight text-white">Frequently Asked Questions</h2>
{items}
        </section>
"""

RELATED_TMPL = """        <section class="bg-tactical-card border border-tactical-accent/30 p-6 md:p-8 rounded-2xl">
            <h2 class="text-lg font-black uppercase tracking-tight text-white mb-4">Related Moving Services</h2>
            <div class="flex flex-wrap gap-2">
{links}
            </div>
        </section>
"""

FOOT_TMPL = """        <section class="bg-tactical-accent rounded-2xl p-6 md:p-10 text-center">
            <h2 class="text-2xl font-black uppercase text-slate-950 tracking-tight">Ready to Move? Let's Talk.</h2>
            <p class="text-slate-900 mt-2 font-semibold">Local, licensed, and insured. Real humans answer the phone.</p>
            <a href="{phone_href}" class="inline-block mt-5 bg-slate-950 text-white font-extrabold px-8 py-3 rounded-xl text-sm uppercase tracking-wider"><i class="fa-solid fa-phone mr-2"></i>{phone}</a>
        </section>
    </main>
    <footer class="border-t border-slate-800 mt-8 px-4 lg:px-8 py-8">
        <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-tactical-muted">
            <span>&copy; 2026 Angry Ducks Moving LLC &mdash; Knoxville, TN</span>
            <span>Mon&ndash;Sat 7 AM&ndash;8 PM, Closed Sundays &nbsp;|&nbsp; <a href="{phone_href}" class="hover:text-tactical-accent">{phone}</a></span>
        </div>
    </footer>
</body>
</html>
"""

def faq_schema(page, faqs):
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "MovingCompany",
                "name": "Angry Ducks Moving",
                "url": BASE + "/",
                "telephone": "+1-865-936-3891",
                "areaServed": page["area_served"],
                "openingHours": "Mo-Sa 07:00-20:00",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": page["canonical"]},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in faqs
                ],
            },
        ],
    }

def render(page):
    schema = json.dumps(faq_schema(page, page["faqs"]), indent=2)
    html = HEAD_TMPL.format(title=page["title"], meta=page["meta"], canonical=page["canonical"],
                            crumb=page["crumb"], h1=page["h1"], intro=page["intro"],
                            phone=PHONE, phone_href=PHONE_HREF, schema=schema)
    for h2, paras in page["sections"]:
        html += SECTION_TMPL.format(h2=h2, paras="\n".join(
            f'            <p class="text-tactical-muted leading-relaxed">{p}</p>' for p in paras))
    faq_items = "\n".join(
        f'''            <div class="border-b border-slate-800 pb-4">
                <h3 class="font-bold text-white text-sm uppercase tracking-wide">{q}</h3>
                <p class="text-tactical-muted text-sm mt-2 leading-relaxed">{a}</p>
            </div>''' for q, a in page["faqs"])
    html += FAQ_TMPL.format(items=faq_items)
    links = "\n".join(
        f'                <a href="{u}" class="text-xs font-bold uppercase tracking-wider bg-slate-950 border border-slate-700 hover:border-tactical-accent text-tactical-muted hover:text-tactical-accent px-4 py-2 rounded-xl transition-colors">{t}</a>'
        for t, u in page["related"])
    html += RELATED_TMPL.format(links=links)
    html += FOOT_TMPL.format(phone=PHONE, phone_href=PHONE_HREF)
    return html

PAGES = [
{
 "slug": "local-moving",
 "title": "Local Movers in Knoxville, TN | Angry Ducks Moving",
 "meta": "Looking for local movers in Knoxville, TN? Angry Ducks Moving offers full-service residential moves with trucks and trained crews across Knoxville and East Tennessee. Call (865) 936-3891.",
 "canonical": BASE + "/local-moving/",
 "crumb": "Local Moving",
 "h1": "Local Movers in Knoxville, TN",
 "area_served": "Knoxville, TN",
 "intro": "Moving across Knoxville? Angry Ducks Moving is a local, licensed and insured moving company built for East Tennessee moves. Our full-service crews bring the truck, the muscle, and the gear — dollies, pads, shrink wrap — and handle your move from first box to final furniture placement. Two movers plus a truck start at $140/hr, with a one-hour service fee that covers travel, fuel, and equipment.",
 "sections": [
  ("Full-Service Local Moving, Done Right", [
   "A local move sounds simple until you're staring at a third-floor walkup, a sleeper sofa that won't fit through the door, and a rental truck with four hours left on the clock. Our crews do this every day across Knoxville — from Sequoyah Hills colonials to downtown lofts to garden apartments off Kingston Pike. We wrap, pad, disassemble, load, transport, unload, and reassemble, so you don't lift a thing.",
   "Every full-service move includes our trucks, professional movers, furniture pads, dollies, and shrink wrap. Three-mover crews ($195/hr) are the sweet spot for most 2–3 bedroom homes; four movers ($250/hr) make big houses and tight timelines dramatically faster. You'll always know the crew size and hourly rate up front — no surprises, no fine-print fees."]),
  ("Why Knoxville Chooses Angry Ducks", [
   "We're not a franchise call center and we're not a couple of guys with a borrowed pickup. Angry Ducks Moving is a Knoxville company — our crews know which downtown streets won't fit a 26-footer, which West Knoxville apartment complexes require elevator reservations, and how to stage a load so nothing shifts on the curves of Chapman Highway.",
   "Because we're local, scheduling is flexible. Need a crew this week? Often this weekend? Call and ask — same-day and next-day help is regularly available, and our office actually picks up the phone. Mon–Sat 7 AM–8 PM."]),
  ("What a Local Move Costs", [
   "Our pricing is hourly and transparent: 2 movers + truck at $140/hr, 3 movers + truck at $195/hr, 4 movers + truck at $250/hr, plus a one-hour service fee covering the truck, fuel, pads, and equipment. Most local apartment moves land in the 3–5 hour range; full houses typically run 6–9 hours depending on volume, stairs, and distance.",
   "Want a firmer number before moving day? Use the cost estimator on our homepage or chat with Sarge, our AI dispatcher — give your name, phone, email, and move date and you'll get a crew recommendation with the exact hourly rate."]),
  ("How Much Does a Knoxville Move Cost?", [
   "The honest answer to the most common moving question: it depends on the clock. Our hourly rates are fixed and published — $140/hr for two movers plus a truck, $195/hr for three, $250/hr for four, plus a one-hour service fee — so your total is driven by how long the job takes, not by surprise fees or fine print. A one-bedroom apartment with an elevator usually runs 3–4 hours; a two-bedroom with stairs, 4–6; a full three-bedroom house, 6–9.",
   "Three things move the number most: volume (how much stuff), access (stairs, long carries, elevator windows), and crew size. A bigger crew costs more per hour but finishes sooner — on houses with stairs, a four-mover crew often beats a two-mover crew on total time and total cost. We'll recommend the crew size that fits your home when you call, and the rate is locked in before moving day.",
   "Be wary of quotes that sound too cheap to be real. Some movers advertise a low hourly rate, then add truck fees, stair fees, fuel surcharges, and equipment charges on moving day. Our one-hour service fee covers the truck, fuel, pads, and equipment — that's the whole picture, stated up front."]),
 ],
 "faqs": [
  ("How much do local movers cost in Knoxville?", "Angry Ducks Moving charges $140/hr for 2 movers plus a truck, $195/hr for 3 movers, and $250/hr for 4 movers, plus a one-hour service fee. Most local moves take 3–9 hours depending on home size."),
  ("What is the average cost of a local move in Knoxville?", "With our published hourly rates, a one-bedroom apartment typically takes 3–4 hours with a two-mover crew, a two-bedroom 4–6 hours, and a three-bedroom house 6–9 hours. Stairs, long carries, and volume are what move the time up or down."),
  ("Are you licensed and insured?", "Yes. Angry Ducks Moving is a licensed and insured moving company serving Knoxville and the surrounding East Tennessee communities."),
  ("Do you move on weekends?", "Yes — we're open Monday through Saturday, 7 AM to 8 PM, and closed Sundays. Weekend slots fill fast, so booking ahead helps."),
 ],
 "related": [("Labor-Only Moving", "/labor-only-moving/"), ("Packing & Unpacking", "/packing-and-unpacking/"), ("Movers in Farragut", "/movers-farragut-tn/"), ("Movers in Bearden", "/movers-bearden-tn/"), ("Movers in Seymour", "/movers-seymour-tn/")],
},
{
 "slug": "labor-only-moving",
 "title": "Labor-Only Movers in Knoxville, TN | Loading & Unloading Help",
 "meta": "Need labor-only movers in Knoxville, TN? Angry Ducks Moving loads and unloads your U-Haul, PODS, or rental truck. 2 movers from $100/hr, 2-hr minimum. Call (865) 936-3891.",
 "canonical": BASE + "/labor-only-moving/",
 "crumb": "Labor-Only Moving",
 "h1": "Labor-Only Movers in Knoxville, TN",
 "area_served": "Knoxville, TN",
 "intro": "Already have the truck? Angry Ducks Moving provides the muscle. Our labor-only crews load and unload rental trucks, trailers, and portable storage containers across Knoxville — U-Haul, Penske, Budget, PODS, U-Box, U-Pack, and ABF trailers. Two movers start at $100/hr with a two-hour minimum, and we bring the dollies, pads, and shrink wrap.",
 "sections": [
  ("Loading Done by People Who Do It Daily", [
   "Anyone can throw boxes in a truck. Packing a 26-foot rental so a washer, a sectional, and forty boxes all ride 400 miles without shifting is a skill — and it's what our crews do every single day. We build tiers, strap the load, distribute weight correctly, and pad everything that can scuff. The difference shows up at the other end when nothing is broken.",
   "Labor-only rates: 2 movers at $100/hr, 3 movers at $165/hr, 4 movers at $225/hr, two-hour minimum. For local jobs where you supply the truck, furniture pads, dollies, and shrink wrap are included. (Pads are excluded from PODS, ABF trailers, and long-distance containers.)"]),
  ("Perfect for DIY Moves, Containers, and Student Moves", [
   "Labor-only help is the sweet spot for UT students moving in and out of dorms and apartments, families loading a PODS container for a cross-country relocation, and anyone who rented a truck to save money but wants professionals handling the heavy, awkward, breakable stuff. We also do in-home moves — rearranging furniture room to room, or moving a single heavy piece like a safe or piano within your house.",
   "Booking is simple: tell us the date, the address, what's being loaded, and what it's going into. We'll recommend the right crew size. Same-day loading help is often available — if your truck shows up early or your friends bail, call (865) 936-3891."]),
  ("Small Jobs and Mini-Moves", [
   "Not every job is a full house. A big share of our labor-only work is the small stuff: moving a single heavy dresser upstairs, carrying a new mattress to the second floor, loading a few pieces into a storage unit, rearranging a living room, or helping clear a rental turnover. These mini-moves run on the same hourly rate — $100/hr for two movers, two-hour minimum — and get the same care as the big jobs: pads, dollies, straps, and crews who do this daily.",
   "Think of us for the in-between jobs too: the couch that arrived while your back is acting up, the treadmill that needs to move from the garage to the basement, the estate cleanout with a trailer to fill. One call, a couple of hours, and it's handled — no minimum crew drama, no full-day booking required."]),
  ("What We Need From You", [
   "Have the truck or container on-site and ready when we arrive, and make sure there's legal parking for it plus our crew vehicle. If your apartment complex needs a loading dock or elevator reservation, book it before moving day — downtown and West Knoxville buildings are strict about this.",
   "Everything should be packed and ready to carry. If it's not, we also offer packing and unpacking services — or our crews can work around you, though an unpacked house always costs more in hourly time."]),
 ],
 "faqs": [
  ("What does labor-only moving cost in Knoxville?", "Angry Ducks Moving charges $100/hr for 2 movers, $165/hr for 3 movers, and $225/hr for 4 movers, with a two-hour minimum. Pads, dollies, and shrink wrap are included on local jobs."),
  ("Do you load U-Haul trucks and PODS containers?", "Yes — U-Haul, Penske, Budget, PODS, U-Box, U-Pack trailers, and ABF trailers. If it holds household goods, our crews can load it correctly."),
  ("Can I get same-day loading help?", "Often, yes. Call (865) 936-3891 and we'll tell you straight whether a crew is available today."),
  ("Do you do small one-item moves?", "Yes — single heavy pieces, room-to-room moves inside your home, and storage-unit loads are regular jobs for us. Same hourly rates, two-hour minimum."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Packing & Unpacking", "/packing-and-unpacking/"), ("Movers in Maryville", "/movers-maryville-tn/"), ("Movers in Oak Ridge", "/movers-oak-ridge-tn/"), ("UT Campus Movers", "/movers-ut-campus-tn/")],
},
{
 "slug": "packing-and-unpacking",
 "title": "Packing and Unpacking Services in Knoxville, TN | Angry Ducks Moving",
 "meta": "Professional packing and unpacking services in Knoxville, TN. Angry Ducks Moving packs kitchens, fragiles, and whole homes — plus unpacking and debris removal. Call (865) 936-3891.",
 "canonical": BASE + "/packing-and-unpacking/",
 "crumb": "Packing & Unpacking",
 "h1": "Packing and Unpacking Services in Knoxville, TN",
 "area_served": "Knoxville, TN",
 "intro": "Packing is the part of moving everyone underestimates. Angry Ducks Moving offers full and partial packing services across Knoxville — kitchens, china, artwork, electronics, closets, garages, or the entire house. Our crews pack fast, label clearly, and protect fragiles the way professionals do, because we've wrapped ten thousand of them.",
 "sections": [
  ("Full Pack, Partial Pack, or Just the Fragiles", [
   "Not every move needs a full pack. Many customers pack the easy stuff themselves — books, clothes, linens — and hand us the kitchen, the china cabinet, the artwork, and anything glass. That's the smart money: professionals on the breakables, you on the t-shirts. We'll also do complete whole-home packing if you'd rather not touch a box at all.",
   "Every packed box is labeled by room and contents, so unloading lands boxes in the right rooms and unpacking doesn't become archaeology. Dish packs, wardrobe boxes, and picture crates are available for the items that need more than a standard box."]),
  ("Unpacking and Debris Removal", [
   "The move isn't over when the truck is empty — it's over when you can find your coffee maker. Our unpacking service puts kitchen and bedroom essentials where they belong, breaks down boxes, and hauls away the mountain of paper and cardboard. Most customers are functional the same evening instead of living out of boxes for two weeks.",
   "Unpacking pairs naturally with furniture assembly: beds rebuilt, dressers placed, TVs mounted back on stands. One crew, one visit, and the house is actually livable when we leave."]),
  ("Why Professional Packing Pays for Itself", [
   "The number-one cause of damage claims in moving isn't the truck — it's bad packing. A poorly packed box crushes; a well-packed box survives a 500-mile ride. Our packers use the right box for the job, double-wall where it counts, and never leave dead space that lets contents shift and collide.",
   "There's also the clock: a two-person crew packs in hours what takes most families an entire weekend. If your time has value — or your move date is bearing down on you — handing off the packing is usually the cheapest stress relief in the whole move."]),
 ],
 "faqs": [
  ("Do you provide the boxes and packing materials?", "Yes — we bring boxes, paper, bubble wrap, tape, and specialty cartons. Materials are billed for what we use; you never pay for a warehouse of supplies you didn't need."),
  ("Can you pack just my kitchen?", "Absolutely. Partial packing is our most popular option — kitchens, dining rooms, and fragiles packed by pros while you handle the rest."),
  ("Do you offer fragile-only packing?", "Yes. If everything else is already boxed and the only things left are the breakables — china, glassware, artwork, mirrors, electronics — we'll come pack just those with the right materials: dish packs, picture crates, and plenty of padding. It's the most cost-effective way to protect the items that actually break."),
  ("Do you unpack too?", "Yes. We unpack boxes onto surfaces, place everyday items, break down cartons, and remove the debris so you're settled the same day."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Furniture Assembly", "/furniture-assembly/"), ("Movers in Farragut", "/movers-farragut-tn/")],
},
{
 "slug": "furniture-assembly",
 "title": "Furniture Assembly Service in Knoxville, TN | Angry Ducks Moving",
 "meta": "Furniture assembly service in Knoxville, TN — beds, dressers, IKEA, home office setups, and gym equipment assembled right. In-home help from Angry Ducks Moving. Call (865) 936-3891.",
 "canonical": BASE + "/furniture-assembly/",
 "crumb": "Furniture Assembly",
 "h1": "Furniture Assembly Service in Knoxville, TN",
 "area_served": "Knoxville, TN",
 "intro": "That flat-pack wardrobe has 47 steps and a bag of hardware that all looks identical. Angry Ducks Moving offers in-home furniture assembly across Knoxville — beds, dressers, desks, IKEA systems, home-office setups, and exercise equipment, assembled correctly, leveled, and placed where you want it. We can also disassemble and reassemble your furniture as part of a move.",
 "sections": [
  ("Assembly Without the Sunday-Afternoon Meltdown", [
   "Our crews assemble furniture daily as part of moves, so the learning curve you're dreading is our Tuesday. We read the diagrams, sort the hardware first, and build in the right order — which is why a bed that takes most people three hours takes us forty minutes, with no leftover screws and no wobble.",
   "We handle IKEA and flat-pack systems, platform and storage beds, dressers and nightstands, desks and office setups, bookshelves, TV stands, and home gym equipment. If it came in a box with an Allen key, we've built its cousin before."]),
  ("Disassembly and Reassembly for Moves", [
   "Most damage to furniture happens at the joints — a bed frame carried whole torques its rails; a dresser moved with drawers in cracks its frame. As part of any Angry Ducks move, we disassemble what should travel flat and reassemble it in your new place, beds made and dressers placed.",
   "This is also a standalone service: bought a floor-model sectional that won't fit through the stairwell? We'll break it down, move it, and rebuild it. Rearranging a room and need the big pieces handled safely? That's an in-home move, and assembly is part of it."]),
  ("How It Works", [
   "Tell us what needs building — photos help — and we'll quote the time honestly. Small jobs (a nightstand, a desk) are quick visits; full room setups take longer. We bring our own tools, take away the packaging, and test everything before we leave: drawers glide, doors close, beds don't squeak.",
   "Assembly is available seven days a week alongside our moving schedule, Monday through Saturday 7 AM–8 PM. Pair it with a move or book it solo — either way, you skip the instruction manual."]),
 ],
 "faqs": [
  ("Do you assemble IKEA furniture?", "Yes — IKEA systems, MALM beds, PAX wardrobes, BESTA storage, desks, and everything in between. Flat-pack is our daily bread."),
  ("Can you take apart furniture for my move and put it back together?", "That's standard on our moves. We disassemble beds, tables, and sectionals for safe transport and reassemble them in your new home."),
  ("Do you haul away the boxes and packaging?", "Yes — we break down and remove all packaging when we finish, so you're not left with a cardboard mountain."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Packing & Unpacking", "/packing-and-unpacking/"), ("Movers in Bearden", "/movers-bearden-tn/"), ("Movers in Maryville", "/movers-maryville-tn/")],
},
{
 "slug": "movers-farragut-tn",
 "title": "Movers in Farragut, TN | Angry Ducks Moving",
 "meta": "Movers in Farragut, TN — Angry Ducks Moving serves Farragut and Turkey Creek with full-service moves, labor-only help, and packing. Licensed & insured. Call (865) 936-3891.",
 "canonical": BASE + "/movers-farragut-tn/",
 "crumb": "Movers in Farragut",
 "h1": "Movers in Farragut, TN",
 "area_served": "Farragut, TN",
 "intro": "Farragut moves have their own character: larger homes, long driveways, HOA rules about truck parking, and a lot of families upsizing within the same school zones. Angry Ducks Moving handles Farragut relocations weekly — full-service moves with our trucks and crews, labor-only loading help, packing, and furniture assembly — from neighborhoods off Kingston Pike to the Turkey Creek corridor.",
 "sections": [
  ("Built for Farragut Homes", [
   "Farragut houses tend to be bigger, which means more volume, more stairs, and more of the heavy pieces — pool tables, gun safes, solid-wood bedroom sets — that punish DIY moves. Our four-mover crews ($250/hr) are the right call for most Farragut homes: the job finishes in a day instead of bleeding into a second, and the hourly math usually beats a smaller crew working twice as long.",
   "We also know the local logistics: which subdivisions restrict street parking for box trucks, where to stage a 26-footer without blocking the cul-de-sac, and how to protect those wide-plank floors and tall staircases Farragut homes are known for. Floor runners, door jamb protectors, and rail padding go down before the first box moves."]),
  ("Moving Within Farragut School Zones", [
   "A huge share of our Farragut work is families moving three miles — same schools, bigger house, or a downsize after the kids leave. Short-distance moves like these are where an experienced local crew shines: we can often load, transport, and unload in a single efficient day, and you'll sleep in your own bed that night.",
   "If you're between closings, ask about split moves — we can load and hold, or coordinate with your storage unit. And if you're buying new furniture from the Turkey Creek stores, we do single-item furniture delivery and setup too."]),
  ("Services Available in Farragut", [
   "Everything we offer in Knoxville is available in Farragut: full-service residential moving, labor-only loading and unloading, packing and unpacking, furniture assembly and disassembly, heavy-item moves (safes, pianos, pool tables), in-home furniture rearranging, and same-day moving help when crews are open.",
   "Rates are the same as Knoxville: 2 movers + truck $140/hr, 3 movers $195/hr, 4 movers $250/hr plus a one-hour service fee; labor-only from $100/hr with a two-hour minimum. Call (865) 936-3891 — a human answers, and we'll give you a straight recommendation, not a phone tree."]),
 ],
 "faqs": [
  ("Do you serve the Turkey Creek area?", "Yes — Farragut, Turkey Creek, and all surrounding West Knoxville communities are core service areas for us."),
  ("Can you move a gun safe or piano in Farragut?", "Yes. Heavy-item moves are a specialty — safes, pianos, pool tables — with the right equipment and crew size for the weight and the stairs involved."),
  ("How far ahead should I book?", "A week or two is ideal, especially for month-end. But call anyway — same-day and next-day openings happen regularly."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Movers in Bearden", "/movers-bearden-tn/"), ("Movers in Oak Ridge", "/movers-oak-ridge-tn/")],
},
{
 "slug": "movers-maryville-tn",
 "title": "Movers in Maryville, TN | Angry Ducks Moving",
 "meta": "Movers in Maryville, TN — full-service moves, labor-only help, and packing from Angry Ducks Moving, serving Maryville, Alcoa & Blount County. Call (865) 936-3891.",
 "canonical": BASE + "/movers-maryville-tn/",
 "crumb": "Movers in Maryville",
 "h1": "Movers in Maryville, TN",
 "area_served": "Maryville, TN",
 "intro": "Maryville and Alcoa keep growing, and we're the Knoxville movers Blount County calls when the job needs doing right. Angry Ducks Moving serves Maryville with full-service residential moves, labor-only loading help for rental trucks and PODS, packing services, and furniture assembly — from historic homes near Maryville College to new builds on the south side.",
 "sections": [
  ("Maryville Moves, Handled Local", [
   "Whether you're moving into one of Maryville's older neighborhoods with narrow doorways and plaster walls, or a new construction with a garage full of boxes from the old place, our crews adapt. We pad and wrap through tight turns, protect new flooring and fresh paint, and stage the truck so the unload is as fast as the load.",
   "A lot of our Maryville work is Knoxville-to-Maryville relocations — families trading the city for Blount County space. We run that corridor constantly, so the timing, routing, and pricing are dialed in. Two movers plus a truck ($140/hr) covers apartments and small homes; three or four movers handle full houses efficiently."]),
  ("Labor-Only Help for DIY Maryville Moves", [
   "Renting a U-Haul or loading a PODS container at your Maryville home? Our labor-only crews ($100/hr for 2 movers, 2-hour minimum) do the heavy lifting — literally. We'll load your rental truck so it rides tight to Nashville, Charlotte, or wherever you're headed, or unload it when you arrive.",
   "This is also the answer for Maryville College students and young professionals in Alcoa apartments: a couple of hours of professional muscle beats bribing friends with pizza, and nothing ends up broken. Same-day help is often available."]),
  ("Packing, Assembly, and the Rest", [
   "Full packing services, partial packing (kitchens and fragiles are the popular choice), unpacking with debris removal, furniture disassembly and reassembly, and in-home moves — rearranging, or moving single heavy pieces like safes and pianos — are all available in Maryville and Alcoa.",
   "We're licensed and insured, open Monday–Saturday 7 AM–8 PM, and closed Sundays. Get a fast quote from Sarge on our homepage or just call (865) 936-3891 and talk to a person who'll give you a straight answer."]),
 ],
 "faqs": [
  ("Do you move between Knoxville and Maryville?", "Constantly — Knoxville-to-Maryville is one of our most common routes, and we serve both directions plus Alcoa and all of Blount County."),
  ("What's the minimum for labor-only help?", "Two hours. Two movers at $100/hr is the most-booked option for truck loading and unloading."),
  ("Do you pack as well as move?", "Yes — full-home packing, partial packing, and unpacking with debris removal, all available in Maryville."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Packing & Unpacking", "/packing-and-unpacking/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Loading & Unloading", "/loading-unloading/"), ("Movers in Alcoa", "/movers-alcoa-tn/"), ("Movers in Farragut", "/movers-farragut-tn/"), ("Movers in Seymour", "/movers-seymour-tn/")],
},
{
 "slug": "movers-seymour-tn",
 "title": "Movers in Seymour, TN | Angry Ducks Moving",
 "meta": "Movers in Seymour, TN — full-service moves, labor-only help & packing from Angry Ducks Moving, serving Seymour, South Knoxville & Sevier County. Call (865) 936-3891.",
 "canonical": BASE + "/movers-seymour-tn/",
 "crumb": "Movers in Seymour",
 "h1": "Movers in Seymour, TN",
 "area_served": "Seymour, TN",
 "intro": "Seymour sits along the Chapman Highway corridor between Knoxville and the Smokies — a community of long-time farm families, new subdivisions, and commuters who want space without giving up the city. Angry Ducks Moving serves Seymour with full-service residential moves, labor-only loading help for rental trucks and containers, packing services, and furniture assembly, from the older homes off Chapman Highway to the new builds spreading toward Sevier County.",
 "sections": [
  ("Seymour Moves: Country Roads and New Subdivisions", [
   "Seymour moves come in two flavors, and our crews handle both. The older properties — farmhouses, homes on acreage, places where the driveway is long gravel and the truck parks a good walk from the front door — need planning: staging gear near the house, protecting floors through the carry, and keeping the load moving so the distance doesn't eat the clock.",
   "The newer subdivisions bring a different job: full houses, tight cul-de-sacs, and neighbors who don't love a box truck blocking the street at 8 AM. We keep setups tight, work quietly, and clear out clean. Either way, tell us about your street when you book and we'll arrive with the right plan — and the right crew size."]),
  ("Knoxville-to-Seymour and the Chapman Highway Corridor", [
   "A steady share of our work is families moving between Knoxville and Seymour — trading city lots for county space, or moving closer to town for a shorter commute. We run the Chapman Highway corridor constantly, so a Knoxville-to-Seymour move is routine: loaded in the morning, unloaded by afternoon, beds reassembled before dinner.",
   "Seymour also sees a lot of moves toward Sevierville, Pigeon Forge, and the lake country. If you're relocating into or out of the area, our unpacking service — kitchen and bedrooms set up, boxes broken down and hauled away — turns a chaotic arrival into a settled home in a single day. Pair it with furniture assembly and the place is genuinely livable when we leave."]),
  ("Labor-Only Help and Straightforward Pricing", [
   "Seymour is a do-it-yourself kind of community, and labor-only help is one of our most-booked job types here. Rent the truck or container — U-Haul, Penske, PODS, U-Box — and we'll load it the way professionals do: heavy furniture as the base layer, boxes stacked by weight, everything strapped and padded so the drive survives the trip across town or across the state.",
   "Standard Angry Ducks rates apply: 2 movers + truck $140/hr, 3 movers $195/hr, 4 movers $250/hr plus a one-hour service fee; labor-only crews from $100/hr with a two-hour minimum. Licensed and insured, open Monday–Saturday 7 AM–8 PM, closed Sundays. Call (865) 936-3891 for a straight answer on crew size and timing, or get an instant quote from Sarge on our homepage."]),
 ],
 "faqs": [
  ("Do you serve Seymour and South Knoxville?", "Yes — Seymour, South Knoxville, and the Chapman Highway corridor are regular service areas, along with Sevier County communities toward Sevierville."),
  ("Can you load my rental truck or PODS container in Seymour?", "Yes — U-Haul, Penske, Budget trucks, PODS, and U-Box containers are regular jobs for us. We load them correctly so nothing shifts in transit."),
  ("How much does a move in Seymour cost?", "Full-service moves run $140/hr for two movers plus the truck, with a one-hour service fee. Labor-only help is $100/hr for two movers with a two-hour minimum. Call for a straight answer based on your home size and distance."),
  ("Do you handle homes with long driveways or acreage?", "Yes — long carries, gravel drives, and hillside properties are common in Seymour, and we plan the staging and carry before the first box moves."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Movers in Maryville", "/movers-maryville-tn/"), ("Movers in Lenoir City", "/movers-lenoir-city-tn/")],
},
{
 "slug": "movers-oak-ridge-tn",
 "title": "Movers in Oak Ridge, TN | Angry Ducks Moving",
 "meta": "Movers in Oak Ridge, TN — Angry Ducks Moving serves Oak Ridge lab families and professionals with full-service moves and labor-only help. Call (865) 936-3891.",
 "canonical": BASE + "/movers-oak-ridge-tn/",
 "crumb": "Movers in Oak Ridge",
 "h1": "Movers in Oak Ridge, TN",
 "area_served": "Oak Ridge, TN",
 "intro": "Oak Ridge runs on relocations — lab families, contractors, and professionals moving in and out on timelines that don't negotiate. Angry Ducks Moving serves Oak Ridge with full-service moves, labor-only loading help, and packing services built for tight schedules: show up on time, work fast, and get you settled without drama.",
 "sections": [
  ("Relocation-Speed Moving for the Secret City", [
   "When your start date is Monday, the move happens this weekend — no extensions, no excuses. Our crews are built for that pressure: we arrive with a plan, protect the house, and keep a pace that gets a full home loaded in hours, not days. Three-mover crews ($195/hr) hit the sweet spot for most Oak Ridge houses; four movers ($250/hr) when the calendar is truly brutal.",
   "We handle the Oak Ridge housing stock well — mid-century ranches with carports, split-levels with tricky stairs, and townhomes where the truck can't get close and everything carries further. Distance from truck to door is where amateur moves die; our crews just keep moving."]),
  ("Unpacking So You're Functional Night One", [
   "Relocation moves have a cruel second act: the boxes. You start work Monday surrounded by cardboard. Our unpacking service fixes that — kitchen and bedrooms set up, boxes broken down and hauled away, beds reassembled — so your first week isn't an excavation.",
   "Pair it with furniture assembly and the place is genuinely livable the day we leave. For families arriving from out of state into a rental, this is the difference between a chaotic landing and a clean one."]),
  ("Labor-Only and Container Loads", [
   "Moving yourself with a U-Box, PODS, or rental truck? Our labor-only crews load Oak Ridge homes correctly — weight distributed, everything strapped, fragiles protected — so your DIY move survives the interstate. Two movers at $100/hr, two-hour minimum, pads and dollies included on local work.",
   "We're licensed and insured, open Monday–Saturday 7 AM–8 PM. Call (865) 936-3891 for a straight answer on timing and crew size, or get an instant quote from Sarge on our homepage."]),
 ],
 "faqs": [
  ("Can you handle a last-minute Oak Ridge move?", "Often, yes. Relocation timelines are our specialty — call and we'll tell you honestly what crews are open."),
  ("Do you unpack as well?", "Yes — unpacking with debris removal, plus furniture reassembly, so you're settled the same day."),
  ("Are you insured?", "Yes, Angry Ducks Moving is licensed and insured for residential moves across East Tennessee."),
  ("My Oak Ridge building needs a certificate of insurance. Can you provide one?", "Yes. We're a licensed and insured moving company — tell us at booking that your building or complex requires a COI and we'll arrange one before moving day."),
  ("Do you work around freight elevator reservations?", "Yes. For buildings with freight elevators or loading docks, reserve your window with the property manager — ideally a couple of weeks out — and tell us the slot when you book. We'll arrive ready to work it."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Movers in Farragut", "/movers-farragut-tn/"), ("Movers in Bearden", "/movers-bearden-tn/")],
},
{
 "slug": "movers-bearden-tn",
 "title": "Movers in Bearden & West Knoxville, TN | Angry Ducks Moving",
 "meta": "Movers in Bearden & West Knoxville, TN — apartments, condos & homes moved by Angry Ducks Moving. Full-service, labor-only & packing. Call (865) 936-3891.",
 "canonical": BASE + "/movers-bearden-tn/",
 "crumb": "Movers in Bearden",
 "h1": "Movers in Bearden & West Knoxville, TN",
 "area_served": "Bearden, Knoxville, TN",
 "intro": "Bearden is where Knoxville's apartments, condos, and townhomes stack up along Kingston Pike — and where moves come with stairs, elevators, parking puzzles, and HOA move-in rules. Angry Ducks Moving runs Bearden and West Knoxville constantly: apartment specialists who've seen every floor plan on the corridor and know how to get a sleeper sofa up three flights without touching a wall.",
 "sections": [
  ("Apartment and Condo Specialists", [
   "Bearden moves are rarely about square footage — they're about access. Third-floor walkups, freight elevators with 2-hour reservation windows, parking lots where a 26-footer barely fits. Our crews plan the carry before the first box: door propped, elevator padded, route walked. That's the difference between a 4-hour move and an 8-hour one.",
   "Two movers plus a truck ($140/hr) handles most one- and two-bedroom apartments; add a third mover ($195/hr) when there's a full living room set plus a storage unit. We disassemble beds and sectionals, wrap everything, and reassemble on the other end — you don't touch a thing."]),
  ("Sequoyah Hills and West Knoxville Homes", [
   "West of Bearden proper, the moves get bigger: Sequoyah Hills colonials with formal dining sets and pianos, West Hills ranches, and the neighborhoods off Papermill and Morrell. These are full-house moves where crew size is everything — four movers ($250/hr) will finish in a day what two movers stretch across two.",
   "We protect what these homes are known for: hardwood floors get runners, banisters get padding, and doorways get measured before the big pieces come through. Heavy items — safes, pianos, pool tables — are quoted honestly based on weight, stairs, and access, not guessed at."]),
  ("UT Students and Young Professionals", [
   "Bearden's rental market turns over hard every August. If you're a UT student or young professional bouncing between apartments, our labor-only option ($100/hr for 2 movers, 2-hour minimum) is the move: we load your U-Haul or truck in a fraction of the time, and you keep the DIY savings where they count.",
   "Need storage between leases? We load storage units tight — Tetris is a professional skill — and come back to unload when the new place is ready. Call (865) 936-3891; August books fast, but we'll always give it to you straight on availability."]),
 ],
 "faqs": [
  ("Do you handle apartment buildings with elevators?", "Yes — we work with elevator reservations and building move-in rules across Bearden and West Knoxville all the time. Book the elevator window and we'll hit it."),
  ("What's the cheapest way to move a 1-bedroom apartment?", "Labor-only help at $100/hr (2-hour minimum) if you have the truck, or a 2-mover full-service crew at $140/hr if you want us to bring everything."),
  ("Can you move a piano in Sequoyah Hills?", "Yes — pianos and other heavy specialty items are quoted based on the piece, the stairs, and access. Call for an honest assessment."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Furniture Assembly", "/furniture-assembly/"), ("Movers in Farragut", "/movers-farragut-tn/"), ("Movers in Hardin Valley", "/movers-hardin-valley-tn/"), ("Movers in Maryville", "/movers-maryville-tn/")],
},
{
 "slug": "apartment-moving",
 "title": "Apartment Movers in Knoxville, TN | Angry Ducks Moving",
 "meta": "Apartment movers in Knoxville, TN — stairs, elevators, and tight hallways handled by Angry Ducks Moving. Downtown lofts, UT campus housing & complexes. Call (865) 936-3891.",
 "canonical": BASE + "/apartment-moving/",
 "crumb": "Apartment Moving",
 "h1": "Apartment Movers in Knoxville, TN",
 "area_served": "Knoxville, TN",
 "intro": "Apartment moves are a different sport: stairs, elevators, narrow hallways, parking lots that barely fit a truck, and building managers with rules. Angry Ducks Moving runs apartment moves across Knoxville every week — downtown lofts, UT campus housing, and the big complexes along Kingston Pike. Two movers plus a truck at $140/hr handles most one- and two-bedroom apartments.",
 "sections": [
  ("Built for Stairs, Elevators, and Tight Turns", [
   "Third-floor walkup? Freight elevator with a two-hour window? A couch that has to go over the balcony rail? We've done all of it. Our crews walk the route before the first box — doors propped, elevator padded, hallway corners measured — so the move flows instead of stalling at every doorway.",
   "We disassemble beds, sectionals, and dining tables, wrap everything in pads and shrink wrap, and reassemble in your new place. Walls, doorframes, and banisters stay unscuffed: that's the standard, not an upgrade."]),
  ("Downtown, Campus, and the Corridor", [
   "Downtown Knoxville lofts come with loading docks, parking garages with low clearances, and strict move-in hours — we plan around all of it. Around UT, August turnover is chaos; our labor-only option ($100/hr, 2-hour minimum) is the student favorite for loading U-Hauls fast, while full-service crews handle the rest.",
   "The big West Knoxville complexes — Bearden, Cedar Bluff, Hardin Valley — each have their own quirks: gate codes, long carries from lot to door, elevators that need reserving. Tell us the complex name when you call and we'll tell you exactly how we'll run it."]),
  ("What It Costs", [
   "Most one-bedroom apartments move in 3–4 hours with a two-mover crew ($140/hr + one-hour service fee). Two-bedrooms with a full living room set usually want a third mover ($195/hr) — the job finishes faster and the hourly math works out.",
   "Need storage between leases? We load storage units tight and come back when the new place is ready. Call (865) 936-3891 — we'll give you a straight crew recommendation, not a phone tree."]),
 ],
 "faqs": [
  ("How much does it cost to move a 1-bedroom apartment in Knoxville?", "Most run 3–4 hours with a 2-mover crew at $140/hr plus a one-hour service fee. Stairs and long carries add time — we'll be honest about it when you call."),
  ("Do you handle apartments with elevators?", "Yes — we work with elevator reservations and building move-in rules across Knoxville weekly. Book your elevator window and we'll hit it."),
  ("Can you move me into a storage unit?", "Absolutely. We load storage units to maximize the space and return to unload when your new place is ready."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Movers in Bearden", "/movers-bearden-tn/"), ("Furniture Assembly", "/furniture-assembly/"), ("UT Campus Movers", "/movers-ut-campus-tn/")],
},
{
 "slug": "piano-heavy-item-moving",
 "title": "Piano & Heavy Item Movers in Knoxville, TN | Angry Ducks Moving",
 "meta": "Piano movers & heavy item movers in Knoxville, TN — uprights, baby grands, gun safes, and pool tables moved safely by Angry Ducks Moving. Call (865) 936-3891.",
 "canonical": BASE + "/piano-heavy-item-moving/",
 "crumb": "Piano & Heavy Item Moving",
 "h1": "Piano & Heavy Item Movers in Knoxville, TN",
 "area_served": "Knoxville, TN",
 "intro": "Some things shouldn't be moved by friends and a prayer. Angry Ducks Moving handles pianos, gun safes, pool tables, and other heavy specialty items across Knoxville — with the right crew size, the right equipment, and an honest quote based on weight, stairs, and access, not a guess.",
 "sections": [
  ("Pianos, Done Properly", [
   "Uprights, consoles, baby grands — each moves differently, and each gets worse with improvisation. We pad and strap uprights to piano boards, remove and wrap grand legs and lids, and never, ever tip a piano end-over-end down stairs. Keyboard actions are fragile; our crews treat them that way.",
   "Tell us the piano type, the stairs at both ends, and the doorways involved, and we'll quote it straight. If a job needs a crane or a fourth man for a grand staircase, we'll say so upfront instead of discovering it on moving day."]),
  ("Gun Safes, Pool Tables, and the Rest", [
   "Gun safes are the classic heavy-item job: 600–1,200 lbs of awkward steel that has to go down a hallway, possibly down stairs, and into a precise spot. We move them with stair-climbing dollies, straps, and enough crew — no scratched floors, no injured backs, no safe wedged in a doorway.",
   "Pool tables get disassembled (slate travels flat and padded), moved, and reassembled — though leveling and re-felting is a billiards specialist's job and we'll tell you that honestly. Hot tubs, commercial equipment, and oversized furniture all fall in the same category: quoted on facts, moved with gear."]),
  ("How Heavy-Item Pricing Works", [
   "Heavy items are quoted individually, not by the standard hourly rate alone — the price depends on the item's weight, the stairs and turns involved, the crew size needed, and whether it's part of a larger move or a standalone trip. A safe moving within the same house costs far less than a baby grand going up two flights.",
   "Call (865) 936-3891 with the details — photos help enormously — and you'll get an honest number. If your job is beyond what we can do safely, we'll tell you that too, and point you toward who can."]),
 ],
 "faqs": [
  ("How much does it cost to move a piano in Knoxville?", "It depends on the piano type, stairs, and distance. Uprights on ground level start modest; baby grands with stairs cost more. Call with photos for an honest quote."),
  ("Can you move a gun safe down stairs?", "Yes — safes are a specialty. We use stair-climbing equipment and the right crew size so floors, walls, and backs all survive."),
  ("Do you disassemble pool tables?", "Yes — slate is removed, travels flat and padded, and the table is reassembled at the new location."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Furniture Assembly", "/furniture-assembly/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Movers in Farragut", "/movers-farragut-tn/")],
},
{
 "slug": "loading-unloading",
 "title": "Loading and Unloading Help in Knoxville, TN | Angry Ducks Moving",
 "meta": "Loading and unloading help in Knoxville, TN — rental trucks, PODS & containers loaded tight by Angry Ducks Moving pros. Same-day help often available. Call (865) 936-3891.",
 "canonical": BASE + "/loading-unloading/",
 "crumb": "Loading & Unloading",
 "h1": "Loading and Unloading Help in Knoxville, TN",
 "area_served": "Knoxville, TN",
 "intro": "The truck is rented, the boxes are packed — now comes the part that decides whether everything arrives intact. Angry Ducks Moving provides professional loading and unloading help across Knoxville: rental trucks, trailers, PODS containers, and U-Boxes loaded tight, strapped right, and unloaded fast. Two movers from $100/hr, two-hour minimum, same-day help often available.",
 "sections": [
  ("Loading Is a Skill — We Do It Daily", [
   "A well-loaded truck is Tetris with consequences. Heavy furniture forms the base tiers against the walls, boxes fill the middle by weight, mattresses become padding, and everything gets strapped so a mountain curve doesn't become a furniture avalanche. Our crews load trucks every single day — the difference shows at the other end when nothing is broken.",
   "We load U-Haul, Penske, and Budget trucks, cargo trailers, PODS and U-Box containers, U-Pack trailers, and ABF freight trailers. If it holds household goods, we know how to pack it. Pads, dollies, and shrink wrap are included on local jobs."]),
  ("Unloading: Fast, Placed, Done", [
   "Arriving in Knoxville with a truck full of your life? We'll meet it, unload it room by room, and place furniture where you want it — not just stacked in the garage. Beds reassembled, boxes in the right rooms, and you're sleeping in your own bed that night instead of on an air mattress surrounded by cardboard.",
   "Unloading pairs well with our unpacking service: we open the kitchen and bedroom boxes, put everyday items away, break down the cartons, and haul off the debris. One visit, and the house is livable."]),
  ("When to Call", [
   "Yesterday would have been ideal; today usually works. Same-day loading and unloading help is regularly available — if your truck arrived early, your friends bailed, or the container company gave you a four-hour window, call (865) 936-3891 and we'll tell you straight whether a crew can be there.",
   "Have the truck or container on-site and ready, with legal parking for it. Everything should be packed and ready to carry — an unpacked house burns hourly time, and hourly time is money."]),
 ],
 "faqs": [
  ("What does loading help cost in Knoxville?", "Two movers at $100/hr with a two-hour minimum. Most truck loads take 2–4 hours depending on volume and stairs."),
  ("Do you load PODS containers?", "Yes — PODS, U-Box, U-Pack, ABF trailers, and all major rental trucks. Containers reward good Tetris skills; that's our specialty."),
  ("Can you unload my truck today?", "Often, yes. Call (865) 936-3891 — if a crew is open, we'll be there."),
 ],
 "related": [("Labor-Only Moving", "/labor-only-moving/"), ("Local Moving", "/local-moving/"), ("Packing & Unpacking", "/packing-and-unpacking/"), ("Movers in Oak Ridge", "/movers-oak-ridge-tn/")],
},
{
 "slug": "furniture-delivery",
 "title": "Furniture Delivery in Knoxville, TN | Angry Ducks Moving",
 "meta": "Furniture delivery in Knoxville, TN — single items & full rooms delivered, carried in, assembled & placed by Angry Ducks Moving. Call (865) 936-3891.",
 "canonical": BASE + "/furniture-delivery/",
 "crumb": "Furniture Delivery",
 "h1": "Furniture Delivery in Knoxville, TN",
 "area_served": "Knoxville, TN",
 "intro": "Bought a couch, a bedroom set, or a whole living room and now need it actually in your house? Angry Ducks Moving does furniture delivery across Knoxville — store pickup, careful transport, carry-in, room placement, assembly, and packaging removal. One call, and the furniture is usable the day it arrives.",
 "sections": [
  ("From Store to Set Up in One Visit", [
   "The big-box delivery left it in your driveway. The online order arrived in seventeen boxes. We fix both: pickup from Turkey Creek stores, Knoxville furniture retailers, or your doorstep, then carry-in, assembly, and placement exactly where you want it. Beds built, dressers leveled, sectionals configured, TV on the stand.",
   "Every delivery includes padding and wrapping for transport, floor and doorway protection at your home, and removal of all boxes and packaging when we're done. You don't lift, build, or break down a single carton."]),
  ("Single Items to Full Rooms", [
   "One heavy dresser up the stairs. A full bedroom set from the showroom. A living room's worth of flat-pack that would eat your entire Saturday. All of it is fair game — small jobs are quick visits, full rooms take a few hours, and the price always matches the actual work.",
   "Designers and stagers: we do white-glove delivery and setup for client homes, including Parade of Homes–style installs — furniture placed per plan, packaging gone, rooms photo-ready. If you're furnishing a model or a showcase home on a deadline, call early."]),
  ("How to Book", [
   "Tell us what you bought (photos or links help), where it's coming from, and where it's going — including stairs and tight turns. We'll quote the job honestly and schedule the pickup and delivery in one coordinated run.",
   "We're open Monday–Saturday 7 AM–8 PM. Call (865) 936-3891 — a human answers, and same-week delivery is the norm, not the exception."]),
 ],
 "faqs": [
  ("Do you pick up from furniture stores?", "Yes — we pick up from Knoxville-area retailers including the Turkey Creek corridor, transport, carry in, assemble, and place your furniture."),
  ("Will you assemble what you deliver?", "That's the point. Beds, dressers, sectionals, desks — built, leveled, and placed, with packaging hauled away."),
  ("Do you deliver for interior designers?", "Yes — white-glove delivery and setup for designer clients, staged homes, and model homes, on deadline."),
 ],
 "related": [("Furniture Assembly", "/furniture-assembly/"), ("Local Moving", "/local-moving/"), ("Movers in Farragut", "/movers-farragut-tn/"), ("Movers in Bearden", "/movers-bearden-tn/")],
},
{
 "slug": "movers-powell-tn",
 "title": "Movers in Powell, TN | Angry Ducks Moving",
 "meta": "Movers in Powell, TN — full-service moves, labor-only help & packing from Angry Ducks Moving, serving Powell, Halls & North Knox County. Call (865) 936-3891.",
 "canonical": BASE + "/movers-powell-tn/",
 "crumb": "Movers in Powell",
 "h1": "Movers in Powell, TN",
 "area_served": "Powell, TN",
 "intro": "Powell's growth means a lot of moving — young families upsizing into the new subdivisions, long-time residents settling into their forever homes, and Knoxville commuters finding space in North Knox County. Angry Ducks Moving serves Powell with full-service residential moves, labor-only loading help, packing, and furniture assembly, from Beaver Creek subdivisions to the older neighborhoods off Emory Road.",
 "sections": [
  ("Powell Moves, North Knox Style", [
   "Powell moves tend to be full houses: 3–4 bedrooms, a garage full of tools and toys, and a yard's worth of outdoor gear. That's four-mover territory ($250/hr) more often than not — the crew that finishes in one day beats the smaller crew that bleeds into a second day, and the hourly math usually favors the bigger team.",
   "We know the area's logistics: new subdivisions with tight turnarounds where a 26-footer needs a plan, Beaver Creek floodplain streets that punish heavy trucks after rain, and the older ranch neighborhoods where everything is ground-level and fast. Tell us your street and we'll tell you how we'll run it."]),
  ("Halls, Heiskell, and the Corridor", [
   "Our Powell service covers the whole North Knox corridor — Halls, Heiskell, and the neighborhoods along Emory Road, Beaver Creek Drive, and Clinton Highway. Knoxville-to-Powell is a constant route for us: families trading city lots for county space, and we run it efficiently in both directions.",
   "Labor-only help ($100/hr, 2-hour minimum) is popular here for the DIY crowd with a rented truck, and our packing crews handle the houses where the garage became a storage unit years ago. Unpacking with debris removal means you're settled the same week, not the same month."]),
  ("Straightforward Pricing", [
   "Same rates as everywhere we serve: 2 movers + truck $140/hr, 3 movers $195/hr, 4 movers $250/hr plus a one-hour service fee; labor-only from $100/hr with a two-hour minimum. Licensed and insured, open Monday–Saturday 7 AM–8 PM.",
   "Call (865) 936-3891 for a fast, honest quote — or chat with Sarge on our homepage. Either way you get a crew recommendation and an exact hourly rate, no phone tree and no games."]),
 ],
 "faqs": [
  ("Do you serve Halls and Heiskell?", "Yes — Powell, Halls, Heiskell, and all of North Knox County are regular service areas."),
  ("How many movers do I need for a 4-bedroom house?", "Usually four. A 4-mover crew at $250/hr finishes most Powell houses in a single day."),
  ("Can you help me load my rental truck?", "Yes — labor-only loading help from $100/hr with a two-hour minimum, pads and dollies included on local jobs."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Movers in Oak Ridge", "/movers-oak-ridge-tn/"), ("Movers in Maryville", "/movers-maryville-tn/")],
},
{
 "slug": "movers-lenoir-city-tn",
 "title": "Movers in Lenoir City, TN | Angry Ducks Moving",
 "meta": "Movers in Lenoir City, TN — full-service moves, labor-only help & packing from Angry Ducks Moving, serving Lenoir City & Tellico Village. Call (865) 936-3891.",
 "canonical": BASE + "/movers-lenoir-city-tn/",
 "crumb": "Movers in Lenoir City",
 "h1": "Movers in Lenoir City, TN",
 "area_served": "Lenoir City, TN",
 "intro": "Lenoir City sits at the crossroads of lake life and Knoxville commuting — Tellico Village retirees, young families along Highway 321, and everyone in between. Angry Ducks Moving serves Lenoir City with full-service residential moves, labor-only loading help, packing services, and furniture assembly, from lakefront homes to the new builds off the interstate corridor.",
 "sections": [
  ("Lake Homes and Village Moves", [
   "Tellico Village moves have their own rhythm: downsizing retirees with a lifetime of belongings, condos and villas with HOA move-in rules, and lake houses where the view is spectacular and the driveway is an adventure. Our crews handle the logistics — gate access, elevator reservations, tight village streets — while treating a lifetime's possessions with the care they deserve.",
   "For the Highway 321 corridor and the neighborhoods around Lenoir City proper, it's classic suburban moving: full houses, two-car garages, and kids' rooms. Three movers ($195/hr) is the workhorse crew for most of these homes; four movers ($250/hr) when there's a deadline or a lot of heavy pieces."]),
  ("Knoxville-to-Lenoir City Relocations", [
   "A steady stream of our work is Knoxville families moving west for space and lake access. We run the I-40/I-75 corridor constantly, so a Knoxville-to-Lenoir City move is routine for us — loaded in the morning, unloaded by afternoon, beds reassembled before dinner.",
   "Coming from out of state into a Tellico Village villa or a Lenoir City new build? Our unpacking service — kitchen and bedrooms set up, boxes broken down and hauled away — turns a chaotic arrival into a settled home in a single day."]),
  ("Pricing and Booking", [
   "Standard Angry Ducks rates: 2 movers + truck $140/hr, 3 movers $195/hr, 4 movers $250/hr plus a one-hour service fee; labor-only crews from $100/hr with a two-hour minimum. Licensed and insured.",
   "Open Monday–Saturday 7 AM–8 PM, closed Sundays. Call (865) 936-3891 for a straight answer on crew size and timing, or get an instant quote from Sarge on our homepage."]),
 ],
 "faqs": [
  ("Do you serve Tellico Village?", "Yes — Tellico Village, Lenoir City, and the surrounding Loudon County communities are regular service areas, including village condos with HOA requirements."),
  ("We're moving from Knoxville to Lenoir City — is that a full day?", "Usually a single day: load in the morning, drive the corridor, unload in the afternoon. We'll confirm timing when you call."),
  ("Do you offer packing services in Lenoir City?", "Yes — full-home packing, partial packing, and unpacking with debris removal."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Packing & Unpacking", "/packing-and-unpacking/"), ("Movers in Farragut", "/movers-farragut-tn/"), ("Movers in Maryville", "/movers-maryville-tn/")],
},
{
 "slug": "movers-hardin-valley-tn",
 "title": "Movers in Hardin Valley, TN | Angry Ducks Moving",
 "meta": "Movers in Hardin Valley, TN — new-construction moves, family relocations & labor-only help from Angry Ducks Moving, serving Hardin Valley, Karns & West Knox. Call (865) 936-3891.",
 "canonical": BASE + "/movers-hardin-valley-tn/",
 "crumb": "Movers in Hardin Valley",
 "h1": "Movers in Hardin Valley, TN",
 "area_served": "Hardin Valley, TN",
 "intro": "Hardin Valley is Knoxville's growth engine — new subdivisions rising every month, young families upsizing, and a steady stream of move-ins from across the country. Angry Ducks Moving serves Hardin Valley with full-service residential moves, labor-only loading help, packing services, and furniture assembly, from the new builds off Hardin Valley Road to the established neighborhoods around Karns.",
 "sections": [
  ("New-Construction Moves Are Our Specialty", [
   "Moving into a brand-new build is its own kind of job: pristine floors, fresh paint, tight closing timelines, and a garage full of boxes from the old place. Our crews treat new construction like it deserves — floor runners down before the first box, door jamb protectors on every frame, and banisters padded before anything heavy comes up the stairs. The house stays showroom-fresh; only the furniture is new.",
   "Timing is everything on new builds. Closings slip, builders hand over keys late, and suddenly moving day is tomorrow. We stay flexible for Hardin Valley's pace — call (865) 936-3891 and we'll give you an honest answer on availability, including same-week and sometimes same-day openings."]),
  ("Growing Families, Growing Houses", [
   "The typical Hardin Valley move is a family trading up: a 3–4 bedroom home, kids' rooms full of furniture, a garage of bikes and tools, and usually a piano or a gun safe in the mix. Three-mover crews ($195/hr) are the workhorse for these homes; four movers ($250/hr) when there's a deadline, a lot of stairs, or the kind of heavy pieces that punish small crews.",
   "We also handle the reverse — empty-nesters downsizing out of Hardin Valley into condos closer to town, and the estate cleanouts that come with family transitions. Whatever direction the move goes, the crew size and hourly rate are quoted up front, and the job finishes when everything is placed, not just unloaded."]),
  ("Karns and West Knox Coverage", [
   "Our Hardin Valley service covers the whole northwest corridor — Karns, the neighborhoods along Oak Ridge Highway, and the subdivisions feeding Hardin Valley Academy. Knoxville-to-Hardin Valley is a constant route for us, so the drive time, the truck staging, and the pricing are all dialed in.",
   "Labor-only help ($100/hr, two-hour minimum) is popular here for the DIY crowd loading rental trucks or PODS containers, and our packing crews handle the kitchens and fragiles while you handle the rest. Licensed and insured, open Monday–Saturday 7 AM–8 PM — call for a straight crew recommendation."]),
 ],
 "faqs": [
  ("Do you serve Karns too?", "Yes — Hardin Valley, Karns, and the whole northwest Knox County corridor are regular service areas."),
  ("Can you protect my new home's floors and paint?", "That's standard on every job. Floor runners, door jamb protectors, and rail padding go down before we carry anything in."),
  ("How fast can you schedule a Hardin Valley move?", "Often within days. Call (865) 936-3891 — new-construction timelines shift constantly, and we're built for that."),
 ],
 "related": [("Local Moving", "/local-moving/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Movers in Farragut", "/movers-farragut-tn/"), ("Movers in Bearden", "/movers-bearden-tn/")],
},
{
 "slug": "movers-alcoa-tn",
 "title": "Movers in Alcoa, TN | Angry Ducks Moving",
 "meta": "Movers in Alcoa, TN — full-service moves, labor-only help & packing from Angry Ducks Moving, serving Alcoa, Maryville & Blount County. Licensed & insured. Call (865) 936-3891.",
 "canonical": BASE + "/movers-alcoa-tn/",
 "crumb": "Movers in Alcoa",
 "h1": "Movers in Alcoa, TN",
 "area_served": "Alcoa, TN",
 "intro": "Alcoa sits at the heart of Blount County's growth — Springbrook Park families, young professionals near the airport corridor, and retirees settling into the foothills. Angry Ducks Moving serves Alcoa with full-service residential moves, labor-only loading help for rental trucks and containers, packing services, and furniture assembly — from Springbrook neighborhoods to the new developments along Alcoa Highway.",
 "sections": [
  ("Alcoa Moves, Blount County Covered", [
   "Alcoa's housing mix keeps our crews versatile: Springbrook Park's established ranch homes with full basements, the townhomes and apartments along the Alcoa Highway corridor, and the newer subdivisions filling in toward the foothills. Basements with exterior stairs, carports that double as staging areas, long driveways — we've run them all.",
   "Two movers plus a truck ($140/hr) handles most Alcoa apartments and smaller homes; three movers ($195/hr) is the sweet spot for full houses. Every move gets the same protection standard: wrapped furniture, padded doorways, and floors that look the same when we leave."]),
  ("Knoxville-to-Alcoa Relocations", [
   "A constant share of our work is Knoxville families moving south for Blount County space — and Alcoa professionals moving north for shorter commutes. We run the Alcoa Highway corridor daily, so a Knoxville-to-Alcoa move is routine: loaded in the morning, unloaded by afternoon, beds reassembled before dinner.",
   "Arriving from out of state? Our unpacking service — kitchen and bedrooms set up, boxes broken down and hauled away — turns a chaotic landing into a settled home in a single day. Pair it with furniture assembly and the place is genuinely livable when we leave."]),
  ("Labor-Only and DIY Support", [
   "Renting a truck or loading a container at your Alcoa home? Our labor-only crews ($100/hr for two movers, two-hour minimum) load it tight and strap it right, so your DIY move survives the interstate. Pads, dollies, and shrink wrap included on local work.",
   "We're licensed and insured, open Monday–Saturday 7 AM–8 PM, closed Sundays. Call (865) 936-3891 for a straight answer on crew size and timing, or get an instant quote from Sarge on our homepage."]),
 ],
 "faqs": [
  ("Do you move between Alcoa and Knoxville?", "Constantly — the Alcoa Highway corridor is one of our regular routes, in both directions."),
  ("What's the minimum for labor-only help in Alcoa?", "Two hours. Two movers at $100/hr is the most-booked option for truck and container loading."),
  ("Do you serve Springbrook Park?", "Yes — Springbrook Park, the Alcoa Highway corridor, and all of Blount County."),
 ],
 "related": [("Movers in Maryville", "/movers-maryville-tn/"), ("Local Moving", "/local-moving/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Packing & Unpacking", "/packing-and-unpacking/")],
},
{
 "slug": "movers-ut-campus-tn",
 "title": "UT Campus Movers in Knoxville, TN | Student Moving | Angry Ducks Moving",
 "meta": "UT campus movers in Knoxville, TN — dorm move-ins, student apartments, and labor-only loading help from Angry Ducks Moving. Same-week help available. Call (865) 936-3891.",
 "canonical": BASE + "/movers-ut-campus-tn/",
 "crumb": "UT Campus Movers",
 "h1": "UT Campus Movers in Knoxville, TN",
 "area_served": "Knoxville, TN (University of Tennessee campus area)",
 "intro": "Moving around the University of Tennessee campus is its own kind of chaos: dorm move-in windows measured in hours, Fort Sanders houses with four flights of stairs, and every student in Knoxville trying to move the same August weekend. Angry Ducks Moving runs UT campus moves constantly — dorm rooms, student apartments, and labor-only loading help for the U-Hauls lined up on Cumberland Avenue. Two movers from $100/hr, two-hour minimum, same-week help the norm.",
 "sections": [
  ("Dorm Rooms and Student Apartments", [
   "A dorm move looks small until you're carrying a mini-fridge, a futon, and forty boxes up to the fourth floor with a two-hour parking window. Our crews do campus moves weekly: we stage at the curb, keep the carry moving, and get everything up in a fraction of the time it takes a family caravan. Dorm rooms, Fort Sanders rental houses, and the student apartment complexes along the Cumberland corridor are all regular stops.",
   "Parents: if you're driving in from out of town with a car full of dorm gear, book a couple of hours of labor-only help and skip the stairs entirely. We'll meet you at the curb, unload the car, and have the room set up while you handle check-in. Two movers at $100/hr with a two-hour minimum — cheaper than the chiropractor."]),
  ("Labor-Only Loading: The Student Favorite", [
   "The most-booked student job is loading a rented truck or trailer: U-Haul, Penske, Budget, or a cargo trailer behind the family SUV. Our crews load them correctly — heavy furniture as the base, boxes stacked by weight, everything strapped so the drive to Nashville, Charlotte, or home survives the interstate. Pads, dollies, and shrink wrap included on local work.",
   "End-of-lease moves out of student apartments are the other classic: everything out, everything into the truck or a storage unit, in one efficient session. August books fast, but same-day and next-day openings happen all month — call (865) 936-3891 and we'll tell you straight what's open."]),
  ("Campus Move-In Logistics, Handled", [
   "UT move-in days run on schedules, not vibes: assigned arrival windows, designated loading zones, and dorms where the elevator line is thirty people deep. We plan around all of it — arrive in your window, work the stairs when the elevator stalls, and keep the hallway clear so your RA stays happy. If your building needs a freight elevator reservation or a loading-dock pass, book it before moving day and we'll hit the slot.",
   "Between leases? We load storage units tight — Tetris is a professional skill — and come back to unload when the new place is ready. We also do in-home moves inside student rentals: roommate swap, bedroom-to-bedroom, or getting the heavy pieces out of the basement at move-out. One call, a couple of hours, done."]),
 ],
 "faqs": [
  ("How much does it cost to move a dorm room or student apartment?", "Labor-only help runs $100/hr for two movers with a two-hour minimum — most dorm and small-apartment jobs finish inside that window. Full-service with our truck is $140/hr for two movers plus a one-hour service fee."),
  ("Can you help on UT move-in day?", "Yes — August is our busiest campus month, so booking a week or two ahead helps. But call anyway: same-day and next-day openings happen regularly, and we'll give you a straight answer."),
  ("Do you move students into storage between leases?", "Absolutely. We load storage units to maximize the space and return to unload when your new place is ready."),
 ],
 "related": [("Apartment Moving", "/apartment-moving/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Local Moving", "/local-moving/"), ("Movers in Bearden", "/movers-bearden-tn/")],
},
{
 "slug": "movers-karns-tn",
 "title": "Movers in Karns, TN | Angry Ducks Moving",
 "meta": "Movers in Karns, TN — Angry Ducks Moving handles Karns subdivision moves, acreage properties, and labor-only loading across northwest Knox County. Call (865) 936-3891.",
 "canonical": BASE + "/movers-karns-tn/",
 "crumb": "Movers in Karns",
 "h1": "Movers in Karns, TN",
 "area_served": "Karns, TN (northwest Knox County)",
 "intro": "Karns sits along the Oak Ridge Highway corridor in northwest Knox County — a mix of established subdivisions, newer construction, and acreage properties with long gravel driveways. That mix is exactly what our crews are built for: tight subdivision streets one job, a rural property with a half-mile driveway the next. Angry Ducks Moving runs full-service moves, labor-only loading help, and packing services across Karns and the surrounding northwest Knox County communities.",
 "sections": [
  ("Karns Moves: Subdivisions, Acreage, and Steep Driveways", [
   "A lot of Karns properties weren't designed with moving trucks in mind: long shared driveways, soft ground after rain, and hillside homes where the truck parks fifty yards from the front door. We plan for all of it — staging gear near the house, protecting floors and doorways, and keeping the carry moving so the distance doesn't eat your clock.",
   "Newer subdivisions off Oak Ridge Highway bring a different challenge: tight cul-de-sacs, HOA rules about truck parking, and neighbors who don't love a box truck blocking the street at 8 AM. We keep setups tight, work quietly, and clear out clean. Tell us about your street when you book and we'll arrive with the right plan."]),
  ("Labor-Only Loading for DIY Movers", [
   "Karns is a do-it-yourself kind of community, and labor-only is our most-booked job type here. Rent the truck or container — U-Haul, Penske, PODS, U-Box — and we'll load it the way professionals do: heavy furniture as the base layer, boxes stacked by weight, everything strapped and padded so the drive survives the interstate or the trip across town.",
   "Two movers at $100/hr with a two-hour minimum, pads and dollies included on local work. Most Karns loading jobs finish inside a few hours, and the same crew can unload at the other end or meet you at a storage unit. One call covers both sides of the move."]),
  ("Packing, Heavy Items, and Furniture Assembly", [
   "Between the packing, the heavy pieces, and the reassembly, moving day has three jobs nobody wants. We take all three: full and partial packing with proper materials, heavy-item crews for pianos, gun safes, and oversized furniture, and furniture assembly so beds, tables, and sectionals are usable the night you arrive — not leaning against a wall for a week.",
   "Farm outbuildings and workshops are common on Karns acreage — we move those too, including workbenches, tool chests, and riding-mower sheds' worth of gear. If it needs to get from the old place to the new one in one piece, it's our kind of job. Call (865) 936-3891 and describe what you've got; we'll tell you straight what crew it takes."]),
 ],
 "faqs": [
  ("How much does a move in Karns cost?", "Full-service moves run $140/hr for two movers plus the truck, with a one-hour service fee. Labor-only help is $100/hr for two movers with a two-hour minimum. Call for a straight answer based on your home size and distance."),
  ("Do you load rental trucks and containers in Karns?", "Yes — U-Haul, Penske, Budget trucks, PODS, and U-Box containers are regular jobs for us. We load them correctly so nothing shifts in transit."),
  ("Can you move a piano or safe at a Karns property?", "Yes. Our heavy-item crews handle pianos, gun safes, and oversized furniture with the right equipment and enough hands — including properties where the truck can't pull up close."),
  ("Do you serve areas around Karns?", "Absolutely — Powell, Halls, Hardin Valley, Oak Ridge, and all of northwest Knox County, plus greater Knoxville."),
 ],
 "related": [("Movers in Powell", "/movers-powell-tn/"), ("Movers in Hardin Valley", "/movers-hardin-valley-tn/"), ("Movers in Clinton", "/movers-clinton-tn/"), ("Labor-Only Moving", "/labor-only-moving/"), ("Local Moving", "/local-moving/")],
},
{
 "slug": "movers-clinton-tn",
 "title": "Movers in Clinton, TN | Angry Ducks Moving",
 "meta": "Movers in Clinton, TN — Angry Ducks Moving handles Clinton homes, rentals, and lake-area moves with full-service crews and labor-only loading. Call (865) 936-3891.",
 "canonical": BASE + "/movers-clinton-tn/",
 "crumb": "Movers in Clinton",
 "h1": "Movers in Clinton, TN",
 "area_served": "Clinton, TN (Anderson County)",
 "intro": "Clinton sits just north of Knoxville along the Clinton Highway (US-25W) corridor — the Anderson County seat, with a historic downtown, established neighborhoods, and lake-area communities around Melton Hill and the Norris Dam side of the Clinch River. Angry Ducks Moving runs Clinton moves regularly: full-service crews, labor-only loading help, and packing services for homes, rentals, and apartments across Clinton and greater Anderson County.",
 "sections": [
  ("Clinton Moves: Downtown, Neighborhoods, and Lake-Area Homes", [
   "Downtown Clinton's older homes are the charming kind and the complicated kind: narrow doorways, steep staircases, and porches built before anyone measured a sleeper sofa. We walk the carry route first, pad the tight spots, and bring the crew size that matches the house — most downtown jobs run smooth with three movers ($195/hr) instead of two movers stretching the day.",
   "Out toward the lake communities and the newer subdivisions, the challenge flips to access: long driveways, boat docks' worth of gear, and properties where the truck stages far from the front door. We plan the staging before the first box and keep the carry moving, so distance from truck to door doesn't eat your hourly clock. Tell us about your property when you book and we'll arrive with the right plan."]),
  ("Labor-Only Loading for DIY Movers", [
   "Clinton is a do-it-yourself kind of town, and labor-only is our most-booked job type here. Rent the truck or container — U-Haul, Penske, PODS, U-Box — and we'll load it the way professionals do: heavy furniture as the base layer, boxes stacked by weight, everything strapped and padded so the drive survives the interstate or the trip across Anderson County.",
   "Two movers at $100/hr with a two-hour minimum, pads and dollies included on local work. Most Clinton loading jobs finish inside a few hours, and the same crew can unload at the other end or meet you at a storage unit. One call covers both sides of the move."]),
  ("Full-Service Moves With Honest Pricing", [
   "Want the whole thing handled? Full-service means our crew, our truck, our pads and equipment: two movers plus the truck at $140/hr, three at $195/hr, four at $250/hr, plus a one-hour service fee that covers the truck, fuel, and gear. No vague quotes — call (865) 936-3891 and we'll give you a straight answer based on your home size and distance.",
   "We're licensed and insured, and we work Monday through Saturday, 7 AM to 8 PM. Furniture assembly, partial and full packing, and heavy items like pianos and safes are all in our wheelhouse — describe what you've got and we'll tell you honestly what crew it takes."]),
 ],
 "faqs": [
  ("How much does a move in Clinton cost?", "Full-service moves run $140/hr for two movers plus the truck, with a one-hour service fee. Labor-only help is $100/hr for two movers with a two-hour minimum. Call for a straight answer based on your home size and distance."),
  ("Do you load rental trucks and containers in Clinton?", "Yes — U-Haul, Penske, PODS, and U-Box loads are regular jobs for us. We load them correctly so nothing shifts in transit."),
  ("Do you serve areas around Clinton?", "Absolutely — Norris, Andersonville, Oak Ridge, Powell, Karns, and all of Anderson County, plus greater Knoxville."),
  ("Are you licensed and insured?", "Yes. Angry Ducks Moving is a licensed and insured moving company serving Clinton and East Tennessee."),
 ],
 "related": [("Movers in Karns", "/movers-karns-tn/"), ("Movers in Oak Ridge", "/movers-oak-ridge-tn/"), ("Movers in Powell", "/movers-powell-tn/"), ("Labor-Only Moving", "/labor-only-moving/")],
},
]

if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    urls = [BASE + "/"]
    for p in PAGES:
        d = os.path.join(out, p["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w") as f:
            f.write(render(p))
        urls.append(p["canonical"])
        print("wrote", p["slug"], len(render(p)), "bytes")
    with open(os.path.join(out, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url><loc>{u}</loc><changefreq>weekly</changefreq><priority>{'1.0' if u == BASE + '/' else '0.8'}</priority></url>\n")
        f.write("</urlset>\n")
    print("sitemap:", len(urls), "urls")
