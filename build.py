#!/usr/bin/env python3
"""Builds landlords/index.html and owners/index.html from template.html. Run: python3 build.py"""
import os, html
T = open("template.html").read()
def li(items): return "".join(f"<li>{x}</li>" for x in items)
def opts(name, items): return "".join(f'<label><input type="radio" name="{name}" value="{html.escape(v)}"{" required" if i==0 else ""}><span>{html.escape(v)}</span></label>' for i, v in enumerate(items))
def how(items): return "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in items)
def checks(items): return "".join(f"<li><b>{a}</b>{b}</li>" for a, b in items)
def faq(items): return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)

PAGES = {
 "landlords": dict(
  title="Guaranteed rent for your property | BA Properties",
  meta="Lease your St. Louis or Indianapolis property to BA Properties. Rent paid on time every month, with no vacancies and no turnover.",
  og="2930-hickory-01.jpg", hero="2930-hickory-01.jpg",
  kicker="For St. Louis &amp; Indianapolis landlords",
  h1="Get paid rent every month, even when it’s empty.",
  sub="BA Properties leases your property, furnishes it and hosts vetted traveling professionals. You get the same rent on the same day every month. No vacancies, no turnover, no tenant calls.",
  ticks=li(["Guaranteed rent, booked or not","Staff and VAs watching your property around the clock","Not one party in several years"]),
  q1="See what we’d pay for your property", cta1="Get my rent offer",
  q1b_label="What kind of property is it?", q1b=opts("q1b",["Single-family house","Condo or townhome","Apartment / unit in a multi-family","Whole multi-family building"]),
  q2_label="What’s the situation right now?", q2=opts("q2",["Vacant now","Tenant leaving in the next 90 days","Tenant in place, just exploring"]),
  q3="Where should we send your offer?", cta3="Send my rent offer",
  done="We’ll look up your property and reach out within one business day to set up a quick walkthrough.",
  how_h="From first call to first rent payment",
  how=how([("Tell us about the property","Two minutes on this page, or a quick call."),("We walk it and make an offer","A standard lease with BA Properties as your tenant, with rent and terms in writing."),("We set it up, you get paid","We furnish and run it. Your rent lands on a fixed date every month.")]),
  cover_k="What’s covered", cover_h="You own it. We handle everything else.",
  cover=checks([("Rent on a fixed date","Whether or not it’s booked that month."),("Watched around the clock","Our full team of VAs and staff monitors every property, day and night."),("No parties in several years","Guests are screened before every booking, and noise sensors and entrance cameras back that up."),("Guests pay for damage, not you","We handle the Airbnb AirCover claims ourselves and make sure the guest pays for any damage."),("Our own crew","Our own cleaners, staff and handyman, so the property is kept up by people we trust."),("Liability insurance","Our policy covers the property while we lease it.")]),
  faq=faq([("Is this subletting?","Yes, with your written permission. BA Properties signs the lease as your tenant and hosts furnished stays in the property. Nothing happens without your approval in the lease."),
           ("What if it doesn’t book?","You still get paid. The rent is ours to pay on the agreed date, whether or not the property is booked."),
           ("Who pays for damage?","The guest does. We file and manage the Airbnb AirCover claim and make sure any guest damage is paid for. Our own handyman takes care of everyday wear and tear."),
           ("What about parties?","We haven’t had a party in several years. Every guest is screened, and our team monitors every property around the clock."),
           ("How much rent will you pay?","It depends on the property, its location and its condition. We’ll look at it and give you a number in writing. Step one is the form above."),
           ("Which areas do you work in?","St. Louis city and county, and Indianapolis. If you’re elsewhere, send it anyway and we’ll tell you honestly if it fits.")]),
  final_h="Find out what we’d pay for your property.", final_p="Two minutes, no obligation. We reply within one business day.",
  sticky="Get my rent offer"),
 "owners": dict(
  title="Airbnb management in St. Louis &amp; Indianapolis | BA Properties",
  meta="Keep your listing and your reviews. BA Properties runs your Airbnb with the same team behind 1,852 guest reviews averaging 4.82 stars.",
  og="greenest-01.jpg", hero="greenest-01.jpg",
  kicker="For St. Louis &amp; Indianapolis Airbnb owners",
  h1="Your Airbnb, without the 2 a.m. messages.",
  sub="The team behind 1,852 guest reviews averaging 4.82 stars will run your listing. You keep your account and your reviews, and pay one fee that’s in writing.",
  ticks=li(["A professional revenue manager pricing your home","A full VA team on every stay, around the clock","A performance report every month"]),
  q1="Get your free earnings estimate", cta1="Get my free estimate",
  q1b_label="Is it on Airbnb or VRBO now?", q1b=opts("q1b",["Yes, I manage it myself","Yes, with a manager or co-host","Not yet, I’m planning to list it"]),
  q2_label="What do you want most?", q2=opts("q2",["More revenue","My time back","Better reviews and guests","All of the above"]),
  q3="Where should we send your estimate?", cta3="Send my free estimate",
  done="We’ll pull the numbers for your address and send your estimate within one business day.",
  how_h="Three steps, and you’re off the phone",
  how=how([("Free earnings estimate","What your home should earn, based on comparable listings and the local event calendar."),("We join as co-host","Your account, your listing, your reviews. You can see every message and booking."),("We run it, you get a monthly report","Pricing, guests, cleaning and maintenance are on us. You get a professional report every month.")]),
  cover_k="What you get", cover_h="Everything we do for our own 12 homes.",
  cover=checks([("A professional revenue manager","We pay a dedicated revenue manager to price every night, around Cardinals games, conventions, Mardi Gras and slow winter weeks."),("A full team, around the clock","Our VAs and staff handle guest questions, lockouts and late check-ins, day and night."),("Our own cleaners, staff and handyman","Reliable people we employ, at fair prices, with no middleman markup."),("Guests pay for damage","We handle the Airbnb AirCover claims and make sure guests pay for anything they break."),("No parties in several years","Every guest is screened, and every stay is monitored."),("A professional report every month","How your home performed, and every dollar in and out.")]),
  faq=faq([("What does it cost?","One percentage of booking revenue, quoted in writing with your estimate. No hidden fees, and we don’t add guest fees that we keep."),
           ("Do I lose my listing or reviews?","No. We join your existing listing as a co-host. It stays in your account."),
           ("Is there a long contract?","We’ll put the terms, including how to end it, in writing before you sign anything."),
           ("Will a manager just price it low to fill it?","No. We price for revenue, not occupancy. Weekends and event dates are where most of the money is, and we price them that way."),
           ("What about parties and damage?","We haven’t had a party in several years. If a guest damages anything, we handle the AirCover claim and make sure the guest pays."),
           ("Which areas do you cover?","St. Louis city and county, and Indianapolis.")]),
  final_h="See what your Airbnb should be earning.", final_p="Free estimate for your address. Two minutes, no obligation.",
  sticky="Get my free estimate"),
}
for slug, c in PAGES.items():
    h = T
    for k, v in c.items(): h = h.replace("{{%s}}" % k, v)
    h = h.replace("{{offer}}", slug)
    assert "{{" not in h, [x for x in h.split("{{")[1:3]]
    os.makedirs(slug, exist_ok=True); open(f"{slug}/index.html", "w").write(h)
print("built", list(PAGES))
