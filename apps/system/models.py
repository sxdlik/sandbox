from django.db import models
from django.contrib.auth.models import AbstractUser


class Menu(models.Model):
    """ 菜单 """
    name = models.CharField(max_length=30, unique=True, verbose_name='菜单名')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name='上级菜单')
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='图标')
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name='编码')
    url = models.CharField(max_length=128, unique=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name

    @classmethod
    def get_menu_by_request_url(cls, url):
        return dict(menu=Menu.objects.get(url=url))


class Role(models.Model):
    """ 角色权限 """
    name = models.CharField(max_length=32, unique=True, verbose_name='角色')
    permissions = models.ManyToManyField("Menu", blank=True, verbose_name='URL授权')
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name='描述')


class Structure(models.Model):
    """ 组织架构 """
    type_choices = (("center", "中心"), ("department", "部门"))
    name = models.CharField(max_length=60, verbose_name='名称')
    type = models.CharField(max_length=20, choices=type_choices, default='department', verbose_name='类型')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name='上级部门')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '组织架构'
        verbose_name_plural = verbose_name


class UserProfile(AbstractUser):
    """ 用户表 """
    name = models.CharField(max_length=20, default='', verbose_name='姓名')
    id_card = models.CharField(max_length=18, null=True, blank=True, verbose_name='身份证')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    gender = models.CharField(max_length=10, verbose_name='性别')
    mobile1 = models.CharField(max_length=11, default='', verbose_name='手机号码')
    mobile2 = models.CharField(max_length=11, default='', verbose_name='紧急联系号码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.jpg',
                              max_length=100, null=True, blank=True)
    department = models.ForeignKey("Structure", null=True, blank=True, on_delete=models.SET_NULL, verbose_name='部门')
    post = models.CharField(max_length=50, null=True, blank=True, verbose_name='职位')
    superior = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name='上级主管')
    roles = models.ManyToManyField("Role", verbose_name='角色', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['id']
