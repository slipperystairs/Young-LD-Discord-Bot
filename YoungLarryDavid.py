import asyncio
import random
import time
import discord
import os
import sys
import string
import lyrics
from spit import init_markov
from spit import spit_game
from discord.ext.commands import Bot
from discord.ext import commands
from collections import defaultdict

BOT_PREFIX = ("+")

client = Bot(command_prefix=BOT_PREFIX)
#client.remove_command('help') will fix this later
"""    
    TODO
    List of potential artist
     - Kendrick
     - Trick Daddy
        - add to random
     - Tupac
    Hip-Hop Facts
    
"""
kanye_lyrics = [
    'The same people that tried to blackball me forgot about two things: my black balls',
    'What’s a black Beatle anyway? A fucking roach? I guess that’s why they got me sitting in fucking coach',
    'Have you ever had sex with a pharaoh? Put the pussy in a sarcophagus. Now she claiming that I bruised her esophagus',
    'My apologies, are you into astrology. Cause I’m tryin’ to make it to Uranus',
    'I keep it 300 like the romans',
    'They be ballin in the D-League. I be speaking Swaghili',
    'And if life’s a bitch, bet she suck my dick, huh I bet she fucked the whole clique, huh',
    'Eatin Asian pussy, all I need was sweet and sour sauce',
    'I just talked to Jesus. He said “What up, Yeezus?!?” I said “Shit, I’m chillin tryna stack these millions',
    'Mayonnaise-colored Benz, I push Miracle Whips'
    'Now, if I fuck this model.\n' + 'And she just bleached her asshole\n' +
    'And I get bleach on my T-shirt\n' + 'I\'ma feel like an asshole'
]

gucci_lyrics = [
    'Overdose of sauce, no meat, just sauce',
    'I pushed a lot of pills, a lot of peas, a lot of powder, It\'s Gucci Mane La Fleur and jiggalo ya cowards.',
    'Gucci Mane broke; pussy nigga is ya stupid?',
    'Trap boys get bricks, athletes get trophies Gucci mane got cake, it\'s my birthday party Want a sweet 16? Thats two times forty!!',
    'My chain got ammonia, watch got the bird flu. Came to the club smellin like a pound of purple.',
    'Still got nasal flow I think I need some claritin.',
    'Girls are like buses, miss one, next fifteen, one comin.',
    'Dope fiend Willie used to finger fuck my rims',
    'Wanna be like Gucci? Little buddy eat your vegetables.',
    'That made me laugh ’cause I’m the king. I cut your head off like the jester',
    'My jewelry game sick, I think my jeweler need chemo',
    'I love bad bitches, so I’m a lesbian.',
    'I don’t feel you cuz I’m paraplegic, where’s my paralegal?',
    'Gucci trap-a-nometry I’m a hustle-ologist.Way I make it rain you could call me meteorologist',
    'Gucci so flossy, all my broads are bossy. Head til’ I’m nauseous, they keep me exhausted',
    'Gucci Mane crazy I might pull up on a zebra. Land on top a eagle smoke a joint of reefa',
    'Like a pigeon in the sky, I just shitted on your ride',
    'Ain\'t got no comparison and I ain\'t being arrogant.',
    'I ball all through the winter and I stunt all through the summer.',
    'I don\'t give a damn how you feel about me, I sip lean pure codeine and I don\'t give a damn what you say about me.',
    'I\'m icy, I\'m icy. So icy, so icy.',
    'A trapper but this rappin got me going places you\'ll never go!',
    'Think I’m a clone but if they cut me this sauce gon’ ooze out',
    'Hi my name is Gucci Mane, I’m addicted to everything. Bad bitch, fast cars, weed and promethazine',
    'If a man does not have the sauce, then he is lost. But the same man can be lost in the sauce.',
    'I stay higher than giraffe pussy',
    'Like a pigeon in the sky, I just shitted on your ride',
    'Gucci Mane broke; pussy nigga is ya stupid?',
    'Trap boys get bricks, athletes get trophies Gucci mane got cake, it\'s my birthday party Want a sweet 16? Thats two times forty!!',
    'Gucci so flossy, all my broads are bossy. Head til’ I’m nauseous, they keep me exhausted'
]

random_lyrics = [
    'Like a pigeon in the sky, I just shitted on your ride',
    'I’m far from broke, got enough bread And mad hoes, ask Beavis I get nothing Butthead',
    'I jumped out the Lincoln, left him stinkin. Put his brains in the street. Now you can see what he was just thinkin',
    'I got drug spots from new york to canada. Cause big l be fuckin with more keys than a janitor',
    'I’m quick to bust a mean nut in some teen slut. Big L is clean-cut with more jewels than King Tut',
    'And when it comes to gettin nookie. I’m not a rookie, I got girls that make that chick Toni Braxton look like Whoopie',
    'Since the burial of Jesus, fuck around and catch all the venereal diseases',
    'Put a hanger on a fuckin stove and let that shit sit there for like a half hour, take it off and stick it in your ass slow like Tssssssss',
    'I\'ll fuckin, I\'ll fuckin cut your kneecaps off and make you kneel in some staircase piss',
    'My chain got ammonia, watch got the bird flu. Came to the club smellin like a pound of purple.',
    'I\'ll fuckin\'...I\'ll fuckin...sew your asshole closed and keep feeding you, and feeding you, and feeding you, and feeding you.',
    'It\'s the nick nack patty wack, I still got the biggest sack.',
    'Numbing up your tonsils, like ambesol anesthetic. Cummin down your throat like chloraseptic',
    'I\'m stickin\' ice picks on the tip of ya dick. Give your testicles a swift kick, ain\'t that some shit?',
    'I scored 1.1 on my SATs, but I still push a whip with a right and left AC.',
    'Next time I\'m feeling kinda horny\nYou can come on over\nAnd I\'ll break you off\nAnd if you can\'t fuck that day baby\nJust lay back and open your mouth\nCause I have never met a girl\nThat I love in the whole wide world.',
    'For a trill, working the wheel, a pimp not a simp\nKeep the dope fiends higher than the Goodyear Blimp',
    'I\'m trapping like a fool, 30 inches on the Hummer ride\nMad \'cause I killed your buddy and I beat the homicide',
    'Young Juiceman whip more chickens than Popeye\'s\nBouldercrest working and I\'m still whipping cream pies',
    'Matter of fact, nigga, just call me when you need some dope'
]

