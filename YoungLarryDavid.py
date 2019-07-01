import asyncio
import random
import time
import discord
import os
import string
from discord.ext.commands import Bot
from discord.ext import commands
from collections import defaultdict

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
    'Next time I\'m feeling kinda horny\n You can come on over\n And I\'ll break you off\n And if you can\'t fuck that day baby\n Just lay back and open your mouth\n Cause I have never met a girl\n That I love in the whole wide world.',
    'For a trill, working the wheel, a pimp not a simp\n Keep the dope fiends higher than the Goodyear Blimp',
    'I\'m trapping like a fool, 30 inches on the Hummer ride\n Mad \'cause I killed your buddy and I beat the homicide',
    'Young Juiceman whip more chickens than Popeye\'s\n Bouldercrest working and I\'m still whipping cream pies',
    'Matter of fact, nigga, just call me when you need some dope'
]

nas_lyrics = [
    'Rappers, I monkey flip \'em with the funky rhythm I be kickin\'\n Musician inflictin\' composition of pain\n I\'m like Scarface sniffin\' cocaine\n Holdin\' an M16, see with the pen I\'m extreme',
    'It drops deep as it does in my breath\n I never sleep—cause sleep is the cousin of death\n Beyond the walls of intelligence, life is defined.\n I think of crime when I\'m in a New York state of mind',
    'I sip the Dom P, watchin\' Gandhi \'til I\'m charged, then\n Writin\' in my book of rhymes, all the words past the margin.\n Behold the mic I\'m throbbin\', mechanical movement\n Understandable smooth shit that murderers move with\n The thief\'s theme, play me at night, they won\'t act right',
    'Yet I\'m the mild, money-gettin\' style, rollin\' foul\n The versatile, honey-stickin\', wild, golden child\n Dwellin\' in the Rotten Apple, you get tackled\n Or caught by the devil\'s lasso, shit is a hassle',
    'There\'s no days for broke days\n We sell it, smoke pays, while all the old folks pray\n To Jesús, soakin\' their sins in trays of holy water',
    'I\'m the young city bandit, hold myself down single-handed\n For murder raps, I kick my thoughts alone, get remanded\n Born alone, die alone, no crew to keep my crown or throne\n I\'m deep by sound alone, caved inside, 1,000 miles from home.',
    'I rap for listeners, bluntheads, fly ladies, and prisoners\n Hennessy-holders and old-school niggas, then I be dissin\'a\n Unofficial that smoke Woolie Thai\n I dropped out of Cooley High, gassed up by a cokehead cutie pie',
    'Yo, they call me Nas, I\'m not your legal type of fella\n  Moët drinking, marijuana smoking street dweller\n Who\'s always on the corner, rolling up blessed\n When I dress, it\'s never nothing less than Guess',
    'Nas is like the Afrocentric Asian: half-man, half-amazin\'\n ‘Cause in my physical I can express through song\n Delete stress like Motrin, then extend strong\n I drink Moët with Medusa, give her shotguns in Hell\n From the spliff that I lift and inhale; it ain\'t hard to tell',
    'This rhythmatic explosion\n Is what your frame of mind has chosen\n I\'ll leave your brain stimulated, niggas is frozen\n Speak with criminal slang, begin like a violin\n End like Leviathan,it\'s deep? Well, let me try again',
    'My poetry\'s deep, I never fell\n Nas\'raps should be locked in a cell; it ain\'t hard to tell'
]

E40_lyrics = [
    'Ever told on a nigga? (nope)\n Ever squeezed a trigger? (yup)',
    'Ever set a nigga up? (nope)\n Ever helped a brother out when he was down on his luck? (yup)',
    'You a sap? (nope)\n You a boss player, you a mack? (yup)',
    'Starving? (nope), Dinner? (yup)',
    'You still sell dope? (nope)\n Now you cleaner than a bar of Dove soap? (yup)',
    'Everybody get choices\n I choose to get money, I\'m stuck to this bread\n Everybody got choices\n These bitches is choosin\', I\'m all in they head',
    'Ugh, lazy? (nope)\n Got dick that\'ll drive a ho crazy? (yup)',
    'Sleep? (nope), Bust moves, hella active in the streets? (yup)',
    'Star Wars? (nope), Yoda? (yup)',
    'Was it love at first sight? (nope)\n Did she ride you like a bike? (yup)\n Was it ripe? (nope), Was her pussy tight? (yup)',
    'Your team weak? (nope)\n You respected in the stree-neets? (yup)',
    'I don\'t like suckas in my mix (mmm mmm)\n Got my name in their mouth like tooth picks (uh huh)',
    'I don\'t pay for pussy, not a John (mmm mmm)\n Sucka shit contagious like a yawn (uh huh)',
    'Never will I go to war over a ho (mmm mmm)\n Bitch I\'m a motha fuckin\' buffalo (uh huh)',
    'Out of date like old people? (mmm mmm)\n In the loop like sewing needle? (uh huh)',
    'You weak at shootin\' dice? (mmm mmm)\n You really \'bout that life? (uh huh)',
    'You eat booty? (mmm mmm)\n You lick coochie? (uh huh)\n Biatch!',
    'Divorced from the streets? (mmm mmm)\n Be in Dubai with the sheiks? (uh huh)',
    'Pan handlin\'? (mmm mmm)\n Shippin\' and handlin\'? (uh huh)'
]

