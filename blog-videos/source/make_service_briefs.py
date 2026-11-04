"""Generate the Persian update brief for each service page (briefs/services/NN-slug.md)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = json.load(open(os.environ.get("SVC_FACTS", "/tmp/claude-0/-home-user-cloud/53e95dc6-dfee-58f1-9dfe-46b29308d0b2/scratchpad/svc/svc_facts.json")))

P = []  # (num, slug, name, data)

def page(n, slug, name, **d): P.append((n, slug, name, d))

# ------------------------------------------------------------------ 01 Allura
page(1, "allura-siding", "Allura siding",
 gsc=(99, 2178, 6.37),
 queries=[("allura siding colors", 23, 315, 1.5), ("allura spectrum colors", 11, 78, 2.5), ("allura siding canada", 1, 93, 4.6),
          ("allura spectrum", 4, 77, 2.8), ("allura cement siding colors", 0, 64, 1.0), ("allura colors", 3, 44, 2.2),
          ("allura siding", 0, 29, 29.6), ("allura siding colours", 7, 26, 1.0), ("allura siding reviews", 0, 4, 5.0)],
 interp="پربازده‌ترین صفحه سرویس سایت است (۹۹ کلیک، CTR برابر ۴.۵٪). تقریباً همه کلیک‌ها از **کوئری‌های رنگ** می‌آیند، که صفحه برایشان جایگاه ۱ تا ۳ دارد. ولی خود صفحه **حتی یک نام رنگ** نمی‌آورد؛ فقط خانواده‌های رنگ و یک تصویر پالت. اگر رقیب یا خود Allura یک صفحه رنگ کامل‌تر بدهد، این جایگاه از دست می‌رود. برای «allura siding» (کلمه اصلی) هم جایگاه ۲۹.۶ است، یعنی صفحه برای نیت «نصب Allura» قوی نیست.",
 questions=[("allura siding colors / spectrum colors / colours canada", "ناقص: نام رنگ‌ها نیامده"), ("allura vs hardie (cost, plank, lap)", "بله، کیفی؛ قیمت نه"),
            ("is allura siding any good / reviews", "ضمنی؛ نظر مشتری ندارد"), ("is allura siding primed / pre-primed", "بله"),
            ("how thick is allura siding", "خیر"), ("allura siding cost per square foot", "خیر (فقط عوامل)"),
            ("allura siding problems", "ناقص (limitations)"), ("allura siding warranty", "خیر؛ گارانتی ۳۰ ساله Allura ذکر نشده"),
            ("is allura siding still in business", "خیر")],
 competitors="رقیب اصلی برای کوئری‌های رنگ، **خود allurausa.com** است (صفحه Spectrum با نام و تصویر هر رنگ، به‌علاوه بلاگ‌های تک‌رنگ مثل Redwood و Sable Brown). Allura روی سایتش گارانتی **۳۰ ساله** برای plank، panel، shake و soffit و یک دفترچه نصب PDF دارد. نصاب محلی Allura با محتوای جدی در ونکوور پیدا نشد؛ این یعنی فرصت.",
 problems=["**نام رنگ‌ها وجود ندارد.** جدولی با ۲۵ رنگ Spectrum (نام، نمونه، خانواده، مناسب برای چه سبکی) اضافه شود؛ تصویر فعلی پالت کوچک است (۱۰۱۰×۶۲۰) و متن آن خوانا نیست.",
           "**گارانتی محصول ذکر نشده** (Allura طبق سایت خودش ۳۰ سال می‌دهد؛ تأیید شود) و از گارانتی ۵ ساله اجرای شما هم در این صفحه حرفی نیست.",
           "غلط تایپی: «Not **ح**an upgrade — the baseline» (یک حرف فارسی در متن انگلیسی).",
           "نام برند: «Silver Side Exterior has been working…» در بخش Why Choose Us.",
           "ضخامت (5/16 اینچ، طبق کاتالوگ‌های Allura؛ تأیید شود)، قیمت تقریبی و «Allura problems» (موجودی، زمان تحویل، نیاز به نصب دقیق) پاسخ مستقیم ندارند.",
           "فقط ۳ تصویر و یکی از آن‌ها رندر است. عکس واقعی پروژه Allura (Burnaby) کوچک است (۱۰۷۵×۵۰۰)."],
 titles=["Allura Siding Colours & Installation in Vancouver | Silversiding", "Allura Spectrum Colours, Cost & Installation | Vancouver"],
 meta="See all 25 Allura Spectrum colours, how Allura compares with James Hardie, and how we install it in Metro Vancouver. 5-year workmanship warranty.",
 sections=["**«Allura Spectrum colour chart»** (H2): جدول ۲۵ رنگ با نام دقیق `[VERIFY از allurausa.com/spectrum]`، تصویر نمونه هر رنگ (مجوز تصویر از Allura یا عکس نمونه فیزیکی خودتان)، و یک ستون «looks best with» (پنجره مشکی، سنگ، چوب). این بخش باید بالاتر از بخش مقایسه با Hardie بیاید، چون کوئری اصلی است.",
              "**«Allura siding warranty»** (H3): گارانتی محصول Allura (۳۰ سال، تأیید شود) در کنار گارانتی ۵ ساله اجرای Silversiding، و توضیح اینکه کدام چه چیزی را پوشش می‌دهد.",
              "**«How thick is Allura siding and what sizes does it come in?»** (H3، با جدول پروفایل‌ها، ضخامت‌ها و طول‌ها) `[VERIFY]`.",
              "**«What does Allura siding cost in Vancouver?»** (H3): بازه قیمت نصب‌شده برای هر فوت مربع از پروژه‌های خودتان، در مقایسه با Hardie و vinyl؛ اگر داده نیست، فقط عوامل و ترتیب قیمت.",
              "**«From our projects»**: پروژه Allura در Burnaby با عکس‌های بزرگ‌تر و توضیح (کدام پروفایل، کدام رنگ Spectrum، چه چالشی)."],
 faqs=["What colours does Allura Spectrum come in?", "How long is the Allura siding warranty?", "How thick is Allura fiber cement siding?",
       "Is Allura siding primed or pre-finished?", "How much does Allura siding cost per square foot in Vancouver?"],
 verify=["تعداد و نام رنگ‌های Spectrum (۲۵ رنگ، با Sherwin-Williams)", "گارانتی ۳۰ ساله Allura و شرایط آن در کانادا", "ضخامت 5/16 اینچ و طول‌های موجود", "ادعای «grain repeats less frequently»: منبع یا لحن نظر کارشناس"],
 keep=["بخش «Allura vs. James Hardie» با سه زیربخش صادقانه", "بخش «Primed vs. Pre-Finished»", "جدول مناطق", "بخش «A Note on What We Can and Cannot Promise»"],
 video="svc01_allura")

# ------------------------------------------------------------------ 02 ACM
page(2, "acm-panels", "ACM panels",
 gsc=(21, 2122, 24.15),
 queries=[("acm exterior panels", 0, 285, 29.9), ("acm panel installers", 0, 282, 22.1), ("acm cladding contractor", 0, 81, 48.4),
          ("acm cladding company", 0, 76, 28.8), ("aluminum composite contractors", 0, 69, 55.2), ("acm panels vancouver", 1, 52, 3.6),
          ("acm siding", 1, 32, 17.1), ("acm panels", 0, 21, 7.7), ("acm panel contractor", 0, 16, 17.9)],
 interp="صفحه برای «acm panels vancouver» جایگاه ۳.۶ دارد (کوئری محلی)، ولی برای کوئری‌های تجاری پرحجم «acm panel installers»، «acm exterior panels» و «acm cladding contractor» در صفحه ۲ تا ۵ است. رقبای این کوئری‌ها شرکت‌های تخصصی نماکاری تجاری هستند (Compass Cladding، Excelsior، Alumax) که **پروژه‌های تجاری با نام، سیستم‌ها و گواهی‌ها** را نشان می‌دهند. صفحه ما بیشتر لحن مسکونی دارد.",
 questions=[("what is acm cladding made of / what is acm siding", "بله"), ("acm panel cost / cost per sq ft / 4x8 price canada", "خیر"),
            ("acm cladding fire rating / fire risk / is acm cladding banned", "**مبهم**: فقط «depends on core»"), ("acm panel thickness (inches)", "خیر"),
            ("acm vs acp / mcm", "خیر"), ("acm panel installation", "بله، کلی")],
 competitors="**Compass Cladding** (BC، فعالیت از ۱۹۹۷): پیمانکار تمام‌سرویس نماکاری فلزی، ACM، ساخت ورق فلزی، پروژه‌های بلندمرتبه. **Excelsior Architectural Products**: ساخت، تأمین و نصب سیستم‌های ACM، عضو HAVAN. **Alumax Panel**: تأمین و نصب ACM. نقطه قوت آن‌ها: پروژه‌های تجاری و چندطبقه مستند، fabrication داخلی، اسم سیستم‌ها (route-and-return، wet seal، dry joint).",
 problems=["**سؤال آتش جواب روشن ندارد.** بعد از آتش‌سوزی‌های پرسروصدا با هسته پلی‌اتیلن، «is acm cladding banned» و «fire rating» از پرجستجوترین سؤال‌ها هستند. صفحه باید صریح توضیح دهد: هسته PE در برابر FR/مینرال، اینکه برای ساختمان‌های بلندتر و چندخانوار معمولاً هسته fire-rated لازم است، و استانداردهای مرتبط (CAN/ULC S134، NFPA 285) `[VERIFY الزام دقیق در BCBC]`.",
           "**ضخامت و ساختار سیستم‌ها نیامده:** ضخامت معمول پنل نما (۳ و ۴ میلی‌متر)، سیستم‌های نصب (route-and-return cassette، wet-seal، dry-joint/rainscreen).",
           "**هیچ پروژه تجاری نام‌دار با عکس بزرگ نیست**، در حالی که تابلوی Mackenzie Street و پروژه Mountain Highway (جایگزینی ACM) در صفحه بنیان‌گذار هست. این‌ها را به این صفحه بیاور.",
           "برای نیت B2B (پیمانکار عمومی، معمار، strata) بخشی وجود ندارد: shop drawings، هماهنگی با GC، بیمه، WorkSafeBC، برنامه ایمنی مکتوب.",
           "قیمت: حتی بازه یا ترتیب قیمت (ACM در برابر metal، AL13، fibre cement) نیامده."],
 titles=["ACM Panel Installation & Cladding Contractor | Vancouver", "ACM Panels Vancouver: Aluminum Composite Cladding Installers"],
 meta="ACM panel installers in Metro Vancouver: fire-rated core options, rainscreen detailing and panel layout for commercial, strata and homes. Free estimate.",
 sections=["**«Are ACM panels fire safe? PE vs fire-rated cores»** (H2، حدود ۲۵۰ کلمه، با جدول هسته‌ها و کاربرد)", "**«ACM panel thickness and systems»** (H2): ۳ یا ۴ میلی‌متر، و سه روش نصب با تصویر یا دیاگرام",
              "**«For general contractors and strata councils»** (H2): بیمه، WorkSafeBC، برنامه ایمنی مکتوب برای هر پروژه، lead time، هماهنگی shop drawing", "**«From our projects»**: Mackenzie Street (تابلوی ACM) و Mountain Highway (جایگزینی ACM به جای محصول وارداتی)، با عکس و توضیح چالش",
              "**«ACM vs ACP vs MCM: what's the difference?»** (H3 کوتاه؛ همه نام‌های مختلف یک خانواده محصول‌اند)"],
 faqs=["Is ACM cladding banned in Canada?", "What is the difference between PE and FR core ACM?", "How thick are ACM panels?", "How much do ACM panels cost per square foot installed?", "Do you work as a subcontractor for general contractors?"],
 verify=["الزامات BCBC برای هسته fire-rated بر اساس ارتفاع و نوع ساختمان", "استانداردهای CAN/ULC S134 و NFPA 285", "برندهای ACM که نصب می‌کنید"],
 keep=["تعریف ACM و بخش «Where ACM Panel Cladding Makes the Most Sense»", "مقایسه با Metal، LUX، Longboard و AL13", "فرایند ۳ مرحله‌ای"],
 video="svc02_acm")

# ------------------------------------------------------------------ 03 Soffit
page(3, "soffit-installation-and-soffit-re-place", "Soffit & fascia",
 gsc=(11, 3919, 22.24),
 queries=[("fascia installation vancouver", 0, 99, 4.6), ("metal soffit west vancouver", 0, 98, 3.5), ("metal soffit north vancouver", 0, 59, 7.7),
          ("soffit installers", 0, 99, 10.4), ("soffit company", 0, 76, 10.6), ("soffit replacement", 0, 120, 22.9), ("lux soffit", 0, 100, 23.9),
          ("soffit installation london", 0, 289, 51.2), ("soffit installation vernon", 0, 244, 15.1), ("soffit and fascia installation severn", 0, 88, 8.4)],
 interp="حدود یک‌سوم ایمپرشن‌ها از شهرهای دیگر است (London، Vernon، Severn، Georgetown، Midland) که هیچ‌وقت مشتری نمی‌شوند. کوئری‌های محلی خوب‌اند (metal soffit west vancouver جایگاه ۳.۵، fascia installation vancouver جایگاه ۴.۶). **عبارت «soffit-re-place» در URL** غلط تایپی است. URL را عوض نکن (ریسک رتبه)، ولی H1 و عنوان را تمیز کن.",
 questions=[("what is soffit and fascia / soffit vs fascia", "بله"), ("vented vs non-vented soffit", "بله"), ("soffit replacement cost / cost per linear foot (Canada)", "**خیر**"),
            ("how long does aluminum soffit last", "خیر"), ("can soffit be replaced without the siding", "بله"), ("how far should soffit vents be spaced", "خیر"), ("lux soffit / longboard soffit price", "خیر")],
 competitors="نتایج ملی (Angi، Rollex، ThePricer) **قیمت هر فوت طولی** می‌دهند: fascia حدود ۵ تا ۱۲، soffit حدود ۴ تا ۲۲، و هر دو با هم ۹ تا ۳۴ دلار برای هر فوت طولی (آمریکا). HomeStars برای ونکوور «trim، fascia و soffit: ۵۰۰ تا ۲٬۰۰۰ دلار» و یک نمونه واقعی ترمیم fascia با ۱٬۸۰۰ دلار نشان می‌دهد. صفحه ما هیچ عددی ندارد.",
 problems=["**هزینه وجود ندارد:** بازه قیمت برای هر فوت طولی soffit و fascia به تفکیک متریال (آلومینیوم، فایبر سیمان، وینیل، LUX/Longboard metal soffit) از پروژه‌های خودتان.",
           "**soffit فلزی woodgrain** (LUX soffit و Longboard soffit) که کوئری پرایمپرشن است («lux soffit» ۱۰۰ ایمپرشن، «lux soffit price» تنها کلیک‌های بلاگ LUX) فقط یک اشاره دارد. یک بخش کامل لازم است.",
           "فاصله منافذ تهویه و قاعده کلی تهویه زیرشیروانی (مثلاً نسبت ۱ به ۳۰۰، طبق BCBC `[VERIFY]`) نیامده.",
           "نام صفحه در H1 و عنوان: «Soffit & Fascia Installation And Replacement» قابل قبول است؛ «re-place» فقط در URL است."],
 titles=["Soffit & Fascia Installation and Replacement | Vancouver", "Metal & Aluminum Soffit Installation | North & West Vancouver"],
 meta="Soffit and fascia replacement in Metro Vancouver: aluminum, fibre cement and woodgrain metal soffit, venting done right. Free on-site assessment.",
 sections=["**«Soffit and fascia replacement cost»** (H2): بازه هر فوت طولی به تفکیک متریال و عوامل (دسترسی، ارتفاع، ترمیم سازه پشت، ناودان)", "**«Woodgrain metal soffit: LUX and Longboard»** (H2): ادامه نمای دیوار تا زیر بام، vented بودن، قیمت نسبی، عکس واقعی (DD6A9011، longboard soffit)",
              "**«How much soffit venting does an attic need?»** (H3) `[VERIFY BCBC]`", "**«How long does aluminum soffit last?»** (H3)"],
 faqs=["How much does soffit and fascia replacement cost in Vancouver?", "How long does aluminum soffit last?", "Can you install woodgrain metal soffit (LUX or Longboard)?", "How far apart should soffit vents be?"],
 verify=["نسبت تهویه زیرشیروانی در BCBC", "بازه قیمت‌ها از پروژه‌های خودتان"],
 keep=["تعریف soffit و fascia", "جدول «Alone or Part of a Larger Project?»", "بخش «Integration with Exterior Cladding»", "FAQ های فعلی"],
 video="svc03_soffit")

# ------------------------------------------------------------------ 04 Metal
page(4, "metal-siding", "Metal siding",
 gsc=(11, 1987, 22.59),
 queries=[("metal siding vancouver", 1, 320, 16.9), ("metal cladding vancouver", 0, 160, 19.9), ("metal siding fabrication vancouver", 0, 158, 20.8),
          ("aluminum siding vancouver", 1, 141, 10.3), ("steel siding repair", 0, 122, 5.0), ("aluminum siding repair near me", 0, 117, 4.4),
          ("aluminum siding contractors", 0, 113, 4.8), ("steel siding vancouver", 0, 103, 9.6), ("metal siding west vancouver", 1, 84, 5.0),
          ("sheet metal siding trim vancouver", 0, 70, 14.6), ("metal cladding supplier west vancouver", 0, 62, 2.0)],
 interp="برای کوئری‌های تعمیر و پیمانکار آلومینیوم جایگاه خوبی دارد (۴ تا ۵)، ولی برای کلمه اصلی «metal siding vancouver» در جایگاه ۱۷ است. «metal siding fabrication vancouver» و «sheet metal siding trim» نشان می‌دهد بخشی از کاربران دنبال **ساخت فلاشینگ و تریم سفارشی** هستند که صفحه به آن نمی‌پردازد. **صفحه هیچ تصویری ندارد** (۰ تصویر)، و بخش «Before & After» خالی است: عنوان دارد ولی عکس ندارد.",
 questions=[("metal siding cost per square foot (Canada)", "خیر"), ("steel vs aluminum siding (cost, which is better)", "بله"), ("does metal siding rust / fade / dent", "بله"),
            ("does metal siding expand and contract", "بله"), ("does metal siding make a house hotter / sweat / interfere with wifi", "خیر"),
            ("metal siding vs hardie board (cost)", "بله، کیفی"), ("is metal siding worth it / increase home value", "ناقص")],
 competitors="نتایج قیمت عمدتاً آمریکایی‌اند (Fixr، Angi). یک منبع کانادایی فولاد را **۸ تا ۱۲ دلار برای هر فوت مربع** ذکر می‌کند. Angi پنل‌های concealed-fastener را تا ۱۶ دلار و ارتقای PVDF را جداگانه نشان می‌دهد. رقبای محلی نماکاری فلزی (Compass Cladding و…) fabrication داخلی و پروژه‌های تجاری را نشان می‌دهند.",
 problems=["**صفر تصویر** و بخش «Before & After» خالی. حداقل ۵ عکس واقعی: metal-siding-in-west-vancouver، Metal-Panel-Siding-West-Vancouver-Dark-Grey/Silver، metal-panel-siding-north-vancouver، metal-siding3.",
           "**قیمت** حتی به صورت بازه یا ترتیب نیامده.", "**Fabrication** (ساخت فلاشینگ، cap و تریم سفارشی) که کوئری دارد، پوشش داده نشده. اگر انجام می‌دهید یا با کارگاه همکاری دارید، بنویسید.",
           "سؤال‌های جانبی پرتکرار (گرمای خانه، تعریق، وای‌فای، صاعقه) جواب ندارند؛ یک FAQ کوتاه برایشان کافی است.",
           "**تداخل:** کوئری‌های «lux metal siding» (۱٬۰۵۸ ایمپرشن) گاهی این صفحه را نشان می‌دهند. اینجا فقط به صفحه LUX لینک بده."],
 titles=["Metal Siding Installation Vancouver | Aluminum & Steel", "Metal Siding & Cladding Contractor | Vancouver & North Shore"],
 meta="Aluminum and steel siding installed in Metro Vancouver: lap, vertical, corrugated and standing seam, with rainscreen and laid-out panels. Free estimate.",
 sections=["**«From our projects»** با ۵ عکس واقعی و توضیح لی‌اوت (قاعده چیدمان از دو گوشه، دیوار ۲ تا ۳ اینچ خارج از تراز؛ از صفحه بنیان‌گذار)", "**«Metal siding cost in Vancouver»** (H2): بازه یا ترتیب قیمت به تفکیک پروفایل (lap، corrugated، standing seam، concealed-fastener) و عوامل",
              "**«Custom flashing and trim»** (H3، در صورت ارائه)", "**FAQ** های کوتاه درباره گرما، تعریق، وای‌فای و صاعقه"],
 faqs=["How much does metal siding cost per square foot in Vancouver?", "Does metal siding make a house hotter?", "Does metal siding interfere with Wi-Fi or cell signal?", "Do you fabricate custom metal flashing and trim?"],
 verify=["ادعاهای مربوط به گرما و وای‌فای (پاسخ محافظه‌کارانه و مستند)", "خدمات fabrication"],
 keep=["بخش aluminum در برابر steel", "مقایسه با vinyl و fibre cement", "توضیح نیاز به گپ برای انبساط"],
 video="svc04_metal")

# ------------------------------------------------------------------ 05 LUX
page(5, "lux-panels", "LUX panels",
 gsc=(10, 4569, 24.78),
 queries=[("lux panels", 0, 1266, 17.3), ("lux metal siding", 0, 1058, 21.0), ("lux siding", 1, 890, 19.4), ("lux panel", 0, 678, 21.2),
          ("lux siding installation", 0, 198, 25.7), ("lux siding alternative", 0, 174, 14.0), ("lux panel colors", 0, 170, 20.2),
          ("lux soffit", 0, 100, 23.9), ("lux folded wall", 0, 54, 21.9), ("lux panel installation", 0, 42, 12.3), ("lux siding calgary", 0, 65, 39.5)],
 interp="**تداخل جدی با بلاگ LUX:** هر دو صفحه برای «lux panels» دیده می‌شوند. بلاگ در جایگاه ۱۱ و این صفحه در جایگاه ۲۵ است. گوگل بلاگ را ترجیح می‌دهد. نقش این صفحه باید **نیت تراکنشی** باشد: «LUX siding installation Vancouver»، «LUX installer»، «LUX soffit installation». کوئری‌های «lux panel colors» (۱۷۰) و «lux folded wall» (۵۴) هم پاسخ کامل ندارند.",
 questions=[("lux siding installation / installer", "بله، ولی عمومی"), ("lux panel colours", "ناقص (فقط خانواده‌ها)"), ("lux soffit / lux soffit price", "ناقص"),
            ("lux board and batten / folded wall", "**خیر**"), ("lux siding cost / price per sq ft", "خیر"), ("lux panels canada / made in", "بله (ساخت کانادا)")],
 competitors="سایت سازنده (luxpanel.ca) برای کوئری‌های برند. پیمانکار ادمونتونی Blue Jay قیمت نصب‌شده LUX را **۳۲ تا ۴۵ دلار برای هر فوت مربع** منتشر کرده است. در ونکوور هیچ نصاب LUX با صفحه اختصاصی جدی پیدا نشد، یعنی فرصت روشن است.",
 problems=["**عنوان FAQ اشتباه است:** «Frequently Asked Questions About **Stone Veneer** Siding» در صفحه LUX. فوراً اصلاح شود.",
           "**تفکیک نقش با بلاگ:** عنوان و H1 باید روی «installation Vancouver» تمرکز کنند. بخش‌های مقایسه‌ای طولانی را کوتاه کن و به بلاگ لینک بده.",
           "پروفایل‌های LUX (Board + Batten، Folded Wall، V-groove، soffit) با نام و عکس نیامده‌اند. «lux folded wall» کوئری دارد.",
           "تصاویر صفحه (lux-woodgrains، lux-metallics و LUX-Architectural-Products) احتمالاً تصاویر سازنده‌اند. حداقل ۲ عکس پروژه واقعی LUX خودتان اضافه کن.",
           "متا با حرف کوچک شروع جمله دارد («durable steel siding…» بعد از نقطه)."],
 titles=["LUX Siding Installation in Vancouver | LUX Panel Installer", "LUX Panels Installed: Siding, Soffit & Board-and-Batten | Vancouver"],
 meta="LUX steel panel installation across Metro Vancouver: woodgrain siding, soffit and board-and-batten, 25-year finish warranty plus our 5-year workmanship.",
 sections=["**«LUX profiles we install»** (H2): Board + Batten، Folded Wall، V-groove، soffit و custom trim، با عکس و توضیح کاربرد `[VERIFY نام‌ها]`", "**«LUX installation cost in Vancouver»** (H2): بازه قیمت از پروژه‌ها، به‌علاوه سافیت",
              "**«From our LUX projects»** با عکس واقعی", "تعویض عنوان FAQ و کوتاه کردن مقایسه با Longboard، با لینک به بلاگ («LUX vs Longboard vs AL13 compared»)"],
 faqs=["What is LUX Folded Wall?", "Can LUX be installed as board and batten?", "How much does LUX siding installation cost in Vancouver?", "Are you an authorized LUX installer?"],
 verify=["نام پروفایل‌ها و رنگ‌های فعلی LUX", "هرگونه رابطه رسمی با سازنده (dealer، installer)", "گارانتی ۲۵ ساله فینیش"],
 keep=["توضیح فولاد Galvalume و Class A", "بخش «Installation Profiles: Horizontal, Vertical & Soffit»", "هشدار DIY"],
 video="svc05_lux")

# ------------------------------------------------------------------ 06 Stone
page(6, "stone-siding", "Stone veneer siding",
 gsc=(8, 1668, 13.88),
 queries=[("cultured stone veneer vancouver", 0, 220, 12.6), ("installing cultured stone vancouver", 0, 206, 4.9), ("cultured stone pricing vancouver", 0, 172, 14.3),
          ("stone veneer siding vancouver", 0, 124, 2.4), ("stone work install north vancouver", 0, 60, 18.6), ("stone work install vancouver", 0, 60, 25.1),
          ("stone work install burnaby", 0, 40, 13.4), ("natural stone veneer bc", 0, 25, 17.5), ("zenith modern stackstone vancouver", 0, 14, 24.1)],
 interp="نیت محلی و تجاری روشن است (installing cultured stone vancouver در جایگاه ۴.۹، stone veneer siding vancouver در جایگاه ۲.۴)، ولی CTR پایین است (۰.۴۸٪). **«cultured stone pricing vancouver» با ۱۷۲ ایمپرشن** بدون جواب مانده. کوئری‌های «stone work install» به‌علاوه نام شهر نشان می‌دهد کاربر دنبال نصاب سنگ است، نه فقط اطلاعات.",
 questions=[("stone veneer cost per sq ft installed (Canada)", "**خیر**"), ("cultured vs natural stone", "بله"), ("does stone veneer need weep holes / a brick ledge", "خیر"),
            ("can stone veneer be installed over brick", "خیر"), ("does stone veneer increase home value", "بله"), ("does stone veneer look cheap", "خیر"), ("stone veneer problems", "ناقص")],
 competitors="رقبای ملی (HomeGuide: ۱۰ تا ۳۵ دلار برای هر فوت مربع نصب‌شده؛ Rising Sun: ۱۵ تا ۳۰ دلار) بازه قیمت و تفکیک «متریال و دستمزد» می‌دهند. برندها (Eldorado، Cultured Stone، Zenith) صفحه کاتالوگ دارند. در ونکوور نصاب‌های سنگ معمولاً گالری پروژه بزرگ دارند.",
 problems=["**قیمت وجود ندارد**، در حالی که کوئری‌اش ۱۷۲ ایمپرشن دارد.", "**جزئیات فنی آبگیری veneer** (weep screed، drainage plane دولایه، rainscreen mat پشت سنگ، فاصله تا زمین) نیامده. این‌ها E-E-A-T فنی هستند.",
           "**تناقض با صفحه Brick & Stone** درباره «structural» (بریف سراسری بند ۷).", "متا: «richmond» با حرف کوچک.", "فقط ۳ تصویر و بخش «See Our Work» به گالری می‌فرستد. عکس‌ها را همین‌جا بیاور.",
           "برندهای سنگ مصنوعی که نصب می‌کنید نام برده نشده‌اند («zenith modern stackstone vancouver» کوئری دارد)."],
 titles=["Stone Veneer & Cultured Stone Installation | Vancouver", "Cultured Stone Installation & Pricing | Vancouver Stone Veneer"],
 meta="Stone veneer and cultured stone installed in Vancouver, North Vancouver, West Vancouver, Burnaby and Richmond. Pricing guide, drainage done right.",
 sections=["**«How much does stone veneer cost in Vancouver?»** (H2): بازه هر فوت مربع برای cultured، natural و panel، و عوامل", "**«How stone veneer is waterproofed»** (H2): دو لایه WRB یا rainscreen mat، weep screed، فاصله از زمین و فلاشینگ؛ با دیاگرام",
              "**«Stone veneer brands we install»** (H3) `[VERIFY]`", "**«From our projects»**: عکس‌های STONE-VENEER-Surrey، IMG_8434 (سنگ به‌علاوه Hardie)، Sone-Siding-Vancouver"],
 faqs=["How much does cultured stone cost per square foot in Vancouver?", "Does stone veneer need weep holes or a weep screed?", "Can stone veneer be installed over brick or stucco?", "Does stone veneer look fake?"],
 verify=["جزئیات آبگیری طبق دستورالعمل سازنده و BCBC", "برندها"],
 keep=["تعریف چهار نوع محصول", "بخش «When Stone Veneer May Not Be the Best Fit»", "FAQ های فعلی"],
 video="svc06_stone")

# ------------------------------------------------------------------ 07 Longboard
page(7, "longboard-siding", "Longboard siding",
 gsc=(8, 1623, 16.03),
 queries=[("longboard siding calgary", 0, 178, 15.7), ("longboard siding", 0, 96, 12.3), ("longboard aluminium siding calgary", 0, 78, 13.4), ("longboard cladding", 0, 66, 12.9),
          ("how does knotwood compare to longboard aluminum cladding?", 0, 42, 14.4), ("longboard aluminum siding", 0, 29, 19.2), ("how to install longboard siding", 0, 14, 25.1),
          ("longboard siding cost", 0, 7, 14.4)],
 interp="بزرگ‌ترین کوئری‌ها مال **کلگری** هستند (۲۵۶ ایمپرشن) و لید نمی‌شوند. کوئری اصلی «longboard siding» جایگاه ۱۲ دارد. «Knotwood vs Longboard» (۴۲ ایمپرشن) هم در این صفحه و هم در بلاگ LUX بی‌جواب مانده. کوئری‌های قیمت کم‌حجم ولی تجاری‌اند.",
 questions=[("what is longboard siding", "بله"), ("longboard siding cost / price per sq ft", "خیر (عمداً)"), ("longboard siding warranty", "**خیر؛ با یادداشت پیش‌نویس**"),
            ("longboard soffit price", "خیر"), ("knotwood vs longboard", "خیر"), ("longboard colours / finishes", "ناقص")],
 competitors="Blue Jay (ادمونتون) قیمت نصب‌شده Longboard را **۵۰ تا ۷۰ دلار برای هر فوت مربع** نوشته است. Bright Siding (HomeStars) Longboard را در لیست محصولاتش دارد. سایت Longboard پروژه‌های ونکوور (Altium Building Corp، Vancouver Community Land Trust) را معرفی می‌کند. سایت Longboard می‌گوید «هر نصاب سایدینگ می‌تواند نصبش کند»، پس تمایز شما باید تجربه لی‌اوت و پروژه‌های تجاری باشد.",
 problems=["**پیش‌نویس داخلی منتشر شده:** در FAQ اول آمده «We don't want to quote a specific year range here without confirming it against the manufacturer's actual finish warranty terms &mdash; happy to include a specific figure once that's confirmed.» فوراً با گارانتی واقعی (طبق بلاگ: lifetime روی زیرلایه و ۱۵ سال non-prorated روی فینیش؛ تأیید شود) جایگزین شود. `&mdash;` خام هم اصلاح شود.",
           "«Long Board» با فاصله در عنوان FAQ و متن؛ برند «Longboard» است.", "مقایسه با Knotwood وجود ندارد.", "هیچ قیمت یا ترتیب قیمتی نیست (حتی در مقایسه با LUX)."],
 titles=["Longboard Siding Installation Vancouver | Wood-Look Aluminum", "Longboard Aluminum Siding Installers | Metro Vancouver"],
 meta="Longboard wood-grain aluminum siding and soffit installed across Metro Vancouver. Finishes, warranty, cost factors and concealed-clip installation.",
 sections=["**«Longboard warranty»** (H3): جایگزین یادداشت پیش‌نویس `[VERIFY]`", "**«Longboard vs Knotwood»** (H3)", "**«What does Longboard cost?»** (H2): ترتیب قیمت (Longboard بالاتر از LUX) و بازه از پروژه‌ها",
              "**«From our Longboard projects»**: چهار عکس تجاری موجود با توضیح (accent band، چندطبقه، fascia بالای ورودی پارکینگ)"],
 faqs=["What warranty does Longboard siding have?", "How does Knotwood compare to Longboard?", "How much does Longboard siding cost per square foot in Vancouver?", "Can Longboard be used for soffits?"],
 verify=["گارانتی فعلی Longboard در کانادا", "مشخصات Knotwood"],
 keep=["تعریف و AAMA 2604/2605", "لیست کاربردهای مسکونی و تجاری", "توصیه دیدن نمونه فیزیکی"],
 video="svc07_longboard")

# ------------------------------------------------------------------ 08 Tyvek
page(8, "tyvek-air-barrier", "Tyvek air barrier",
 gsc=(6, 824, 6.21),
 queries=[("tyvek vapor barrier", 0, 42, 2.1), ("is tyvek an air barrier", 0, 14, 6.2), ("zip system vs tyvek", 0, 7, 1.0), ("tyvek installation", 0, 4, 10.0),
          ("tyvek vs zip system", 0, 3, 1.0), ("air barrier membrane in surrey", 0, 4, 19.2)],
 interp="جایگاه میانگین خوب است (۶.۲)، و برای سؤال‌های «is tyvek a vapor barrier» و «zip vs tyvek» جایگاه ۱ تا ۲ دارد. این‌ها سؤال‌های اطلاعاتی‌اند و کاربرشان معمولاً DIY یا سازنده است، نه مشتری. ولی ارزش topical authority بالایی دارند. CTR پایین (۰.۷٪) طبیعی است، چون جواب در snippet دیده می‌شود.",
 questions=[("is tyvek waterproof / a vapour barrier / breathable / an air barrier", "بله"), ("does tyvek need to be taped", "بله (ضمنی)"), ("does tyvek go on before windows", "**خیر**"),
            ("is tyvek directional", "خیر"), ("tyvek vs typar / tar paper / blueskin", "**خیر**"), ("zip system vs tyvek", "**خیر** (با اینکه جایگاه ۱ دارد)"), ("tyvek homewrap vs commercialwrap", "خیر")],
 competitors="DuPont (سازنده) راهنمای نصب و جزئیات پنجره دارد. GreenBuildingAdvisor و JLC مقایسه‌های WRB دارند. هیچ پیمانکار محلی صفحه جدی برای این موضوع ندارد.",
 problems=["**سؤال‌هایی که کاربر واقعاً می‌پرسد بی‌جواب‌اند:** «Tyvek vs ZIP» (جایگاه ۱ بدون محتوا؛ ریسک از دست دادن)، «Tyvek before or after windows»، «HomeWrap vs CommercialWrap»، «Tyvek vs Blueskin».",
           "فقط ۱ تصویر. عکس‌های واقعی Tyvek روی پروژه‌ها (IMG-20250926-WA0006، Tyvek_Air-Barrier-1، tyvek-700x700) اضافه شود.", "بخش مربوط به تفاوت HomeWrap (مسکونی) و CommercialWrap (تجاری، که در عکس پروژه شما دیده می‌شود) نیامده."],
 titles=["Tyvek Air Barrier Installation | Vancouver Building Envelope", "Tyvek House Wrap Installation: Air vs Vapour Barrier | Vancouver"],
 meta="Tyvek air barrier installed as one system with flashing and rainscreen. Air vs vapour barrier, Tyvek vs ZIP, and how windows are detailed. Free estimate.",
 sections=["**«Tyvek vs ZIP System»** (H2): پنل شیت‌دار با WRB یکپارچه در برابر غشای جدا؛ مزایا، معایب و اینکه هر دو rainscreen لازم دارند", "**«Does Tyvek go on before windows?»** (H3): ترتیب لایه‌ها (sill pan، Tyvek، پنجره، head flashing) با دیاگرام",
              "**«HomeWrap vs CommercialWrap»** (H3)", "**«Tyvek vs Blueskin and other membranes»** (H3)"],
 faqs=["Is Tyvek better than ZIP System?", "Does Tyvek go on before or after windows?", "What is the difference between Tyvek HomeWrap and CommercialWrap?", "Is Tyvek directional?"],
 verify=["مشخصات HomeWrap و CommercialWrap از DuPont", "ترتیب نصب پنجره طبق راهنمای DuPont"],
 keep=["بخش «Air Barrier vs. Vapor Barrier» (عالی؛ همین جایگاه ۲ را گرفته)", "بخش جزئیات و دلیل حرفه‌ای بودن نصب", "FAQ"],
 video="svc08_tyvek")

# ------------------------------------------------------------------ 09 AL13
page(9, "al13-panels", "AL13 panels",
 gsc=(4, 1041, 8.04),
 queries=[("al13 panels", 0, 69, 6.7), ("al13", 0, 61, 9.8), ("al13 siding", 0, 58, 5.1), ("al13 architectural systems", 0, 30, 12.7), ("al 13 panels", 0, 16, 9.6),
          ("al13 siding calgary", 0, 16, 11.3), ("al13 cladding", 0, 7, 8.4)],
 interp="جایگاه صفحه اول (۵ تا ۱۰)، ولی CTR پایین (۰.۴٪). کاربر کوئری برند می‌زند و احتمالاً دنبال سایت سازنده است. برای تبدیل، صفحه باید **پروژه واقعی AL13** و قیمت یا ترتیب نشان دهد. فقط ۱ تصویر دارد.",
 questions=[("al13 panel cost", "خیر"), ("al13 vs (acm, lux)", "بله"), ("al13 fire (FR core)", "بله"), ("al13 plank", "بله"), ("al13 colors", "خیر")],
 competitors="سایت AL13 (سازنده) کاتالوگ، جزئیات فنی و گالری دارد. در ونکوور هیچ نصاب با صفحه اختصاصی برجسته پیدا نشد.",
 problems=["**فقط ۱ تصویر** (AL13-Siding-Contractor). عکس AL13-panelSystem-Vancouver و پروژه‌های دیگر را اضافه کن.", "رنگ‌ها و فینیش‌ها نیامده‌اند.", "قیمت یا ترتیب قیمت نیامده (بلاگ LUX می‌گوید AL13 «mid-tier» است؛ همان را بیاور).",
           "در مقایسه با LUX، ادعای «difference tends to come down to profile and finish range» با بلاگ (plank در برابر panel) کمی متفاوت است. یکدست شود."],
 titles=["AL13 Panel & Plank Installation | Vancouver Installer", "AL13 Siding Installers in Vancouver: Panel and Plank Systems"],
 meta="AL13 panel and plank systems supplied and installed in Metro Vancouver: built-in pressure-equalized rainscreen, FR core options, cut-to-fit on site.",
 sections=["**«From our AL13 projects»** با عکس‌ها", "**«AL13 finishes and colours»** (H3) `[VERIFY]`", "**«What does AL13 cost?»** (H3): ترتیب قیمت در مقایسه با LUX، ACM و Longboard"],
 faqs=["How much does AL13 cost compared with ACM or LUX?", "What colours does AL13 come in?", "Can AL13 panel and plank be combined?"],
 verify=["مشخصات و رنگ‌های فعلی AL13", "گارانتی ۲۰ ساله (طبق بلاگ)"],
 keep=["توضیح snap-lock و cut-to-fit", "بخش FR core", "مقایسه با ACM"],
 video="svc09_al13")

# ------------------------------------------------------------------ 10 Hardie
page(10, "james-hardie-siding", "James Hardie siding",
 gsc=(2, 2430, 36.06),
 queries=[("fiber cement siding vancouver", 2, 380, 16.8), ("james hardie siding contractor", 0, 255, 60.9), ("hardie board installer", 0, 145, 49.5),
          ("james hardie siding vancouver", 0, 112, 31.2), ("hardie siding vancouver", 0, 70, 20.9), ("vancouver james hardie contractor", 0, 62, 37.0),
          ("james hardie siding installation vancouver", 0, 61, 33.5), ("hardie board siding innisfil", 0, 65, 47.4), ("hardie board siding severn", 0, 60, 33.3)],
 interp="**ضعیف‌ترین جایگاه بین صفحات پرایمپرشن** (میانگین ۳۶). کوئری‌های تجاری Hardie در صفحه ۳ تا ۶ هستند. رقیب اصلی محلی (Ideal Siding، Burnaby) نشان **James Hardie Elite Preferred Contractor** و صدها نظر در HomeStars دارد. بدون سیگنال اعتماد مشابه (گواهی، نظر، پروژه)، این صفحه رقابت نمی‌کند. بخشی از ایمپرشن‌ها از انتاریو است (Innisfil، Severn، Wasaga Beach).",
 questions=[("hardie board cost per sq ft (Canada)", "خیر"), ("hardie vs vinyl / stucco / LP SmartSide", "بله، به‌جز LP SmartSide"), ("is hardie board made in Canada / canadian", "خیر"),
            ("is hardie fireproof / non-combustible / waterproof", "ناقص"), ("hardie siding problems / installation problems", "ناقص"), ("james hardie warranty (Canada, transfer)", "**خیر**"),
            ("how long will hardie siding last", "بله (۵۰+ سال)"), ("asbestos", "بله")],
 competitors="**Ideal Siding** (Burnaby): Elite Preferred، پوشش کل BC، نظرات زیاد. **Siding Vancouver** و **West Coast Barrier**: نظرات HomeStars با پروژه‌های Hardie. **jameshardie.ca**: صفحات محصول، گارانتی و «Find a contractor».",
 problems=["**سیگنال اعتماد مخصوص Hardie نیست:** اگر Silversiding در برنامه پیمانکاران James Hardie ثبت است (Preferred یا Elite Preferred)، باید بالای صفحه بیاید. اگر نیست، ارزش دارد اقدام شود؛ این مهم‌ترین عامل رقابتی این کوئری‌هاست.",
           "**گارانتی Hardie** (۳۰ ساله محصول non-prorated و ۱۵ ساله ColorPlus در آمریکای شمالی؛ برای کانادا تأیید شود) و ارتباطش با نصب درست ذکر نشده.", "**پروژه Hardie مستند** نیست: Mountain Highway (دو پروفایل فایبر سیمان) و Mackenzie Street (V-groove عمودی) در صفحه بنیان‌گذار هستند. اینجا بیاورشان (برند را فقط اگر Hardie بوده بنویس).",
           "**تصاویر** فقط ۲ عدد کوچک (۶۷۴×۲۲۶). عکس‌های james-hardie-coquitlam، james-hardie-Siding5/6، hardie-panel-siding-vancouver و IMG_8434 اضافه شود.", "مقایسه با **LP SmartSide** (کوئری پرتکرار) وجود ندارد.", "«Is Hardie made in Canada?» جواب ندارد."],
 titles=["James Hardie Siding Installer Vancouver | Fiber Cement", "James Hardie & Fibre Cement Siding Contractor | Metro Vancouver"],
 meta="James Hardie fiber cement siding installed to Hardie's details across Metro Vancouver: Plank, Panel and Trim, rainscreen standard, 5-year workmanship warranty.",
 sections=["**سیگنال گواهی یا عضویت** (در صورت وجود) بالای صفحه", "**«James Hardie warranty in Canada»** (H2) `[VERIFY]`", "**«From our fibre cement projects»**: Mountain Highway و Mackenzie Street با عکس و داستان",
              "**«James Hardie vs LP SmartSide»** (H3)", "**«How much does James Hardie cost in Vancouver?»** (H2): بازه از پروژه‌ها؛ تفاوت ColorPlus و primed", "**«Is James Hardie made in Canada?»** (FAQ) `[VERIFY]`"],
 faqs=["What is the James Hardie warranty in Canada?", "Is James Hardie siding made in Canada?", "James Hardie vs LP SmartSide: which is better here?", "How much does James Hardie siding cost per square foot in Vancouver?", "Are you a James Hardie preferred contractor?"],
 verify=["گارانتی Hardie کانادا", "محل تولید محصولات Hardie برای بازار BC", "وضعیت عضویت در برنامه پیمانکاران Hardie"],
 keep=["بخش «Same Product, Two Names»", "سه خانواده محصول", "FAQ آزبست"],
 video="svc10_hardie")

# ------------------------------------------------------------------ 11 Repair
page(11, "siding-repair", "Siding repair",
 gsc=(2, 2192, 44.76),
 queries=[("siding repair vancouver", 0, 748, 10.5), ("vancouver siding repair", 2, 451, 9.9), ("siding repair", 0, 396, 17.7), ("replacement siding vancouver", 0, 392, 11.4),
          ("siding repair near me", 1, 210, 6.4), ("garage siding repair", 0, 196, 39.9), ("siding repair north vancouver", 0, 172, 10.5), ("cedar siding repair north vancouver", 0, 106, 6.2),
          ("steel siding repair", 0, 122, 5.0), ("aluminum siding repair near me", 0, 117, 4.4)],
 interp="کوئری‌های تعمیر در کل سایت **۸٬۵۳۱ ایمپرشن** دارند (بیشترین حجم بعد از کوئری‌های عمومی). ولی میانگین جایگاه خود این صفحه ۴۴.۸ است. یعنی برای بسیاری از این کوئری‌ها گوگل صفحه دیگری (احتمالاً صفحه اصلی) را نشان می‌دهد، یا این صفحه فقط برای long-tail دیده می‌شود. «cedar siding repair north vancouver» در جایگاه ۶ است، ولی صفحه صریحاً می‌گوید **ترمیم cedar انجام نمی‌دهد** (فقط تعویض). این باید شفاف و با جایگزین پیشنهادی بماند.",
 questions=[("siding repair cost / per sq ft", "**خیر**"), ("siding repair vs replacement", "بله (عالی)"), ("can siding be repaired (vinyl, aluminum, cracked)", "بله"),
            ("when to replace siding", "بله"), ("how long does siding last", "ناقص"), ("does insurance cover siding repair", "بله")],
 competitors="HomeStars ونکوور: «repair or replace damaged panels: ۱۵۰ تا ۳٬۰۰۰ دلار؛ trim، fascia و soffit: ۵۰۰ تا ۲٬۰۰۰ دلار»، به‌علاوه نمونه‌های واقعی (ترمیم cedar حدود ۲٬۵۰۰، fascia حدود ۱٬۸۰۰ و ترمیم بزرگ حدود ۹٬۸۰۰ دلار). رقبا (Siding Vancouver، Ideal Siding) نظرات زیادی درباره تعمیر دارند.",
 problems=["**بخش ناقص:** «Siding Repair Across Metro Vancouver … In» در وسط جمله قطع شده (احتمالاً یک جدول یا پاراگراف حذف شده). روی سایت زنده بررسی شود.", "**هزینه:** هیچ بازه قیمتی نیست، در حالی که «siding repair cost» پرتکرارترین سؤال است.",
           "**هیچ عکس واقعی قبل و بعد از تعمیر نیست** (دو عکس موجود عمومی یا stock به نظر می‌رسند). برای E-E-A-T صفحه تعمیر، عکس قبل و بعد از کارهای خودتان حیاتی است.", "صفحه بلند است (حدود ۴٬۰۰۰ کلمه). جدول مشکل/علت/نتیجه عالی است، ولی بخش‌های مواد تکراری‌اند؛ می‌شود ۲۰٪ کوتاه‌ترش کرد.",
           "**فرصت محلی:** «siding repair north vancouver» (۱۷۲) و «cedar siding repair north vancouver» (۱۰۶). یک بخش کوتاه North Shore با لینک به صفحه منطقه اضافه کن."],
 titles=["Siding Repair & Replacement Vancouver | Assessment First", "Siding Repair Vancouver & North Shore | 5-Year Warranty"],
 meta="Siding repair and replacement in Metro Vancouver: cracked panels, water damage and rot, colour-matched work, cause fixed, 5-year workmanship warranty.",
 sections=["**اصلاح بخش ناقص** «Siding Repair Across Metro Vancouver»", "**«What does siding repair cost in Vancouver?»** (H2): سه سطح (تعمیر کوچک، تعمیر بخش با ترمیم پشت، تعویض یک نما) از پروژه‌های خودتان، و چرا قیمت از روی عکس داده نمی‌شود",
              "**«Before and after»**: حداقل ۳ پروژه تعمیر با عکس", "**«Cedar siding in North Vancouver: repair or replace?»** (H3)"],
 faqs=["How much does siding repair cost in Vancouver?", "Do you repair cedar siding?", "Can you match discontinued siding?"],
 verify=["بازه قیمت‌ها از داده خودتان"],
 keep=["جدول مشکل/علت/نتیجه", "بخش‌های «Small and Minor» و «Urgent»", "بخش «Matching Existing Siding»", "FAQ بیمه و گارانتی"],
 video="svc11_repair")

# ------------------------------------------------------------------ 12 Windows
page(12, "windows-preparation", "Window & door preparation",
 gsc=(1, 85, 16.78),
 queries=[("west vancouver replacement windows", 0, 23, 1.1), ("replacement windows west vancouver", 0, 20, 1.0), ("vinyl replacement windows", 0, 12, 22.7), ("window prep", 0, 7, 10.4), ("window and siding repair", 0, 3, 6.0)],
 interp="ایمپرشن کم. کوئری‌های «replacement windows west vancouver» در جایگاه ۱ هستند، ولی صفحه **پنجره نمی‌فروشد یا نصب نمی‌کند**؛ فقط opening را آماده می‌کند. این عدم تطابق نیت باعث صفر کلیک است. یا یک جمله روشن اضافه کن («we prepare and flash openings; window supply is by your window company, and we coordinate with them») یا اگر نصب پنجره انجام می‌دهید، صریح بنویس.",
 questions=[("how to flash a window (tape, Tyvek, sill)", "ناقص"), ("should you replace windows before siding", "**خیر**"), ("do you have to replace siding when replacing windows", "**خیر**"), ("window sill pan", "ناقص")],
 competitors="راهنمای DuPont و Blueskin برای فلاشینگ پنجره، و ویدیوهای پرطرفدار یوتیوب (Matt Risinger و…). پیمانکاران محلی پنجره (Westeck، Ecoline) صفحه‌های «replacement windows West Vancouver» دارند.",
 problems=["**صفر تصویر** و کوتاه (حدود ۱٬۲۰۰ کلمه).", "عدم تطابق نیت با کوئری «replacement windows».", "سؤال پرجستجوی «windows before or after siding» جواب ندارد.", "توالی لایه‌ها (sill pan، WRB، پنجره، head flashing) با دیاگرام نشان داده نشده."],
 titles=["Window & Door Flashing Before New Siding | Vancouver", "Window Opening Preparation & Flashing | Siding Projects Vancouver"],
 meta="Every window and door opening flashed, sill-protected and sealed before new siding goes on, so walls don't leak at the openings. Metro Vancouver.",
 sections=["**«Windows or siding first?»** (H2)", "**«The flashing sequence»** (H2، با دیاگرام و عکس واقعی از opening آماده‌شده)", "**جمله شفاف درباره تأمین پنجره**", "۳ عکس واقعی از openingهای flashed روی پروژه‌ها"],
 faqs=["Should I replace my windows before new siding?", "Do I have to replace siding when I replace windows?", "Do you install the windows too?"],
 verify=["آیا Silversiding خودش نصب پنجره انجام می‌دهد؟"],
 keep=["لیست ۷ مرحله‌ای", "لیست «What Happens When This Step Is Skipped»"],
 video="svc12_windows")

# ------------------------------------------------------------------ 13 Vinyl
page(13, "vinyl-siding", "Vinyl siding",
 gsc=(0, 361, 23.25),
 queries=[("vinyl siding contractors", 5, 305, 7.7), ("vinyl siding vancouver", 0, 272, 24.3), ("vinyl siding repair companies near me", 0, 119, 8.1), ("vinyl siding repair near me", 0, 108, 7.4),
          ("vinyl siding repair contractors near me", 0, 101, 5.1), ("vancouver vinyl siding", 0, 43, 23.4), ("vinyl siding installation vancouver", 0, 24, 16.2)],
 interp="کوئری‌های وینیل در کل سایت ۱٬۳۹۷ ایمپرشن و ۵ کلیک دارند (احتمالاً روی صفحه اصلی)، ولی خود این صفحه **صفر کلیک** و جایگاه ۲۳ دارد. «vinyl siding vancouver» (۲۷۲) در جایگاه ۲۴ است. صفحه **هیچ تصویری ندارد**، که برای یک صفحه محصول بصری ضعف بزرگی است.",
 questions=[("vinyl siding cost per sq ft (Canada / Ontario)", "**خیر**"), ("vinyl vs hardie / metal / aluminum", "بله"), ("vinyl siding lifespan", "بله (۲۰ تا ۴۰ سال)"),
            ("insulated vinyl siding (cost, vs regular)", "ناقص"), ("is vinyl siding fire resistant / combustible", "بله"), ("can vinyl siding be painted", "بله"), ("is vinyl siding made in Canada", "خیر")],
 competitors="نتایج «vinyl siding vancouver» عمدتاً HomeStars و دایرکتوری‌ها، به‌علاوه پیمانکاران محلی با گالری و نظر هستند. قیمت‌های ملی ۲ تا ۷ دلار و وینیل عایق حدود ۱۲ دلار برای هر فوت مربع است (HomeAdvisor، آمریکا).",
 problems=["**صفر تصویر.** حداقل Vinyl-Siding-Surrey (واقعی، گالری) و ۲ پروژه دیگر.", "**قیمت** نیامده.", "**تناقض rainscreen** با بلاگ wet-climate (بریف سراسری بند ۸).", "برندهای وینیل (Gentek، Kaycan، Royal، Mitten؛ برندهای کانادایی) نام برده نشده‌اند؛ «is vinyl siding made in Canada» کوئری دارد.", "بخش تعمیر وینیل با صفحه Repair همپوشانی دارد. کوتاهش کن و لینک بده."],
 titles=["Vinyl Siding Installation & Repair Vancouver | Silversiding", "Vinyl Siding Contractors in Vancouver: Install, Replace, Repair"],
 meta="Vinyl siding installed, replaced and repaired across Metro Vancouver: lap, board-and-batten and insulated vinyl, hung to move, not nailed tight. Free estimate.",
 sections=["**«Vinyl siding cost in Vancouver»** (H2): بازه از پروژه‌ها؛ وینیل عادی در برابر عایق", "**«Vinyl brands we install»** (H3) `[VERIFY]`", "**«From our vinyl projects»** با عکس", "اصلاح متن rainscreen به نسخه دقیق و هماهنگ با بلاگ"],
 faqs=["How much does vinyl siding cost per square foot in Vancouver?", "Is insulated vinyl siding worth it?", "Is vinyl siding made in Canada?"],
 verify=["برندها", "بازه قیمت‌ها"],
 keep=["سه پروفایل", "بخش «Is Vinyl Siding the Right Fit»", "توضیح nailing slots", "FAQ"],
 video="svc13_vinyl")

# ------------------------------------------------------------------ 14 Brick & stone
page(14, "brick-and-stone-siding", "Brick & stone siding",
 gsc=(0, 256, 31.9),
 queries=[("brick installation vancouver", 0, 25, 26.7), ("brick siding", 0, 4, 44.0), ("how much does it cost to put brick on your house", 0, 1, 1.0), ("brick siding for houses", 0, 1, 2.0)],
 interp="ایمپرشن کم و جایگاه ضعیف. موضوع صفحه («brick and stone با هم») برای جستجوگر مبهم است. مردم «brick veneer»، «thin brick» یا «brick veneer cost» جستجو می‌کنند، نه «brick and stone siding». تمرکز اصلی را روی **brick veneer** بگذار و ترکیب با سنگ را به عنوان زیرموضوع نگه دار.",
 questions=[("brick veneer vs brick", "بله"), ("brick veneer cost per sq ft", "ناقص (فقط ترتیب)"), ("thin brick", "بله"), ("brick veneer vs stone veneer", "ناقص"), ("does brick veneer need weep holes / a brick ledge", "**خیر**"), ("faux brick siding cost", "خیر")],
 competitors="نتایج «brick veneer cost» ملی‌اند (HomeGuide، Angi). سازنده‌های thin brick (Glen-Gery، Interstate) جزئیات فنی دارند. پیمانکاران آجر محلی (masonry) پروژه‌های بزرگ‌تر نشان می‌دهند.",
 problems=["**«Call us at»** بدون شماره تلفن در پایان صفحه.", "**صفر تصویر در متن**، در حالی که پروژه آجری Mountain Highway (brick-siding-north-vancouver-1 تا ۵) روی سایت هست و حتی VideoObject آن در اسکیما آمده. این عکس‌ها و ویدیو را در متن صفحه نمایش بده.",
           "VideoObject با `uploadDate: \"2025-10\"`: تاریخ کامل لازم است.", "**تناقض با صفحه Stone** (بریف سراسری بند ۷).", "سؤال‌های فنی brick veneer (weep holes، brick ledge، air gap، brick ties) که نشانه تخصص‌اند، نیامده‌اند."],
 titles=["Brick Veneer & Stone Siding Installation | Vancouver", "Brick Veneer, Thin Brick & Stone Cladding | Metro Vancouver"],
 meta="Brick veneer, thin brick and stone installed together as one designed exterior in Metro Vancouver: drainage gap standard. See our Mountain Highway project.",
 sections=["**«From our projects: Mountain Highway, North Vancouver»** (H2): عکس‌ها، ویدیوی ۱۹ ثانیه‌ای، و داستان (آجر به‌علاوه ACM و دو پروفایل فایبر سیمان؛ رنگ‌آمیزی مجدد)", "**«Brick veneer details that prevent leaks»** (H2): weep holes، air space، brick ties، flashing، ledge `[VERIFY]`",
              "**«Brick veneer cost»** (H3): بازه از پروژه‌ها", "اصلاح شماره تلفن و یکدست کردن تعریف veneer با صفحه Stone"],
 faqs=["Does brick veneer need weep holes?", "How much does brick veneer cost per square foot in Vancouver?", "What is the difference between thin brick and brick veneer?"],
 verify=["جزئیات فنی brick veneer طبق BCBC بخش ۹.۲۰ و دستورالعمل سازنده"],
 keep=["تعریف veneer در برابر سازه‌ای", "بخش «Combining Brick and Stone»", "بخش «Benefits and Honest Considerations»"],
 video="svc14_brickstone")

# ------------------------------------------------------------------ 15 Rainscreen
page(15, "rainscreen", "Rain screen system",
 gsc=(0, 0, 0),
 queries=[("rain screening vancouver", 0, 5, 3.6), ("rainscreened", 0, 3, 6.0), ("rainscreen (site-wide; mostly the blog)", 0, 15, 22.1)],
 interp="**این صفحه در ۳ ماه هیچ ایمپرشنی ثبت نکرده**، در حالی که indexable است (robots meta برابر index، canonical درست، در sitemap هست و از تقریباً همه صفحات سرویس لینک داخلی دارد). محتمل‌ترین دلیل: گوگل برای همه کوئری‌های rainscreen **پست بلاگ** /what-is-a-rainscreen-wall/ (منتشرشده ۲۷ سپتامبر) را انتخاب کرده، یا این صفحه در وضعیت «Crawled – currently not indexed» است. **اقدام فوری:** URL Inspection در سرچ کنسول.",
 questions=[("rainscreen siding cost", "**خیر**"), ("rainscreen vs furring strips / plastic furring strips", "**خیر**"), ("is rainscreen necessary / required in BC", "بله"), ("rainscreen retrofit", "بله"), ("rainscreen contractor / vancouver", "ضمنی")],
 competitors="صفحه بلاگ خودتان رقیب اصلی است. بیرون از سایت: Mataverde (قیمت سیستم‌ها)، JLC (۲۵ تا ۳۰٪ افزایش هزینه)، و بولتن‌های ونکوور و BC.",
 problems=["**تداخل با بلاگ:** محتوای «How a Rain Screen System Works»، «Ventilated vs Drainscreen» و «BC Building Code» تقریباً همان بلاگ است. این صفحه باید **سرویس** را بفروشد: هزینه، retrofit روی خانه موجود، جنس فورینگ، تیم، زمان‌بندی، و پروژه‌ها. توضیح مفهومی را به ۱۰۰ تا ۱۵۰ کلمه کوتاه کن و برای جزئیات به بلاگ لینک بده.",
           "**صفر تصویر.** عکس واقعی از فورینگ، توری پایین و دیوار باز روی پروژه‌های خودتان، بزرگ‌ترین تمایز این صفحه است.", "**هزینه** نیامده.", "عبارت «Rain Screen» (دو کلمه) در عنوان و «rainscreen» (یک کلمه) در URL و بلاگ: هر دو شکل جستجو می‌شوند؛ هر دو را در متن داشته باش."],
 titles=["Rainscreen Installation & Retrofit | Vancouver Contractor", "Rain Screen System Installation for Siding | Metro Vancouver"],
 meta="Rainscreen installed with new siding or retrofitted during a reclad in Metro Vancouver: strapping or mat, vents and flashing checked. Free wall assessment.",
 sections=["**URL Inspection و در صورت نیاز Request Indexing** (قبل از هر چیز)", "**«Rainscreen installation cost»** (H2): درصد اضافه روی پروژه سایدینگ یا دلار برای هر فوت مربع، از پروژه‌های خودتان", "**«Adding a rainscreen to an existing house»** (H2): مراحل retrofit، extension jamb پنجره، زمان‌بندی",
              "**«Furring strips: wood vs plastic, and drainage mats»** (H3)", "**«From our projects»**: عکس‌های مراحل نصب", "کوتاه کردن بخش‌های مفهومی و لینک به بلاگ"],
 faqs=["How much does a rainscreen add to a siding job in Vancouver?", "Wood or plastic furring strips for a rainscreen?", "How long does a rainscreen retrofit take?"],
 verify=["وضعیت ایندکس در سرچ کنسول", "بازه هزینه از پروژه‌ها"],
 keep=["بخش «Rain Screen System vs. Air Barrier»", "فرایند ۳ مرحله‌ای (به‌خصوص بازبینی vent و weep)"],
 video="svc15_rainscreen")


def esc(x): return str(x).replace("|", "\\|")


def md(n, slug, name, d):
    f = {k: (esc(v) if isinstance(v, str) else v) for k, v in FACTS[slug].items()}
    f["h1"] = [esc(h) for h in FACTS[slug]["h1"]]
    cl, imp, pos = d["gsc"]
    ctr = f"{cl / imp * 100:.2f}٪" if imp else "—"
    L = [f"# بریف آپدیت صفحه سرویس {n:02d}: {name}", "",
         "## ۰. دستورالعمل برای مدل هوش مصنوعی",
         "- **زبان پاسخ:** تحلیل و توضیحاتت را **به فارسی** بنویس. هر متنی که مستقیم در سایت انگلیسی قرار می‌گیرد (عنوان، متا، هدینگ، پاراگراف، FAQ، کپشن تصویر، اسکیما) را به **انگلیسی کانادایی** بنویس و زیر هر کدام یک توضیح کوتاه فارسی بگذار.",
         "- قبل از این بریف، فایل `sitewide-eeat.md` (مشکلات مشترک همه صفحات) را بخوان و اعمال کن.",
         "- این یک **صفحه سرویس** است: هدف، تبدیل بازدیدکننده محلی (Metro Vancouver) به درخواست برآورد است. لحن صادق و فنی فعلی را حفظ کن.",
         "- برند در متن: **Silversiding**. بنیان‌گذار: **Mahmoud Ardeshiri**. هیچ گواهی، قیمت، نظر مشتری یا مشخصات محصولی را از خودت نساز. اگر منبع نداری، کنارش `[VERIFY]` بگذار.", "",
         "## ۱. مشخصات فعلی صفحه (۵ نوامبر ۲۰۲۶)",
         "| مورد | وضعیت فعلی |", "|---|---|",
         f"| URL | https://silversiding.ca/services/{slug}/ |",
         f"| Title tag | {f['title']} |", f"| Meta | {f['meta']} |", f"| H1 | {' / '.join(f['h1'])} |",
         f"| حجم | حدود {f['words']:,} کلمه (به‌علاوه بلوک‌های قالب)، {f['imgs']} تصویر محتوایی، {f['faq_schema']} سؤال در اسکیمای FAQ |",
         f"| اسکیما | {', '.join(x for x in f['schema'] if x not in ('Answer', 'Question', 'ListItem', 'GeoCoordinates', 'PostalAddress', 'ContactPoint', 'Place', 'City'))} |", "",
         "## ۲. داده‌های سرچ کنسول (۳ ماه: ۳ آگوست تا ۲ نوامبر ۲۰۲۶)",
         f"- کل صفحه: **{cl} کلیک، {imp:,} ایمپرشن، CTR {ctr}، جایگاه میانگین {pos if imp else '—'}.**",
         "- کوئری‌های مرتبط (از فایل کل سایت، با تطبیق کلمه کلیدی؛ ممکن است بعضی از این کوئری‌ها صفحه دیگری از سایت را نشان داده باشند):", "",
         "| کوئری | کلیک | ایمپرشن | جایگاه |", "|---|---|---|---|"]
    L += [f"| {esc(q)} | {c} | {i} | {p} |" for q, c, i, p in d["queries"]]
    L += ["", f"**تفسیر:** {d['interp']}", "",
          "## ۳. سؤال‌های جستجوگرها (Google Autocomplete؛ باکس PAA برای دسترسی خودکار مسدود است)",
          "| سؤال | در صفحه جواب داده شده؟ |", "|---|---|"]
    L += [f"| {esc(q)} | {esc(a)} |" for q, a in d["questions"]]
    L += ["", "## ۴. رقبا", d["competitors"], "", "## ۵. مشکلات و کمبودها (به ترتیب اثر)"]
    L += [f"{i + 1}. {p}" for i, p in enumerate(d["problems"])]
    L += ["", "## ۶. برنامه آپدیت", "### ۶.۱ عنوان و متا (حداکثر ۶۰ و ۱۵۵ کاراکتر)"]
    L += [f"- `{t}`" for t in d["titles"]]
    L += [f"- متا: `{d['meta']}`", "", "### ۶.۲ بخش‌های جدید یا اصلاحی"]
    L += [f"- {s}" for s in d["sections"]]
    L += ["", "### ۶.۳ سؤال‌های جدید FAQ (جواب هر کدام ۴۰ تا ۷۰ کلمه، به انگلیسی)"]
    L += [f"{i + 1}. {q}" for i, q in enumerate(d["faqs"])]
    L += ["", "### ۶.۴ E-E-A-T در این صفحه",
          "- باکس «Reviewed by Mahmoud Ardeshiri, Founder» با لینک به صفحه او و یک جمله تجربه مرتبط با همین متریال.",
          "- ۲ یا ۳ نظر واقعی مشتری که به همین سرویس مربوط است، به‌علاوه لینک Google Business Profile.",
          "- اعتبارنامه‌ها در یک نوار کوتاه: WorkSafeBC، بیمه مسئولیت، برنامه ایمنی مکتوب، گارانتی ۵ ساله اجرا (جدا از گارانتی محصول).",
          "- حداقل ۳ عکس واقعی با کپشن مکان؛ رندرهای AI با برچسب «Illustration».", "",
          "### ۶.۵ ویدیو",
          f"ویدیوی یوتیوب همین پکیج (`video.mp4`) بعد از بخش اول embed شود، با `VideoObject` کامل (`uploadDate` به صورت YYYY-MM-DD) و یک خلاصه ۲ تا ۳ خطی زیر ویدیو.", "",
          "## ۷. موارد قابل راستی‌آزمایی"]
    L += [f"- {v}" for v in d["verify"]]
    L += ["", "## ۸. این‌ها دست نخورند"] + [f"- {k}" for k in d["keep"]]
    L += ["", "## ۹. چک‌لیست تحویل",
          "- [ ] همه موارد §۵ اصلاح شده", "- [ ] عنوان و متا آپدیت شده", "- [ ] بخش‌های §۶.۲ و FAQ های §۶.۳ اضافه شده",
          "- [ ] E-E-A-T (§۶.۴) و ویدیو (§۶.۵) اعمال شده", "- [ ] همه موارد `[VERIFY]` حل شده", ""]
    return "\n".join(L)


if __name__ == "__main__":
    out = os.path.join(HERE, "briefs", "services")
    os.makedirs(out, exist_ok=True)
    for n, slug, name, d in P:
        p = os.path.join(out, f"{n:02d}-{slug}.md")
        open(p, "w", encoding="utf-8").write(md(n, slug, name, d))
        print(p)
