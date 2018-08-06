from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import Categorys, Base, CatItems, User

# This code was from the Udacity course material but changed to
# to build out my example database.

engine = create_engine('sqlite:///waylandDatabase.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


User1 = User(
    name="Robert McMillen",
    email="rob.mcmillen@gmail.com",
    picture="""https://pbs.twimg.com/profile_images/2671170543
    /18debd694829ed78203a5a36dd364160_400x400.png""")
session.add(User1)
session.commit()


pistolesCat = Categorys(user_id=1, name='Pistols')

session.add(pistolesCat)
session.commit()

item1 = CatItems(
    user_id=1,
    name='Armat M4A3 Service Pistol',
    description="""Based on the Colt M1911. The standard issue
    sidearm for the USCM. Holds 12 rounds. Offers greater
    accuracy and firepower than other pistols but at
    a reduced rate of fire.""",
    categorys=pistolesCat)

session.add(item1)
session.commit()

item2 = CatItems(
    user_id=1,
    name='W-Y 88 Mod 4 Combat Pistol',
    description="""Based on the Heckler & Koch VP70.
    Constructed from nano-bound, hard impact plastics and other
    synthetic materials. Holds 18 rounds. Lower damage than
    the M4A3 but a higher rate of fire, and can be modified to
    full-auto.""",
    categorys=pistolesCat)

session.add(item2)
session.commit()

# Rifle Categorys
riflesCat = Categorys(user_id=1, name='Rifles')

session.add(riflesCat)
session.commit()

item1 = CatItems(
    user_id=1,
    name='Armat M41A Pulse Rifle MK2',
    description="""Updated version of the M41A seen in Aliens. The
    M41A Pulse Rifle MK2 is the standard issue weapon of the Colonial
    Marines in the game. Fires 10mm explosive-tipped caseless rounds.
    Features additional customization options including a variety of
    underbarrel launcher attachments. Total magazine capacity has been
    reduced from 99 rounds to 40 rounds, presumably for balance, although
    an extended magazine can increase the capacity to 60 rounds.""",
    categorys=riflesCat)

session.add(item1)
session.commit()

item2 = CatItems(
    user_id=1,
    name='W-Y NSG 23 Assault Rifle',
    description="""Mid-ranged 7.62mm burst fire assault rifle.
    Holds 30 rounds.Has a noticeably lighter action compared to
    competitors, with more controllable firing patterns as a result.""",
    categorys=riflesCat)

session.add(item2)
session.commit()

item3 = CatItems(
    user_id=1,
    name='Armat M4RA Battle Rifle',
    description="""Semi-automatic mid- to long-range bullpup marksman rifle.
    Has a 15 round magazine. Mounts a variety of underbarrel attachments and
    several different optics for differing situations. """,
    categorys=riflesCat)

session.add(item3)
session.commit()

subCat = Categorys(user_id=1, name='Submachines')

session.add(subCat)
session.commit()

item1 = CatItems(
    user_id=1,
    name='Armat M39 Submachine Gun',
    description="""Compact sub-machine gun with a high rate of fire. Holds 48
    rounds, which can be extended to 72 rounds. """,
    categorys=subCat)

session.add(item1)
session.commit()

shotgunCat = Categorys(user_id=1, name='Shotguns')

session.add(shotgunCat)
session.commit()

item1 = CatItems(
    user_id=1,
    name='Armat M37A2 Pump Shotgun',
    description="""Based on the Ithaca Model 37 "Stakeout". Holds 8 rounds.
    Offers better firepower and accuracy than the tactical shotgun but with
    noticeably less customization and a slower rate of fire and
    reload speed. """,
    categorys=shotgunCat)

session.add(item1)
session.commit()

item2 = CatItems(
    user_id=1,
    name='W-Y MK221 Tactical Shotgun',
    description="""Based on the Benelli M4 Super 90. A close-range
    self-loading semi-automatic weapon made from heat resistant alloys
    that is capable of firing rapid shots in quick succession without
    overheating. Holds 8 rounds. Highly effective in tight spaces
    but inaccurate at long range due to spread. """,
    categorys=shotgunCat)

session.add(item2)
session.commit()

item3 = CatItems(
    user_id=1,
    name='W-Y MK221 Tactical Shotgun',
    description="""Based on the Benelli M4 Super 90. A close-range
    self-loading semi-automatic weapon made from heat resistant
    alloys that is capable of firing rapid shots in quick succession
    without overheating. Holds 8 rounds. Highly effective in tight spaces
    but inaccurate at long range due to spread. """,
    categorys=shotgunCat)

session.add(item3)
session.commit()

heavyCat = Categorys(user_id=1, name='HeavyWeapons')

session.add(heavyCat)
session.commit()

item1 = CatItems(
    user_id=1,
    name='M56 Smartgun',
    description="""Powerful machine gun with auto-aim and target tracking
    capabilities.""",
    categorys=heavyCat)

session.add(item1)
session.commit()

item2 = CatItems(
    user_id=1,
    name='M240 Incinerator Unit',
    description="""The M240 Incinerator Unit is capable of producing a lethal
    burst of intense flame, devastating against organic targets but potentially
    hazardous to the user. """,
    categorys=heavyCat)

session.add(item2)
session.commit()

item3 = CatItems(
    user_id=1,
    name='UA 571-C Automated Sentry Gun',
    description="""While not a usable weapon, UA 571-C Automated Sentry Guns
    can be moved and placed by the player to help them defend an area from
    attack. """,
    categorys=heavyCat)

session.add(item3)
session.commit()
