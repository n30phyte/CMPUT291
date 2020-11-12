package models;

import org.bson.Document;

public class Tag {

    int Id;
    String TagName;
    int Count;

    int ExcerptPostId;
    int WikiPostId;

    public Document toDocument() {
        return new Document("Id", this.Id).append("TagName", this.TagName)
                .append("Count", this.Count)
                .append("ExcerptPostId", this.ExcerptPostId)
                .append("WikiPostId", this.WikiPostId);
    }
}
