from superperms import *

perms = ["".join([str(p) for p in perm]) for perm in Permutator(list(range(7))).results]

a = "012345601234506123450162345012634501236450123465012340561234051623405126340512364051234605123406512340156234015263401523640152346015234061523401652340125634012536401253460125340612534016253401265340123564012354601235406123540162354012635401236540123045612304516230451263045123604512306451230465123041562304152630415236041523064152304615230416523041256304125360412530641253046125304162530412653041235604123506412350461235041623504126350412365041230564132065413206451320641532064135204613250461320546132045613204651320461532046135204163250416320541632045163204156320416532041635204136520143562014352601432560143265014326051432601543260145326014352061432506143205614320651432061543206145320614352016432501643205164320156432016543201645320164352014632501463205146320154632014563201465320146352014365201346520136452013654201356420135462013542601345260134256013426501342605134260153426013542061345206134250613420561342065134206153420613542016345201634250163420516342015634201653420163542013652401356240135264013256401326540132645013264051326401532640135246013254601324560132465013246051324601532460135240613254061324506132405613240651324061532406135240163254016324501632405163240156324016532401635240136520413562041352604132560413265041326054132604513260415326041352064132506413205641302561430256134025163042516302451630254163025146302516430251634025136402513460251340625134026513042651302465130264513026541302651430265134025613042561302456130254613025641305261430526134052163045216305421630524163052146305216430521634052136405213460521340652134056213450621345602134562013456210346521034625103462150346125036412503614250361245036125403612504361250346152036415203614520361542036152403615204361520346150236415023614502361540236150423615024361502346150324165032415603241506342150634125063415206341502634150623415063241503624150326415032461503426150346210534612053641205361420536124053612045361205436120534610253641025361402536104253610245361025436102534610523641052361405236104523610542361052436105234610532416053241065342106534120653410265341062534106523410653241056342105634120563410256341052634105623410563241053624105326410532461053426105346210354261035421603452160342516032451603254106325410362541032651403261540326145032614053261403526140325614032651043261504326105432610453261043526104325610432651034265103246510326451036245103642510364521036451203654120356412035461203541620345162034156203416520341625034162053416203541260345126034152603412560341265034126053412603541206354120365142035614203516420315642031654203164520316425031642053164203514620315462031456203146520314625031462053146203514260315426031452603142560314265031426053142603514206315420631452063142506314205631420653142063514203651240356124035162403156240316524031625403162450316240531624035126403152640312564031265403126450312640531264035124603152460312546031245603124650312460531246035124063152406312540631245063124056312406531240635124036512043561204351620431562043165204316250431620543162045316204351260431526043125604312650431260543126045312604351206431520643125064312056431206543120645312064351204631520463125046312054631204563120465312046351204365120346512036451023654102356410235461023541602345160234156023416502341605234160253416023541062354102635410236514023561402351640231564023165402316450231640523164025316402351460231546023145602314650231460523146025314602351406231540623145062314056231406523140625314062351402631540263145026314052631402563140265314026351402365104235610423516042315604231650423160542316045231604253160423510642315064231056423106542310645231064253106423510462315046231054623104562310465231046253104623510426315042631054263104526310425631042653104263510423651024356102435160243156024316502431605243160254316024531602435106243150624310562431065243106254310624531062435102643150264310526431025643102654310264531026435102463150246310524631025463102456310246531024635102436510234651023645103265410325641032546103254160325146032154603214560321465032146053214603521460325164032156403216540321645032164053216403521640325160432156043216504321605432160453216043521604325160342156034216503421605342160354210635241036524103562410352641035246103524160352410635214063251406321540632145063214056321406532140635210463251046321504632105463210456321046532104635210643251064321506432105643210654321064532106435210634512063451026345106234510632451063425106345210635421036542103564210354621034561203456102345610324561034256103452610345621304652130462513046215304621350462130546213045621340526130452613054261305246130526413056241306524130625413062451306241530624135062413056421306542130645213064251306421536042135604213650241360524136025413602451360241536024135602413650214360521436025143620513462051364205136240513620451362054136205143625013462501364250136245013625401362504136250143625104362150436210543621045362104356210436521043625140362154036214503621405362140356214036521403625143062154306214530621435062143056214306521430625143602154360214536021435602143650213465021364502136540213564021354602135406213540261350426135024613502641350261435026134502613540216350421635024163502146350216435021634502163540213650421360542136045213604251360421536402153460215340621534026153042615302461530264153026145302615430261534021653042165302416530214653021645302165430216534021563042156302415630214563021546302156430215634021536420153624015362041536201453620154362015346201536421053642150364215306421350642130564123054612305416230541263054123605412306541230145623014526301452360145230614523016452301465230142563014253601425306142530164253014625301426530142356014235061423501642350146235014263501423650142305614230516423051462305142630514236051423065142301564230154623015426301542360154230615423016542301245630124536012453061245301624530126453012465301243560124350612435016243501264350124635012436501243056124305162430512643051246305124360512430651243015624301526430152463015243601524306152430165243012564301254630125436012543061254301625430126543012"

for perm in perms:
	assert perm in a
	
print(len(a))


