from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

CITIES = (
    ('new_taipei_city', 'New Taipei City'),
    ('taipei_city', 'Taipei City'),
)

DISTRICTS = (
    ('beitou', 'Beitou'),
    ('daan', 'Daan'),
    ('datong', 'Datong'),
    ('nangang', 'Nangang'),
    ('neihu', 'Neihu'),
    ('shilin', 'Shilin'),
    ('songshan', 'Songshan'),
    ('wanhua', 'Wanhua'),
    ('wenshan', 'Wenshan'),
    ('xinyi', 'Xinyi'),
    ('zhongshang', 'Zhongshan'),
    ('zhongzheng', 'Zhongzheng'),
    ('banqiao', 'Banqiao'),
    ('zhonghe', 'Zhonghe'),
    ('yonghe', 'Yonghe'),
    ('tucheng', 'Tucheng'),
    ('shulin', 'Shulin'),
    ('sanxia', 'Sanxia'),
    ('yingge', 'Yingge'),
    ('xinzhuang', 'Xinzhuang'),
    ('sanchong', 'Sanchong'),
    ('luzhou', 'Luzhou'),
    ('wugu', 'Wugu'),
    ('taishan', 'Taishan'),
    ('linkou', 'Linkou'),
    ('tamsui', 'Tamsui'),
    ('bali', 'Bali'),
    ('sanzhi', 'Sanzhi'),
    ('shimen', 'Shimen'),
    ('jinshan', 'Jinshan'),
    ('wanli', 'Wanli'),
    ('xizhi', 'Xinzhi'),
    ('ruifang', 'Ruifang'),
    ('gongliao', 'Gongliao'),
    ('pinxi', 'Pinxi'),
    ('shangxi', 'Shuangxi'),
    ('xindian', 'Xindian'),
    ('shenkeng', 'Shenkeng'),
    ('shiding', 'Shiding'),
    ('pinglin', 'Pinglin'),
    ('wulai', 'Wulai'),
    ('other', 'Other'),
)

class ClassLocation(models.Model):
    location_name = models.CharField(max_length=200)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120)
    classroom = models.CharField(max_length=10, default='', null=True, blank=True)
    district = models.CharField(max_length=120, choices=DISTRICTS)
    city = models.CharField(max_length=120, choices=CITIES)
    contact_name = models.CharField(max_length=120, null=True, blank=True)
    contact_phone = models.CharField(max_length=10, null=True, blank=True, validators=[
        RegexValidator(regex='^\d{10}$', message='Length has to be 10', code='Invalid number')])
    contact_phone_extension = models.CharField(max_length=5, null=True, blank=True)
    other_information = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return "{}  {}".format(self.location_name, self.classroom)
        #return self.location_name