snoop_dogg_lyrics = [
    'He fucked the fleas off a bitch.\n He shaked the ticks off his dick.\n And in the booty, he buries his motherfuckin\' bone.\n And if there\'s any left over\n He\'ll roll over and take a doggy bag home',
    'Shit, I got a pocket full of rubbers and my homeboys do too\n So turn off the lights and close the doors\n But (but what?) we don\'t love them hoes, yeah\n So we gon\' smoke a ounce to this\n G\'s up, hoes down, while you motherfuckers bounce to this.',
    '‘Cause when I bust my nut I\'m raising up off the cot\n Don\'t get upset, girl, that\'s just how it goes\n I don\'t love you, hoes, I\'m out the door, and I\'ll be...',
    'Guess who back in the motherfucking house\n With a fat dick for your motherfucking mouth',
    'Now as the sun rotates and my game grows bigger\n How many bitches wanna fuck this nigga named Snoop\n Doggy, I\'m all the above\n I\'m too swift on my toes to get caught up with you hoes\n But see it ain\'t no fun\n If my homies can\'t get a taste of it\n Cause you know I don\'t love em',
    'Some of these niggas is so deceptive\n Using my styles like a contraceptive\n I hope you get burnt\n Seems you haven\'t learnt\n It\'s the knick-knack, patty-whack\n I still got the biggest sack!',
    'Speaking of hoes, I\'ll get to the point\n You think you got the bomb cause I rolled you a joint?',
    'You\'se a flea, and I\'m the Big Dogg,\n I\'ll scratch you off my balls with my motherfuckin\' paws',
    'So I ain\'t holdin nuttin\' back\n And motherfucker, I got five on that twenty sack\n It\'s like that and as a matter of fact (rat-tat-tat-tat)\n \'Cause I never hesitate to put a nigga on his back',
    'Yeah roll up the dank, and pour the drank\n And watch your step (why?) \'cause Doggy\'s on the gank',
    'Layin that, playin that G Thang\n She want the nigga with the biggest nuts, and guess what?\n He is I, and I am him, slim with the tilted brim\n What\'s my motherfuckin name?'
]

three_six_lyrics = [
    'Bitch don\'t play dumb\n Stick out your tongue\n And let me take a plunge\n For plenty you don\'t have to suck your thumb\n I got yum-yum',
    'Slob on my knob\n Like corn on the cob\n Check in with me\n And do your job\n lay on the bed\n And give me head\n Don\'t have to ask\n Don\'t have to beg',
    'These bitches got me goin\'\n The feelin\' of a warm mouth\n Man I tell you bout\' these hoes chewin\' in the South',
    'On through the wall now she howlin\' like a dog swept poor\n We hit the floor it don\'t quit\n Another one break it\'s just another victim of Lord Infamous late night tip',
    'Lord Infamous, the futuristic rowdy bounty hunter\n Nigga, I come from the land down under',
    'Ten times out of twelve\n Nine times out of ten\n Gansta Boo is in it to win',
    'When I say weak ass, you say bitch!\n Weak ass, bitch!, weak ass, bitch!',
    'You ol\' pussy-ass, cake-ass, punk-ass, trick-ass, sucker-ass,\n Fuck-ass, dick-in-the-booty-ass, K-Y Jelly-packing-ass nigga',
    'Yeah, nigga, y\'all know the motherfucking sco\', y\'all non-snorters, non-smokers, non-sippers,\n Get the fuck up out of here, bitch\n Nigga, it\'s some sipping-ass, pouring up-ass, smoking-ass, getting high-ass niggas in here,\n Three 6, UGK, nigga, we putting it down in this motherfucker\n And we ain\'t playing wit\'chu, y\'all know the motherfucking sco\', homie\n Now pour it up, nigga.',
    'People always asking me, is the Three 6 high on that?\n Rolling on them X pills, stuttering, pup-pup powder packs',
    'Woah, where the weed at, ain\'t like that we need that\n NyQuil will slow me down, something that keep me easy\n Nothing like that yella yella, that\'ll have you itching, man\n Talking like, what\'s up, fool? Vocal chords sounding lame',
    'Gone on coke, eyes all bucked, this here shit\'ll knock you down\n Knock you out, make you fall asleep when you\'re on them wheels',
    'She popped her a pill of X, and drank on some orange juice\n And just when you thought she was freaking, she done got super loose',
    'Juice got weed Juice got pills\n Juice got the work on the corner cuttin deals',
    'We ball out in the club wit our niggaz stayin trill\n We never wrote a check just them big face bills\n A playa drinkin Makers, Marker, cranberry vodka\n Wearin a mink coat thats furry as Chewbacca',
    'Nose all runny\n Found a snow bunny\n Take her to da\' crib\n Make her drink cummy',
    'Cocaine Blaine that\'s my dog\n I called him up to house this slut\n We gon\' fuck her in the back of da\' bus\n And fill her nose up full o\' dat\' dust',
    'In da\' bathroom \'bout two whole hours\n Gettin\' real high passed out on the floor\n Fuck that shit niggas\' on the frame\n Take \'em 1 on 1 back in the game',
    'Used to be my nigga\n Now you fake\n But I stomp on you trick in the grass\n You little snake bitch'
]

