from django.db import models
from django.utils import timezone
from cms.models.pluginmodel import CMSPlugin
from django.core.urlresolvers import reverse
from sufix.formatChecker import ContentTypeRestrictedFileField
####################################################################

class Partners(models.Model):
    partner_name = models.CharField(unique=True, max_length=192, db_index=True, help_text="Наименование Контрагента (полное) *", verbose_name="Наименование Контрагента")
    partner_shortname = models.CharField(unique=True, max_length=32, help_text="Сокращенное наименование (Максимальная длинна - 32 знака) *", verbose_name="Сокращенное наименование")
    type = models.ForeignKey('PartnerType', help_text="Тип Контрагента", verbose_name="Тип")
    status = models.ForeignKey('PartnerStatus', help_text="Статус Контрагента *", verbose_name="Статус")
    class Meta:
        db_table = "sfx_partners"
        unique_together = ("partner_name","partner_shortname")
        ordering = ["partner_name", "status"]
        verbose_name = "Контрагента"
        verbose_name_plural = "Контрагенты"
    def __str__(self):
           return self.partner_shortname

class PartnerDetails(models.Model):
    partner = models.OneToOneField('Partners')
    adress_legal = models.CharField(max_length=256, help_text="Юридический адрес *", verbose_name="Юридический адрес")
    adress_actual = models.CharField(null=True, blank=True, max_length=256, help_text="Фактический адрес", verbose_name="Фактический адрес")
    inn = models.CharField(max_length=11, help_text="ИНН *", verbose_name="ИНН")
    kpp = models.CharField(max_length=9, help_text="КПП *", verbose_name="КПП")
    ogrn = models.CharField(null=True, blank=True, max_length=13, help_text="ОГРН", verbose_name="ОГРН")
    details_of_bank = models.TextField(null=True, blank=True, help_text="Банковские реквизиты", verbose_name="Банковские реквизиты")
    tel_fax = models.CharField(null=True, blank=True, max_length=12, help_text="Телефон", verbose_name="Телефон")
    email = models.EmailField(null=True, blank=True, max_length=32, help_text="Адрес эл. почты", verbose_name="E-Mail")
    #details_active = models.BooleanField(default=True, help_text="Статус реквизитов", verbose_name="Активный")
    #active_start = models.DateField (default=timezone.now, help_text="Дата активации *(По умолчанию: устанавливается дата добавления)", verbose_name="Дата активации")
    #active_stop = models.DateField (null=True, blank=True, help_text="Дата деактивации (Дата с которой данная запись определена как \"Недействительная\")", verbose_name="Дата деактивации")
    class Meta:
        db_table = "sfx_partner_details"
        unique_together = ("inn","kpp")
        verbose_name = "Раздел - Дополнительная информация по Контрагенту"
        verbose_name_plural = "Дополнительная информация по Контрагентам"
    def __str__(self):
        return '%s' % (self.partner)

class PartnersDescriptions(models.Model):
    desc_to_partner = models.OneToOneField('Partners')
    description = models.TextField(null=True, blank=True, help_text="Дополнительные свведения или описание", verbose_name="Описание")
    class Meta:
        db_table = "sfx_partners_descriptions"
        verbose_name = "Дополнительное описание"
        verbose_name_plural = "Дополнительные описания"
    def __str__(self):
        return '%s' % (self.desc_to_partner)

class PartnerType(models.Model):
    PARTNERTYPES = (
        ("Не определен", "Не определен"),
        ("Агент", "Агент"),
        ("Заказчик", "Заказчич"),
        ("Субподрядчик", "Субподрядчик")
    )
    type = models.CharField(max_length=16, choices=PARTNERTYPES, default="Не определен", help_text="Тип Контрагента", verbose_name="Тип")
    class Meta:
        db_table = "sfx_partner_type"
        verbose_name = "Тип Контрагента"
        verbose_name_plural = "Типы Контрагентов"
    def __str__(self):
        return '%s' % (self.type)

class PartnerStatus(models.Model):
    status = models.CharField(max_length=32, help_text="Статус Контрагента *", verbose_name="Статус")
    class Meta:
        db_table = "sfx_partner_status"
        verbose_name = "Статус Контрагента"
        verbose_name_plural = "Статусы Контрагентов"
    def __str__(self):
        return '%s' % (self.status)

