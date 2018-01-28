# Django开发的教学网站

### 预览图

![](https://s1.ax1x.com/2018/01/28/pvX7RS.png)

> 关于配置：
在路径iMooc_django/iMooc/config中, 可以详细修改你的配置脚本
*   settings_db.py 数据库配置
*   settings_local.py 开发配置
*   settings_product.py 生产环境配置

> 关于安装：

#### 安装现代人类使用包管理工具pipenv
```shell
#pip install pipenv -i https://pypi.douban.com/simple
```
#### 进入目录
```shell
#cd iMooc_django

```
#### 使用pipenv安装依赖
```python
pipenv install
```
#### 生成数据库迁移文件
```python
python manage.py migrate
```
#### 启动项目
```python
python manage.py runserver 0:8080
```

(访问浏览器localhost:8080端口可以查看)

> 关于部署：

可以参考 ![自强学堂Django部署Nginx](https://code.ziqiangxuetang.com/django/django-nginx-deploy.html)