project_pat_lyrics =[
    'I ain\'t goin\' back to jail, I ain\'t goin\' back to jail\n I got mo\' pussy to swell, and mo\' dreams to tell',
    'Bullets do fly through air when them guns p-poppin\'\n Pistol swang to ya mouth, then the blood is gushin\'',
    'Cross killers in these streets, bullets will spray\n Innocent bystander can catch a stray ya dig?',
    'Put two dollars in the air, for these two dollar niggas\n They get mad and they fuss, they don\'t shine like us',
    'I\'m flickin\' on you snakes, I got wood, leather stitchin\'\n Clothes stickin\', cause ya ridin\' bucket, cloth seats itchin\'',
    'Couldn\'t get me, saw it in the clouds, like my nigga Rickey\n Mr. James, all these superfreaks, out here tryna get me',
    'Wanna hit me, wanna say, they done been \'round the truth\n In ya bed, or the booth, I\'m the ghetto Dr. Ruth',
    'When I do, step on out, moonlight, hit the Range\n Pretty jewels they attract broads, like shiny thangs',
    'When I came, to ya hood, I was new face, in the place\n Game spitter from the North, so ya wanna catch a case',
    'Cause ya see me holl\'in\' at \'cha ex-girl, don\'t \'cha?\n Murder charge for a broad who don\'t even want \'cha',
    'You suckers crazy, so y\'all out here pushin\' daisies\n Over Daisy, she was on some purple hazey',
    'Had the baby, year later on my income\n Tax, so a nigga could receive mo\' income',
    'Hangin\' stout broads, \'round my arms, decoration\n These punks give me dap, same time playa hation',
    'Erasin\', you lamers, hatin\' got\'cha famous\n Confronted by the broad, got shot in ya anus\n Heinous, heard they took the slugs out\'cha dookie roll\n Gun powder and the blood burn in ya bootyhole',
    'Wanna fight, my nigga, wanna shoot, my nigga\n Talk ya gal out her cap, when ya loot my nigga',
    'Do you, my nigga, fall in love wit\' these tramps\n Goin\' raw, on her, and she did the whole Camp?\n But you rest havin\' that, knowin\' that, she\'ll go\n Lickin\' balls, suckin\' cat, knees burnt from the flo\'',
    'She got a bubble gum cap with a Gucci dats snappin\'\n With some rhino legs and a booty that\'s flappin\'\n With some fire-oh head \'cause you know we love cappin\'\n Got her toes done up with her fingernails matchin\'',
    'Here dat big ol\' butt that you\'re walkin\' cross the street with\n Peep this, for a happy meal can I squeeze it?',
    'Them freaky freaks I heard on the loose, let ya pockets out\n Got trick niggaz watchin\' your caboose with they wallets out',
    'You should stop, lil\' somethin\' somethin\' bad to the bone\n That ain\'t a monkey hangin\' off ya back that\'s Donkey Kong',
    'Good googly moogly, that thang is juicy',
    'How you gon\' prance around with all that, sayin\' you ain\'t all that, Everybody at ya wanna hit ya like a ball bat',
    'That thang make ya look back, be like man who is that\n You can see a hiny on a hiny I\'m pursuin\' that',
    'A dirty south hoody rat tryin\' to hold goodies back Waist like a wasp, butt cheeks pokin\' really fat',
    'I\'m Crown Vic old school, squeezin\' on her boo-boo\n Hugged up, pokin\' in her brains so what ya wanna do',
    'You can call me Mister Whipple, I won\'t do no harmin\'\n Never to the Charmin, come holla at me woman',
    'Bwok bwok, chicken chicken\n Bwok bwok, chicken heads',
    'Bald-head skally-wag\n Ain\'t got no hair in back\n Gelled up weaved up\n Yo hair is messed'
]