####################################################################

class Contacts(models.Model):
    last_name = models.CharField(max_length=50, help_text="Фамилия сотрудника *", verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, help_text="Имя сотрудника *", verbose_name="Имя")
    patronymic = models.CharField(null=True, blank=True, max_length=50, help_text="Отчество сотрудника ", verbose_name="Отчество")
    active = models.BooleanField(default=True, help_text="Статус Контакта", verbose_name="Активный")
    partner = models.ForeignKey('Partners', help_text="Наименование Организации *", verbose_name="Организация")
    class Meta:
        db_table = "sfx_contacts"
        unique_together = ("last_name", "first_name", "patronymic")
        ordering = ["last_name", "first_name", "patronymic"]
        verbose_name = "Контактное лицо Контрагента"
        verbose_name_plural = "Контактные лица Контрагентов"
    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.patronymic)

class ContactDetails(models.Model):
    contact = models.OneToOneField('Contacts')
    poosition = models.CharField(null=True, blank=True, max_length=64, help_text="Должность", verbose_name="Должность")
    adress_location = models.CharField(null=True, blank=True, max_length=256, help_text="Адрес расположения", verbose_name="Адрес расположения")
    mobile_tel = models.CharField(null=True, blank=True, max_length=12, help_text="Номер телефона (мобильный)", verbose_name="Телефон (моб.)")
    work_tel = models.CharField(null=True, blank=True, max_length=20, help_text="Номер телефона (рабочий)", verbose_name="Телефон (раб.)")
    email = models.EmailField(max_length=32, help_text="*Адрес электронной почты *", verbose_name="E-Mail")
    class Meta:
        db_table = "sfx_contact_details"
        verbose_name = "Раздел - \"Расширенные сведения по Контакту\""
        verbose_name_plural = "Дополнительная информация по Контакту"
    def __str__(self):
        return '%s' % (self.contact)

class ContactsDescriptions(models.Model):
    desc_to_contact = models.OneToOneField('Contacts')
    description = models.TextField(null=True, blank=True, help_text="Дополнительные свведения или описание", verbose_name="Описание")
    class Meta:
        db_table = "sfx_contacts_descriptions"
        verbose_name = "Раздел - \" Дополнительное описание\""
        verbose_name_plural = "Дополнительное описание"
    def __str__(self):
        return '%s' % (self.desc_to_contact)

####################################################################

class Projects(models.Model):
    project_name = models.CharField(max_length=256, help_text="Полное наименование Проекта/Контракта (Максимальная длинна 256 знаков/символов)*", verbose_name="Наименование проекта")
    project_shortname = models.CharField(max_length=64, help_text="Сокращенное наименование Проекта/Контракта (Максимальная длинна 64 знака/символа)*", verbose_name="Сокращенное наименование")
    project_to_partner = models.ForeignKey('Partners', help_text="Наименование партнера - Заказчика *", verbose_name="Заказчик")
    date_in = models.DateField(default=timezone.now,
                               help_text="Дата начала *(По умолчанию: устанавливается дата добавления)",
                               verbose_name="Дата начала")
    date_out = models.DateField(help_text="Дата окончания, устанавливается по условию Контракта", verbose_name="Дата окончания *")
    date_closed = models.DateField(null=True, blank=True, help_text="Дата фактического закрытия контракта", verbose_name="Дата закрытия")
    type = models.ForeignKey('ProjectType', help_text="Тип проекта *", verbose_name="Тип проекта")
    status = models.ForeignKey('ProjectStatus', help_text="Статус проекта *", verbose_name="Статус проекта")
    class Meta:
        db_table = "sfx_projects"
        ordering = ["-date_in", "project_name"]
        verbose_name = "Проект/Контракт"
        verbose_name_plural = "Проекты/Контракты"
    def __str__(self):
        return '%s' % (self.project_shortname)

    def data_fields(self):
        return '%s %s %s %s %s' % (self.project_name, self.project_shortname, self.date_in, self.date_out,self.date_closed )
    def get_absolute_url(self):
        return reverse("projects_details",kwargs={"pk":self.pk})

