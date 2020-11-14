public class Program {

    /**
     * @param args
     */
    public static void main(String[] args) {
        int portNumber = 27017;
        if (args.length == 2) {
            portNumber = Integer.parseInt(args[1]);
        }

        Database db = new Database(portNumber);
    }
}