wu_tang_lyrics = [
    'Ghostface catch the blast of a hype verse\n My Glock burst, leave in a hearse, I did worse',
    'Aww shit, Wu-Tang Clan spark the wicks, an\'\n However I master the trick just like Nixon',
    'Causin\' terror, quick damage your whole era\n Hard rocks is locked the fuck up, or found shot',
    'I watch my back like I\'m locked down\n Hardcore-hittin\' soundn\n Watch me act bugged and tear down\n Illiterate-type asshole, songs goin\' gold',
    'Yeah, they fake and all that, carryin\' gats\n But yo, my Clan rollin\' like forty macks\n Now you act convinced, I guess it makes sense\n Wu-Tang, yo, soooo represent!',
    'And that\'s one in the chamber, Wu-Tang banger\n 36 styles of danger',
    'I rip it hardcore, like porno-flick bitches\n I roll with groups of ghetto bastards with biscuits',
    'Check it, my method on the microphone\'s bangin\'\n Wu-Tang slang\'ll leave your headpiece hangin\'',
    'Redrum, I verbally assault with the tongue\n Murder One, my style shocks your knot like a stun gun',
    'Set it on the microphone, and competition get blown\n By this nasty-ass nigga with my nigga, the RZA\n Charged like a bull and got pulled like a trigga\n So bad, stabbin\' up the pad with the vocab, crab\n I scream on your ass like your dad, bring it on...',
    'Yo, I\'m more rugged than slave man boots\n New recruits, I\'m fuckin\' up MC troops\n I break loose, and trample shit, while I stomp\n A mudhole in that ass \'cause I\'m straight out the swamp',
    'I blow up his fuckin\' prism, make it a vicious act of terrorism\n You wanna bring it, so fuck it, come on and bring the ruckus!',
    'En garde, I\'ll let you try my Wu-Tang style.',
    'Shame on a nigga who try to run game on a nigga\n Wu buck wild with the trigger',
    'Shame on a nigga who try to run game on a nigga\n Wu buck… I\'ll fuck your ass up!',
    'Ol\' Dirty Bastard, live and uncut\n Styles unbreakable, shatterproof\n To the young youth, you wanna get gun? Shoot!\n Blaow! How you like me now?',
    'Don\'t fuck the style, ruthless wild\n Do you wanna get your teeth knocked the fuck out?\n Wanna get on it like that? Well, then shout!',
    'Yo RZA, yo razor, hit me with the major\n The damage, my Clan understand it be flavor\n Gunnin\', hummin\', comin\' at ya First I\'m gonna get ya, once I got ya, I gat ya',
    'You could never capture the Method Man\'s stature\n For rhyme and for rapture, got niggas resignin\', now master\n My style? Never!',
    'I put the fuckin\' buck in the wild kid, I\'m terror, razor sharp, I sever\n The head from the shoulders, I\'m better than my competta\n You mean competitor, whatever, let\'s get together',
    'So, when you see me on the real\n Formin\' like Voltron, remember I got deep like a Navy Seal',
    'Burn me, I get into shit, I let it out like diarrhea\n Got burnt once but that was only gonorrhea',
    'The Wu is comin\' through, the outcome is critical\n Fuckin\' with my style is sort of like a miracle',
    '\'Cause I don\'t know you, therefore show me what you know\n I come sharp as a blade and I cut you slow',
    'You become so Pat as my style increases\b What\'s that in your pants? Ahh, human feces!\n Throw your shitty drawers in the hamper\n Next time, come strapped with a fuckin\' Pamper',
    'Can it be that it was all so simple then?\n Dedicated to the 5\'s, 850i\'s\n (Dedicated to niggas who do drive-by\'s)',
    'Raw I\'ma give it to ya, with no trivia\n Raw like cocaine straight from Bolivia',
    'Well, I\'m a sire, I set the microphone on fire\n Rap styles vary and carry like Mariah',
    'I come from the Shaolin slum, and the isle I\'m from\n Is comin\' through with nuff niggas and nuff guns\n So if you wanna come sweatin\', stressin\', contestin\'\n You\'ll catch a sharp sword to the midsection',
    'Rough like Timberland wear, yeah\n Me and the Clan in \'Yota Landcruisers out there\n Peace to all the crooks, all the niggas with bad looks\n Bald heads, braids, blow this hook',
    'I only been a good nigga for a minute though\n \'Cause I got to get my props and win it, yo',
    'I got beef with commercial-ass niggas with gold teeth\n Lampin\' in a Lexus, eatin\' beef\n Straight up and down, don\'t even bother\n I got 40 niggas up in here now who kill niggas\' fathers',
    'My peoples, are you with me? Where you at?\n In the front, in the back, Killa Bees on attack',
    'My peoples, are you with me? Where you at?\n Smokin\' meth, hittin\' cats on the block with the gats',
    'Homicide\'s illegal and death is the penalty\n One justifies the homicide when he dies in his own iniquity?',
    'The flow changes like a chameleon\n Plays like a friend and stabs you like a dagger\n This technique attacks the immune system\n Disguised like a lie, paralyzin\' the victim',
    'You scream as it enters your bloodstream\n Erupts your brain from the pain these thoughts contain\n Movin\' on a nigga with the speed of a centipede\n And injure any motherfuckin\' contender',
    'And the survey said you\'re dead\n Fatal Flying Guillotine chops off your fuckin\' head',
    'And if you want beef, then bring the ruckus!\n Wu-Tang Clan ain\'t nuthing ta fuck wit',
    'Straight from the motherfuckin\' slums that\'s busted\n Wu-Tang Clan ain\'t nuthing ta fuck wit',
    'Like déjà vu, I\'m rubber, niggas is like glue\n Whatever you say rubs off me sticks to you',
    'I grew up on the crime side, the New York Times side\n Stayin\' alive was no jive',
    'But it was just a dream for the teen who was a fiend\n Started smokin\' woolies at 16',
    'No question I would speed for cracks and weed\n The combination made my eyes bleed',
    'No question I would flow off and try to get the dough all\n Stickin\' up white boys in ball courts',
    'Cash rules everything around me\n C.R.E.A.M., get the money\n Dollar dollar bill, y\'all',
    'A man with a dream with plans to make cream\n Which failed; I went to jail at the age of fifteen\n A young buck sellin\' drugs and such, who never had much\n Tryin\' to get a clutch at what I could not',
    'The court played me short, now I face incarceration\n Pacin\', goin\' upstate\'s my destination\n Handcuffed in the back of a bus, forty of us Life as a shorty shouldn\'t be so rough',
    'But as the world turned I learned life is hell\n Livin\' in the world no different from a cell',
    'But shorty\'s runnin\' wild, smokin\' sess, drinkin\' beer\n And ain\'t tryin\' to hear what I\'m kickin\' in his ear\n Neglected for now, but yo, it gots to be accepted\n That what? That life is hectic',
    'I smoke on the mic like "Smokin\' Joe" Frazier\n The hell-raiser, raisin\' hell with the flavor',
    'Terrorize the jam like troops in Pakistan\n Swingin\' through your town like your neighborhood Spider-Man',
    'Call me the rap assassinator\n Rhymes rugged and built like Schwarzenegger',
    'It\'s the Method Man, for short Mr. Mef\n Movin\' on your left, UH!',
    'And set it off, get it off, let it off like a gat\n I wanna break, fool, cock me back',
    'First things first, man, you\'re fuckin\' with the worst\n I\'ll be stickin\' pins in your head like a fuckin\' nurse',
    'Niggas be rollin\' with a stash, ain\'t sayin\' cash\n Bite my style, I\'ll bite your motherfuckin\' ass',
    'Crazy flamboyant for the rap enjoyment\n My clan increase like black unemployment',
    'The Wu is too slammin\' for these Cold Killin\' labels\n Some ain\'t had hits since I seen Aunt Mabel\n Be doin\' artists in like Cain did Abel\n Now they money\'s gettin\' stuck to the gum under the table',
    'Now that thought was just as bright as a 20-watt light bulb\n Should\'ve pumped it when I rocked it\n Niggas so stingy they got short arms and deep pockets'
]