class ProjectsDescriptions(models.Model):
    desc_to_project = models.OneToOneField('Projects')
    description = models.TextField(null=True, blank=True, help_text="Дополнительные свведения или описание", verbose_name="Описание")
    project_summ = models.DecimalField(null=False, default='0.0', max_digits=12, decimal_places=2, help_text="Сумма контракта, без НДС  *", verbose_name="Сумма контракта")
    class Meta:
        db_table = "sfx_projects_descriptions"
        verbose_name = "Раздел - Дополнительное описание"
        verbose_name_plural = ""
    def __str__(self):
        return '%s' % (self.desc_to_project)

class ProjectType(models.Model):
    type = models.CharField(unique=True, max_length=32, verbose_name="Категория\Тип проекта")
    order = models.PositiveSmallIntegerField(default=0, db_index = True, verbose_name = "Порядковый номер")
    class Meta:
        db_table = "sfx_project_type"
        verbose_name = "Категория\Тип Проекта"
        verbose_name_plural = "Категории\Типы Проектов"
    def __str__(self):
        return self.type

class ProjectStatus(models.Model):
    status = models.CharField(unique=True, max_length=32, help_text="Статус проекта *", verbose_name="Статус проекта")
    class Meta:
        db_table = "sfx_project_status"
        verbose_name = "Статус Проекта"
        verbose_name_plural = "Статусы Проектов"
    def __str__(self):
        return self.status

####################################################################

