import os

bots_folder = "bots"

# إذا كان هناك ملف بنفس اسم المجلد، احذفه
if os.path.isfile(bots_folder):
    os.remove(bots_folder)

# أنشئ المجلد إن لم يكن موجودًا
if not os.path.exists(bots_folder):
    os.makedirs(bots_folder)

# ثم أكمل قراءة الملفات
for filename in os.listdir(bots_folder):
    # الكود هنا...