biggie_lyrics = [
    'Smoking blunts in the project hallways\n Shooting dice all day',
    'Back in the days our parents used to take care of us\n Look at \'em now, they even fuckin\' scared of us',
    'If I wasn\'t in the rap game\n I\'d probably have a key knee-deep in the crack game\n Because the streets is a short stop\n Either you\'re slinging crack rock or you got a wicked jump shot',
    'Shit, it\'s hard being young from the slums\n Eating 5 cent gums, not knowing where your meal\'s coming from',
    'No need for that, just grab the fucking gat\n The first pocket that\'s fat, the Tec is to his back',
    'Nigga, you ain\'t got to explain shit\n I\'ve been robbing motherfuckas since the slave ships\n With the same clip and the same .45\n Two point blank, a motherfucker sure to die',
    'Then I\'m dipping up the block and I\'m robbing bitches too\n Up the herringbones and bamboos\n I wouldn\'t give a fuck if you\'re pregnant Give me the baby rings and the #1 Mom pendant',
    'I\'m slamming niggas like Shaquille, shit is real\n When it\'s time to eat a meal, I rob and steal',
    'Big up, big up, it\'s a stick up, stick up\n And I\'m shooting niggas quick if ya hiccup',
    'One in the chamber, thirty-two in the clip\n Motherfuckas better strip, (yeah nigga, peel)\n Before you find out how blue steel feel',
    'And when I rock her and drop her, I\'m taking her doorknockers\n And if she\'s resistant: blakka, blakka, blakka',
    'Tell him Biggie took it, what the fuck he gonna do?\n Man I hope apologetic or I\'m a have to set it\n And if I set it, the cocksucker won\'t forget it',
    'I fuck around and get hardcore\n C-4 to your door, no beef no more nigga',
    'Super Nintendo, Sega Genesis\n When I was dead broke, man, I couldn\'t picture this',
    'When I die, fuck it, I wanna go to hell\n \'Cause I\'m a piece of shit, it ain\'t hard to fuckin\' tell',
    'All my life I been considered as the worst\n Lyin\' to my mother, even stealin\' out her purse\n Crime after crime, from drugs to extortion\n I know my mother wish she got a fuckin\' abortion'
]

