# Конструктор сотрудника

class Employee:
    
    # Задать первичные данные справочника сотрудников
    def set_first(self, data):
        self.__first_name = data

    def set_last(self, data):
        self.__last_name = data

    def set_middle(self, data):
        self.__middle_name = data

    def set_SNILS(self, data):
        self.__SNILS = data

    # Получить информацию о сотрудниках
    def get_first(self):
        return self.__first_name

    def get_last(self):
        return self.__last_name

    def get_middle(self):
        return self.__middle_name

    def get_SNILS(self):
        return self.__SNILS
    
    # Дефолтный флаг пустоты
    def __str__(self):
        return self.__SNILS

# Данные для передачи
class SendingData:
    
    # Задать данные о выполненных работах
    # Допустимые значения
    # 1 - Пригоден
    # 2 - Непригоден
    def set_ResultVerificationIdType(self, ResultVerificationIdType):
        self.ResultVerificationIdType = ResultVerificationIdType

    # Заадть метод сохранения
    # 1 - Черновик
    # 2 - Отправлено
    def set_TypeSaveMethod(self, TypeSaveMethod):
        self.TypeSaveMethod = TypeSaveMethod
        
    def set_SNILS(self, SNILS):
        self.SNILS = SNILS

    def set_NameType(self, NameType):
        self.NameType = NameType

    def set_Last(self, Last):
        self.Last = Last

    def set_First(self, First):
        self.First = First

    def set_Middle(self, Middle):
        self.Middle = Middle

    def set_VerificationMesuringInstrument(self, VerificationMesuringInstrument):
        self.VerificationMesuringInstrument = VerificationMesuringInstrument

    def set_NumberVerification(self, NumberVerification):
        self.NumberVerification = NumberVerification

    def set_DateVerification(self, DateVerification):
        self.DateVerification = DateVerification

    def set_DateEndVerification(self, DateEndVerification):
        self.DateEndVerification = DateEndVerification

    def set_TypeMeasuringInstrument(self, TypeMeasuringInstrument):
        self.TypeMeasuringInstrument = TypeMeasuringInstrument

    def set_FullNumberVerification(self, FullNumberVerification):
        self.FullNumberVerification = FullNumberVerification

    # Получить данные о проведённых работах
    def get_ResultVerificationIdType(self):
        return self.ResultVerificationIdType

    def get_TypeSaveMethod(self):
        return self.TypeSaveMethod
        
    def get_SNILS(self):
        return self.SNILS

    def get_NameType(self):
        return self.NameType

    def get_Last(self):
        return self.Last

    def get_First(self):
        return self.First

    def get_Middle(self):
        return self.Middle

    def get_VerificationMesuringInstrument(self):
        return self.VerificationMesuringInstrument

    def get_NumberVerification(self):
        return self.NumberVerification

    def get_DateVerification(self):
        return self.DateVerification

    def get_DateEndVerification(self):
        return self.DateEndVerification

    def get_TypeMeasuringInstrument(self):
        return self.TypeMeasuringInstrument

    def get_FullNumberVerification(self):
        return self.FullNumberVerification