nas_lyrics = [
    'Rappers, I monkey flip \'em with the funky rhythm I be kickin\'\nMusician inflictin\' composition of pain\nI\'m like Scarface sniffin\' cocaine\nHoldin\' an M16, see with the pen I\'m extreme',
    'It drops deep as it does in my breath\nI never sleep—cause sleep is the cousin of death\nBeyond the walls of intelligence, life is defined.\nI think of crime when I\'m in a New York state of mind',
    'I sip the Dom P, watchin\' Gandhi \'til I\'m charged, then\nWritin\' in my book of rhymes, all the words past the margin.\nBehold the mic I\'m throbbin\', mechanical movement\nUnderstandable smooth shit that murderers move with\nThe thief\'s theme, play me at night, they won\'t act right',
    'Yet I\'m the mild, money-gettin\' style, rollin\' foul\nThe versatile, honey-stickin\', wild, golden child\nDwellin\' in the Rotten Apple, you get tackled\nOr caught by the devil\'s lasso, shit is a hassle',
    'There\'s no days for broke days\nWe sell it, smoke pays, while all the old folks pray\nTo Jesús, soakin\' their sins in trays of holy water',
    'I\'m the young city bandit, hold myself down single-handed\nFor murder raps, I kick my thoughts alone, get remanded\nBorn alone, die alone, no crew to keep my crown or throne\nI\'m deep by sound alone, caved inside, 1,000 miles from home.',
    'I rap for listeners, bluntheads, fly ladies, and prisoners\nHennessy-holders and old-school niggas, then I be dissin\'a\nUnofficial that smoke Woolie Thai\nI dropped out of Cooley High, gassed up by a cokehead cutie pie',
    'Yo, they call me Nas, I\'m not your legal type of fella\nMoët drinking, marijuana smoking street dweller\nWho\'s always on the corner, rolling up blessed\nWhen I dress, it\'s never nothing less than Guess',
    'Nas is like the Afrocentric Asian: half-man, half-amazin\'\n‘Cause in my physical I can express through song\nDelete stress like Motrin, then extend strong\nI drink Moët with Medusa, give her shotguns in Hell\nFrom the spliff that I lift and inhale; it ain\'t hard to tell',
    'This rhythmatic explosion\nIs what your frame of mind has chosen\nI\'ll leave your brain stimulated, niggas is frozen\nSpeak with criminal slang, begin like a violin\nEnd like Leviathan,it\'s deep? Well, let me try again',
    'My poetry\'s deep, I never fell\nNas\'raps should be locked in a cell; it ain\'t hard to tell'
]

E40_lyrics = [
    'Ever told on a nigga? (nope)\nEver squeezed a trigger? (yup)',
    'Ever set a nigga up? (nope)\nEver helped a brother out when he was down on his luck? (yup)',
    'You a sap? (nope)\nYou a boss player, you a mack? (yup)',
    'Starving? (nope), Dinner? (yup)',
    'You still sell dope? (nope)\nNow you cleaner than a bar of Dove soap? (yup)',
    'Everybody get choices\nI choose to get money, I\'m stuck to this bread\nEverybody got choices\nThese bitches is choosin\', I\'m all in they head',
    'Ugh, lazy? (nope)\nGot dick that\'ll drive a ho crazy? (yup)',
    'Sleep? (nope), Bust moves, hella active in the streets? (yup)',
    'Star Wars? (nope), Yoda? (yup)',
    'Was it love at first sight? (nope)\nDid she ride you like a bike? (yup)\nWas it ripe? (nope), Was her pussy tight? (yup)',
    'Your team weak? (nope)\nYou respected in the stree-neets? (yup)',
    'I don\'t like suckas in my mix (mmm mmm)\nGot my name in their mouth like tooth picks (uh huh)',
    'I don\'t pay for pussy, not a John (mmm mmm)\nSucka shit contagious like a yawn (uh huh)',
    'Never will I go to war over a ho (mmm mmm)\nBitch I\'m a motha fuckin\' buffalo (uh huh)',
    'Out of date like old people? (mmm mmm)\nIn the loop like sewing needle? (uh huh)',
    'You weak at shootin\' dice? (mmm mmm)\nYou really \'bout that life? (uh huh)',
    'You eat booty? (mmm mmm)\nYou lick coochie? (uh huh)\nBiatch!',
    'Divorced from the streets? (mmm mmm)\nBe in Dubai with the sheiks? (uh huh)',
    'Pan handlin\'? (mmm mmm)\nShippin\' and handlin\'? (uh huh)'
]

snoop_dogg_lyrics = [
    'He fucked the fleas off a bitch.\nHe shaked the ticks off his dick.\nAnd in the booty, he buries his motherfuckin\' bone.\nAnd if there\'s any left over\nHe\'ll roll over and take a doggy bag home',
    'Shit, I got a pocket full of rubbers and my homeboys do too\nSo turn off the lights and close the doors\nBut (but what?) we don\'t love them hoes, yeah\nSo we gon\' smoke a ounce to this\nG\'s up, hoes down, while you motherfuckers bounce to this.',
    '‘Cause when I bust my nut I\'m raising up off the cot\nDon\'t get upset, girl, that\'s just how it goes\nI don\'t love you, hoes, I\'m out the door, and I\'ll be...',
    'Guess who back in the motherfucking house\nWith a fat dick for your motherfucking mouth',
    'Now as the sun rotates and my game grows bigger\nHow many bitches wanna fuck this nigga named Snoop\nDoggy, I\'m all the above\nI\'m too swift on my toes to get caught up with you hoes\nBut see it ain\'t no fun\nIf my homies can\'t get a taste of it\nCause you know I don\'t love em',
    'Some of these niggas is so deceptive\nUsing my styles like a contraceptive\nI hope you get burnt\nSeems you haven\'t learnt\nIt\'s the knick-knack, patty-whack\nI still got the biggest sack!',
    'Speaking of hoes, I\'ll get to the point\nYou think you got the bomb cause I rolled you a joint?',
    'You\'se a flea, and I\'m the Big Dogg,\nI\'ll scratch you off my balls with my motherfuckin\' paws',
    'So I ain\'t holdin nuttin\' back\nAnd motherfucker, I got five on that twenty sack\nIt\'s like that and as a matter of fact (rat-tat-tat-tat)\n\'Cause I never hesitate to put a nigga on his back',
    'Yeah roll up the dank, and pour the drank\nAnd watch your step (why?) \'cause Doggy\'s on the gank',
    'Layin that, playin that G Thang\nShe want the nigga with the biggest nuts, and guess what?\nHe is I, and I am him, slim with the tilted brim\nWhat\'s my motherfuckin name?'
]

