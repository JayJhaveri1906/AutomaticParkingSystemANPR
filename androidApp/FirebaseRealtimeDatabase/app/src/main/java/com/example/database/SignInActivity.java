package com.example.database;

import android.content.Intent;
import android.os.Bundle;
import androidx.annotation.NonNull;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import com.example.database.models.User;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class SignInActivity extends BaseActivity implements View.OnClickListener {
	private EditText mEmailField, mPasswordField;
	private FirebaseAuth mAuth;
	private Button btnReset;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_sign_in);

		mEmailField = findViewById(R.id.field_email);
		mPasswordField = findViewById(R.id.field_password);
		findViewById(R.id.button_sign_in).setOnClickListener(this);
		findViewById(R.id.button_sign_up).setOnClickListener(this);
		btnReset= (Button)findViewById(R.id.btn_reset_password);
		btnReset.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				String email = mEmailField.getText().toString().trim();

				if(TextUtils.isEmpty(email)){
					Toast.makeText(SignInActivity.this,"Enter your registered email",Toast.LENGTH_LONG).show();
					return;
				}
//				progressBar.setVisibility(View.VISIBLE);
				mAuth.sendPasswordResetEmail(email).addOnCompleteListener(new OnCompleteListener<Void>() {
					@Override
					public void onComplete(@NonNull Task<Void> task) {
						if (task.isSuccessful()){
							Toast.makeText(SignInActivity.this,"We have sent you instructions to reset your password!",Toast.LENGTH_LONG).show();
						}else {
							Toast.makeText(SignInActivity.this,"Failed to send reset email!",Toast.LENGTH_LONG).show();
						}
//						progressBar.setVisibility(View.GONE);
					}
				});
			}
		});
		mAuth = FirebaseAuth.getInstance();

	}

	@Override
	public void onStart() {
		super.onStart();
		if (mAuth.getCurrentUser() != null) {
			onAuthSuccess(mAuth.getCurrentUser());
		}
	}

	private void onAuthSuccess(FirebaseUser firebaseUser) {
		String email = firebaseUser.getEmail();
		String username = email;
		if (email != null && email.contains("@")) {
			username = email.split("@")[0];
		}

		User user = new User(username, email);
		DatabaseReference mDatabase = FirebaseDatabase.getInstance().getReference();
		mDatabase.child("users").child(firebaseUser.getUid()).setValue(user);

		startActivity(new Intent(this, MainActivity.class));
		finish();
	}

	private void signIn() {
		String email = mEmailField.getText().toString().trim();
		String password = mPasswordField.getText().toString().trim();

		if (validateForm(email, password)) {
			showProgressDialog();
			mAuth.signInWithEmailAndPassword(email, password).addOnCompleteListener(new OnCompleteListener<AuthResult>() {
				@Override
				public void onComplete(@NonNull Task<AuthResult> task) {
					hideProgressDialog();
					if (task.isSuccessful()) {
						onAuthSuccess(task.getResult().getUser());
					} else {
						Toast.makeText(SignInActivity.this, task.getException().getMessage(), Toast.LENGTH_LONG).show();
					}
				}
			});
		}
	}

	private void signUp() {
		String email = mEmailField.getText().toString().trim();
		String password = mPasswordField.getText().toString().trim();

		if (validateForm(email, password)) {
			showProgressDialog();
			mAuth.createUserWithEmailAndPassword(email, password).addOnCompleteListener(new OnCompleteListener<AuthResult>() {
				@Override
				public void onComplete(@NonNull Task<AuthResult> task) {
					hideProgressDialog();
					if (task.isSuccessful()) {
						onAuthSuccess(task.getResult().getUser());
					} else {
						Toast.makeText(SignInActivity.this, task.getException().getMessage(), Toast.LENGTH_SHORT).show();
					}
				}
			});
		}
	}

	private boolean validateForm(String email, String password) {
		if (TextUtils.isEmpty(email)) {
			mEmailField.setError(getString(R.string.required));
			return false;
		} else if (TextUtils.isEmpty(password)) {
			mPasswordField.setError(getString(R.string.required));
			return false;
		} else {
			mEmailField.setError(null);
			mPasswordField.setError(null);
			return true;
		}
	}

	@Override
	public void onClick(View v) {
		switch (v.getId()) {
			case R.id.button_sign_in:
				signIn();
				break;
			case R.id.button_sign_up:
				signUp();
				break;
		}
	}

}