doc_oct_lyrics = [
    'Fuck my pussy, Doctor!\n',
    'I crank up lyrical flows, spit Spats, what\'s that?\n The pattern records, don\'t touch the DATs, yo',
    'Suckers with mics that end up with tooth decay\n I, the Doctor, stop ya, in your world, rock ya',
    'Scratches in mattress business money reattaches worldwide\n Deep inside stops the diamond rocks',
    'Hello, this is the offices of Dr. Octagon.\n If you have insurance or medical problems, I\'m here for you for any type\n of intestine surgery, rectal rebuilding, relocated saliva glands,\n and chimpanzee acne—and of course, moosebumps. You can call 1-800-PP5-1-doodoo. I\'m in your corner.',
    'First patient, pull out the skull, remove the cancer\n Breaking his back, chisel necks for the answer',
    'Supersonic-bionic-robot-voodoo power\n Equator ex my chance to flex skills on Ampex',
    'With power meters and heaters gauge anti-freeze\n Octagon oxygen, aluminum intoxicants',
    'More ways to blow blood cells in your face\n React with four bombs and six fire missiles',
    'Armed with seven rounds of space doo-doo pistols\n You may not believe, living on the Earth planet',
    'My skin is green and silver, forehead looking mean\n Astronauts get played, tough like the ukelele',
    'As I move in rockets, overriding, levels\n Nothing\'s aware, same data, same system',
    'Radiation leakage on the promenade deck, access for authorized personnel only',
    'Disappear again, zapped like an android\n Face the fact, I fly on planets every day\n My nucleus friend, prepare, I return again\n My 7XL is not yet invented'
]

eminem_lyrics = [
    'You don\'t wanna fuck with me\n Girls neither, you ain\'t nothin\' but a slut to me',
    'I invented violence, you vile venomous volatile vicious\n Vain Vicodin, vrin vrin vrin!',
    'Texas Chainsaw, left his brains all\n Danglin\' from his neck while his head barely hangs on',
    'Blood, guts, guns, cuts\n Knives, lives, wives, nuns, sluts — bitch, I\'ma kill you!',
    'I said you don\'t wanna fuck with Shady (Why?)\n ‘Cause Shady will fucking kill you',
    'I ain\'t "acid rap," but I rap on acid',
    'When I go out, I’ma go out shootin’\n I don’t mean when I die, I mean when I go out to the club, stupid!',
    'I’m tryin’ to clean up my fuckin’ image\n So I promised the fuckin’ critics\n I wouldn’t say “fuckin’” for six minutes\n Six minutes, Slim Shady, you’re on!',
    'My baby’s mom, bitch made me an angry blonde\n So I made me a song, killed her and put Hailie on',
    'Shit, half the shit I say, I just make it up\n To make you mad, so kiss my white naked ass',
    'You motherfuckin\' chickens ain\'t brave enough\n To say the stuff I say, so just tape it shut',
    'And if it\'s not a rapper that I make it as\n I\'ma be a fuckin\' rapist in a Jason mask',
    'The mother did drugs, hard liquor, cigarettes and speed\n The baby came out, disfigured ligaments, indeed\n It was a seed who would grow up just as crazy as she\n Don\'t dare make fun of that baby, ‘cause that baby was me',
    'I\'m a criminal, an animal caged who turned crazed\n But how the fuck you supposed to grow up when you weren\'t raised?',
    'My morals went *pffft* when the president got oral Sex in his Oval Office on top of his desk off of his own employee',
    '‘Cause if I ever stuck it to any singer in showbiz\n It\'d be Jennifer Lopez — and Puffy, you know this\n I\'m sorry Puff, but I don\'t give a fuck\n If this chick was my own mother\n I\'d still fuck her with no rubber and cum inside her\n And have a son and a new brother at the same time\n And just say that it ain\'t mine — what\'s my name?',
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
    'She let me hit it cause I\'m thuggin\'\n Squares need not apply, I\'m so fly I might fuck her cousin',
    '"We’re not against rap, but we\'re against those thugs"\nCan\'t be legit when every nigga in your clique sold drugs',
    'I hate to say it, ain\'t no need to be discreet\nIf she don\'t cop from me, she get it from a nigga up the street\nCause he thuggin\', and yo, she\'d probably suck his dick for it\n She turnt out so it ain\'t shit to turn a trick for it',
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
    'The music is like that green stuff\n Provided to you by sack man',
    'Pac man how in the fuck do you think we gon\' do that man?\n Ridin\' round Old National on 18\'s without no gat man',
    'I\'m strapped man & ready to bust on any nigga like that man\n Me and my nigga we roll together like Batman and Robin',
    'Twice upon a time there was a boy who died twice\n And lived happily ever after but that\'s another chapter',
    'Live from home of the brave with dirty dollars\n And beauty parlors & baby bottles and bowling ball Impalas',
    'And street scholars that\'s majoring in culinary arts\n You know how to work bread cheese and dough\n From scratch but see the catch is you can get caught\n Know what ya sellin\' what ya bought so cut that big talk',
    'Let\'s walk to the bridge now meet me halfway\n Now you may see some children dead off in the pathway\n It\'s them poor babies walkin\' slowly to the candy lady',
    'Like the words maybe, if, or probably more than a hobby\n When my turntables get wobbly they don\'t fall',
    'The name is Big Boi Daddy Fat Sax\n The nigga that like them Cadillacs',
    'Get off the testicles and the nut sacks\n You bust a rhyme we bust back',
    'My mind warps and bends floats the wind count to ten\n Meet the twin Andre Ben. welcome to the lion\'s den',
    'Original skin many men comprehend\n I extend myself so you go out and tell a friend',
    'Sin all depends on what you believing in\n Faith is what you make it that\'s the hardest shit since MC Ren',
    'Alien can blend right on in wit\' yo\' kin\n Look again \'cause I swear I spot one every now and then',
    'It\'s happenin\' again wish I could tell you when\n Andre this is Andre y\'all just gon\' have to make amends'
]