class Orders(models.Model):
    order_name = models.CharField(max_length=255, db_index=True, help_text="Наименование заказы *", verbose_name="Наименование заказа")
    project_name = models.ForeignKey('Projects', help_text="Выбирете наименование Контакта /Проекта/ *", verbose_name="Контракт")
    subcontractor_name = models.ForeignKey('Partners', help_text="Выбирете организацию Исполнителя /Субподрядчика/ *", verbose_name="Исполнитель")
    date_in = models.DateField(default=timezone.now, help_text="Плановая дата начала работ *", verbose_name="Дата начала (план)")
    date_inreal = models.DateField(null=True, blank=True, help_text="Фактическая дата начала работ", verbose_name="Дата начала (факт)")
    date_out = models.DateField(help_text="Плановая дата окончания работ *", verbose_name="Дата окончания (план)")
    date_outreal = models.DateField(null=True, blank=True, help_text="Фактическая дата окончания работ", verbose_name="Дата окончания (факт)")
    date_closed = models.DateField(null=True, blank=True, help_text="Дата закрытия заказа", verbose_name="Дата закрытия")
    type = models.ForeignKey('OrderType', help_text="Тип заказа *", verbose_name="Тип")
    status = models.ForeignKey('OrderStatus', help_text="Статус заказа *", verbose_name="Статус")
    nomenclature = models.ManyToManyField('CatValWork', through="OrderNomenclature", )
    class Meta:
        db_table = "sfx_orders"
        unique_together = ("order_name", "project_name")
        ordering = ["date_in", "date_out"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    def __str__(self):
        return '%s' % (self.order_name)
    def get_absolute_url(self):
        return reverse("orders_details",kwargs={"pk":self.pk})

class OrdersDescription(models.Model):
    desc_to_order = models.OneToOneField('Orders')
    description = models.TextField(null=True, blank=True, help_text="Дополнительные сведения или описание", verbose_name="Описание")
    order_summ = models.DecimalField(null=False, default='0.0', max_digits=12, decimal_places=2, help_text="Сумма заказа, без НДС", verbose_name="Сумма заказа")
    class Meta:
        db_table = "sfx_orders_descriptions"
        verbose_name = "Пункт - Дополнительное описание"
        verbose_name_plural = "Раздел  - Дополнительное описание"
    def __str__(self):
        return '%s' % (self.desc_to_order)

class OrderType(models.Model):
    type = models.CharField(unique=True, max_length=32, help_text="Тип заказа *", verbose_name="Тип")
    class Meta:
        db_table = "sfx_order_type"
        verbose_name = "Тип Заказа"
        verbose_name_plural = "Типы Заказов"
    def __str__(self):
        return self.type

class OrderStatus(models.Model):
    status = models.CharField(unique=True, max_length=32, help_text="Статус заказа *", verbose_name="Статус")
    class Meta:
        db_table = "sfx_order_status"
        verbose_name = "Статус Заказа"
        verbose_name_plural = "Статусы Заказов"
    def __str__(self):
        return self.status

class OrderNomenclature(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE, help_text="Наименование Заказа *", verbose_name="Наименование Заказа")
    val_work = models.ForeignKey('CatValWork', on_delete=models.CASCADE, help_text="Наименование расценки *", verbose_name="Наименование расценки")
    quantity = models.IntegerField(default=1, help_text="Количество единиц", verbose_name="Кол-во ед.")
    class Meta:
        db_table = "sfx_order_nomenclature"
        ordering = ["order", "val_work"]
        unique_together=("order", "val_work")
        verbose_name = "Пункт - Номенклатура Заказа"
        verbose_name_plural = "Раздел - Номенклатура работ выполненных в Заказах"
    def __str__(self):
        return '%s' % (self.order)

####################################################################

class CatValWork(models.Model):
    UNITS = (
        ("ед.", "Единица"),
        ("каб.", "Кабель"),
        ("кам.", "Камера"),
        ("км.", "Киллометр"),
        ("комп.раб.", "Комплекс работ"),
        ("ком.", "Комплект"),
        ("кон.", "Контейнер"),
        ("м.", "Метр"),
        ("об.", "Объект"),
        ("площ.", "Площадка"),
        ("порт", "Порт"),
        ("пр.", "Пролёт"),
        ("пункт", "Пункт"),
        ("сх.", "Схема"),
        ("тчк", "Точка"),
        ("ТУ", "Технические Условия"),
        ("шк.", "Шкаф"),
        ("шт.", "Штук")
        )
    work_num = models.CharField(max_length=8, help_text="Номер п/п *", verbose_name="Номер п/п")
    work_name = models.CharField(db_index=True, max_length=256, help_text="Наименование расценки *", verbose_name="Наименование расценки")
    project_name = models.ForeignKey('Projects')
    work_price = models.DecimalField(default=0.0, max_digits=11, decimal_places=2, help_text="Стоимость работ за единицу, без НДС", verbose_name="Стоимость работ")
    work_pir_price = models.DecimalField(default=0.0, max_digits=11, decimal_places=2, help_text="Стоимость работ за единицу в т.ч. ПИР, без НДС", verbose_name="Стоимость работ с ПИР")
    unit = models.CharField(max_length=16, choices=UNITS, default="ед.", help_text="Единица измерения", verbose_name="Ед. изм.")
    class Meta:
        db_table = "sfx_cat_val_work"
        ordering = ["project_name", "work_num"]
        verbose_name = "Пункт - Позиции расценки работ"
        verbose_name_plural = "Саправочник расценок по Проекту/Контракту"
    def __str__(self):
        return '%s - Расценка № %s - %s' % (self.project_name, self.work_num,self.work_name)

class CatValWorkDescription(models.Model):
    work = models.OneToOneField('CatValWork')
    description = models.TextField(null=True, blank=True, help_text="Дополнительные свведения или описание", verbose_name="Описание")
    class Meta:
        db_table = "sfx_cat_val_work_descriptions"
        verbose_name = "Дополнительное описание "
        verbose_name_plural = "Дополнительные описания"

#
####################################################################
#

class Docs(models.Model):
    doc_name = models.CharField(max_length=128, db_index=True, help_text="Наименование документа *", verbose_name="Наименование документа")
    reg_num = models.CharField(null=True, blank=True, max_length=16, help_text="Рег. номер", verbose_name="Рег. номер")
    doc_data = ContentTypeRestrictedFileField(upload_to="docs2orders/docs", content_types=['application/pdf','application/zip','application/x-rar-compressed','application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'], max_upload_size=10485760, help_text="Типы: PDF, DOC, DOCX, RAR, ZIP. <br>Размер: до 10Мб", verbose_name="Ссылка")
    doc_date = models.DateField(help_text="Дата документа *", verbose_name="Дата документа")
    order_name = models.ForeignKey('Orders', help_text="Наименование Заказа *", verbose_name="Заказ")
    type = models.ForeignKey('DocType', help_text="Тип *", verbose_name="Тип")
    status = models.ForeignKey('DocStatus', help_text="Статус *", verbose_name="Статус")
    status_add = models.ForeignKey('DocStatusAdd', help_text="Источник *", verbose_name="Источник")
    def save(self, *args, **kwargs):
        try:
            this_reacord = Docs.objects.get(id=self.id)
            if this_reacord.doc_data!=self.doc_data:
                this_reacord.doc_data.delete(save=False)
        except:
            pass
        super(Docs, self).save(*args,**kwargs)
    def delete(self, *args, **kwargs):
        self.doc_data.delete(save=False)
        super(Docs, self).delete(*args, **kwargs)
    class Meta:
        db_table = "sfx_docs"
        unique_together = ("doc_name", "reg_num", "order_name")
        ordering = ["order_name", "-doc_date"]
        verbose_name = "Документ"
        verbose_name_plural = "Раздел - Документы добавляемые к Заказу"
    def __str__(self):
        return '%s,%s,%s - (%s, %s) от %s'% (self.doc_name, self.reg_num, self.doc_data, self.type, self.status, self.doc_date)
        #return '%s' % (self.doc_name)

class DocsDescription(models.Model):
    document = models.OneToOneField('Docs')
    description = models.TextField(null=True, blank=True, help_text="Дополнительные свведения или описание", verbose_name="Описание")
    class Meta:
        db_table = "sfx_docs_descriptions"
        verbose_name = "Дополнительное описание"
        verbose_name_plural = "Дополнительные описания"

class DocType(models.Model):
    type = models.CharField(unique=True, max_length=32, help_text="Тип документа *", verbose_name="Тип")
    class Meta:
        db_table = "sfx_doc_type"
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"
    def __str__(self):
            return self.type

class DocStatus(models.Model):
    status = models.CharField(unique=True, max_length=32, help_text="Статус документа *", verbose_name="Статус")
    class Meta:
        db_table = "sfx_doc_status"
        verbose_name = "Статус Документа"
        verbose_name_plural = "Статусы Документов"
    def __str__(self):
        return self.status

class DocStatusAdd(models.Model):
    status_add = models.CharField(unique=True, max_length=32, help_text="Источник документа (тип Контрагента) *", verbose_name="Источник документа")
    class Meta:
        db_table = "sfx_doc_status_add"
        verbose_name = "Источник Документа"
        verbose_name_plural = "Источники Документов"
    def __str__(self):
        return self.status_add

#
####################################################################
#

class Docs4Projects(models.Model):
    doc_name = models.CharField(max_length=128, db_index=True, help_text="Наименование документа *", verbose_name="Наименование документа")
    reg_num = models.CharField(null=True, blank=True, max_length=16, help_text="Рег. номер ", verbose_name="Рег. номер")
    doc_data = ContentTypeRestrictedFileField(upload_to="docs2projects/docs", content_types=['application/pdf','application/zip','application/x-rar-compressed','application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'], max_upload_size=10485760, help_text="Типы: PDF, DOC, DOCX, RAR, ZIP. <br>Размер: до 10Мб", verbose_name="Ссылка")
    doc_date = models.DateField(help_text="Дата документа *", verbose_name="Дата документа")
    project_name = models.ForeignKey('Projects', help_text="Наименование Контракта /Проекта/ *", verbose_name="Проект")
    type = models.ForeignKey('DocType4Projects', help_text="Тип документа *", verbose_name="Тип")
    status = models.ForeignKey('DocStatus4Projects', help_text="Статус документа *", verbose_name="Статус")
    status_add = models.ForeignKey('DocStatusAdd4Projects', help_text="Источник документа *", verbose_name="Источник")
    def save(self, *args, **kwargs):
        try:
            this_reacord = Docs4Projects.objects.get(id=self.id)
            if this_reacord.doc_data!=self.doc_data:
                this_reacord.doc_data.delete(save=False)
        except:
            pass
        super(Docs4Projects, self).save(*args,**kwargs)
    def delete(self, *args, **kwargs):
        self.doc_data.delete(save=False)
        super(Docs4Projects, self).delete(*args, **kwargs)
    class Meta:
        db_table = "sfx_docs_for_projects"
        unique_together = ("doc_name", "reg_num", "project_name")
        ordering = ["project_name", "-doc_date"]
        verbose_name = "Документ"
        verbose_name_plural = "Раздел - Документы добавляемые к Проекту/Контракту"
    def __str__(self):
        return '%s - (%s, %s) от %s'% (self.reg_num, self.type, self.status, self.doc_date)

class DocsDescription4Projects(models.Model):
    document = models.OneToOneField('Docs4Projects')
    description = models.TextField(null=True, blank=True, help_text="Дополнительные свведения или описание", verbose_name="Описание")
    class Meta:
        db_table = "sfx_docs_descriptions_for_projects"
        verbose_name = "Дополнительное описание"
        verbose_name_plural = "Дополнительные описания"

class DocType4Projects(models.Model):
    type = models.CharField(unique=True, max_length=32, help_text="Тип документа *", verbose_name="Тип")
    class Meta:
        db_table = "sfx_doc_type_for_projects"
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"
    def __str__(self):
            return self.type

class DocStatus4Projects(models.Model):
    status = models.CharField(unique=True, max_length=32, help_text="Статус документа *", verbose_name="Статус")
    class Meta:
        db_table = "sfx_doc_status_for_projects"
        verbose_name = "Статус Документа"
        verbose_name_plural = "Статусы Документов"
    def __str__(self):
        return self.status

class DocStatusAdd4Projects(models.Model):
    status_add = models.CharField(unique=True, max_length=32, help_text="Источник документа - указывается тип Контрагента от которого  пришел документ *", verbose_name="Источник документа")
    class Meta:
        db_table = "sfx_doc_status_add_for_projects"
        verbose_name = "Источник Документа"
        verbose_name_plural = "Источники Документов"
    def __str__(self):
        return self.status_add

#
####################################################################
#

class Payments(models.Model):
    #pay_name = models.CharField(default="Операция#"+str(), unique=True, max_length=255, help_text="Наименование платежа *", verbose_name="Наименование")
    pay_date = models.DateField(default=timezone.now, help_text="Дата платежа *", verbose_name="Дата платежа")
    order_name = models.ForeignKey('Orders', help_text="Заказ по которому произведён платеж", verbose_name="Наименование заказ")  #
    intention = models.ForeignKey('PayIntention', help_text="Цель совершения платежа", verbose_name="Цель")
    status = models.ForeignKey('PayStatus', help_text="Статус платежа", verbose_name="Статус")
    class Meta:
        db_table = "sfx_payments"
        ordering = ["-pay_date", "order_name"]
        verbose_name = "Финансовые операции"
        verbose_name_plural = "Финансовые операции"
    def __str__(self):
        return str(self.id)

class PaymentsDescription(models.Model):
    payment = models.OneToOneField('Payments')
    description = models.TextField(null=True, blank=True, help_text="Дополнительные свведения или описание", verbose_name="Описание")
    class Meta:
        db_table = "sfx_payments_descriptions"
        verbose_name = "Дополнительное описание"
        verbose_name_plural = "Дополнительные описания"

class PayDetails(models.Model):
    payment = models.OneToOneField('Payments')
    pay_summ = models.DecimalField(default=0, max_digits=12, decimal_places=2, help_text="Сумма платежа, без НДС  *", verbose_name="Сумма, без НДС")
    #pay_vat_sign = models.BooleanField(default=True, help_text="Включая НДС", verbose_name="Включая НДС")
    pay_vat_size = models.ForeignKey('PayVatSize', null=True, blank=True, help_text="Размер ставки НДС, %", verbose_name="Добавить НДС")
    pay_vat_summ = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2,help_text="Сумма НДС", verbose_name="Сумма НДС")
    pay_total_summ = models.DecimalField(max_digits=13, decimal_places=2, help_text="Общая сумма, в т.ч. НДС", verbose_name="Общая сумма")
    class Meta:
        db_table = "sfx_pay_details"
        verbose_name = "Детали платежа"
        verbose_name_plural = "Раздел - детализация платежей"
    def __str__(self):
        return str(self.payment)

