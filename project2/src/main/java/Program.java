import com.mongodb.*;
import com.mongodb.util.JSON;
import java.io.*;
import java.nio.charset.StandardCharsets;
import org.json.simple.parser.JSONParser;
import com.google.common.io.Files;

public class Program {

    /**
     * @param args
     */
    public static void main(String[] args) {
        int portNumber = 0;
        if (args.length > 2) {
            portNumber = Integer.parseInt(args[1]);
        }

        MongoClientURI mongoClientURI = new MongoClientURI(String.format("mongodb://localhost:%o", portNumber));
        MongoClient mongoClient;
        try {
            // todo: singleton
            mongoClient = new MongoClient(mongoClientURI);

            // create a database named 291db (if it does not exist)
            DB db = mongoClient.getDB("291db");
            JSONParser parser = new JSONParser();
            // create three collections named: Posts, Tags, Votes
            // if collections exist, drop and create new collections

            DBCollection posts = db.getCollection("Posts");
            File postsFile = new File("./Posts.json");
            String postsString = Files.asCharSource(postsFile, StandardCharsets.UTF_8).toString();
            DBObject postsObj = (DBObject) JSON.parse(postsString);
            posts.insert(postsObj);

            DBCollection tags = db.getCollection("Tags");
            try (Reader tagsReader = new FileReader("./Tags.json")) {

                DBObject tagsObj = (DBObject) JSON.parse("");
                tags.insert(tagsObj);
            } catch (IOException e) {
                e.printStackTrace();
            }

            DBCollection votes = db.getCollection("Votes");
            try (Reader votesReader = new FileReader("./Votes.json")) {
                DBObject votesObj = (DBObject) JSON.parse("");
                votes.insert(votesObj);
            } catch (IOException e) {
                e.printStackTrace();
            }

            mongoClient.close();
        } catch (java.net.UnknownHostException e) {
            e.printStackTrace();
        }
    }
}

