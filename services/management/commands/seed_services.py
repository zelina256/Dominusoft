"""Run: python manage.py seed_services

Place this file in YOUR_APP/management/commands/ and models.py in YOUR_APP/.
Repeated runs update the four source services and matching children, without
removing other records. Review editorial copy before publishing.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from ...models import (Services, ServiceDetail, ServiceHighlight, ServiceBenefit,
                       ServicePackage, ServicePackageItem, ServiceOffering)

DATA = [{'name': 'B2B Professional Training',
  'slug': 'b2b-professional-training',
  'meta_title': 'B2B Professional Training & Trajnime për Biznese | Dominusoft',
  'meta_description': 'Trajnime profesionale B2B të përshtatura për kompani dhe ekipe. Dominusoft '
                      'ndërton programe praktike për zhvillimin e aftësive profesionale dhe '
                      'digjitale.',
  'detail': {'title': 'B2B Professional Training për Biznese dhe Ekipe',
             'lead': 'Zhvilloni aftësitë e ekipit tuaj me trajnime profesionale të ndërtuara mbi '
                     'nevojat reale të biznesit.',
             'summary': 'Në Dominusoft besojmë se zhvillimi i një biznesi fillon nga zhvillimi i '
                        'njerëzve që e ndërtojnë atë. Përmes B2B Professional Training, krijojmë '
                        'programe trajnimi të personalizuara për kompani, institucione dhe ekipe '
                        'që kërkojnë të zhvillojnë kompetenca të reja dhe të përshtaten me '
                        'kërkesat e tregut.',
             'summary_additional': 'Trajnimet kombinojnë njohuritë profesionale me praktikën, duke '
                                   'krijuar një eksperiencë mësimi që mund të aplikohet '
                                   'drejtpërdrejt në punën e përditshme.',
             'why_section_title': 'Pse Dominusoft për B2B Professional Training?',
             'why_section_subtitle': 'Një qasje e ndërtuar rreth biznesit tuaj',
             'why_section_body': 'Në Dominusoft, trajnimi profesional nuk nis nga një program '
                                 'standard, por nga nevojat reale të kompanisë dhe ekipit. '
                                 'Analizojmë objektivat, nivelin aktual të pjesëmarrësve dhe '
                                 'aftësitë që biznesi kërkon të zhvillojë, për të ndërtuar një '
                                 'program trajnimi të përshtatur dhe me fokus praktik.\n'
                                 '\n'
                                 'Eksperienca jonë në edukimin profesional dhe fushën digjitale na '
                                 'mundëson të kombinojmë njohuritë me situata dhe procese që '
                                 'profesionistët hasin në punën e përditshme. Synimi është që '
                                 'njohuritë e fituara gjatë trajnimit të mos mbeten vetëm teori, '
                                 'por të kthehen në aftësi që ekipi mund t’i aplikojë në punë.',
             'benefits_section_title': 'Përfitimet kryesore të trajnimeve B2B',
             'benefits_intro': 'Investimi në trajnimin dhe zhvillimin profesional të stafit '
                               'ndihmon kompanitë të ndërtojnë ekipe më të përgatitura, të '
                               'përmirësojnë kompetencat e brendshme dhe të përshtaten me '
                               'ndryshimet teknologjike dhe profesionale.\n'
                               '\n'
                               'Programet B2B të Dominusoft ndërtohen për të krijuar vlerë si për '
                               'pjesëmarrësit, ashtu edhe për organizatën.',
             'packages_section_title': 'Paketat e trajnimeve B2B',
             'projects_section_title': 'Projekte / Trajnime të realizuara',
             'cta_text': 'Kërko një konsultë',
             'cta_url': '#kontakt'},
  'highlights': [{'title': 'Trajnime të personalizuara',
                  'description': 'Përmbajtja dhe niveli i trajnimit përshtaten sipas nevojave, '
                                 'objektivave dhe profilit të ekipit.'},
                 {'title': 'Mësim përmes praktikës',
                  'description': 'Programet kombinojnë konceptet kryesore me ushtrime, shembuj dhe '
                                 'situata konkrete nga mjedisi profesional.'},
                 {'title': 'Ekspertizë profesionale dhe digjitale',
                  'description': 'Trajnimet zhvillohen me fokus në aftësi relevante për mënyrën se '
                                 'si bizneset dhe profesionistët punojnë sot.'},
                 {'title': 'Fokus te rezultatet',
                  'description': 'Objektivi është zhvillimi i kompetencave që pjesëmarrësit mund '
                                 't’i përdorin edhe pas përfundimit të trajnimit.'}],
  'benefits': [{'title': 'Zhvillim i aftësive profesionale',
                'description': 'Ekipi fiton njohuri dhe kompetenca të reja që lidhen drejtpërdrejt '
                               'me punën dhe përgjegjësitë e tij.'},
               {'title': 'Trajnim sipas nevojave të kompanisë',
                'description': 'Programi përshtatet me nivelin, objektivat dhe sfidat konkrete të '
                               'organizatës.'},
               {'title': 'Më shumë praktikë, më pak teori',
                'description': 'Fokusi vendoset te aplikimi i njohurive përmes ushtrimeve dhe '
                               'situatave reale profesionale.'},
               {'title': 'Përmirësim i performancës së ekipit',
                'description': 'Zhvillimi i kompetencave ndihmon punonjësit të përdorin më mirë '
                               'mjetet, proceset dhe njohuritë e nevojshme për rolin e tyre.'},
               {'title': 'Zhvillim i vazhdueshëm profesional',
                'description': 'Trajnimi krijon një bazë mbi të cilën punonjësit mund të vazhdojnë '
                               'të zhvillojnë aftësitë dhe ekspertizën e tyre.'}],
  'packages': [{'name': 'Team Training',
                'description': 'Trajnime profesionale për ekipe që kërkojnë të zhvillojnë '
                               'kompetenca specifike dhe të përmirësojnë mënyrën e punës.',
                'items': []},
               {'name': 'Custom Corporate Training',
                'description': 'Program trajnimi i ndërtuar posaçërisht rreth objektivave, stafit '
                               'dhe nevojave të kompanisë.',
                'items': []}],
  'offerings': []},
 {'name': 'Design',
  'slug': 'design-branding',
  'meta_title': 'Design & Branding për Biznese | Dominusoft',
  'meta_description': 'Shërbime profesionale design dhe branding për biznese. Logo, identitet '
                      'vizual, materiale promocionale dhe dizajn digjital nga Dominusoft.',
  'detail': {'title': 'Design & Branding që i Jep Identitet Biznesit Tuaj',
             'lead': 'Nga ideja te identiteti vizual, krijojmë design që e bën brand-in tuaj të '
                     'dallueshëm dhe të qëndrueshëm.',
             'summary': 'Një brand nuk është vetëm një logo. Është mënyra se si një biznes '
                        'prezantohet, komunikon dhe mbahet mend.\n'
                        '\n'
                        'Dominusoft ofron shërbime profesionale design dhe branding, duke '
                        'kombinuar kreativitetin me një qasje të strukturuar për të ndërtuar '
                        'identitete vizuale që përfaqësojnë karakterin dhe vlerat e biznesit.',
             'summary_additional': 'Nga logo dhe identiteti vizual te materialet promocionale dhe '
                                   'përmbajtja për kanalet digjitale, çdo element ndërtohet për të '
                                   'komunikuar në mënyrë të qartë dhe konsistente.',
             'why_section_title': 'Pse të zgjidhni Dominusoft për Design & Branding?',
             'why_section_subtitle': 'Design i menduar për brand-in tuaj',
             'why_section_body': 'Në Dominusoft, Design & Branding nis me kuptimin e biznesit '
                                 'përpara se të kalojë te pjesa vizuale. Analizojmë identitetin, '
                                 'audiencën dhe mënyrën se si brand-i duhet të komunikojë, për të '
                                 'krijuar një prezencë vizuale që është e dallueshme, profesionale '
                                 'dhe në përputhje me objektivat e biznesit.\n'
                                 '\n'
                                 'Kombinojmë kreativitetin, strategjinë dhe design-in për të '
                                 'ndërtuar një identitet që funksionon në mënyrë konsistente në '
                                 'website, rrjete sociale, materiale promocionale dhe komunikim të '
                                 'printuar. Çdo element vizual krijohet si pjesë e të njëjtit '
                                 'brand, jo si një design i izoluar.',
             'benefits_section_title': 'Përfitimet kryesore të Design & Branding për biznesin tuaj',
             'benefits_intro': 'Një identitet vizual profesional e ndihmon biznesin të prezantohet '
                               'në mënyrë më të qartë dhe konsistente. Kur logoja, ngjyrat, '
                               'tipografia dhe materialet grafike ndjekin të njëjtën gjuhë '
                               'vizuale, brand-i bëhet më i lehtë për t’u identifikuar dhe për t’u '
                               'mbajtur mend.\n'
                               '\n'
                               'Shërbimet Design & Branding të Dominusoft synojnë të krijojnë një '
                               'identitet që jo vetëm duket profesional, por funksionon në të '
                               'gjitha pikat ku biznesi komunikon me audiencën.',
             'packages_section_title': 'Paketat Design & Branding',
             'projects_section_title': 'Projekte të realizuara',
             'cta_text': 'Kërko një konsultë',
             'cta_url': '#kontakt'},
  'highlights': [{'title': 'Qasje e personalizuar',
                  'description': 'Nuk punojmë me një formulë të njëjtë për çdo biznes. Identiteti '
                                 'vizual ndërtohet duke marrë parasysh karakterin, audiencën dhe '
                                 'pozicionimin e brand-it tuaj.'},
                 {'title': 'Design me qëllim',
                  'description': 'Çdo zgjedhje vizuale, nga ngjyrat dhe tipografia te elementet '
                                 'grafike, duhet të ndihmojë brand-in të komunikojë më qartë dhe '
                                 'të krijojë një identitet të dallueshëm.'},
                 {'title': 'Konsistencë në çdo kanal',
                  'description': 'Ndërtojmë një gjuhë vizuale që mund të aplikohet në mënyrë të '
                                 'qëndrueshme në website, social media, materiale marketingu dhe '
                                 'print.'},
                 {'title': 'Branding që mund të zhvillohet me biznesin',
                  'description': 'Krijojmë baza vizuale që nuk i shërbejnë vetëm nevojave të '
                                 'momentit, por mund të përshtaten ndërsa biznesi dhe komunikimi i '
                                 'tij zhvillohen.'}],
  'benefits': [{'title': 'Identitet vizual i dallueshëm',
                'description': 'Krijoni një prezencë që reflekton personalitetin dhe vlerat e '
                               'biznesit tuaj dhe e ndihmon brand-in të dallohet.'},
               {'title': 'Imazh më profesional i biznesit',
                'description': 'Një sistem vizual i mirëstrukturuar krijon një prezantim më serioz '
                               'dhe koherent përballë klientëve dhe partnerëve.'},
               {'title': 'Konsistencë e brand-it',
                'description': 'Ruani të njëjtën gjuhë vizuale në website, rrjete sociale, '
                               'prezantime, materiale promocionale dhe print.'},
               {'title': 'Komunikim vizual më i qartë',
                'description': 'Design-i ndihmon që mesazhet, produktet dhe shërbimet e biznesit '
                               'të prezantohen në mënyrë më të organizuar dhe të kuptueshme.'},
               {'title': 'Brand i përshtatshëm për kanale të ndryshme',
                'description': 'Elementet vizuale projektohen që të funksionojnë si në platformat '
                               'digjitale, ashtu edhe në materialet fizike të biznesit.'}],
  'packages': [{'name': 'Brand Starter',
                'description': 'Për biznese të reja që duan të ndërtojnë një identitet vizual '
                               'profesional që nga fillimi.',
                'items': ['Logo Design – 2 koncepte',
                          'Primary Logo + Logo Variation',
                          'Paleta e ngjyrave',
                          'Typography Selection',
                          'Favicon',
                          'Social Media Profile & Cover',
                          'Mini Brand Guide',
                          'Formate për web & print',
                          '2 raunde rishikimesh'],
                'is_featured': False},
               {'name': 'Brand Identity',
                'description': 'Për biznese që kërkojnë një identitet të plotë dhe konsistent në '
                               'çdo kanal komunikimi.',
                'items': ['Brand Discovery',
                          'Logo Suite – Primary, Secondary & Icon',
                          'Color System',
                          'Typography System',
                          'Visual Style & Graphic Elements',
                          'Business Card',
                          'Email Signature',
                          'Social Media Kit',
                          'Brand Guidelines',
                          'Mockups të aplikimit të brand-it',
                          'Source Files',
                          '3 raunde rishikimesh'],
                'is_featured': True},
               {'name': 'Brand Strategy & Rebranding',
                'description': 'Për kompani që duan të ripozicionojnë, modernizojnë ose ndërtojnë '
                               'nga e para një brand më të plotë.',
                'items': ['Brand Audit',
                          'Competitor & Market Analysis',
                          'Brand Positioning',
                          'Brand Personality & Direction',
                          'Logo & Complete Visual Identity',
                          'Advanced Color & Typography System',
                          'Graphic Elements / Patterns',
                          'Tone of Voice & Messaging Direction',
                          'Social Media Brand Kit',
                          'Business & Marketing Collateral',
                          'Comprehensive Brand Guidelines',
                          'Rebranding / Brand Rollout Direction',
                          'Source Files',
                          'Konsultë për implementimin e brand-it'],
                'is_featured': False}],
  'offerings': []},
 {'name': 'Online Marketing',
  'slug': 'online-marketing',
  'meta_title': 'Online Marketing & Marketing Digjital | Dominusoft',
  'meta_description': 'Shërbime online marketing për biznese: social media, content creation dhe '
                      'fushata digjitale. Ndërtoni prezencën online me Dominusoft.',
  'detail': {'title': 'Online Marketing për Rritjen e Biznesit Tuaj',
             'lead': 'Ndërtojmë strategji digjitale që e lidhin biznesin tuaj me audiencën e '
                     'duhur.',
             'summary': 'Të jesh online nuk mjafton. Biznesi duhet të dijë çfarë të komunikojë, '
                        'kujt t’ia komunikojë dhe pse.\n'
                        '\n'
                        'Dominusoft ofron shërbime Online Marketing dhe Digital Marketing për '
                        'biznese që kërkojnë të ndërtojnë një prezencë më profesionale dhe të '
                        'strukturuar në kanalet digjitale.',
             'summary_additional': 'Nga strategjia dhe krijimi i përmbajtjes te menaxhimi i '
                                   'rrjeteve sociale dhe fushatat online, çdo aktivitet ndërtohet '
                                   'rreth objektivave të biznesit.',
             'why_section_title': 'Pse të zgjidhni Dominusoft për Online Marketing?',
             'why_section_subtitle': 'Marketing digjital i ndërtuar rreth biznesit tuaj',
             'why_section_body': 'Në Dominusoft, Online Marketing nuk fillon me publikimin e '
                                 'postimeve, por me kuptimin e biznesit, audiencës dhe objektivave '
                                 'që dëshironi të arrini.\n'
                                 '\n'
                                 'Ndërtojmë një qasje të personalizuar ku strategjia digjitale, '
                                 'content creation, social media management dhe fushatat online '
                                 'funksionojnë së bashku. Qëllimi është të krijojmë një prezencë '
                                 'online konsistente, relevante për audiencën dhe të lidhur me '
                                 'objektivat reale të biznesit.',
             'benefits_section_title': 'Përfitimet kryesore të Online Marketing për biznesin tuaj',
             'benefits_intro': 'Një strategji e mirë e marketingut digjital e ndihmon biznesin të '
                               'jetë prezent aty ku ndodhet audienca e tij, të komunikojë në '
                               'mënyrë më profesionale dhe të ndërtojë marrëdhënie afatgjata me '
                               'klientët.\n'
                               '\n'
                               'Me shërbimet Online Marketing të Dominusoft, strategjia, '
                               'përmbajtja dhe promovimi trajtohen si pjesë të së njëjtës prezencë '
                               'digjitale.',
             'packages_section_title': 'Paketat Online Marketing',
             'projects_section_title': 'Projekte të realizuara',
             'cta_text': 'Kërko një konsultë',
             'cta_url': '#kontakt'},
  'highlights': [{'title': 'Strategji e personalizuar',
                  'description': 'Çdo biznes ka një audiencë dhe objektiva të ndryshme. Për këtë '
                                 'arsye, strategjia përshtatet me brand-in, tregun dhe kanalet ku '
                                 'ka më shumë kuptim të komunikojë.'},
                 {'title': 'Content me qëllim',
                  'description': 'Krijojmë përmbajtje që nuk synon vetëm të plotësojë kalendarin e '
                                 'publikimeve, por të informojë, të angazhojë dhe të komunikojë '
                                 'vlerën e brand-it.'},
                 {'title': 'Komunikim konsistent',
                  'description': 'Ruajmë të njëjtin identitet, ton komunikimi dhe mesazh në '
                                 'kanalet digjitale, duke ndihmuar në ndërtimin e një prezence më '
                                 'të qëndrueshme.'},
                 {'title': 'Vendimmarrje e bazuar në të dhëna',
                  'description': 'Monitorojmë performancën e përmbajtjes dhe fushatave për të '
                                 'kuptuar çfarë funksionon dhe ku ka hapësirë për optimizim.'}],
  'benefits': [{'title': 'Prezencë më e fortë online',
                'description': 'Ndërtoni një imazh profesional dhe të qëndrueshëm të biznesit në '
                               'kanalet digjitale.'},
               {'title': 'Arritje e audiencës së duhur',
                'description': 'Strategjia dhe fushatat orientohen drejt segmenteve të audiencës '
                               'që janë relevante për produktet ose shërbimet tuaja.'},
               {'title': 'Content profesional dhe konsistent',
                'description': 'Komunikoni rregullisht me përmbajtje të përshtatur me identitetin, '
                               'mesazhin dhe objektivat e brand-it.'},
               {'title': 'Rritje e ndërveprimit me audiencën',
                'description': 'Përmbajtja dhe komunikimi strategjik krijojnë më shumë mundësi për '
                               'ndërveprim mes brand-it dhe klientëve potencialë.'},
               {'title': 'Matje dhe optimizim i performancës',
                'description': 'Analiza e rezultateve ndihmon në përmirësimin e vazhdueshëm të '
                               'përmbajtjes, fushatave dhe strategjisë së marketingut.'}],
  'packages': [{'name': 'Digital Presence',
                'description': 'Për biznese që duan të ndërtojnë dhe menaxhojnë një prezencë '
                               'profesionale dhe konsistente në rrjetet sociale.',
                'items': ['Social Media Strategy',
                          'Menaxhim të 2 platformave sociale',
                          'Monthly Content Plan',
                          'Content Creation',
                          'Copywriting për postimet',
                          'Graphic Design për Social Media',
                          'Scheduling & Publishing',
                          'Basic Community Management',
                          'Monthly Performance Report'],
                'is_featured': False},
               {'name': 'Digital Growth',
                'description': 'Për biznese që duan të rrisin prezencën online dhe të kombinojnë '
                               'content marketing me fushata të targetuara.',
                'items': ['Digital Marketing Strategy',
                          'Menaxhim të platformave kryesore',
                          'Monthly Content Calendar',
                          'Content Creation & Copywriting',
                          'Social Media Design',
                          'Short-form Content / Reels',
                          'Meta Ads Campaign Management',
                          'Audience Targeting',
                          'Community Management',
                          'Performance Monitoring',
                          'Monthly Reporting & Optimization'],
                'is_featured': True},
               {'name': 'Digital Performance',
                'description': 'Për kompani që kërkojnë një qasje më të plotë dhe të orientuar '
                               'drejt rritjes dhe performancës digjitale.',
                'items': ['Advanced Digital Marketing Strategy',
                          'Social Media Management',
                          'Content Strategy & Creation',
                          'Campaign Planning',
                          'Meta Ads Management',
                          'Google Ads Management',
                          'Remarketing Campaigns',
                          'Audience & Competitor Analysis',
                          'Landing Page Recommendations',
                          'Campaign Optimization',
                          'Analytics & Performance Tracking',
                          'Detailed Monthly Reporting',
                          'Monthly Strategy Consultation'],
                'is_featured': False}],
  'offerings': [{'title': 'Google Ads'},
                {'title': 'Meta Ads'},
                {'title': 'SEO Content'},
                {'title': 'Blog & Article Writing'},
                {'title': 'Email Marketing'},
                {'title': 'Newsletter Design'},
                {'title': 'Photography & Video Content'},
                {'title': 'Reels & Short-form Video'},
                {'title': 'Landing Page Design'}]},
 {'name': 'Website Design & Development',
  'slug': 'website-design-development',
  'meta_title': 'Website Design & Development për Biznese | Dominusoft',
  'meta_description': 'Krijim dhe zhvillim website profesional për biznese. UI/UX, responsive web '
                      'design, SEO dhe performancë me zgjidhje të personalizuara nga Dominusoft.',
  'detail': {'title': 'Website Design & Development për Biznese',
             'lead': 'Ndërtojmë website moderne që kombinojnë design-in, teknologjinë dhe '
                     'eksperiencën e përdoruesit.',
             'summary': 'Website-i është më shumë sesa prezenca online e një biznesi. Për shumë '
                        'klientë, është kontakti i parë me brand-in tuaj.\n'
                        '\n'
                        'Në Dominusoft projektojmë dhe zhvillojmë website profesionale, responsive '
                        'dhe të personalizuara, duke kombinuar UI/UX Design me zhvillimin web dhe '
                        'optimizimin teknik.',
             'summary_additional': 'Nga struktura fillestare te publikimi final, çdo website '
                                   'ndërtohet duke pasur në fokus identitetin e biznesit, '
                                   'përdoruesin dhe objektivat që faqja duhet të përmbushë.',
             'why_section_title': 'Pse të zgjidhni Dominusoft për Website Design & Development?',
             'why_section_body': 'Në Dominusoft, një website nuk ndërtohet vetëm për të qenë '
                                 'prezent online. Ai projektohet për të përfaqësuar '
                                 'profesionalisht biznesin, për të krijuar një eksperiencë të mirë '
                                 'për përdoruesin dhe për të mbështetur objektivat e tij '
                                 'digjitale.\n'
                                 '\n'
                                 'Kombinojmë UI/UX Design, zhvillimin web, responsive design dhe '
                                 'optimizimin SEO në një proces të vetëm, duke krijuar website të '
                                 'personalizuara sipas identitetit dhe nevojave të çdo biznesi.',
             'benefits_section_title': 'Përfitimet kryesore të Website Design & Development',
             'benefits_intro': 'Krijim website me fokus te përdoruesi dhe biznesi\n'
                               '\n'
                               'Një website profesional duhet të bëjë më shumë sesa të duket '
                               'bukur. Duhet të jetë i qartë, i shpejtë, i përshtatshëm për mobile '
                               'dhe ta drejtojë vizitorin natyrshëm drejt informacionit ose '
                               'veprimit që kërkon. Dominusoft ndërthur web design, UI/UX dhe '
                               'zhvillimin e website-it për të krijuar një eksperiencë që '
                               'përfaqëson profesionalisht biznesin dhe funksionon në çdo pajisje.',
             'packages_section_title': 'Paketat e Shërbimeve Website Design & Development',
             'projects_section_title': 'Projekte të realizuara',
             'cta_text': 'Diskuto projektin tuaj',
             'cta_url': '#kontakt'},
  'highlights': [{'title': 'Zgjidhje të personalizuara',
                  'description': 'Çdo biznes është i ndryshëm. Struktura, design-i dhe '
                                 'funksionalitetet e website-it përshtaten me brand-in, audiencën '
                                 'dhe objektivat që dëshironi të arrini.'},
                 {'title': 'Design me fokus te përdoruesi',
                  'description': 'Ndërtojmë ndërfaqe intuitive dhe struktura të qarta që e '
                                 'ndihmojnë vizitorin të gjejë informacionin lehtësisht dhe të '
                                 'ndërveprojë natyrshëm me website-in.'},
                 {'title': 'Website responsive në çdo pajisje',
                  'description': 'Website-et projektohen për të ofruar një eksperiencë të '
                                 'qëndrueshme në desktop, tablet dhe mobile, pavarësisht madhësisë '
                                 'së ekranit.'},
                 {'title': 'SEO dhe performancë që nga struktura',
                  'description': 'SEO nuk trajtohet vetëm pas përfundimit të website-it. Struktura '
                                 'e faqeve, hierarkia e përmbajtjes dhe elementet teknike '
                                 'ndërtohen duke marrë parasysh SEO, shpejtësinë dhe '
                                 'performancën.'},
                 {'title': 'Design dhe Development në një proces të integruar',
                  'description': 'Nga koncepti dhe UI/UX Design deri te zhvillimi dhe publikimi, '
                                 'procesi menaxhohet si një zgjidhje e plotë. Kjo ndihmon që '
                                 'design-i final dhe implementimi teknik të funksionojnë në '
                                 'harmoni.'},
                 {'title': 'Mbështetje edhe pas publikimit',
                  'description': 'Një website vazhdon të evoluojë së bashku me biznesin. '
                                 'Dominusoft mund të ofrojë mbështetje për mirëmbajtjen, '
                                 'përditësimin dhe zhvillimin e mëtejshëm të website-it sipas '
                                 'nevojave të kompanisë.'}],
  'benefits': [{'title': 'Website responsive',
                'description': 'Çdo biznes është i ndryshëm. Struktura, design-i dhe '
                               'funksionalitetet e website-it përshtaten me brand-in, audiencën '
                               'dhe objektivat që dëshironi të arrini.'},
               {'title': 'Design i personalizuar',
                'description': 'Ndërtojmë ndërfaqe intuitive dhe struktura të qarta që e ndihmojnë '
                               'vizitorin të gjejë informacionin lehtësisht dhe të ndërveprojë '
                               'natyrshëm me website-in.'},
               {'title': 'Strukturë SEO-friendly',
                'description': 'SEO nuk trajtohet vetëm pas përfundimit të website-it. Struktura e '
                               'faqeve, hierarkia e përmbajtjes dhe elementet teknike ndërtohen '
                               'duke marrë parasysh SEO, shpejtësinë dhe performancën.'},
               {'title': 'Performancë dhe përdorshmëri',
                'description': 'Nga koncepti dhe UI/UX Design deri te zhvillimi dhe publikimi, '
                               'procesi menaxhohet si një zgjidhje e plotë. Kjo ndihmon që '
                               'design-i final dhe implementimi teknik të funksionojnë në '
                               'harmoni.'},
               {'title': 'Teknologji moderne',
                'description': 'Një website vazhdon të evoluojë së bashku me biznesin. Dominusoft '
                               'mund të ofrojë mbështetje për mirëmbajtjen, përditësimin dhe '
                               'zhvillimin e mëtejshëm të website-it sipas nevojave të '
                               'kompanisë.'}],
  'packages': [{'name': 'Business Website',
                'description': 'Paketa Business Website është e përshtatshme për kompani që kanë '
                               'nevojë për një website modern, të qartë dhe responsive për të '
                               'prezantuar brand-in, shërbimet dhe aktivitetin e tyre. Struktura '
                               'ndërtohet me fokus te përdoruesi, duke e bërë informacionin të '
                               'aksesueshëm dhe kontaktin me biznesin sa më të thjeshtë.',
                'items': ['UI/UX & Responsive Design',
                          'Faqet kryesore të website-it',
                          'Prezantimin e shërbimeve',
                          'Contact Form & CTA',
                          'Integrim me Social Media',
                          'Basic On-Page SEO',
                          'Performance Optimization',
                          'Mobile & Tablet Optimization',
                          'Publikimin e website-it'],
                'is_featured': False},
               {'name': 'Custom Website',
                'description': 'Paketa Custom Website ndërtohet rreth kërkesave specifike të '
                               'biznesit, duke kombinuar UI/UX Design, zhvillim të personalizuar '
                               'dhe funksionalitete të avancuara. Nga arkitektura e informacionit '
                               'deri te implementimi teknik, çdo element projektohet në funksion '
                               'të objektivave dhe mënyrës se si përdoruesit do të ndërveprojnë me '
                               'platformën.',
                'items': ['Custom UI/UX Design',
                          'Strukturë dhe faqe të personalizuara',
                          'Funksionalitete të avancuara',
                          'Formularë dhe ndërveprime dinamike',
                          'Integrime me platforma të jashtme',
                          'CMS / Menaxhim përmbajtjeje',
                          'Advanced On-Page SEO',
                          'Performance & Speed Optimization',
                          'Responsive Development',
                          'Testing & Quality Assurance',
                          'Support & Maintenance'],
                'is_featured': False}],
  'offerings': [{'title': '01 — Business & Corporate Websites',
                 'description': 'Website profesionale për kompani dhe organizata që duan të '
                                'prezantojnë brand-in, shërbimet, projektet dhe aktivitetin e tyre '
                                'në mënyrë të strukturuar dhe profesionale.'},
                {'title': '02 — Custom Website Development',
                 'description': 'Zhvillim website me strukturë, design dhe funksionalitete të '
                                'personalizuara sipas kërkesave specifike të biznesit dhe '
                                'përdoruesve të tij.'},
                {'title': '03 — E-commerce Development',
                 'description': 'Dyqane online të ndërtuara për prezantimin dhe shitjen e '
                                'produkteve, me katalog, kategori, filtra, shportë, checkout dhe '
                                'integrime sipas nevojave të biznesit.'},
                {'title': '04 — Landing Page Development',
                 'description': 'Landing pages të fokusuara në një produkt, shërbim ose fushatë '
                                'specifike, me strukturë të qartë dhe CTA të menduara për të '
                                'gjeneruar kontakte dhe konvertime.'},
                {'title': '05 — Web Applications & Platforms',
                 'description': 'Zhvillim platformash dhe aplikacionesh web me funksionalitete më '
                                'të avancuara, dashboard, profile përdoruesish, menaxhim të të '
                                'dhënave dhe procese të personalizuara.'},
                {'title': '06 — Website Redesign',
                 'description': 'Ridizenjim dhe modernizim i website-ve ekzistuese për të '
                                'përmirësuar pamjen vizuale, strukturën, eksperiencën e '
                                'përdoruesit dhe përshtatjen me pajisjet mobile.'},
                {'title': '07 — UI/UX Design',
                 'description': 'Projektim i strukturës dhe ndërfaqes së website-it për të krijuar '
                                'një eksperiencë intuitive, të qartë dhe në përputhje me '
                                'identitetin vizual të brand-it.'},
                {'title': '08 — Website Maintenance & Support',
                 'description': 'Mirëmbajtje dhe suport teknik pas publikimit, duke përfshirë '
                                'përditësime, korrigjime, monitorim dhe përmirësime të '
                                'vazhdueshme.'},
                {'title': '09 — SEO & Performance Optimization',
                 'description': 'Optimizim teknik dhe on-page i website-it për strukturë '
                                'SEO-friendly, shpejtësi më të mirë, mobile usability dhe '
                                'performancë.'},
                {'title': '10 — Third-Party Integrations',
                 'description': 'Integrim i website-it me shërbime dhe sisteme të tjera, si CRM, '
                                'newsletter, booking systems, analytics, payment gateways ose API '
                                'të jashtme.'}]}]

class Command(BaseCommand):
    help = 'Import the four Dominusoft services and their page sections'

    @transaction.atomic
    def handle(self, *args, **options):
        for entry in DATA:
            service, _ = Services.objects.update_or_create(
                slug=entry['slug'], defaults={
                    'services_name': entry['name'],
                    'services_title': entry['meta_title'],
                    'services_description': entry['detail']['summary'],
                    'services_meta_description': entry['meta_description'],
                })
            ServiceDetail.objects.update_or_create(
                service=service, defaults={
                    **entry['detail'], 'meta_title': entry['meta_title'],
                    'meta_description': entry['meta_description'],
                })
            for model, key in ((ServiceHighlight, 'highlights'),
                               (ServiceBenefit, 'benefits'),
                               (ServiceOffering, 'offerings')):
                for position, item in enumerate(entry[key], 1):
                    model.objects.update_or_create(
                        service=service, title=item['title'],
                        defaults={**item, 'order': position})
            for position, item in enumerate(entry['packages'], 1):
                package, _ = ServicePackage.objects.update_or_create(
                    service=service, name=item['name'], defaults={
                        'description': item['description'],
                        'is_featured': item.get('is_featured', False),
                        'order': position,
                    })
                for item_position, text in enumerate(item['items'], 1):
                    ServicePackageItem.objects.update_or_create(
                        package=package, text=text, defaults={'order': item_position})
            self.stdout.write(self.style.SUCCESS(f'Imported: {service.services_name}'))