class PayVatSize(models.Model):
    pay_vat_size = models.DecimalField(unique=True, max_digits=3, decimal_places=1, default=18.0, help_text="Размер НДС *", verbose_name="Размер НДС")
    class Meta:
        db_table = "sfx_pay_vat_size"
        verbose_name = "Размер НДС"
        verbose_name_plural = "Размер НДС"
    def __str__(self):
        return str(self.pay_vat_size)

class PayIntention(models.Model):
    intention = models.CharField(unique=True, max_length=32, help_text="Намерения или цель платежа *", verbose_name="Цель платежа")
    pay_type = models.ForeignKey('PayType')
    class Meta:
        db_table = "sfx_pay_intention"
        verbose_name = "Намерения или цели платежа"
        verbose_name_plural = "Намерения или цели платежей"
    def __str__(self):
        return self.intention

class PayType(models.Model):
    type = models.CharField(unique=True, max_length=32, help_text="Тип платежа *", verbose_name="Тип")
    class Meta:
        db_table = "sfx_pay_type"
        verbose_name = "Тип платежа"
        verbose_name_plural = "Типы платежей"
    def __str__(self):
        return self.type

class PayStatus(models.Model):
    status = models.CharField(unique=True, max_length=32, help_text="Статус платежа *", verbose_name="Статус")
    class Meta:
        db_table = "sfx_pay_status"
        verbose_name = "Статус платежа"
        verbose_name_plural = "Статусы платежей"
    def __str__(self):
        return self.status

