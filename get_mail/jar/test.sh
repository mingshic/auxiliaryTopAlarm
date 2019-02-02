javac DcNotesManager.java
cp -rp DcNotesManager.class com/wbm/dcnotes/
rm -rf dc.jar
jar cvf dc.jar *