three_six_lyrics = [
    'Bitch don\'t play dumb\nStick out your tongue\nAnd let me take a plunge\nFor plenty you don\'t have to suck your thumb\nI got yum-yum',
    'Slob on my knob\nLike corn on the cob\nCheck in with me\nAnd do your job\nlay on the bed\nAnd give me head\nDon\'t have to ask\nDon\'t have to beg',
    'These bitches got me goin\'\nThe feelin\' of a warm mouth\nMan I tell you bout\' these hoes chewin\' in the South',
    'On through the wall now she howlin\' like a dog swept poor\nWe hit the floor it don\'t quit\nAnother one break it\'s just another victim of Lord Infamous late night tip',
    'Lord Infamous, the futuristic rowdy bounty hunter\nNigga, I come from the land down under',
    'Ten times out of twelve\nNine times out of ten\nGansta Boo is in it to win',
    'When I say weak ass, you say bitch!\nWeak ass, bitch!, weak ass, bitch!',
    'You ol\' pussy-ass, cake-ass, punk-ass, trick-ass, sucker-ass,\nFuck-ass, dick-in-the-booty-ass, K-Y Jelly-packing-ass nigga',
    'Yeah, nigga, y\'all know the motherfucking sco\', y\'all non-snorters, non-smokers, non-sippers,\nGet the fuck up out of here, bitch\nNigga, it\'s some sipping-ass, pouring up-ass, smoking-ass, getting high-ass niggas in here,\nThree 6, UGK, nigga, we putting it down in this motherfucker\nAnd we ain\'t playing wit\'chu, y\'all know the motherfucking sco\', homie\nNow pour it up, nigga.',
    'People always asking me, is the Three 6 high on that?\nRolling on them X pills, stuttering, pup-pup powder packs',
    'Woah, where the weed at, ain\'t like that we need that\nNyQuil will slow me down, something that keep me easy\nNothing like that yella yella, that\'ll have you itching, man\nTalking like, what\'s up, fool? Vocal chords sounding lame',
    'Gone on coke, eyes all bucked, this here shit\'ll knock you down\nKnock you out, make you fall asleep when you\'re on them wheels',
    'She popped her a pill of X, and drank on some orange juice\nAnd just when you thought she was freaking, she done got super loose',
    'Juice got weed Juice got pills\nJuice got the work on the corner cuttin deals',
    'We ball out in the club wit our niggaz stayin trill\nWe never wrote a check just them big face bills\nA playa drinkin Makers, Marker, cranberry vodka\nWearin a mink coat thats furry as Chewbacca',
    'Nose all runny\nFound a snow bunny\nTake her to da\' crib\nMake her drink cummy',
    'Cocaine Blaine that\'s my dog\nI called him up to house this slut\nWe gon\' fuck her in the back of da\' bus\nAnd fill her nose up full o\' dat\' dust',
    'In da\' bathroom \'bout two whole hours\nGettin\' real high passed out on the floor\nFuck that shit niggas\' on the frame\nTake \'em 1 on 1 back in the game',
    'Used to be my nigga\nNow you fake\nBut I stomp on you trick in the grass\nYou little snake bitch'
]

project_pat_lyrics =[
    'I ain\'t goin\' back to jail, I ain\'t goin\' back to jail\nI got mo\' pussy to swell, and mo\' dreams to tell',
    'Bullets do fly through air when them guns p-poppin\'\nPistol swang to ya mouth, then the blood is gushin\'',
    'Cross killers in these streets, bullets will spray\nInnocent bystander can catch a stray ya dig?',
    'Put two dollars in the air, for these two dollar niggas\nThey get mad and they fuss, they don\'t shine like us',
    'I\'m flickin\' on you snakes, I got wood, leather stitchin\'\nClothes stickin\', cause ya ridin\' bucket, cloth seats itchin\'',
    'Couldn\'t get me, saw it in the clouds, like my nigga Rickey\nMr. James, all these superfreaks, out here tryna get me',
    'Wanna hit me, wanna say, they done been \'round the truth\nIn ya bed, or the booth, I\'m the ghetto Dr. Ruth',
    'When I do, step on out, moonlight, hit the Range\nPretty jewels they attract broads, like shiny thangs',
    'When I came, to ya hood, I was new face, in the place\nGame spitter from the North, so ya wanna catch a case',
    'Cause ya see me holl\'in\' at \'cha ex-girl, don\'t \'cha?\nMurder charge for a broad who don\'t even want \'cha',
    'You suckers crazy, so y\'all out here pushin\' daisies\nOver Daisy, she was on some purple hazey',
    'Had the baby, year later on my income\nTax, so a nigga could receive mo\' income',
    'Hangin\' stout broads, \'round my arms, decoration\nThese punks give me dap, same time playa hation',
    'Erasin\', you lamers, hatin\' got\'cha famous\nConfronted by the broad, got shot in ya anus\nHeinous, heard they took the slugs out\'cha dookie roll\nGun powder and the blood burn in ya bootyhole',
    'Wanna fight, my nigga, wanna shoot, my nigga\nTalk ya gal out her cap, when ya loot my nigga',
    'Do you, my nigga, fall in love wit\' these tramps\nGoin\' raw, on her, and she did the whole Camp?\nBut you rest havin\' that, knowin\' that, she\'ll go\nLickin\' balls, suckin\' cat, knees burnt from the flo\'',
    'She got a bubble gum cap with a Gucci dats snappin\'\nWith some rhino legs and a booty that\'s flappin\'\nWith some fire-oh head \'cause you know we love cappin\'\nGot her toes done up with her fingernails matchin\'',
    'Here dat big ol\' butt that you\'re walkin\' cross the street with\nPeep this, for a happy meal can I squeeze it?',
    'Them freaky freaks I heard on the loose, let ya pockets out\nGot trick niggaz watchin\' your caboose with they wallets out',
    'You should stop, lil\' somethin\' somethin\' bad to the bone\nThat ain\'t a monkey hangin\' off ya back that\'s Donkey Kong',
    'Good googly moogly, that thang is juicy',
    'How you gon\' prance around with all that, sayin\' you ain\'t all that, Everybody at ya wanna hit ya like a ball bat',
    'That thang make ya look back, be like man who is that\nYou can see a hiny on a hiny I\'m pursuin\' that',
    'A dirty south hoody rat tryin\' to hold goodies back Waist like a wasp, butt cheeks pokin\' really fat',
    'I\'m Crown Vic old school, squeezin\' on her boo-boo\nHugged up, pokin\' in her brains so what ya wanna do',
    'You can call me Mister Whipple, I won\'t do no harmin\'\nNever to the Charmin, come holla at me woman',
    'Bwok bwok, chicken chicken\nBwok bwok, chicken heads',
    'Bald-head skally-wag\nAin\'t got no hair in back\nGelled up weaved up\nYo hair is messed'
]

