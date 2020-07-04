package com.example.database.fragment;


import com.example.database.models.Post;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.Query;

public class MyPostsFragment extends PostListFragment {
    public MyPostsFragment() {}

    @Override
    public Query getQuery(DatabaseReference databaseReference) {
        // All my posts

        return databaseReference.child("user-posts").child(getUid()).child("History");
    }
}