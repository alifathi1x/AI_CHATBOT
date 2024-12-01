# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GqFfzYwUVx8aiQ_r-7AkMW-Ed3ql9EVy
"""

import pandas as pd
import numpy as np

!pip install sentence_transformers

from sentence_transformers import SentenceTransformer, util

question_bank = [
    {"question":"چگونه می‌توانم اضطراب روزانه‌ام را مدیریت کنم؟","answer":"تمرین نفس عمیق و مدیتیشن."},
    {"question":"چه زمانی اضطراب نیاز به درمان حرفه‌ای دارد؟","answer":"وقتی که عملکرد روزانه‌تان مختل می‌شود"},
    {"question":"آیا ورزش می‌تواند اضطراب را کاهش دهد؟","answer":"بله، به‌ویژه یوگا و پیاده‌روی"},
    {"question":"چگونه از حمله‌های پانیک جلوگیری کنم؟","answer":"تنفس عمیق و شناسایی محرک‌ها"},
    {"question":"آیا تغذیه بر اضطراب تأثیر دارد؟","answer":"بله، کاهش کافئین و افزایش مصرف میوه و سبزی"},
    {"question":"آیا داروهای ضد اضطراب اعتیادآور هستند؟","answer":"برخی بله، تحت نظر پزشک مصرف کنید"},
    {"question":"آیا موسیقی آرامش‌بخش می‌تواند اضطراب را کاهش دهد؟","answer":"بله، به‌خصوص موسیقی بی‌کلام"},
    {"question":"چگونه می‌توانم با اضطراب اجتماعی کنار بیایم؟","answer":"تمرین مهارت‌های اجتماعی و مواجهه تدریجی"},
    {"question":"آیا تکنیک‌های CBT برای اضطراب موثر است؟","answer":"بله، تغییر الگوهای فکری بسیار کمک‌کننده است"},
    {"question":"چگونه شب‌ها اضطراب را کنترل کنم؟","answer":"روتین خواب منظم و نوشتن افکار قبل از خواب"},
    {"question":"چگونه با حس ناامیدی مقابله کنم؟","answer":"به اهداف کوچک فکر کنید و از دوستان حمایت بگیرید"},
    {"question":"آیا افسردگی بدون دارو قابل درمان است؟","answer":"بله، با روان‌درمانی و سبک زندگی سالم"},
    {"question":"چگونه می‌توانم احساس ارزشمندی را بازسازی کنم؟","answer":"تمرکز بر دستاوردها و مهارت‌های شخصی"},
    {"question":"چه زمانی افسردگی نیاز به مداخله اورژانسی دارد؟","answer":"در صورت وجود افکار خودکشی"},
    {"question":"آیا افسردگی ژنتیکی است؟","answer":"بله، اما عوامل محیطی هم تأثیرگذارند"},
    {"question":"آیا خواب زیاد نشانه افسردگی است؟","answer":"ممکن است باشد؛ به یک متخصص مراجعه کنید"},
    {"question":"چگونه با افسردگی پس از زایمان مقابله کنم؟","answer":"حمایت خانواده و مشاوره حرفه‌ای"},
    {"question":"آیا هنر درمانی برای افسردگی مؤثر است؟","answer":"بله، می‌تواند احساسات را تسکین دهد"},
    {"question":"چگونه انرژی‌ام را در طول افسردگی بازگردانم؟","answer":"تغذیه مناسب، فعالیت بدنی و استراحت کافی"},
    {"question":"آیا داروهای ضد افسردگی ایمن هستند؟","answer":"بله، تحت نظر پزشک"},
    {"question":"چگونه می‌توانم استرس شغلی را کاهش دهم؟","answer":"مدیریت زمان و استراحت‌های منظم"},
    {"question":"آیا تکنیک‌های ذهن‌آگاهی برای استرس مؤثر است؟","answer":"بله، تمرکز بر لحظه حال کمک می‌کند"},
    {"question":"چگونه استرس امتحانات را مدیریت کنم؟","answer":"برنامه‌ریزی دقیق و استراحت مناسب"},
    {"question":"آیا روابط پرتنش باعث استرس می‌شود؟","answer":"بله، با گفتگو مشکلات را حل کنید"},
    {"question":"چگونه بدنم را از اثرات استرس رها کنم؟","answer":"ماساژ، ورزش و مدیتیشن کمک می‌کند"},
    {"question":"آیا استرس می‌تواند باعث بیماری جسمی شود؟","answer":"بله، مشکلات قلبی و گوارشی"},
    {"question":"چگونه می‌توانم تمرکز خود را در زمان استرس حفظ کنم؟","answer":"تقسیم وظایف به بخش‌های کوچک"},
    {"question":"آیا تکنیک‌های تنفس عمیق مفید است؟","answer":"بله، ضربان قلب را کاهش می‌دهد"},
    {"question":"چگونه از استرس مزمن جلوگیری کنم؟","answer":"سبک زندگی متعادل و برنامه‌های استراحت"},
    {"question":"آیا موسیقی به کاهش استرس کمک می‌کند؟","answer":"بله، موسیقی آرامش‌بخش مفید است"},
    {"question":"چگونه می‌توانم مشکل بی‌خوابی را برطرف کنم؟","answer":"ایجاد یک روتین منظم خواب و اجتناب از کافئین در شب"},
    {"question":"آیا تکنیک‌های تنفس برای بهبود خواب مفید هستند؟","answer":"بله، تنفس عمیق می‌تواند به آرامش کمک کند"},
    {"question":"چگونه خواب سبک را به خواب عمیق تبدیل کنم؟","answer":"محیط تاریک، دمای مناسب و خواب منظم"},
    {"question":"چرا همیشه خسته از خواب بیدار می‌شوم؟","answer":"ممکن است به کیفیت خواب یا آپنه خواب مربوط باشد"},
    {"question":"آیا استفاده از موبایل قبل از خواب مضر است؟","answer":"بله، نور آبی آن کیفیت خواب را کاهش می‌دهد"},
    {"question":"چگونه با کابوس‌های مکرر مقابله کنم؟","answer":"کاهش استرس و مراجعه به روان‌شناس"},
    {"question":"آیا کم‌خوابی می‌تواند باعث مشکلات روانی شود؟","answer":"بله، اضطراب و افسردگی را تشدید می‌کند"},
    {"question":"چگونه خوابم را تنظیم کنم؟","answer":"هر روز سر یک ساعت مشخص بخوابید و بیدار شوید"},
    {"question":"آیا چرت روزانه مفید است؟","answer":"بله، اما کوتاه (۱۵-۲۰ دقیقه)"},
    {"question":"چگونه با بی‌خوابی ناشی از استرس کنار بیایم؟","answer":"مدیتیشن و نوشتن افکار قبل از خواب"},
    {"question":"چگونه می‌توانم وسواس فکری را کاهش دهم؟","answer":"تمرین تغییر تمرکز و کمک گرفتن از روان‌درمانی"},
    {"question":"آیا وسواس قابل درمان است؟","answer":"بله، با ترکیب دارودرمانی و روان‌درمانی"},
    {"question":"چگونه از تکرار رفتارهای وسواسی جلوگیری کنم؟","answer":"شناسایی محرک‌ها و تغییر الگوهای رفتاری"},
    {"question":"آیا تکنیک‌های سی بی تی برای وسواس موثر است؟","answer":"بله، به‌ویژه تکنیک‌های مواجهه و پیشگیری از پاسخ"},
    {"question":"چگونه از شر افکار مزاحم خلاص شوم؟","answer":"پذیرش بدون قضاوت و تمرین ذهن‌آگاهی"},
    {"question":"آیا وسواس می‌تواند زندگی روزمره را مختل کند؟","answer":"بله، در صورت شدید بودن"},
    {"question":"آیا ورزش برای کاهش وسواس مفید است؟","answer":"بله، ورزش استرس را کاهش می‌دهد"},
    {"question":"آیا وسواس می‌تواند ژنتیکی باشد؟","answer":"بله، اما عوامل محیطی نیز موثرند"},
    {"question":"چگونه از خستگی ناشی از وسواس جلوگیری کنم؟","answer":"استراحت کافی و برنامه‌های آرام‌بخش"},
    {"question":"آیا داروهای وسواس ایمن هستند؟","answer":"بله، با نظارت پزشک"},
    {"question":"چگونه می‌توانم عزت نفسم را افزایش دهم؟","answer":"تمرکز بر نقاط قوت و دستاوردها"},
    {"question":"چرا خودم را با دیگران مقایسه می‌کنم؟","answer":"این عادت طبیعی است؛ تمرکز بر خودتان کنید"},
    {"question":"آیا تمرین‌های خودگویی مثبت مفید هستند؟","answer":"بله، کمک می‌کنند افکار منفی را کاهش دهید"},
    {"question":"چگونه بر احساس بی‌ارزشی غلبه کنم؟","answer":"تعیین اهداف کوچک و مشاوره حرفه‌ای"},
    {"question":"آیا شبکه‌های اجتماعی عزت نفس را کاهش می‌دهند؟","answer":"ممکن است؛ زمان استفاده را محدود کنید"},
    {"question":"چگونه اعتمادبه‌نفسم را در جمع افزایش دهم؟","answer":"تمرین مهارت‌های اجتماعی و مواجهه تدریجی"},
    {"question":"چگونه از افکار منفی درباره خودم جلوگیری کنم؟","answer":"جایگزینی افکار منفی با مثبت"},
    {"question":"آیا یادگیری مهارت‌های جدید به عزت نفس کمک می‌کند؟","answer":"بله، احساس پیشرفت ایجاد می‌کند"},
    {"question":"چگونه بر ترس از شکست غلبه کنم؟","answer":"شکست را به‌عنوان بخشی از یادگیری بپذیرید"},
    {"question":"آیا کتاب‌خوانی می‌تواند به عزت نفس کمک کند؟","answer":"بله، به‌ویژه کتاب‌های انگیزشی و روان‌شناسی"},
    {"question":"چگونه با شریک عاطفی‌ام بهتر ارتباط برقرار کنم؟","answer":"گوش دادن فعال و بیان واضح نیازها"},
    {"question":"چگونه بر حسادت در رابطه غلبه کنم؟","answer":"اعتمادسازی و تمرکز بر خود"},
    {"question":"چرا در روابط عاطفی احساس ناامنی می‌کنم؟","answer":"ممکن است به عزت نفس پایین یا تجربیات گذشته مربوط باشد"},
    {"question":"چگونه می‌توانم تعارضات رابطه‌ای را حل کنم؟","answer":"صحبت در زمان مناسب و اجتناب از سرزنش"},
    {"question":"آیا فاصله عاطفی در رابطه طبیعی است؟","answer":"گاهی بله، اما نیاز به تلاش مشترک دارد"},
    {"question":"چگونه از وابستگی بیش‌ازحد جلوگیری کنم؟","answer":"حفظ استقلال شخصی و تقویت خودشناسی"},
    {"question":"چرا بعد از جدایی احساس گناه می‌کنم؟","answer":"طبیعی است؛ پذیرش و زمان کمک می‌کند"},
    {"question":"آیا مشاوره زوج‌ها مؤثر است؟","answer":"بله، به بهبود ارتباط و حل مشکلات کمک می‌کند"},
    {"question":"چگونه به شریکم اعتماد کنم؟","answer":"شفافیت و گفتگوهای صادقانه"},
    {"question":"چگونه بعد از خیانت بهبود یابم؟","answer":"مشاوره حرفه‌ای و زمان برای بازسازی اعتماد"},
    {"question":"آیا اختلالات شخصیتی قابل درمان هستند؟","answer":"قابل مدیریت هستند، اما درمان کامل ممکن است چالش‌برانگیز باشد"},
    {"question":"چگونه اختلال شخصیت مرزی را بشناسم؟","answer":"بی‌ثباتی عاطفی و روابط ناپایدار نشانه‌های اصلی‌اند"},
    {"question":"آیا افراد با اختلال شخصیت ضد اجتماعی می‌توانند تغییر کنند؟","answer":"تغییر سخت است، اما ممکن با درمان"},
    {"question":"چگونه با فردی با اختلال شخصیت خودشیفته برخورد کنم؟","answer":"مرزهای واضح تعیین کنید و از خودتان مراقبت کنید"},
    {"question":"آیا اختلال شخصیت پارانوئید خطرناک است؟","answer":"اگر شدید باشد، ممکن است به روابط آسیب برساند"},
    {"question":"چگونه با فردی با اختلال شخصیت اجتنابی رفتار کنم؟","answer":"حمایت و تشویق به تعامل تدریجی"},
    {"question":"آیا اختلال شخصیت دوقطبی درمان‌پذیر است؟","answer":"با دارو و روان‌درمانی قابل مدیریت است"},
    {"question":"چگونه تشخیص دهم که اختلال شخصیت دارم؟","answer":"ارزیابی حرفه‌ای توسط روان‌شناس یا روان‌پزشک"},
    {"question":"آیا همه اختلالات شخصیتی نیاز به دارو دارند؟","answer":"خیر، بسیاری با روان‌درمانی مدیریت می‌شوند"},
    {"question":"چگونه به فردی با اختلال شخصیت کمک کنم؟","answer":"او را به مشاوره حرفه‌ای ترغیب کنید"},
    {"question":"چگونه خشمم را کنترل کنم؟","answer":"تنفس عمیق و تکنیک‌های آرامش‌بخش"},
    {"question":"آیا خشم همیشه منفی است؟","answer":"نه، اگر سازنده مدیریت شود"},
    {"question":"چگونه از عصبانیت ناگهانی جلوگیری کنم؟","answer":"شناخت محرک‌ها و آماده‌سازی ذهنی"},
    {"question":"آیا ورزش به کنترل خشم کمک می‌کند؟","answer":"بله، انرژی منفی را تخلیه می‌کند"},
    {"question":"چگونه در دعوا آرامش خود را حفظ کنم؟","answer":"مکث کرده و به تأخیر انداختن واکنش"},
    {"question":"چگونه با خشم دیگران برخورد کنم؟","answer":"آرام بمانید و فضای امن ایجاد کنید"},
    {"question":"چطوری افسردگیمو کم کنم؟","answer":"فعالیت بدنی (ورزش منظم) و ارتباط با دوستان و خانواده و خواب کافی و منظم و تغذیه سالم و مشاوره با روان‌شناس یا روان‌پزشک و تمرین مدیتیشن یا تکنیک‌های آرامش‌بخش"},
    {"question":"آیا نوشتن احساسات به کنترل خشم کمک می‌کند؟","answer":"بله، روش مفیدی برای تخلیه است"},
    {"question":"چگونه از سرزنش کردن در زمان عصبانیت اجتناب کنم؟","answer":"تمرکز بر بیان احساس خودتان به جای مقصر دانستن دیگران"},
    {"question":"آیا خشم سرکوب‌شده خطرناک است؟","answer":"بله، ممکن است منجر به مشکلات جسمی و روانی شود"},
    {"question":"چگونه بر ترس از تصمیم‌گیری غلبه کنم؟","answer":"اطلاعات جمع‌آوری کرده و اعتماد به شهودتان داشته باشید"},
    {"question":"چرا بعد از تصمیم‌گیری احساس شک می‌کنم؟","answer":"به انتخاب خود احترام بگذارید و از بازبینی زیاد اجتناب کنید"},
    {"question":"چگونه تصمیمات بزرگ زندگی را بگیرم؟","answer":"مزایا و معایب را نوشته و مشورت کنید"}


]
df = pd.DataFrame(question_bank)

model = SentenceTransformer("HooshvareLab/bert-fa-zwnj-base")

def get_embedding(sentences):
  embeddings = model.encode(sentences, convert_to_tensor=True)
  return embeddings

def find_similar_question(new_question, questions, threshold=0.9):
  embeddings = get_embedding(questions + [new_question])
  cosine_scores = util.pytorch_cos_sim(embeddings[-1], embeddings[:-1])
  max_score = cosine_scores.max().item()
  if max_score >= threshold:
    item = df.iloc[cosine_scores.argmax().item()]
    return item["question"], item["answer"], max_score
  return "Cant Match Your Questions", "Call Admin", max_score

while True:
  new_question = input("Enter Question : ")
  if new_question == "exit":
    break
  question, answer, score = find_similar_question(new_question, list(df["question"]), 0.8)
  print("Matched Question :", question)
  print("MatchedAnswer :", answer)
  print("Match Score :", score)
  print("-----------------------------------")