wu_tang_lyrics = [
    'Ghostface catch the blast of a hype verse\nMy Glock burst, leave in a hearse, I did worse',
    'Aww shit, Wu-Tang Clan spark the wicks, an\'\nHowever I master the trick just like Nixon',
    'Causin\' terror, quick damage your whole era\nHard rocks is locked the fuck up, or found shot',
    'I watch my back like I\'m locked down\nHardcore-hittin\' soundn\nWatch me act bugged and tear down\nIlliterate-type asshole, songs goin\' gold',
    'Yeah, they fake and all that, carryin\' gats\nBut yo, my Clan rollin\' like forty macks\nNow you act convinced, I guess it makes sense\nWu-Tang, yo, soooo represent!',
    'And that\'s one in the chamber, Wu-Tang banger\n36 styles of danger',
    'I rip it hardcore, like porno-flick bitches\nI roll with groups of ghetto bastards with biscuits',
    'Check it, my method on the microphone\'s bangin\'\nWu-Tang slang\'ll leave your headpiece hangin\'',
    'Redrum, I verbally assault with the tongue\nMurder One, my style shocks your knot like a stun gun',
    'Set it on the microphone, and competition get blown\nBy this nasty-ass nigga with my nigga, the RZA\nCharged like a bull and got pulled like a trigga\nSo bad, stabbin\' up the pad with the vocab, crab\nI scream on your ass like your dad, bring it on...',
    'Yo, I\'m more rugged than slave man boots\nNew recruits, I\'m fuckin\' up MC troops\nI break loose, and trample shit, while I stomp\nA mudhole in that ass \'cause I\'m straight out the swamp',
    'I blow up his fuckin\' prism, make it a vicious act of terrorism\nYou wanna bring it, so fuck it, come on and bring the ruckus!',
    'En garde, I\'ll let you try my Wu-Tang style.',
    'Shame on a nigga who try to run game on a nigga\nWu buck wild with the trigger',
    'Shame on a nigga who try to run game on a nigga\nWu buck… I\'ll fuck your ass up!',
    'Ol\' Dirty Bastard, live and uncut\nStyles unbreakable, shatterproof\nTo the young youth, you wanna get gun? Shoot!\nBlaow! How you like me now?',
    'Don\'t fuck the style, ruthless wild\nDo you wanna get your teeth knocked the fuck out?\nWanna get on it like that? Well, then shout!',
    'Yo RZA, yo razor, hit me with the major\nThe damage, my Clan understand it be flavor\nGunnin\', hummin\', comin\' at ya First I\'m gonna get ya, once I got ya, I gat ya',
    'You could never capture the Method Man\'s stature\nFor rhyme and for rapture, got niggas resignin\', now master\nMy style? Never!',
    'I put the fuckin\' buck in the wild kid, I\'m terror, razor sharp, I sever\nThe head from the shoulders, I\'m better than my competta\nYou mean competitor, whatever, let\'s get together',
    'So, when you see me on the real\nFormin\' like Voltron, remember I got deep like a Navy Seal',
    'Burn me, I get into shit, I let it out like diarrhea\nGot burnt once but that was only gonorrhea',
    'The Wu is comin\' through, the outcome is critical\nFuckin\' with my style is sort of like a miracle',
    '\'Cause I don\'t know you, therefore show me what you know\nI come sharp as a blade and I cut you slow',
    'You become so Pat as my style increases\nWhat\'s that in your pants? Ahh, human feces!\nThrow your shitty drawers in the hamper\nNext time, come strapped with a fuckin\' Pamper',
    'Can it be that it was all so simple then?\nDedicated to the 5\'s, 850i\'s\n(Dedicated to niggas who do drive-by\'s)',
    'Raw I\'ma give it to ya, with no trivia\nRaw like cocaine straight from Bolivia',
    'Well, I\'m a sire, I set the microphone on fire\nRap styles vary and carry like Mariah',
    'I come from the Shaolin slum, and the isle I\'m from\nIs comin\' through with nuff niggas and nuff guns\nSo if you wanna come sweatin\', stressin\', contestin\'\nYou\'ll catch a sharp sword to the midsection',
    'Rough like Timberland wear, yeah\nMe and the Clan in \'Yota Landcruisers out there\nPeace to all the crooks, all the niggas with bad looks\nBald heads, braids, blow this hook',
    'I only been a good nigga for a minute though\n\'Cause I got to get my props and win it, yo',
    'I got beef with commercial-ass niggas with gold teeth\nLampin\' in a Lexus, eatin\' beef\nStraight up and down, don\'t even bother\nI got 40 niggas up in here now who kill niggas\' fathers',
    'My peoples, are you with me? Where you at?\nIn the front, in the back, Killa Bees on attack',
    'My peoples, are you with me? Where you at?\nSmokin\' meth, hittin\' cats on the block with the gats',
    'Homicide\'s illegal and death is the penalty\nOne justifies the homicide when he dies in his own iniquity?',
    'The flow changes like a chameleon\nPlays like a friend and stabs you like a dagger\nThis technique attacks the immune system\nDisguised like a lie, paralyzin\' the victim',
    'You scream as it enters your bloodstream\nErupts your brain from the pain these thoughts contain\nMovin\' on a nigga with the speed of a centipede\nAnd injure any motherfuckin\' contender',
    'And the survey said you\'re dead\nFatal Flying Guillotine chops off your fuckin\' head',
    'And if you want beef, then bring the ruckus!\n Wu-Tang Clan ain\'t nuthing ta fuck wit',
    'Straight from the motherfuckin\' slums that\'s busted\nWu-Tang Clan ain\'t nuthing ta fuck wit',
    'Like déjà vu, I\'m rubber, niggas is like glue\nWhatever you say rubs off me sticks to you',
    'I grew up on the crime side, the New York Times side\n Stayin\' alive was no jive',
    'But it was just a dream for the teen who was a fiend\nStarted smokin\' woolies at 16',
    'No question I would speed for cracks and weed\nThe combination made my eyes bleed',
    'No question I would flow off and try to get the dough all\nStickin\' up white boys in ball courts',
    'Cash rules everything around me\nC.R.E.A.M., get the money\nDollar dollar bill, y\'all',
    'A man with a dream with plans to make cream\nWhich failed; I went to jail at the age of fifteen\nA young buck sellin\' drugs and such, who never had much\nTryin\' to get a clutch at what I could not',
    'The court played me short, now I face incarceration\nPacin\', goin\' upstate\'s my destination\nHandcuffed in the back of a bus, forty of us Life as a shorty shouldn\'t be so rough',
    'But as the world turned I learned life is hell\nLivin\' in the world no different from a cell',
    'But shorty\'s runnin\' wild, smokin\' sess, drinkin\' beer\n And ain\'t tryin\' to hear what I\'m kickin\' in his ear\nNeglected for now, but yo, it gots to be accepted\nThat what? That life is hectic',
    'I smoke on the mic like "Smokin\' Joe" Frazier\n The hell-raiser, raisin\' hell with the flavor',
    'Terrorize the jam like troops in Pakistan\n Swingin\' through your town like your neighborhood Spider-Man',
    'Call me the rap assassinator\nRhymes rugged and built like Schwarzenegger',
    'It\'s the Method Man, for short Mr. Mef\nMovin\' on your left, UH!',
    'And set it off, get it off, let it off like a gat\nI wanna break, fool, cock me back',
    'First things first, man, you\'re fuckin\' with the worst\nI\'ll be stickin\' pins in your head like a fuckin\' nurse',
    'Niggas be rollin\' with a stash, ain\'t sayin\' cash\nBite my style, I\'ll bite your motherfuckin\' ass',
    'Crazy flamboyant for the rap enjoyment\nMy clan increase like black unemployment',
    'The Wu is too slammin\' for these Cold Killin\' labels\nSome ain\'t had hits since I seen Aunt Mabel\nBe doin\' artists in like Cain did Abel\nNow they money\'s gettin\' stuck to the gum under the table',
    'Now that thought was just as bright as a 20-watt light bulb\nShould\'ve pumped it when I rocked it\nNiggas so stingy they got short arms and deep pockets'
]

