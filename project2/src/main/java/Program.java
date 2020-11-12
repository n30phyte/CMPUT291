import com.mongodb.*;
import com.mongodb.util.JSON;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;
import java.util.List;
import org.json.*;
import org.json.simple.parser.JSONParser;

public class Program {

    /**
     *
     * @param args
     */
    public static void main(String[] args) {
        int portNumber = 0;
        if(args.length > 2) {
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
            try (Reader postsReader = new FileReader("./Posts.json")) {
                DBObject postsObj = (DBObject) JSON.parse(postsReader);
                posts.insert(postsObj);
            } catch (IOException e) {
                e.printStackTrace();
            }

            DBCollection tags = db.getCollection("Tags");
            try (Reader tagsReader = new FileReader("./Tags.json")) {
                DBObject tagsObj = (DBObject) JSON.parse(tagsReader);
                tags.insert(tagsObj);
            } catch (IOException e) {
                e.printStackTrace();
            }

            DBCollection votes = db.getCollection("Votes");
            try (Reader votesReader = new FileReader("./Votes.json")) {
                DBObject votesObj = (DBObject) JSON.parse(votesReader);
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

