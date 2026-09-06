from bs4 import BeautifulSoup
import yuag
import os
yuag.clear()

page_i = 1
path = "سنة أولى/الفصل الأول/أساسيات علوم الحاسب"

def merge_html_files(file_list):
    global page_i

    # إنشاء مستند HTML أساسي
    head = """
    <meta charset="UTF-8">
    <title>Book</title>
    <link rel="stylesheet" href="main.css">
    <link rel="stylesheet" href="../../../quiz.css">
    """

    merged = BeautifulSoup(f"<html><head>{head}</head><body></body></html>", "html.parser")
    
    for file_path in file_list:
        if not os.path.exists(file_path):
            print(f"تحذير: الملف {file_path} غير موجود")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            
            body_content = soup.body
            if body_content:
                # استخراج كل div.page
                pages = body_content.select(".page")
                
                for page in pages:
                    page.select(".page-num-circle")[0].string = f"{page_i}"
                    page_i += 1
                    
                    merged.body.append(page)
    
    return merged

files = []
for i in range(9):
    i += 1
    files.append(f"{path}/{yuag.makeZeroNum(i)}.html")
    files.append(f"{path}/{yuag.makeZeroNum(i)} quiz.html")
files.append(f"{path}/Answer Key.html")

result = merge_html_files(files)

yuag.saveFile(result.prettify(), f"{path}/book.html")


yuag.doneMessage(0)