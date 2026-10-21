from rembg import remove
from PIL import Image

# فتح الصورة (بدّل الاسم ديال الصورة الثالثة هنا)
input_path = "/home/mohamad/Pictures/qw.png"
output_path = "image3_no_bg.png"

img = Image.open(input_path)

# إزالة الخلفية تلقائياً
result = remove(img)

# حفظ النتيجة
result.save(output_path)

print("Done! Background removed")