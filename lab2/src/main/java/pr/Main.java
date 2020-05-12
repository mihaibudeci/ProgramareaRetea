package pr;


public class Main {
    public static void main(String[] args) {

        String host = "pop.gmail.com";
        String mailStoreType = "pop3";
        String username = "utmstudentac";
        String password = "UtmStudentTI171";
        EmailUtil.check(host, mailStoreType, username, password);
        System.out.println("Sending email...");
        EmailUtil.send(username, password, "alexandru.ketroy@gmail.com", "Programarea in retea", "Email trimis");

    }
}