big_L_lyrics = [
    'I knocked out so many teeth the tooth fairy went bankrupt',
    'Fucking punk you ain\'t a leader, nobody followed you, you was never shit your mother should\'ve swallowed you...',
    'I\'m tellin you shit is about to get drastic soon\n I\'m quick to blast a goon\n And break a motherfucker like a plastic spoon',
    'Some say I\'m ruthless, some say I\'m grim\n Once a brother done broke into my house and I robbed him',
    'Old folks get mugged and raided\n Crimes are drug related\n And we live by the street rules that thugs created',
    'I got drug spots from New York to Canada\n Cause Big L be fuckin\' with more keys than a janitor',
    'I made every little kid from my hood run\n I was just like that little bastard from the Good Son',
    'L da Harlem pimp baby, for real\n I got mo\' dimes dan dat Sprint Lady',
    'What’s this motherfuckin rap game without L?\n Yo, that’s like jewels without ice\n That’s like china without rice or the Holy Bible without Christ',
    'To be seen clean in the mean Beam\n Is every team’s dream; Big L’s a cream fiend\n With more green than Springsteen',
    'I’m so ahead of my time my parents haven’t met yet',
    'Cause I got all of ‘em strung jack\n My girls are like boomerangs\n No matter how far I throw \'em, they come back',
    'Facts on tracks I recite well\n Everybody wanna be like Mike, but Mike wanna be like L',
    '"I got more riches than you, fuck more bitches than you\n Only thing I haven\'t got is more stitches than you',
    'Breaking in cribs with a crowbar\n I wasn\'t poor, I was po\' - I couldn\'t afford the \'o-r\''
]

BOT_PREFIX = ("+")


client = Bot(command_prefix=BOT_PREFIX)
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
        *kanye_lyrics,
        *gucci_lyrics,
        *random_lyrics,
        *nas_lyrics,
        *E40_lyrics,
        *snoop_dogg_lyrics,
        *three_six_lyrics,
        *project_pat_lyrics,
        *wu_tang_lyrics,
        *biggie_lyrics,
        *doc_oct_lyrics,
        *eminem_lyrics,
        *freddie_gibbs_lyrics,
        *big_L_lyrics,
        *outkast_lyrics
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

"""
def convert(temp, unit):
    unit = unit.lower()

    if unit == 'c':
        temp = 9.0 / 5.0 * temp + 32
        return "%s F"% temp
    if unit == 'f':
        temp = (temp - 32) / 9.0 * 5.0
        return "%s C"% temp
"""

@client.event
async def on_ready():
    print("It's Gucci Time!")
    init_markov()
    await client.change_presence(game=discord.Game(name='+help for command list!'))

