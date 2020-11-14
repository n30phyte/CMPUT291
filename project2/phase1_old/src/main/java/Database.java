import com.google.common.base.Charsets;
import com.google.common.io.Resources;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.mongodb.MongoCommandException;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import java.net.URL;
import java.util.HashMap;
import models.Post;
import models.Tag;
import models.Vote;
import org.bson.Document;

public class Database {

    MongoClient client;

    MongoDatabase database;

    MongoCollection<Document> postsCollection;
    MongoCollection<Document> tagsCollection;
    MongoCollection<Document> votesCollection;

    Tag[] tags = {};
    Post[] posts = {};
    Vote[] votes = {};

    Database(int port) {
        client = MongoClients.create(String.format("mongodb://localhost:%s", port));

        database = client.getDatabase("291db");

        try {
            database.createCollection("Posts");
        } catch (MongoCommandException e) {
            database.getCollection("Posts").drop();
        }

        try {
            database.createCollection("Tags");
        } catch (MongoCommandException e) {
            database.getCollection("Tags").drop();
        }

        try {
            database.createCollection("Votes");
        } catch (MongoCommandException e) {
            database.getCollection("Votes").drop();
        }

        postsCollection = database.getCollection("Posts");
        tagsCollection = database.getCollection("Tags");
        votesCollection = database.getCollection("Votes");

        tags = loadTags();
        posts = loadPosts();
        votes = loadVotes();
    }

    Tag[] loadTags() {
        try {
            URL tagFile = Resources.getResource("Tags.json");
            String tagJson = Resources.asCharSource(tagFile, Charsets.UTF_8).read();
            HashMap<String, HashMap<String, Tag[]>> topLevel = new Gson().fromJson(tagJson,
                    new TypeToken<HashMap<String, HashMap<String, Tag[]>>>() {}.getType());

            Tag[] tagList = topLevel.get("tags").get("row");

            for (Tag tag : tagList) {
                tagsCollection.insertOne(tag.toDocument());
            }

            return tagList;

        } catch (Exception ex) {
            ex.printStackTrace();
        }

        return new Tag[]{};
    }

    Post[] loadPosts() {
        try {
            URL postsFile = Resources.getResource("Posts.json");
            String postJson = Resources.asCharSource(postsFile, Charsets.UTF_8).read();
            HashMap<String, HashMap<String, Post[]>> topLevel = new Gson().fromJson(postJson,
                    new TypeToken<HashMap<String, HashMap<String, Post[]>>>() {}.getType());

            Post[] postList = topLevel.get("posts").get("row");

            for (Post post : postList) {
                postsCollection.insertOne(post.toDocument());
            }
            return postList;

        } catch (Exception ex) {
            ex.printStackTrace();
        }

        return new Post[]{};
    }

    Vote[] loadVotes() {
        try {
            URL votesFile = Resources.getResource("Votes.json");
            String votesJson = Resources.asCharSource(votesFile, Charsets.UTF_8).read();
            HashMap<String, HashMap<String, Vote[]>> topLevel = new Gson().fromJson(votesJson,
                    new TypeToken<HashMap<String, HashMap<String, Vote[]>>>() {}.getType());

            Vote[] voteList = topLevel.get("votes").get("row");

            for (Vote vote : voteList) {
                votesCollection.insertOne(vote.toDocument());
            }
            return voteList;

        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return new Vote[]{};
    }

}