####################################################################

####################################################################
#

class Docs4Payments(models.Model):
    doc_name = models.CharField(max_length=128, db_index=True, help_text="Наименование документа *", verbose_name="Наименование документа")
    reg_num = models.CharField(null=True, blank=True, max_length=16, help_text="Рег. номер ", verbose_name="Рег. номер")
    doc_data = ContentTypeRestrictedFileField(upload_to="docs2payments/docs", content_types=['application/pdf','application/zip','application/x-rar-compressed','application/vnd.ms-excel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'], max_upload_size=2621440, help_text="Типы: PDF, XLS, XLSX, RAR, ZIP. <br>Размер: до 2,5Мб", verbose_name="Ссылка")
    doc_date = models.DateField(help_text="Дата документа *", verbose_name="Дата документа")
    payment_name = models.ForeignKey('Payments', help_text="Наименование операции *", verbose_name="Операция")
    type = models.ForeignKey('DocType4Payments', help_text="Тип документа *", verbose_name="Тип")
    status = models.ForeignKey('DocStatus4Payments', help_text="Статус документа *", verbose_name="Статус")
    status_add = models.ForeignKey('DocStatusAdd4Payments', help_text="Источник документа *", verbose_name="Источник")
    def save(self, *args, **kwargs):
        try:
            this_reacord = Docs4Payments.objects.get(id=self.id)
            if this_reacord.doc_data!=self.doc_data:
                this_reacord.doc_data.delete(save=False)
        except:
            pass
        super(Docs4Payments, self).save(*args,**kwargs)
    def delete(self, *args, **kwargs):
        self.doc_data.delete(save=False)
        super(Docs4Payments, self).delete(*args, **kwargs)
    class Meta:
        db_table = "sfx_docs_for_payments"
        unique_together = ("doc_name", "payment_name")
        ordering = ["payment_name", "-doc_date"]
        verbose_name = "Документ"
        verbose_name_plural = "Раздел - Документы добавляемые к Фин. операции"
    def __str__(self):
        return '%s - (%s, %s) от %s'% (self.reg_num, self.type, self.status, self.doc_date)

