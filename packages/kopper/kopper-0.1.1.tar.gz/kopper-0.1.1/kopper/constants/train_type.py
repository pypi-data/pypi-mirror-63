import enum


class TRAIN_TYPE(enum.Enum):
    KTX = '00'
    새마을호 = '01'
    무궁화호 = '02'
    통근열차 = '03'
    누리로 = '04'
    전체 = '05'
    공학직통 = '06'
    KTX_산천 = '07'
    ITX_새마을 = '08'
    ITX_청춘 = ('09', '10')
