# 通过CGI将大华相机叠加入指定OSD

本项目通过修改CGI方法，将数据动态叠加入相机OSD中，可随时更换相机OSD中叠加数据，或相机OSD进行清除。



## 本项目功能描述

客户为某地医保局，当某药店客户使用医保卡购买药品并结算后生成一笔结算数据。

程序通过定时向第三方接口请求获取当前数据，并将这些数据叠加入对应药店相机通道的OSD中，展示数秒钟。

在展示时间结束后，对这些相机OSD通道置空。



## 特点

通过CGI方式修改OSD，该方式适用于几乎*所有大华相机*。



## 不足

测试发现大华相机叠加OSD换行方式有两种，一种为使用“|” 符号分割每一行，一种为使用“\n”（提交请求时URL编码为 %0A ）来分割每一行。

当提交OSD为:



aaa|bbb|ccc

ddd

eee

### 第一种分割显示情况

如果相机使用第一种方法分割，则OSD展示内容为：

aaa 

bbb

ccc  

即只展示第一行按竖线分割后的结果。

### 第二种分割方法显示情况

如果相机使用第二种分割方法，则OSD展示内容为：

aaa|bbb|ccc

ddd

eee

即全部展示。















 