biggie_lyrics = [
    'Smoking blunts in the project hallways\nShooting dice all day',
    'Back in the days our parents used to take care of us\nLook at \'em now, they even fuckin\' scared of us',
    'If I wasn\'t in the rap game\nI\'d probably have a key knee-deep in the crack game\nBecause the streets is a short stop\nEither you\'re slinging crack rock or you got a wicked jump shot',
    'Shit, it\'s hard being young from the slums\nEating 5 cent gums, not knowing where your meal\'s coming from',
    'No need for that, just grab the fucking gat\nThe first pocket that\'s fat, the Tec is to his back',
    'Nigga, you ain\'t got to explain shit\nI\'ve been robbing motherfuckas since the slave ships\nWith the same clip and the same .45\nTwo point blank, a motherfucker sure to die',
    'Then I\'m dipping up the block and I\'m robbing bitches too\nUp the herringbones and bamboos\nI wouldn\'t give a fuck if you\'re pregnant Give me the baby rings and the #1 Mom pendant',
    'I\'m slamming niggas like Shaquille, shit is real\nWhen it\'s time to eat a meal, I rob and steal',
    'Big up, big up, it\'s a stick up, stick up\nAnd I\'m shooting niggas quick if ya hiccup',
    'One in the chamber, thirty-two in the clip\nMotherfuckas better strip, (yeah nigga, peel)\nBefore you find out how blue steel feel',
    'And when I rock her and drop her, I\'m taking her doorknockers\nAnd if she\'s resistant: blakka, blakka, blakka',
    'Tell him Biggie took it, what the fuck he gonna do?\nMan I hope apologetic or I\'m a have to set it\nAnd if I set it, the cocksucker won\'t forget it',
    'I fuck around and get hardcore\nC-4 to your door, no beef no more nigga',
    'Super Nintendo, Sega Genesis\nWhen I was dead broke, man, I couldn\'t picture this',
    'When I die, fuck it, I wanna go to hell\n\'Cause I\'m a piece of shit, it ain\'t hard to fuckin\' tell',
    'All my life I been considered as the worst\nLyin\' to my mother, even stealin\' out her purse\nCrime after crime, from drugs to extortion\nI know my mother wish she got a fuckin\' abortion'
]

doc_oct_lyrics = [
    'Fuck my pussy, Doctor!\n',
    'I crank up lyrical flows, spit Spats, what\'s that?\nThe pattern records, don\'t touch the DATs, yo',
    'Suckers with mics that end up with tooth decay\nI, the Doctor, stop ya, in your world, rock ya',
    'Scratches in mattress business money reattaches worldwide\nDeep inside stops the diamond rocks',
    'Hello, this is the offices of Dr. Octagon.\nIf you have insurance or medical problems, I\'m here for you for any type\nof intestine surgery, rectal rebuilding, relocated saliva glands,\nand chimpanzee acne—and of course, moosebumps. You can call 1-800-PP5-1-doodoo. I\'m in your corner.',
    'First patient, pull out the skull, remove the cancer\nBreaking his back, chisel necks for the answer',
    'Supersonic-bionic-robot-voodoo power\nEquator ex my chance to flex skills on Ampex',
    'With power meters and heaters gauge anti-freeze\nOctagon oxygen, aluminum intoxicants',
    'More ways to blow blood cells in your face\nReact with four bombs and six fire missiles',
    'Armed with seven rounds of space doo-doo pistols\nYou may not believe, living on the Earth planet',
    'My skin is green and silver, forehead looking mean\nAstronauts get played, tough like the ukelele',
    'As I move in rockets, overriding, levels\nNothing\'s aware, same data, same system',
    'Radiation leakage on the promenade deck, access for authorized personnel only',
    'Disappear again, zapped like an android\nFace the fact, I fly on planets every day\nMy nucleus friend, prepare, I return again\nMy 7XL is not yet invented'
]

