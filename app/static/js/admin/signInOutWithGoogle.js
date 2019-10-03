// Script for configuring Firebase Authentication (Sign In/Out with Google).
// See https://firebase.google.com/docs/auth/web/google-signin for more information.

var provider = new firebase.auth.GoogleAuthProvider();

// Collect token when users sign in with their Google accounts
firebase.auth().getRedirectResult().then(function(result) {
    if (result.credential && result.user) {
        document.getElementById("message_body").innerText = "You have successfully signed in. Now redirecting you back to site."
        const identityToken = result.credential.idToken;
        firebase.auth().currentUser.getIdToken(false).then(function(firebaseIdToken) {
        document.cookie = `firebase_id_token=${firebaseIdToken}`;
        setTimeout(function() { window.location.replace("/admin"); }, 1500);
        })   
    } else {
        document.getElementById("message_body").innerText = "Now redirecting you to Google."
        setTimeout(function() { signInWithGoogle(); }, 1500);
    }
}).catch(function(error) {
    console.log(error);
});

// Redirect users to Google
function signInWithGoogle() {
    firebase.auth().signInWithRedirect(provider);
}

function signOutWithGoogle() {
    firebase.auth().signOut().then(function() {
        document.cookie = "firebase_id_token=;";
        window.location.replace('/admin');
    }).catch(function (error) {
        console.log(error);
    });
}