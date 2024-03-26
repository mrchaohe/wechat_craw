from django.db import models


class MyAccount(models.Model):
    """自身公众号"""


    id = models.AutoField(primary_key=True,help_text="公众号id")
    name = models.CharField(max_length=32,help_text="公众号名称")
    cookie = models.TextField(help_text="公众号cookie")
    token = models.CharField(max_length=32,help_text="公众号token")
    isactivate = models.IntegerField( default=0, help_text="是否作为当前爬取公号,0 不激活 1激活， 默认0")

    # def save(self, *args, **kwargs):
    #     if not self.isactivate==1:
    #         pass
    #         # todo 其他 为0
    #     super(Account, self).save(*args, **kwargs)


    class Meta:
        verbose_name = "my_account"


class Account(models.Model):
    """爬取公众号"""
    id = models.AutoField(primary_key=True,help_text="公众号id")
    fake_id = models.CharField(max_length=32,default="",help_text="公众号唯一标识，系统给定")
    name = models.CharField(max_length=32,help_text="公众号名称")
    create_time = models.DateField(auto_now=True, help_text="在系统添加时间")
    
    def save(self, *args, **kwargs):
        if not self.fake_id:
            from req.wechat import Wechat
            myac = MyAccount.objects.get(isactivate=1)
            wc = Wechat()
            fackid = wc.get_fakeid(myac.token, myac.cookie, self.name)
            self.fake_id = fackid
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "account"