class DocsDescription4Payments(models.Model):
    document = models.OneToOneField('Docs4Payments')
    description = models.TextField(null=True, blank=True, help_text="Дополнительные свведения или описание", verbose_name="Описание")
    class Meta:
        db_table = "sfx_docs_descriptions_for_payments"
        verbose_name = "Дополнительное описание"
        verbose_name_plural = "Дополнительные описания"

class DocType4Payments(models.Model):
    type = models.CharField(unique=True, max_length=32, help_text="Тип документа *", verbose_name="Тип")
    class Meta:
        db_table = "sfx_doc_type_for_payments"
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"
    def __str__(self):
            return self.type

class DocStatus4Payments(models.Model):
    status = models.CharField(unique=True, max_length=32, help_text="Статус документа *", verbose_name="Статус")
    class Meta:
        db_table = "sfx_doc_status_for_payments"
        verbose_name = "Статус Документа"
        verbose_name_plural = "Статусы Документов"
    def __str__(self):
        return self.status

class DocStatusAdd4Payments(models.Model):
    status_add = models.CharField(unique=True, max_length=32, help_text="Источник документа - указывается тип Контрагента от которого  пришел документ *", verbose_name="Источник документа")
    class Meta:
        db_table = "sfx_doc_status_add_for_payments"
        verbose_name = "Источник Документа"
        verbose_name_plural = "Источники Документов"
    def __str__(self):
        return self.status_add

#
####################################################################