eminem_lyrics = [
    'You don\'t wanna fuck with me\nGirls neither, you ain\'t nothin\' but a slut to me',
    'I invented violence, you vile venomous volatile vicious\nVain Vicodin, vrin vrin vrin!',
    'Texas Chainsaw, left his brains all\nDanglin\' from his neck while his head barely hangs on',
    'Blood, guts, guns, cuts\nKnives, lives, wives, nuns, sluts — bitch, I\'ma kill you!',
    'I said you don\'t wanna fuck with Shady (Why?)\n‘Cause Shady will fucking kill you',
    'I ain\'t "acid rap," but I rap on acid',
    'When I go out, I’ma go out shootin’\nI don’t mean when I die, I mean when I go out to the club, stupid!',
    'I’m tryin’ to clean up my fuckin’ image\nSo I promised the fuckin’ critics\nI wouldn’t say “fuckin’” for six minutes\n*Six minutes, Slim Shady, you’re on!*',
    'My baby’s mom, bitch made me an angry blonde\nSo I made me a song, killed her and put Hailie on',
    'Shit, half the shit I say, I just make it up\nTo make you mad, so kiss my white naked ass',
    'You motherfuckin\' chickens ain\'t brave enough\nTo say the stuff I say, so just tape it shut',
    'And if it\'s not a rapper that I make it as\nI\'ma be a fuckin\' rapist in a Jason mask',
    'The mother did drugs, hard liquor, cigarettes and speed\nThe baby came out, disfigured ligaments, indeed\nIt was a seed who would grow up just as crazy as she\nDon\'t dare make fun of that baby, ‘cause that baby was me',
    'I\'m a criminal, an animal caged who turned crazed\nBut how the fuck you supposed to grow up when you weren\'t raised?',
    'My morals went *pffft* when the president got oral Sex in his Oval Office on top of his desk off of his own employee',
    '‘Cause if I ever stuck it to any singer in showbiz\nIt\'d be Jennifer Lopez — and Puffy, you know this\nI\'m sorry Puff, but I don\'t give a fuck\nIf this chick was my own mother\nI\'d still fuck her with no rubber and cum inside her\nAnd have a son and a new brother at the same time\nAnd just say that it ain\'t mine — what\'s my name?',
    'I\'ll show you pussy footin, I\'ll kick a bitch in the cunt, \'til it makes her queef and sounds like a fucking whoopy cushion.'
]

freddie_gibbs_lyrics = [
    '24 hours to live, what would you do?\nJust get high, treat everyday like my birthday, smoke with the crew',
    'Before I check out, let me diamond my neck out\nBlow a mil on my niggas, fuck bitches like I was fresh out',
    'Fresh to death when I step out, every day approaching the gates\nI live a helluva life, baby, heaven can wait',
    'Everyday I pray to be as strong as Huey Newton\nBefore you pull that trigger, take a closer look at who you shooting',
    'Mirror image, nothing different, you just another slave\nTryin to succeed in these European\'s narcotics trade',
    'Worked all week, 140 dollars was all I made\nFuck a job, I\'d rather chop a rock and be chopping blades',
    'Gotta watch these cops cause I came too far to die in a cage\nWatch who you fuck, rather catch a bullet than die from AIDS',
    'Before I check out, let me diamond my neck out\nCrushing feelings on Broadway, I pulled that Monte SS out',
    'Buy my mom a new spot and make sure that bitch super decked out\nSwear I can\'t leave this Earth \'til I\'m sure that you never stress out',
    'Hit the lab so I can lay all the shit I didn\'t get to spit\nCould die tonight, but what I write they forever gon\' reminisce\nIt\'s Gangsta Gibbs',
    'Niggas be like "Fred, you ain\'t never lied"\nFuck the rap shit, my gangsta been solidified',
    'Still do my business on the side\nBitch, if you polices, then pay me no nevermind',
    'I was thuggin\', black and red laces in my number threes\nTake a pull up off the wood and let that motherfucker breathe',
    'Sit outside a busta crib and let that motherfucker leave\nWalk his ass back in and put him on his motherfuckin\' knees',
    'Thuggin\', never takin\' no for an answer\nMight just take a loss, but bitch, I’d rather take my chances',
    'This liquor got me lurkin\' where you live at in the night time\n59Fifty to the left, but I\'m in my right mind',
    'Thuggin\', pants gon\' be saggin\' til I\'m 40\n Still lyrically sharper than any short bus shawty',
    'Phonies ain\'t gon\' throw me in this minstrel show\nThese labels see how far up in they mouth my dick can go',
    'So gon\', choke on this meat, throw my song on repeat\nMight move away one day but I\'m always gon\' belong to the streets',
    'Selling you the science of the street rap\nEvery motherfuckin\' show I do is off the meat rack',
    'Never trippin\' on a dame, I\'m too cold for you broke hoes\nDon\'t let the knob hit your booty when the door close, bitch',
    'She let me hit it cause I\'m thuggin\'\nSquares need not apply, I\'m so fly I might fuck her cousin',
    '"We’re not against rap, but we\'re against those thugs"\nCan\'t be legit when every nigga in your clique sold drugs',
    'I hate to say it, ain\'t no need to be discreet\nIf she don\'t cop from me, she get it from a nigga up the street\nCause he thuggin\', and yo, she\'d probably suck his dick for it\nShe turnt out so it ain\'t shit to turn a trick for it',
    'My uncle last bitch put him on the glass dick\nTried to rob a man to feed his habit, he got blasted',
    'Cause in the past, my low-class black ass would serve my own fucking family members'
]

"""
- Spottieottie
- Ms. Jackson
- So Fresh, So clean
- B.O.B
- Git up
- ATLiens
- Jazzy Belle
- Hootie Hoo
- Players Ball
"""
outkast_lyrics = [
    'The music is like that green stuff\nProvided to you by sack man',
    'Pac man how in the fuck do you think we gon\' do that man?\nRidin\' round Old National on 18\'s without no gat man',
    'I\'m strapped man & ready to bust on any nigga like that man\nMe and my nigga we roll together like Batman and Robin',
    'Twice upon a time there was a boy who died twice\nAnd lived happily ever after but that\'s another chapter',
    'Live from home of the brave with dirty dollars\nAnd beauty parlors & baby bottles and bowling ball Impalas',
    'And street scholars that\'s majoring in culinary arts\nYou know how to work bread cheese and dough\nFrom scratch but see the catch is you can get caught\nKnow what ya sellin\' what ya bought so cut that big talk',
    'Let\'s walk to the bridge now meet me halfway\nNow you may see some children dead off in the pathway\nIt\'s them poor babies walkin\' slowly to the candy lady',
    'Like the words maybe, if, or probably more than a hobby\nWhen my turntables get wobbly they don\'t fall',
    'The name is Big Boi Daddy Fat Sax\nThe nigga that like them Cadillacs',
    'Get off the testicles and the nut sacks\nYou bust a rhyme we bust back',
    'My mind warps and bends floats the wind count to ten\nMeet the twin Andre Ben. welcome to the lion\'s den',
    'Original skin many men comprehend\nI extend myself so you go out and tell a friend',
    'Sin all depends on what you believing in\nFaith is what you make it that\'s the hardest shit since MC Ren',
    'Alien can blend right on in wit\' yo\' kin\nLook again \'cause I swear I spot one every now and then',
    'It\'s happenin\' again wish I could tell you when\nAndre this is Andre y\'all just gon\' have to make amends'
]

