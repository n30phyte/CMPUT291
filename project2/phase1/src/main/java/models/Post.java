package models;

import java.io.Serializable;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import org.bson.Document;


public class Post implements Serializable {

    DateFormat DATE_FORMAT = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");

    int Id;
    int PostTypeId;
    int AcceptedAnswerId;
    String CreationDate;
    int Score;
    int ViewCount;
    String Body;
    int OwnerUserId;
    int LastEditorUserId;
    String LastEditDate;
    String LastActivityDate;
    String Title;
    String Tags;
    int AnswerCount;
    int CommentCount;
    int FavouriteCount;
    String ContentLicense;

    public Document toDocument() {
        return new Document("Id", this.Id).append("PostTypeId", this.PostTypeId)
                .append("AcceptedAnswerId", this.AcceptedAnswerId)
                .append("CreationDate", this.CreationDate)
                .append("Score", this.Score)
                .append("ViewCount", this.ViewCount)
                .append("Body", this.Body)
                .append("OwnerUserId", this.OwnerUserId)
                .append("LastEditorUserId", this.LastEditorUserId)
                .append("LastEditDate", this.LastEditDate)
                .append("LastActivityDate", this.LastActivityDate)
                .append("Title", this.Title)
                .append("Tags", Tags)
                .append("AnswerCount", this.AnswerCount)
                .append("CommentCount", this.CommentCount)
                .append("FavouriteCount", this.FavouriteCount)
                .append("ContentLicense", this.ContentLicense);

    }
}
