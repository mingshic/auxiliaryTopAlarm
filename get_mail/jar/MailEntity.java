package com.wbm.dcnotes;

public class MailEntity {
    private String universalID;
    private String noteId;
    private String from;
    private String sendto;
    private String subject;
    private String body;
    private String created;

    MailEntity() {
    }

    public MailEntity(String universalID, String noteId, String from, String sendto, String subject, String body, String created) {
        this.universalID = universalID;
        this.noteId = noteId;
        this.from = from;
        this.sendto = sendto;
        this.subject = subject;
        this.body = body;
        this.created = created;
    }

    public String getUniversalID() {
        return universalID;
    }

    public void setUniversalID(String universalID) {
        this.universalID = universalID;
    }

    public String getNoteId() {
        return noteId;
    }

    public void setNoteId(String noteId) {
        this.noteId = noteId;
    }

    public String getFrom() {
        return from;
    }

    public void setFrom(String from) {
        this.from = from;
    }

    public String getSendto() {
        return sendto;
    }

    public void setSendto(String sendto) {
        this.sendto = sendto;
    }

    public String getSubject() {
        return subject;
    }

    public void setSubject(String subject) {
        this.subject = subject;
    }

    public String getBody() {
        return body;
    }

    public void setBody(String body) {
        this.body = body;
    }

    public String getCreated() {
        return created;
    }

    public void setCreated(String created) {
        this.created = created;
    }

    @Override
    public String toString() {
        return "MailEntity{" +
                "universalID='" + universalID + '\'' +
                ", noteId='" + noteId + '\'' +
                ", from='" + from + '\'' +
                ", sendto='" + sendto + '\'' +
                ", subject='" + subject + '\'' +
                ", body='" + body + '\'' +
                ", created=" + created +
                '}';
    }
}