big_L_lyrics = [
    'I knocked out so many teeth the tooth fairy went bankrupt',
    'Fucking punk you ain\'t a leader, nobody followed you, you was never shit your mother should\'ve swallowed you...',
    'I\'m tellin you shit is about to get drastic soon\nI\'m quick to blast a goon\nAnd break a motherfucker like a plastic spoon',
    'Some say I\'m ruthless, some say I\'m grim\nOnce a brother done broke into my house and I robbed him',
    'Old folks get mugged and raided\nCrimes are drug related\nAnd we live by the street rules that thugs created',
    'I got drug spots from New York to Canada\nCause Big L be fuckin\' with more keys than a janitor',
    'I made every little kid from my hood run\nI was just like that little bastard from the Good Son',
    'L da Harlem pimp baby, for real\nI got mo\' dimes dan dat Sprint Lady',
    'What’s this motherfuckin rap game without L?\nYo, that’s like jewels without ice\nThat’s like china without rice or the Holy Bible without Christ',
    'To be seen clean in the mean Beam\nIs every team’s dream; Big L’s a cream fiend\nWith more green than Springsteen',
    'I’m so ahead of my time my parents haven’t met yet',
    'Cause I got all of ‘em strung jack\nMy girls are like boomerangs\nNo matter how far I throw \'em, they come back',
    'Facts on tracks I recite well\nEverybody wanna be like Mike, but Mike wanna be like L',
    '"I got more riches than you, fuck more bitches than you\nOnly thing I haven\'t got is more stitches than you',
    'Breaking in cribs with a crowbar\nI wasn\'t poor, I was po\' - I couldn\'t afford the \'o-r\''
]


markov = defaultdict(lambda: defaultdict(int))

def remove_punction(text):
    """
    Removes the punctuation from a given string
    """
    return text.translate(str.maketrans("", "", string.punctuation))

def get_trigrams(data):
    """
    Generates the trigrams of an array of elements. For example, if `data = [a, b, c, d]` then the
    output will be `[[a,b,c], [b,c,d]]`.
    """
    for i in range(len(data) - 2):
        yield data[i:i + 3]

def get_ngrams(degree, data):
    """
    Generates the n-grams of an array of elements. For example, if `data = [a, b, c, d]` and
    `degree = 2` then the output will be `[[a,b], [b,c], [c,d]]`. This is just a generic
    version of the `get_trigrams` function, here for reference.
    """
    for i in range(len(data) - degree + 1):
        yield data[i:i + degree]

def weighted_choice(states):
    """
    Given a dictionary of keys and weights, choose a random key based on its weight.
    """
    n = random.uniform(0, sum(states.values()))
    for key, val in states.items():
        if n < val:
            return key
        n -= val

    # Something went wrong, don't make a choice.
    return None

def init_markov():
    # just join the array into a single string
    data = ' '.join([
        *lyrics.kanye_lyrics,
        *lyrics.gucci_lyrics,
        *lyrics.random_lyrics,
        *lyrics.nas_lyrics,
        *lyrics.E40_lyrics,
        *lyrics.snoop_dogg_lyrics,
        *lyrics.three_six_lyrics,
        *lyrics.project_pat_lyrics,
        *lyrics.wu_tang_lyrics,
        *lyrics.biggie_lyrics,
        *lyrics.doc_oct_lyrics,
        *lyrics.eminem_lyrics,
        *lyrics.freddie_gibbs_lyrics,
        *lyrics.big_L_lyrics,
        *lyrics.outkast_lyrics
    ])

    print('data: ' + data)
    data = remove_punction(data).replace('\n', ' ')
    parsed_data = data.split(' ')

    # Now split the input data into trigrams for parsing.
    for (w1, w2, w3) in get_trigrams(parsed_data):
        # Use lowercase to normalize the data.
        w1 = w1.lower()
        w2 = w2.lower()
        w3 = w3.lower()

        # Update the tally for this combination.
        markov[(w1, w2)][w3] += 1
    print('ok its initialized')

def spit_game():
     # Use random to pick a random initial state (or set it yourself).
    start_state = random.choice(list(markov.keys()))
    # You can preview it by writing ```print("Initial State: %s" % repr(start_state))```

    # Now start 'walking' along the Markov Chain to generate stuff. Unfortunately, the hard part
    # is knowing when to stop. Here I say I want sentences no longer than 15 words, and if there's
    # a dead-end, stop immediately. Naturally, there's much better ways to do this.
    s1, s2 = start_state
    max_length = 15
    result = [s1, s2]
    for _ in range(max_length):
        next_state = weighted_choice(markov[(s1, s2)])
        if next_state is None:
            break
        result.append(next_state)
        s1 = s2
        s2 = next_state

    # the result is an array so just make it a string
    return ' '.join(result) + '.'

@client.event
async def on_ready():
    print("Young LD is online")
    init_markov()
    await client.change_presence(game=discord.Game(name='+help for command list!'))

# Sends a message to a new member that joins the discord server.
@client.event
async def on_member_join(member):
    await client.send_message(member, "Sup!? It's ya boy Young LD, and my sole purpose in this world is to provide you and your crew with some dank, absurd, hard hittin' rap lyrics.\n" 
    "For a list of all available commands, use the +help command.\n"
    "ps - Wu-Tang is 4 da children and don't forget to Protect Ya Kneck.")
   
