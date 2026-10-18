%%writefile main.py
import os
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from docxtpl import DocxTemplate

class ResidenceApp(App):
    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        root = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=20)
        layout.bind(minimum_height=layout.setter('height'))
        
        title = Label(text="تطبيق شهادة الإقامة - الهاتف", font_size=24, color=(0, 0, 0, 1), bold=True, size_hint_y=None, height=50)
        layout.add_widget(title)
        
        self.fields = {}
        # قائمة الحقول المطلوبة لشهادة الإقامة كما حددتها
        fields_list = [
            ('first_name_ar', 'الاسم الشخصي (بالعربية)'), ('first_name_fr', 'Prénom (en Français)'),
            ('last_name_ar', 'الاسم العائلي (بالعربية)'), ('last_name_fr', 'Nom (en Français)'),
            ('birth_date_ar', 'تاريخ الازدياد (الموافق لـ)'), ('birth_date_fr', 'Né le (Date)'),
            ('birth_place_ar', 'مكان الازدياد (جماعة...)'), ('birth_place_fr', 'Lieu de naissance (Commune)'),
            ('father_name_ar', 'اسم الأب كاملاً'), ('father_name_fr', 'Nom du Père'),
            ('grandfather_p_ar', 'اسم الجد من الأب'), ('grandfather_p_fr', 'Grand-père paternel'),
            ('mother_name_ar', 'اسم الأم كاملة'), ('mother_name_fr', 'Nom de la Mère'),
            ('grandfather_m_ar', 'اسم الجد من الأم'), ('grandfather_m_fr', 'Grand-père maternel'),
            ('job_ar', 'المهنة (بالعربية)'), ('job_fr', 'Profession (en Français)'),
            ('status_ar', 'الحالة العائلية (أعزب/متزوج)'), ('status_fr', 'État civil'),
            ('cin', 'رقم البطاقة الوطنية CIN'),
            ('address_ar', 'العنوان (دوار...)'), ('address_fr', 'Adresse (Douar...)')
        ]
        
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        for key, name in fields_list:
            lbl = Label(text=name, color=(0.2, 0.2, 0.2, 1), size_hint_x=0.4, halign='right')
            txt = TextInput(multiline=False, size_hint_x=0.6, size_hint_y=None, height=40)
            self.fields[key] = txt
            grid.add_widget(txt)
            grid.add_widget(lbl)
            
        layout.add_widget(grid)
        
        btn = Button(text="إنشاء وحفظ مستند شهادة الإقامة", background_color=(0.1, 0.6, 0.3, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        btn.bind(on_press=self.generate_doc)
        layout.add_widget(btn)
        
        self.status_label = Label(text="", color=(1, 0, 0, 1), size_hint_y=None, height=30)
        layout.add_widget(self.status_label)
        
        root.add_widget(layout)
        return root

    def generate_doc(self, instance):
        try:
            data = {key: txt.text for key, txt in self.fields.items()}
            # تأكد من وضع ملف residence_template.docx في مجلد التطبيق
            template_path = "residence_template.docx"
            if not os.path.exists(template_path):
                self.status_label.text = "خطأ: ملف النموذج residence_template.docx غير موجود!"
                return
                
            doc = DocxTemplate(template_path)
            doc.render(data)
            output_name = f"شهادة_إقامة_{data['last_name_ar']}.docx"
            doc.save(output_name)
            self.status_label.text = f"تم الحفظ بنجاح: {output_name}"
            self.status_label.color = (0, 0.6, 0, 1)
        except Exception as e:
            self.status_label.text = f"فشل الحفظ: {str(e)}"
            self.status_label.color = (1, 0, 0, 1)

if __name__ == '__main__':
    ResidenceApp().run()
  
