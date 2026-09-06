from bs4 import BeautifulSoup
import yuag
import random
yuag.clear()

def get_shuffle(main_list, random_list) -> int:
    """
    main_list = [a,b,c,d]
    random_list = [d,b,a,c]
    → 4213
    """

    res = []
    
    for item in random_list:
        index = main_list.index(item)
        res.append(str(index + 1))
    
    return int(''.join(res))

def random_arr(arr) -> list:
    res = arr.copy()
    random.shuffle(res)

    return res

path = "سنة أولى/الفصل الأول/أساسيات علوم الحاسب"
files = [f"{path}/{yuag.makeZeroNum(i+1)} quiz.html" for i in range(9)]
answers_file = f"{path}/Answer Key.html"

with open(answers_file, 'r', encoding='utf-8') as f:
    answers_content = f.read()
answers_soup = BeautifulSoup(answers_content, 'html.parser')

data = {}
for file in files:
    file_i = file.split("/")[-1].split(" quiz")[0]
    data[file_i] = []

    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

    questions = soup.select(".question")
    
    # تخزين الإجابات الجديدة لكل سؤال
    new_answers = []
    
    for q in questions:
        # استخراج الخيارات
        options = q.select(".opt")
        opt_texts = []
        
        for opt in options:
            letter = opt.select_one(".opt-letter").text.strip()
            text = opt.select_one(".opt-text").text.strip()
            opt_texts.append(text)
        
        opt_texts_shuffled = random_arr(opt_texts)
        data[file_i].append(get_shuffle(opt_texts, opt_texts_shuffled))

        for i, opt in enumerate(options):
            text_ = opt.select_one(".opt-text")
            text_.string = opt_texts_shuffled[i]
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

answers = answers_soup.select(".cell .q-char")

yuag.saveJSON(data, "shuffle.json")

data_arr = sum(data.values(), [])
for i, answer in enumerate(answers):
    chars = ["A", "B", "C", "D"]
    char = answer.string # A, B, C, D
    shuffle = str(data_arr[i]) # "1423"

    answer.string = chars[shuffle.index(str(chars.index(char)+1))]

# حفظ ملف Answer Key المعدل
with open(answers_file, 'w', encoding='utf-8') as f:
    f.write(str(answers_soup))

yuag.doneMessage(0)