"""
# Sends a message to a new member that joins the discord server.
@client.event
async def on_member_join(member):
    await client.send_message(member, "Sup!? It's ya boy Young LD, and my sole purpose in this world is to provide you and your crew with some dank, absurd, hard hittin' rap lyrics.\n" 
    "For a list of all available commands, use the +help command.\n"
    "ps - Wu-Tang is 4 da children and don't forget to Protect Ya Kneck.")

    
    TODO
    List of potential artist
     - Kendrick
     - Trick Daddy
        - add to random
     - Tupac
    Hip-Hop Facts
    
"""
@client.event
async def on_message(message):
    # Don't need the bot to reply to itself.
    if message.author == client.user:
        return

    # Randomly picks a lyric from the list of kanye_lyrics
    if message.content.upper().startswith('+KANYE'):
        await client.send_message(message.channel, random.choice(kanye_lyrics))

    # Randomly picks a lyric from the list of gucci_lyrics
    if message.content.upper().startswith('+GUCCI'):
        await client.send_message(message.channel, random.choice(gucci_lyrics))

    # Randomly picks a lyrics from the list of random_lyrics
    if message.content.upper().startswith('+RANDOM'):
        await client.send_message(message.channel, random.choice(random_lyrics))

    # Randomly picks lyrics from the list of nas_lyrics
    # primarily lyrics from illmatic aka the best hip hop album of all time
    if message.content.upper().startswith('+NAS'):
        await client.send_message(message.channel, random.choice(nas_lyrics))

    # Randomly picks lyrics from the list of E40_lyrics
    if message.content.upper().startswith('+E40'):
        await client.send_message(message.channel, random.choice(E40_lyrics))

    # Randomly picks lyrics from the list of snoop_dogg_lyrics
    if message.content.upper().startswith('+SNOOP'):
        await client.send_message(message.channel, random.choice(snoop_dogg_lyrics))

    # Randomly picks lyrics from the list of three_six_lyrics
    if message.content.upper().startswith('+TRIPLE6'):
        await client.send_message(message.channel, random.choice(three_six_lyrics))

    # Randomly picks lyrics from the list of project_pat_lyrics
    if message.content.upper().startswith('+PAT'):
        await client.send_message(message.channel, random.choice(project_pat_lyrics))

    # Randomly picks lyrics from the list of wu_tang_lyrics
    if message.content.upper().startswith('+WUTANG'):
        await client.send_message(message.channel, random.choice(wu_tang_lyrics))

    # Randomly picks lyrics from the list of biggie_lyrics
    if message.content.upper().startswith('+BIGGIE'):
        await client.send_message(message.channel, random.choice(biggie_lyrics))

    # Rancomly picks lyrics from the list of doc_oct_lyrics
    if message.content.upper().startswith('+DROCTAGON'):
        await client.send_message(message.channel, random.choice(doc_oct_lyrics))

    # Randomly picks lyrics from the list of eminem_lyrics
    if message.content.upper().startswith('+EMINEM'):
        await client.send_message(message.channel, random.choice(eminem_lyrics))

    # Randomly picks lyrics from the list of gangsta gibbs lyrics
    if message.content.upper().startswith('+GIBBS'):
        await client.send_message(message.channel, random.choice(freddie_gibbs_lyrics))

    # Randomly picks lyrics from the list of Big L lyrics
    if message.content.upper().startswith('+BIGL'):
        await client.send_message(message.channel, random.choice(big_L_lyrics))

    # Randomly picks lyrics from the list of Outkast lyrics
    if message.content.upper().startswith('+OUTKAST'):
        await client.send_message(message.channel, random.choice(outkast_lyrics))

    # Displays the bots personal opinion on who are the top 10 best hip-hop artist of all time
    if message.content.upper().startswith('+TOP10'):
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
    if message.content.upper().startswith('+PRODUCERS'):
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

    if message.content.upper().startswith('+SPIT'):
        await client.send_message(message.channel, spit_game())

    if message.content.upper().startswith('+HELP'):
        await client.send_message(message.channel,'```\n' 'Command List\n' + '+kanye\n' +
                                  '+gucci\n' + '+nas\n' + '+e40\n' '+snoop\n' + '+triple6\n' + '+pat\n' + '+wutang\n' + '+biggie\n' + '+droctagon\n' + '+eminem\n' + '+gibbs\n' + '+bigl\n' + '+outkast\n' + '+random \n'
                                   + '+top10\n' +  '+producers\n' + '+spit' + '```\n')

"""
FIX THIS SHIT LATER
@client.command()
async def info(ctx):
    embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="<YOUR-USERNAME>")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(client.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)

client.remove_command('help')

@client.command()
async def help(ctx):
    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)

    embed.add_field(name="$add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="$multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="$greet", value="Gives a nice greet message", inline=False)
    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)

    await ctx.send(embed=embed)
"""

async def list_server():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_server())
#client.run(TOKEN)
client.run(os.getenv('TOKEN'))
