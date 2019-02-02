package com.wbm.dcnotes;

import com.alibaba.fastjson.JSONObject;
import lotus.domino.*;
import net.sf.json.JSONArray;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.LinkedList;
import java.util.List;

public class DcNotesManager {
    private static String dominoServerName = "10.0.2.116";
    private static String dominoUserName = "service_request";
    private static String dominoPassword = "";

    public static void main(String[] args) {
        System.out.println(
            new DcNotesManager().receive(
                    "{'accesstime': '2018-09-20 04:45:13', " +
                            "'id': '810C5BCDDBE022470483B7C0105BDC1A', " +
                            "'appsecret': '5BC5A7424F929FF8F57B112951AE16A3', " +
                            "'appid': 'dcitsMonitor'}")
        );
    }

    /**
     * 收取Notes邮件
     *
     * @param jsonStr
     * json：{
     *      appid：不可空，dcitsMonitor,
     *      accesstime：不可空，访问时间，格式（yyyy-MM-dd HH:mm:ss）,
     *      appsecret：不可空，加密串，加密方法（md5(appkey+accesstime)）,
     *      serverName：可空，默认(10.0.2.116)，邮件服务器地址,
     *      itcode：可空，默认(service_request)，用户名,
     *      itPassword：可空，用户密码,
     *      universalID：可空，空则查询所有邮件
     *
     *
     * }
     * @return
     * json:[
     *     成功：{code:200,data:xxx}
     *     失败：{code:10,message:xxx}
     * ]
     */
    public String run(String str){
        return str;
    }
    public String receive(String jsonStr){
        JSONObject returnJson = new JSONObject();
        JSONObject json = JSONObject.parseObject(jsonStr);

        String appkey = "52023eec8ad5516bab1c6bd2992be660";//后期根据appid从系统中读取

        String appid = json == null ? null : json.getString("appid");//dcitsMonitor
        String accesstime = json == null ? null : json.getString("accesstime");//yyyy-MM-dd HH:mm:ss
        String appsecret = json == null ? null : json.getString("appsecret");//md5(appkey+accesstime)

        String serverName = json == null ? null : json.getString("serverName");
        String itcode = json == null ? null : json.getString("itcode");
        String itPassword = json == null ? null : json.getString("itPassword");
        String universalID = json == null ? null : json.getString("universalID");

        if(isBlank(appid) || isBlank(accesstime) || isBlank(appsecret)){
            returnJson.put("code", 10);
            returnJson.put("message", "失败，appid、accessTime、appsecret都不能为空");
            return returnJson.toJSONString();
        }

        if(!appsecret.equals(MD5Util.md5(appkey+accesstime))){
            returnJson.put("code", 10);
            returnJson.put("message", "失败，appsecret校验不正确");
            return returnJson.toJSONString();
        }

        if (!isBlank(serverName) && !isBlank(itcode) && !isBlank(itPassword)) {
            dominoServerName = serverName;
            dominoUserName = itcode;
            dominoPassword = itPassword;
        }else if (!isBlank(serverName) && !isBlank(itcode)) {
            dominoServerName = serverName;
            dominoUserName = itcode;
        }
        
        if(isBlank(dominoServerName)){
            returnJson.put("code", 10);
            returnJson.put("message", "失败，dominoServerName不能为空");
            return returnJson.toJSONString();
        }
        if(isBlank(dominoUserName)){
            returnJson.put("code", 10);
            returnJson.put("message", "失败，dominoUserName不能为空");
            return returnJson.toJSONString();
        }

        List<MailEntity> list = receiveLastMail(universalID);

        if(list != null) {
            JSONArray jsonArray = JSONArray.fromObject(list);
            returnJson.put("code",200);
            returnJson.put("data",jsonArray);
        }else{
            returnJson.put("code", 10);
            returnJson.put("message", "失败，查询数据为空");
        }

        System.out.println("返回数据:"+returnJson.toJSONString());
        return returnJson.toJSONString();
    }

    private List<MailEntity> receiveLastMail(String universalID) {
        List<MailEntity> mailEntities = new LinkedList<>();
        Session session = null;
        Database database = null;
        View view = null;
        Document doc = null;

        try {
            if(dominoPassword != null && dominoPassword.trim() != "") {
                session = NotesFactory.createSession(dominoServerName, dominoUserName, dominoPassword);
            }else {
                session = NotesFactory.createSession(dominoServerName);
            }

            database = session.getDatabase(session.getServerName(), "mail//" + dominoUserName + ".nsf", false);

            if (database != null) {
                view = database.getView("($Inbox)");
                doc = view.getLastDocument();

                while (doc != null && doc.hasItem("Form")) {
                    String unid = doc.getUniversalID();

                    //中断跳出
                    if (universalID != null && universalID.trim() != "" && universalID.equals(unid)) {
                        break;
                    }
                    System.out.println(doc.getItemValueString("Subject")+":返回数据:"+unid);

                    String noteID = doc.getNoteID();
                    String from = doc.getItemValueString("From");
                    String sendto = doc.getItemValueString("Sendto");
                    String subject = doc.getItemValueString("Subject");
                    String body = doc.getItemValueString("Body");
                    DateTime created = doc.getCreated();
                    String createStr = "";
                    if(created != null){
                        DateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                        createStr = sdf.format(created.toJavaDate());
                    }

                    mailEntities.add(new MailEntity(universalID,noteID,from,sendto,subject,body,createStr));
                    doc = view.getPrevDocument(doc);
                }
            } else {
                System.out.println("cannot open " + dominoUserName + "'s database");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
            System.out.println(ex.getMessage());
        } finally {
            if (doc != null) {
                try {
                    doc.recycle();
                } catch (NotesException e) {
                    e.printStackTrace();
                    System.out.println(e.getMessage());
                }
            }
            if (view != null) {
                try {
                    view.recycle();
                } catch (NotesException e) {
                    e.printStackTrace();
                    System.out.println(e.getMessage());
                }
            }
            if (database != null) {
                try {
                    database.recycle();
                } catch (NotesException e) {
                    e.printStackTrace();
                    System.out.println(e.getMessage());
                }
            }
            if (session != null) {
                try {
                    session.recycle();
                } catch (NotesException e) {
                    e.printStackTrace();
                    System.out.println(e.getMessage());
                }
            }
        }
//        System.out.println(mailEntities);

        return mailEntities;
    }

    private boolean isBlank(CharSequence cs) {
        int strLen;
        if (cs != null && (strLen = cs.length()) != 0) {
            for(int i = 0; i < strLen; ++i) {
                if (!Character.isWhitespace(cs.charAt(i))) {
                    return false;
                }
            }

            return true;
        } else {
            return true;
        }
    }

}