@client.event
async def on_message(message):
    # Don't need the bot to reply to itself.
    if message.author == client.user:
        return

    # Randomly picks a lyric from the list of kanye_lyrics
    if message.content.upper().startswith('+kanye'):
        await client.send_message(message.channel, random.choice(lyrics.kanye_lyrics))

    # Randomly picks a lyric from the list of gucci_lyrics
    if message.content.upper().startswith('+gucci'):
        await client.send_message(message.channel, random.choice(lyrics.gucci_lyrics))

    # Randomly picks a lyrics from the list of random_lyrics
    if message.content.upper().startswith('+random'):
        await client.send_message(message.channel, random.choice(lyrics.random_lyrics))

    # Randomly picks lyrics from the list of nas_lyrics
    # primarily lyrics from illmatic aka the best hip hop album of all time
    if message.content.upper().startswith('+nas'):
        await client.send_message(message.channel, random.choice(lyrics.nas_lyrics))

    # Randomly picks lyrics from the list of E40_lyrics
    if message.content.upper().startswith('+e40'):
        await client.send_message(message.channel, random.choice(lyrics.E40_lyrics))

    # Randomly picks lyrics from the list of snoop_dogg_lyrics
    if message.content.upper().startswith('+snoop'):
        await client.send_message(message.channel, random.choice(lyrics.snoop_dogg_lyrics))

    # Randomly picks lyrics from the list of three_six_lyrics
    if message.content.upper().startswith('+triple6'):
        await client.send_message(message.channel, random.choice(lyrics.three_six_lyrics))

    # Randomly picks lyrics from the list of project_pat_lyrics
    if message.content.upper().startswith('+pat'):
        await client.send_message(message.channel, random.choice(lyrics.project_pat_lyrics))

    # Randomly picks lyrics from the list of wu_tang_lyrics
    if message.content.upper().startswith('+wutang'):
        await client.send_message(message.channel, random.choice(lyrics.wu_tang_lyrics))

    # Randomly picks lyrics from the list of biggie_lyrics
    if message.content.upper().startswith('+biggie'):
        await client.send_message(message.channel, random.choice(lyrics.biggie_lyrics))

    # Rancomly picks lyrics from the list of doc_oct_lyrics
    if message.content.upper().startswith('+droct'):
        await client.send_message(message.channel, random.choice(lyrics.doc_oct_lyrics))

    # Randomly picks lyrics from the list of eminem_lyrics
    if message.content.upper().startswith('+eminem'):
        await client.send_message(message.channel, random.choice(lyrics.eminem_lyrics))

    # Randomly picks lyrics from the list of gangsta gibbs lyrics
    if message.content.upper().startswith('+gibbs'):
        await client.send_message(message.channel, random.choice(lyrics.freddie_gibbs_lyrics))

    # Randomly picks lyrics from the list of Big L lyrics
    if message.content.upper().startswith('+bigl'):
        await client.send_message(message.channel, random.choice(lyrics.big_L_lyrics))

    # Randomly picks lyrics from the list of Outkast lyrics
    if message.content.upper().startswith('+outkast'):
        await client.send_message(message.channel, random.choice(lyrics.outkast_lyrics))

    # Displays the bots personal opinion on who are the top 10 best hip-hop artist of all time
    if message.content.upper().startswith('+top10'):
        await client.send_message(message.channel, "This is my top ten list of the best hip-hop artist of all time.\n"
                                  "1. Nas\n"
                                  "2. Ghostface Killah\n"
                                  "3. Andre 3000\n"
                                  "4. The Notorious B.I.G.\n"
                                  "5. Big L\n"
                                  "6. Raekwon da Chef\n"
                                  "7. Tupac\n"
                                  "8. Kendrick Lamar\n"
                                  "9. Eminem\n"
                                  "10. Jay-Z")

    # Displays the bots personal opinion on who are the top 10 best hip-hop producers of all time
    if message.content.upper().startswith('+producers'):
        await client.send_message(message.channel, "This is my top ten list of best hip-hop producers of all time.\n"
                                  "1. J Dilla\n"
                                  "2. Madlib\n"
                                  "3. RZA\n"
                                  "4. Dr. Dre\n"
                                  "5. Organized Noize\n"
                                  "6. No I.D.\n"
                                  "7. Pete Rock\n"
                                  "8. Sounwave\n"
                                  "9. Q-Tip\n"
                                  "10. Kanye West")
    
    # Uses markov chain to generate random lyrics
    if message.content.upper().startswith('+SPIT'):
        await client.send_message(message.channel, spit_game())
    
    # Displays commands for the user
    if message.content.upper().startswith('+HELP'):
        commands={}
        commands['+help']='Young LD Displays the list of command that can be used.'
        commands['+kanye']='Displays random lyrics from the greatest artist of our generation.'
        commands['+gucci']='Displays lyrics by Guwop AKA El Gato the Human Glacier.'
        commands['+nas']='Displays random lyrics from the greatest album of all time, Illmatic.'
        commands['+e40']='Displays random lyrics by E40 AKA Charlie Hustle.'
        commands['+snoop']='Displays random lyrics by the Dogg Father.'
        commands['+triple6']='Displays random lyrics by Three 6 Mafia.'
        commands['+pat']='Displays random lyrics by Project Pat.'
        commands['+wutang']='Wu-Tang is for the the children.'
        commands['+biggie']='Displays random lyrics by the black Frank White.'
        commands['+droct']='Displays random lyrics by Dr.Octagon AKA the Dr.Octagonecologyst.'
        commands['+eminem']='Displays random lyrics by Eminem.'
        commands['+gibbs']='Displays random lyrics by Gangsta Gibbs.'
        commands['+bigl']='Displays random lyrics by Big L.'
        commands['+outkast']='Displays random lyrics by Outkast.'
        commands['+top10']='Young LD displays his top 10 list of the best Hip-Hop artist of all time.'
        commands['+producers']='Young LD displays his top 10 list of the best Hip-Hop producers of all time.'
        commands['+random']='Displays random lyrics from a bunch of different artist.'
        commands['+spit']='Uses a Markov chain to combine lyrics and comes up with some funky shit.'

        msg=discord.Embed(title='Young Larry David', description='Written by SnoopFrogg', color=0x0000ff)
        for command, description in commands.items():
            msg.add_field(name=command, value=description, inline=False)
        #msg.add_field(name='Join our Discord/For Questions/Chilling', value='', inline=False)
        await client.send_message(message.channel, embed=msg)

async def list_server():
    await client.wait_until_ready()
    while not client.is_closed:
        servers = list(client.servers)
        print("Its Gucci Time! Young LD is connected to " + str(len(client.servers)) + " servers:")
        for server in servers:
            print(server.name)

        await asyncio.sleep(600)

client.loop.create_task(list_server())
client.run(os.getenv('TOKEN'))
