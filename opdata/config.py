#!/usr/bin/env python


mailaccount = "auto_its_toponline+service_request=dcits.com@163.com"

Analysis_smart_field = {'客户名称': 'mailCustomerName','监控系统名称': 'mailMonitorName','服务对象': 'serviceObject', '维护人员': 'maUser', '型号': 'mailModelName', '告警内容描述': 'mailAlertContent', '维护人员手机': 'maMobile', '监控系统版本': 'mailMonitorVersion', 'KPI名称': 'kpiName', '告警发生时间': 'alertTime', '服务名': 'serviceName', 'KPI分类': 'kpiAssortment', '业务系统': 'businessSystem', 'email': 'email', 'identityCode': 'identityCode', '维护部门': 'maDept', 'KPI值': 'kpiValue', '序列号': 'mailSn', '所在城市': 'mailCity', '厂商': 'mailFactoryName', 'IP': 'mailIp', '维护人员邮箱': 'maEmail'}

#'所在城市': 'city'

To_top_field = ['reqAlertLevel','reqAlertTitle','reqAlertContent','reqAlertFrom','repDeviceName','reqBadParts','repCity','repSn','reqAnalysisId','repCustId','repCustName','repProjectName','repProjectId','repFactoryName','repModelName']


#Top_relate_field = ['设备标识']

Analysis_field_mail = ['客户名称', '监控系统名称', '监控系统版本', 'KPI名称', 'KPI值', '告警内容描述', 'IP', '机器名/设备名/数据库名', '服务名', '厂商', '型号', '序列号', '业务系统', '维护部门', '维护人员', '维护人员手机', '维护人员邮箱']


to_top_data_field = ["info_id","receive_info_id","customer_code","monitor_code","monitor_version","identity_code","kpi_assortment","kpi_name","kpi_value","alert_content","ip","alert_time","service_object","service_name","factory_name","model_name","sn","city","business_system","ma_dept","ma_user","ma_mobile","ma_email","analysised_time","auto_create_flg","in_service_flg","deal_status","create_on","modified_on","id","cust_system_code","customer_code","customer_name","monitor_code","monitor_name","monitor_version","address","parameter","remark","active_flg","create_by","create_on","modified_by","modified_on"]

