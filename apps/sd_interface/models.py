from django.db import models

# Create your models here.
class SD_Host(models.Model):
    ip = models.CharField(max_length=16, verbose_name="sd服务主机ip",primary_key=True, null=False, default='fang')
    port = models.CharField(max_length=16, verbose_name="sd服务主机port",null=True)
    status = models.IntegerField(verbose_name="0：关闭，1: 开启", default=0)

    class Meta:
        verbose_name = "sd主机信息"
        verbose_name_plural = verbose_name
        db_table = "sd_host"


class SD_Task_Process(models.Model):
    ip = models.CharField(max_length=16, verbose_name="sd服务主机ip", null=True, default='ip')
    port = models.CharField(max_length=16, verbose_name="sd服务主机port",null=True)
    rqbody = models.TextField(blank=True, null=False, verbose_name="请求体")
    service_type = models.IntegerField(verbose_name="0：txt2img，1: img2img", default=0)
    is_optimize = models.IntegerField(verbose_name="0：不优化权重参数，1: 优化权重参数", default=0)
    task_id = models.CharField(max_length=55, verbose_name="task_id",null=False)
    status = models.IntegerField(verbose_name="0：关闭，1: 开启", default=0)
    pic_description = models.TextField(blank=True, null=True, verbose_name="图片信息")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")


    class Meta:
        verbose_name = "sd处理过程数据"
        verbose_name_plural = verbose_name
        db_table = "sd_task_process"