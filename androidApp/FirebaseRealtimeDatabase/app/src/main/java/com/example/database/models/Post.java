package com.example.database.models;

import com.google.firebase.database.Exclude;
import com.google.firebase.database.IgnoreExtraProperties;

import java.util.HashMap;
import java.util.Map;

@IgnoreExtraProperties
public class Post {
    public String uid;
    public String author;
    public String title;
    public String body;
    public String Parking_time;
    public String Status;
    public int starCount = 0;
    public int Cost = 0;
    public Map<String, Boolean> stars = new HashMap<>();

    public Post() {
        // Default constructor required for calls to DataSnapshot.getValue(Post.class)
    }

    public Post(String uid, String author, String title, String body, int Cost, String Parking_time, String Status) {
        this.uid = uid;
        this.author = author;
        this.title = title;
        this.body = body;
        this.Cost = Cost;
        this.Parking_time = Parking_time;
        this.Status = Status;
    }
    public Post(String uid, String author, String title, String body) {
        this.uid = uid;
        this.author = author;
        this.title = title;
        this.body = body;
    }

    @Exclude
    public Map<String, Object> toMap() {
        HashMap<String, Object> result = new HashMap<>();
        result.put("uid", uid);
        result.put("author", author);
        result.put("title", title);
        result.put("body", body);
        result.put("starCount", starCount);
        result.put("stars", stars);
        result.put("Parking_time", Parking_time);
        result.put("Cost", Cost);
        result.put("Status", Status);
        return result;
    }
}