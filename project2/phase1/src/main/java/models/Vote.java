package models;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import org.bson.Document;

public class Vote {

    DateFormat DATE_FORMAT = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");

    int Id;
    int PostId;
    int VoteTypeId;
    String CreationDate;

    public Document toDocument() {
        return new Document("Id", this.Id).append("PostId", this.PostId)
                .append("VoteTypeId", this.VoteTypeId)
                .append("CreationDate", this.CreationDate);
    }
}
