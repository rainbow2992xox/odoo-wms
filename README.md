### 一、项目文件说明

内网gitlab账号：gyodoo 密码：gyodoo2023 <br>
内网项目地址：http://172.16.10.172:9091/guoyaolgh/LogisticsManagementSystem <br>
已在服务器上绑定账号，之后代码更新直接使用git命令即可 <br>


#### 项目目录说明：

- 服务器odoo部署目录：<br>
/opt/odoo-wms 正式环境 <br>
/opt/odoo-test 测试环境 

- 服务器java服务部署目录： <br>
/home/reagent <br>

- 项目目录说明：<br>
  + .bin 启动脚本 （start.sh为正式环境，test.sh为测试环境，正式环境脚本已绑定至supervisor配置）<br>
  + java java项目文件目录
    + sync-0.0.1-SNAPSHOT.jar 封装了市局上传接口供Odoo项目调用 <br>
    + application_pro.yml  生产配置文件 <br> 
    + application_test.yml 测试配置文件 <br>
    + start_pro.sh  生产启动脚本 已绑定至supervisor配置<br> 
    + start_test.sh 配置启动脚本 <br>
  + .env 本地python环境（已弃用目前使用的是本地conda的python环境） <br>
  + .filestore 本地odoo缓存数据库文件 （重要勿动！！ 若要迁移服务器需要一并迁移）<br>
  + .local 本地odoo插件其中wms即为危化数据上传相关项目代码 <br>
  + .logs 日志文件 <br>
  + .src odoo安装目录（该目录是odoo源码，未上传至github） <br>
  + .odoo-pro.cfg 生产odoo启动配置文件 <br>
  + .odoo-uat.cfg 测试odoo启动配置文件 <br>
  + .README.md 说明文档 <br>
  + .requirement.txt pip依赖包清单文件

- 项目代码说明：<br>
.local/wms 危化数据上传相关项目只需关注其中两个文件夹
    - models 包含所有模型逻辑
      + api_log.py  
        所有接口上传逻辑，在odoo定时任务配置中会直接调用该模型的call方法，通过传入不同关键词来调用不同上传接口。所有数据除了车辆进出记录为人为填写，其余数据均通过sql查询获得。获取数据会优先去重插入Odoo数据库，然后校验数据是否满足上传条件，满足则调用JAVA接口上传数据。
      + in_stock.py 入库模型文件
      + merchandise.py 货品模型文件
      + move_stokc 移库模型文件
      + out_stock 出库模型文件
      + stock 库存模型文件
      + vehicle 危化车辆进出入记录
      + vehicle_nor 普通车辆进出入记录
      + vistor 访客模型文件
      + warehouse_area 仓储空间文件     
    - views 所有页面xml
      + api_log.xml API调用日志页面
      + in_stock.xml 入库记录页面
      + move_stock.xml 移库记录页面
      + out_stock.xml  出库记录页面
      + stock.xml  库存页面
      + vehicle_nor.xml 访客出入记录、访客出厂管理
      + vehicle.xml  危险车辆出入记录、危险车辆出厂管理

#### java项目说明：
- 服务器odoo部署目录：/home/reagent <br>
- 项目文件说明：<br>
  sync-0.0.1-SNAPSHOT.jar 封装了市局上传接口供Odoo项目调用 <br>
  application_pro.yml  生产配置文件 <br> 
  application_test.yml 测试配置文件 <br>
  start_pro.sh  生产启动脚本 已绑定至supervisor配置<br> 
  start_test.sh 配置启动脚本 <br>

### 二、部署说明

#### Supervisor

目前项目是使用supervisor来守护进程，supervisor的配置文件：/etc/supervisor/supervisord.conf <br>
    
    ; supervisor config file
    
    [unix_http_server]
    file=/var/run/supervisor.sock   ; (the path to the socket file)
    chmod=0700                       ; sockef file mode (default 0700)
    
    [supervisord]
    user = root ;
    logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
    pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
    childlogdir=/var/log/supervisor            ; ('AUTO' child log dir, default $TEMP)
    
    ; the below section must remain in the config file for RPC
    ; (supervisorctl/web interface) to work, additional interfaces may be
    ; added by defining them in separate rpcinterface: sections
    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
    
    [supervisorctl]
    serverurl=unix:///var/run/supervisor.sock ; use a unix:// URL  for a unix socket
    
    ; The [include] section can just contain the "files" setting.  This
    ; setting can list multiple files (separated by whitespace or
    ; newlines).  It can also contain wildcards.  The filenames are
    ; interpreted as relative to this file.  Included files *cannot*
    ; include files themselves.
    
    #以上为默认配置无需调整
    
    [include]
    files = /etc/supervisor/conf.d/*.conf  #所有守护的服务配置文件地址，目前之配置了odoo.conf
    
    
    #网页版supervisor配置
    
    [inet_http_server]         ; inet (TCP) server disabled by default
    port=*:8888        ; (ip_address:port specifier, *:port for all iface)
    username=admin             ; (default is no username (open server))
    password=123               ; (default is no password (open server))


supervisor的odoo应用配置文件：/etc/supervisor/conf.d/odoo.conf 

    [program:odoo.Server]
    directory = /opt/odoo-wms/src/odoo/ #odoo项目地址
    command = sh /opt/odoo-wms/bin/start.sh  #odoo项目启动脚本位置
    #以下为标准配置无需调整
    user = root
    numprocs = 1
    stopsignal = QUIT
    autostart = true
    autorestart = true
    stopasgroup = true
    ikillasgroup = true
    startsecs=60
    
    #日志地址配置
    stdout_logfile = /var/log/odoo/odoo-15.log
    stderr_logfile = /var/log/odoo/odoo-15.error.log


代码更新步骤： <br>
1、修改代码push至gitlab<br>
2、登录服务器进入/opt/odoo-wms <br>
3、使用git pull同步最新代码 <br>
4、登录http://10.3.0.150:8888/  admin/123  点击restart重启所有服务即可 <br>

### 三、定时任务说明

目前所有上传接口均采用Odoo定时任务调度，具体配置方法如下： 

1、admin账号登录 <br>
2、左上角点击菜单选择设置 <br>
3、设置页面下滑到最后，点击激活开发者模式 <br>
4、完成第3步，右上角会出现一个debug按钮，点击打开菜单选择"成为超级用户"  <br>
5、再次点击设置-技术-安排的动作 <br>
6、每个请求都有单独动作，可以设置定期执行时间是否重试等，也可以手动单独执行
